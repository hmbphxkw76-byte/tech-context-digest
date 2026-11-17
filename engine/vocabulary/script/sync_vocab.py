#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sync_vocab.py — 词汇库 → 业务提示词自动同步工具。

职责与机制：
- 将词汇库（engine/vocabulary/data/<topic>/terms.md）词条按预设格式写入业务提示词的标记区间
  （`<!-- VOCAB-SYNC:BEGIN topic=... -->` … `<!-- VOCAB-SYNC:END -->`），区间外内容字节级零触碰；
- 增量检测：逐词条 hash（sha256）与上次同步状态比对，仅在有新增/修改/删除时写盘；
- 双重校验：同步前 diff（check），同步后回读验证（区间完整性 + 词条覆盖 + 区间外内容与
  写入前逐字节一致）；校验失败自动回滚备份；
- 触发方式三选一：vocab_tool import/tag 成功后的自动钩子（auto_trigger=true，默认）、
  常驻 watch 轮询、手动 `sync`（也是失败后的手动重试入口）。

退出码（对齐仓库工具链约定）：0=成功（含无变更）；1=错误（已回滚或配置问题，修复后重试）；2=警告/有待同步差异。

用法：
  python engine/vocabulary/script/sync_vocab.py sync  [--topic T] [--full]     # 执行同步（手动/重试入口）
  python engine/vocabulary/script/sync_vocab.py check [--topic T]              # 仅对比差异，不写盘
  python engine/vocabulary/script/sync_vocab.py verify [--topic T]             # 校验已写入区间的正确性
  python engine/vocabulary/script/sync_vocab.py watch [--interval N]           # 常驻轮询监听变更
  python engine/vocabulary/script/sync_vocab.py status                         # 查看绑定与同步状态
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vocab_tool import load_storage  # noqa: E402  复用词库解析器，保证解析口径一致

SYNC_ROOT = Path(__file__).resolve().parent.parent          # vocabulary/
DEFAULT_SYNC_CONFIG = SYNC_ROOT / "config" / "sync.json"
DEFAULT_TOPICS_CONFIG = SYNC_ROOT / "config" / "topics.json"

BEGIN_MARK = "<!-- VOCAB-SYNC:BEGIN"
END_MARK = "<!-- VOCAB-SYNC:END -->"
KEY_FIELDS = ("id", "term", "aliases", "category", "tags", "definition", "source")


# ---------- 基础工具 ----------

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text_raw(path: Path) -> str:
    """保留原始换行符读取（确保区间外内容字节级不变）。"""
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text_atomic(path: Path, text: str):
    tmp = path.with_suffix(path.suffix + ".sync-tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, path)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def plog(log_path: Path, msg: str):
    entry = f"[{now_iso()}] {msg}"
    print(entry)
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8", newline="") as f:
            f.write(entry + "\n")
    except OSError as exc:
        print(f"[warn] 日志写入失败：{exc}")


# ---------- 配置 ----------

def load_sync_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"同步配置不存在：{path}")
    cfg = load_json(path)
    if not isinstance(cfg.get("bindings"), list) or not cfg["bindings"]:
        raise ValueError("同步配置缺少非空 bindings 数组")
    for b in cfg["bindings"]:
        if not b.get("topic") or not isinstance(b.get("targets"), list) or not b["targets"]:
            raise ValueError("每个 binding 需要 topic 与非空 targets 数组")
    return cfg


def load_topics(path: Path) -> dict:
    cfg = load_json(path)
    if not isinstance(cfg.get("topics"), dict):
        raise ValueError(f"主题注册表缺少 topics 对象：{path}")
    return cfg


def collect_bindings(cfg: dict, topic_filter):
    for binding in cfg["bindings"]:
        if topic_filter and binding["topic"] != topic_filter:
            continue
        for tcfg in binding["targets"]:
            yield binding, tcfg


def resolve_source(binding: dict, topics: dict) -> Path:
    tid = binding["topic"]
    if tid not in topics["topics"]:
        raise ValueError(f"binding.topic '{tid}' 未在 topics.json 注册")
    rel = binding.get("source") or topics["topics"][tid].get("storage")
    if not rel:
        raise ValueError(f"主题 '{tid}' 未配置 storage 且 binding 未提供 source")
    p = Path(rel)
    return p if p.is_absolute() else SYNC_ROOT / p


def resolve_target(tcfg: dict) -> Path:
    p = Path(tcfg["path"])
    return p if p.is_absolute() else SYNC_ROOT / p


# ---------- 词条与差异 ----------

def apply_filters(terms: list, tcfg: dict) -> list:
    out = terms
    inc_cat = tcfg.get("categories_include") or []
    inc_tag = tcfg.get("tags_include") or []
    if inc_cat:
        out = [t for t in out if t["category"] in inc_cat]
    if inc_tag:
        out = [t for t in out if any(x in t["tags"] for x in inc_tag)]
    return out


def term_sig(t: dict) -> str:
    return json.dumps({k: t.get(k) for k in KEY_FIELDS}, ensure_ascii=False, sort_keys=True)


def term_hashes(terms: list) -> dict:
    return {t["id"]: sha(term_sig(t)) for t in terms}


def diff_hashes(new: dict, old: dict):
    added = [i for i in new if i not in old]
    removed = [i for i in old if i not in new]
    modified = [i for i in new if i in old and new[i] != old[i]]
    return added, modified, removed


def fmt_ids(ids: list, name_of: dict, limit: int = 8) -> str:
    return "、".join(name_of.get(i, i) for i in ids[:limit]) + ("…" if len(ids) > limit else "")


# ---------- 区块构建与校验 ----------

def find_block(text: str, topic: str):
    return re.search(
        rf"<!-- VOCAB-SYNC:BEGIN topic={re.escape(topic)}\b.*?<!-- VOCAB-SYNC:END -->",
        text, re.S)


def build_block(tmeta: dict, tcfg: dict, terms: list, version: str, nl: str) -> str:
    fmt = tcfg.get("format", "digest")
    title = tcfg.get("section_title", "## 词汇速览（词汇库自动同步）")
    L = [f"<!-- VOCAB-SYNC:BEGIN topic={tmeta['id']} do-not-edit -->", title, ""]
    L.append(f"> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 {tmeta['id']} {version}，"
             f"共 {len(terms)} 条（同步于 {now_iso()}）。标记区间内请勿手工编辑；词条变更走词汇库"
             f"导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。")
    L.append("")

    def cellv(s) -> str:
        return str(s).replace("|", "／").replace("\r", " ").replace("\n", " ").strip()

    if fmt == "table":
        L += ["| 词条 | 别名 | 分类 |", "|---|---|---|"]
        for t in terms:
            L.append(f"| {cellv(t['term'])} | {cellv(';'.join(t['aliases']))} | {cellv(t['category'])} |")
    else:  # digest（缺省）：按分类归组的紧凑速览
        order = list(tmeta.get("categories") or [])
        cats = [c for c in order if any(t["category"] == c for t in terms)]
        cats += [c for c in dict.fromkeys(t["category"] for t in terms) if c not in cats]
        for cat in cats:
            ts = [t for t in terms if t["category"] == cat]
            items = [f"{t['term']}（{'、'.join(t['aliases'])}）" if t["aliases"] else t["term"] for t in ts]
            L.append(f"- **{cat}**（{len(ts)}）：{'；'.join(items)}")
    L.append(END_MARK)
    return nl.join(L)


def verify_block(text: str, topic: str, terms: list) -> list:
    """校验已写入区间：标记配对 + 词条覆盖。"""
    errs = []
    if text.count(BEGIN_MARK) != text.count(END_MARK):
        errs.append("VOCAB-SYNC 标记数量不配对")
    m = find_block(text, topic)
    if m is None:
        errs.append(f"缺少 {topic} 的 VOCAB-SYNC 区间")
        return errs
    block = m.group(0)
    missing = [t["term"] for t in terms if t["term"] not in block]
    if missing:
        errs.append(f"词条未覆盖 {len(missing)} 条（如 {'、'.join(missing[:3])}）")
    return errs


def backup_target(topic: str, tpath: Path, backup_dir: Path, keep: int) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = backup_dir / f"{topic}.{tpath.name}.{ts}.bak"
    shutil.copyfile(tpath, dst)
    prefix = f"{topic}.{tpath.name}."
    olds = sorted(backup_dir.glob(f"{prefix}*.bak"))
    for p in olds[:-keep] if keep > 0 and len(olds) > keep else []:
        try:
            p.unlink()
        except OSError:
            pass
    return dst


# ---------- 核心同步 ----------

def sync_one(cfg: dict, topics: dict, binding: dict, tcfg: dict, state: dict,
             log_path: Path, dry: bool = False, force: bool = False):
    """对单个 target 执行同步；返回 (exit_code, message, counts)。异常向上抛出。"""
    tid = binding["topic"]
    tmeta = dict(topics["topics"][tid])
    tmeta["id"] = tid
    source = resolve_source(binding, topics)
    if not source.exists():
        raise FileNotFoundError(f"词汇库不存在：{source}（先运行 vocab_tool init/import）")
    tpath = resolve_target(tcfg)
    if not tpath.exists():
        raise FileNotFoundError(f"目标提示词不存在：{tpath}")

    terms_all, versions = load_storage(source)
    version = versions[-1][0] if versions else "v1.0"
    terms = apply_filters(terms_all, tcfg)
    name_of = {t["id"]: t["term"] for t in terms_all}
    key = f"{tid}=>{tcfg['path']}"

    text = read_text_raw(tpath)
    new_h = term_hashes(terms)
    old = state.setdefault("targets", {}).get(key)
    if old:
        added, modified, removed = diff_hashes(new_h, old.get("term_hashes", {}))
        first = False
    else:
        added, modified, removed = [t["id"] for t in terms], [], []
        first = True
    has_block = find_block(text, tid) is not None

    counts = {"added": len(added), "modified": len(modified), "removed": len(removed)}
    drift = verify_block(text, tid, terms) if has_block else []
    pending = bool(added or modified or removed) or not has_block or force or bool(drift)
    target_disp = tcfg["path"]

    if not pending:
        if drift:
            msg = f"结构漂移待修复：{'；'.join(drift[:2])}"
        else:
            msg = "无变更（词汇库与提示词区间一致）"
        return 0, msg, counts

    if dry:
        if first:
            msg = f"初次同步：待写入 {len(added)} 条（未写盘）"
        else:
            msg = (f"待同步：新增 {len(added)}（{fmt_ids(added, name_of)}） / "
                   f"修改 {len(modified)}（{fmt_ids(modified, name_of)}） / "
                   f"删除 {len(removed)}（{fmt_ids(removed, name_of)}）（未写盘）"
                   if (added or modified or removed) else f"结构漂移待修复：{'；'.join(drift[:2])}")
        return 2, msg, counts

    nl = "\r\n" if "\r\n" in text else "\n"
    block = build_block(tmeta, tcfg, terms, version, nl)
    backup_dir = SYNC_ROOT / cfg.get("backup_dir", "data/sync-backups")
    backup = backup_target(tid, tpath, backup_dir, int(cfg.get("backup_keep", 5)))

    m = find_block(text, tid)
    tail: str
    if m:
        prefix, suffix = text[:m.start()], text[m.end():]
        tail = suffix
        new_text = prefix + block + suffix
        mode = "区块替换"
    else:
        anchor = tcfg.get("insert_before")
        if not anchor:
            raise ValueError(f"目标缺少同步区间且未配置 insert_before 锚点：{target_disp}")
        idx = text.find(anchor)
        if idx == -1:
            raise ValueError(f"未找到插入锚点「{anchor}」：{target_disp}")
        prefix, suffix = text[:idx], text[idx:]
        tail = nl + nl + suffix
        new_text = prefix + block + tail
        mode = "新区块插入"

    write_text_atomic(tpath, new_text)

    # 写后校验：回读磁盘，验证区间 + 词条覆盖 + 区间外内容与写入前逐字节一致
    disk = read_text_raw(tpath)
    errs = verify_block(disk, tid, terms)
    m2 = find_block(disk, tid)
    if m2 is None:
        errs.append("写盘后未找到同步区间")
    else:
        if disk[:m2.start()] != prefix:
            errs.append("区间前内容发生变化（异常，已不具备保留性）")
        if disk[m2.end():] != tail:
            errs.append("区间后内容发生变化（异常，已不具备保留性）")
    if errs:
        shutil.copyfile(backup, tpath)
        raise RuntimeError(f"写入后校验失败，已自动回滚备份 {backup.name}：{'；'.join(errs[:3])}")

    state["targets"][key] = {
        "topic": tid,
        "target": tcfg["path"],
        "vocab_version": version,
        "term_count": len(terms),
        "synced_at": now_iso(),
        "source_hash": sha(source.read_text(encoding="utf-8-sig")),
        "term_hashes": new_h,
    }
    msg = (f"{mode}成功：新增 {len(added)} / 修改 {len(modified)} / 删除 {len(removed)}，"
           f"共 {len(terms)} 条（{version}）；备份 {backup_dir.name}/{backup.name}")
    return 0, msg, counts


# ---------- 子命令 ----------

def cmd_sync(cfg, topics, state, log_path, topic_filter, force=False) -> int:
    ok = True
    for binding, tcfg in collect_bindings(cfg, topic_filter):
        try:
            code, msg, _ = sync_one(cfg, topics, binding, tcfg, state, log_path, force=force)
            plog(log_path, f"[sync] {binding['topic']} -> {tcfg['path']}：{msg}")
            ok = ok and code == 0
        except Exception as exc:
            ok = False
            plog(log_path, f"[error] {binding['topic']} -> {tcfg['path']}：{exc}")
            plog(log_path, f"[error] 可修复后手动重试：python engine/vocabulary/script/sync_vocab.py sync --topic {binding['topic']}")
    if state.get("targets"):
        dump_json(SYNC_ROOT / cfg.get("state_file", "data/sync-state.json"), state)
    return 0 if ok else 1


def cmd_check(cfg, topics, state, log_path, topic_filter) -> int:
    pending_any = False
    for binding, tcfg in collect_bindings(cfg, topic_filter):
        try:
            _, msg, _ = sync_one(cfg, topics, binding, tcfg, state, log_path, dry=True)
            if not msg.startswith("无变更"):
                pending_any = True
            plog(log_path, f"[check] {binding['topic']} -> {tcfg['path']}：{msg}")
        except Exception as exc:
            pending_any = True
            plog(log_path, f"[error] {binding['topic']} -> {tcfg['path']}：{exc}")
    return 2 if pending_any else 0


def cmd_verify(cfg, topics, state, log_path, topic_filter) -> int:
    ok = True
    for binding, tcfg in collect_bindings(cfg, topic_filter):
        tid = binding["topic"]
        try:
            source = resolve_source(binding, topics)
            terms_all, versions = load_storage(source)
            terms = apply_filters(terms_all, tcfg)
            tpath = resolve_target(tcfg)
            if not tpath.exists():
                raise FileNotFoundError(f"目标提示词不存在：{tpath}")
            errs = verify_block(read_text_raw(tpath), tid, terms)
            key = f"{tid}=>{tcfg['path']}"
            rec = state.get("targets", {}).get(key)
            drift = []
            if rec is None:
                drift.append("状态文件无同步记录")
            elif rec.get("source_hash") != sha(source.read_text(encoding="utf-8-sig")):
                drift.append("词汇库在最近一次同步后有变更（建议重新 sync）")
            if errs or drift:
                ok = False
                detail = "；".join(errs + drift)
                plog(log_path, f"[verify] {tid} -> {tcfg['path']}：不通过（{detail}）")
            else:
                plog(log_path, f"[verify] {tid} -> {tpath.name}：通过（{len(terms)} 条覆盖完整，"
                               f"区间外内容一致，词汇库 {versions[-1][0] if versions else '—'}）")
        except Exception as exc:
            ok = False
            plog(log_path, f"[error] {tid}：{exc}")
    return 0 if ok else 1


def cmd_watch(cfg, topics, log_path, topic_filter, interval: int) -> int:
    targets = list(collect_bindings(cfg, topic_filter))
    if not targets:
        plog(log_path, "[watch] 无匹配的绑定，退出")
        return 1

    def snapshot() -> dict:
        snap = {}
        for binding, tcfg in targets:
            key = f"{binding['topic']}=>{tcfg['path']}"
            try:
                src = resolve_source(binding, topics)
                tgt = resolve_target(tcfg)
                snap[key] = (
                    sha(src.read_text(encoding="utf-8-sig")) if src.exists() else None,
                    sha(read_text_raw(tgt)) if tgt.exists() else None,
                    binding["topic"],
                )
            except OSError:
                snap[key] = (None, None, binding["topic"])
        return snap

    plog(log_path, f"[watch] 开始监听 {len(targets)} 个绑定目标（间隔 {interval}s，Ctrl+C 停止）")
    snap = snapshot()
    state = {}
    state_path = SYNC_ROOT / cfg.get("state_file", "data/sync-state.json")
    if state_path.exists():
        state = load_json(state_path)
    try:
        while True:
            time.sleep(interval)
            cur = snapshot()
            changed = [k for k in cur if cur[k][:2] != snap.get(k, (None, None))[:2]]
            if changed:
                for k in changed:
                    plog(log_path, f"[watch] 检测到变更：{k}")
                topics_to_sync = sorted({cur[k][2] for k in changed})
                for tid in topics_to_sync:
                    try:
                        cmd_sync(cfg, topics, state, log_path, topic_filter=tid)
                    except Exception as exc:
                        plog(log_path, f"[error] watch 同步失败（{tid}）：{exc}；watch 继续运行")
                dump_json(state_path, state)
                snap = snapshot()
            else:
                snap = cur
    except KeyboardInterrupt:
        plog(log_path, "[watch] 已停止")
        return 0


def cmd_status(cfg, topics, log_path) -> int:
    state_path = SYNC_ROOT / cfg.get("state_file", "data/sync-state.json")
    state = load_json(state_path) if state_path.exists() else {"targets": {}}
    print(f"同步配置：{cfg.get('_path')}（{cfg.get('version', '?')}，auto_trigger={cfg.get('auto_trigger', False)}）")
    n = 0
    for binding, tcfg in collect_bindings(cfg, None):
        n += 1
        key = f"{binding['topic']}=>{tcfg['path']}"
        rec = state.get("targets", {}).get(key)
        try:
            src = resolve_source(binding, topics)
            drift = (rec is not None and src.exists()
                     and rec.get("source_hash") != sha(src.read_text(encoding="utf-8-sig")))
            state_txt = (f"已同步 {rec['synced_at']}（{rec['term_count']} 条，词汇库 {rec['vocab_version']}）"
                         + ("；有未同步变更" if drift else ""))
        except Exception as exc:
            state_txt = f"状态读取失败：{exc}"
        print(f"  {binding['topic']} -> {tcfg['path']}  {state_txt if rec else '从未同步'}")
    print(f"共 {n} 个绑定目标。手动重试入口：python engine/vocabulary/script/sync_vocab.py sync [--topic T]")
    return 0


# ---------- 入口 ----------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="词汇库 → 业务提示词自动同步工具（标记区间保护 + 增量检测 + 校验回滚）")
    ap.add_argument("--config", default=str(DEFAULT_SYNC_CONFIG), help="同步配置路径（默认 engine/vocabulary/config/sync.json）")
    ap.add_argument("--topics", default=str(DEFAULT_TOPICS_CONFIG), help="主题注册表路径（默认 engine/vocabulary/config/topics.json）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sync", help="执行同步（手动/重试入口）")
    p.add_argument("--topic", default="", help="仅同步指定主题")
    p.add_argument("--full", action="store_true", help="忽略增量状态，全量重写区间")
    p = sub.add_parser("check", help="仅对比词汇库与提示词差异，不写盘")
    p.add_argument("--topic", default="")
    p = sub.add_parser("verify", help="校验已写入区间的正确性")
    p.add_argument("--topic", default="")
    p = sub.add_parser("watch", help="常驻轮询监听变更（词汇库或目标文件任一变化即同步）")
    p.add_argument("--interval", type=int, default=None, help="轮询间隔秒数（默认取配置 watch_interval_sec）")
    p.add_argument("--topic", default="")
    sub.add_parser("status", help="查看绑定与同步状态")

    args = ap.parse_args(argv)
    try:
        cfg = load_sync_config(Path(args.config))
        cfg["_path"] = args.config
        topics = load_topics(Path(args.topics))
        log_path = SYNC_ROOT / cfg.get("log_file", "data/sync.log")
        state_path = SYNC_ROOT / cfg.get("state_file", "data/sync-state.json")
        state = load_json(state_path) if state_path.exists() else {"targets": {}}
        if args.cmd == "sync":
            return cmd_sync(cfg, topics, state, log_path, args.topic or None, force=args.full)
        if args.cmd == "check":
            return cmd_check(cfg, topics, state, log_path, args.topic or None)
        if args.cmd == "verify":
            return cmd_verify(cfg, topics, state, log_path, args.topic or None)
        if args.cmd == "watch":
            interval = args.interval or int(cfg.get("watch_interval_sec", 5))
            return cmd_watch(cfg, topics, log_path, args.topic or None, interval)
        if args.cmd == "status":
            return cmd_status(cfg, topics, log_path)
    except (KeyError, ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        plog(SYNC_ROOT / "data/sync.log", f"[error] {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
