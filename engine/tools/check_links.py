"""路径引用可达性校验（CI: ci.yml / scheduled-maintenance 的链接关卡）。

扫描文本文件（.py/.md/.json/.yml/.yaml/.html/.txt）中的路径引用，逐条校验目标存在：
1. 仓库相对路径（首段为已知根条目）：先按仓库根解析，缺失时回退按「文件所在目录」解析
   —— 兼容文档中以业务目录为基准的相对写法（如 `prompts/business-config.md`）；
2. `./` 与 `../` 相对链接：按文件所在目录解析；
3. GitHub `blob/main/<path>` URL：提取路径段后按仓库根校验。

排除：外部 URL、锚点（#…）、邮箱、{{…}} 变量、含通配/占位符的 token（`{ } * | < >`）、
冻结留痕（engine/audit/records/、sync-backups/、topic-backups/、*.log）与冻结文档
（词汇库 README / CHANGELOG）；跳过 `.meituan-catpaw/`（客户端 worktree 存储，非仓库内容）。

退出码：0 = 无断链；1 = 存在断链。

用法：
    python engine/tools/check_links.py              # 全量扫描
    python engine/tools/check_links.py --verbose    # 同时列出已校验通过的引用数
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_business_dirs, known_roots  # noqa: E402

SCAN_SUFFIXES = {".py", ".md", ".json", ".yml", ".yaml", ".html", ".txt"}
# `.meituan-catpaw/` 为客户端 worktree 存储（与 naming_check 同口径），非仓库内容，不扫描。
SKIP_DIR_MARKERS = ("sync-backups", "topic-backups", ".git", "__pycache__", ".meituan-catpaw")

# 冻结文档：含历史旧路径 / 时点快照的留痕文档（不参与断链判定）
FROZEN_DOCS = {
    "engine/vocabulary/README.md",
    "CHANGELOG.md",
}

# 路径 token：至少含一个 `/`，由字母数字与 ._- 组成
PATH_RE = re.compile(r"(?<![/])[\w.\-]+(?:/[\w.\-]+)+")
# 同目录相对链接（点斜杠开头）
DOT_RE = re.compile(r"(?<!\.)\./[\w.\-]+(?:/[\w.\-]+)*/?")
# 上级相对链接（点点斜杠开头）；(?<!\.) 避免把 URL 截断标记（三个点斜杠）误判为上级链接
DOTDOT_RE = re.compile(r"(?<!\.)(?:\.\./)+(?:[\w.\-]+)(?:/[\w.\-]+)*/?")
# GitHub blob/main URL 中的路径段
BLOB_RE = re.compile(r"blob/main/([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*)")

# 含通配 / 占位符的 token 不参与判定（如 prompt-{baseline|monthly}.md、registry_*.xlsx）
GLOB_CHARS = set("{}*|<>")

# 业务目录相对引用首段（如 prompts/business-config.md 指任一条业务线的对应文件）
BUSINESS_SUBDIRS = {"prompts", "reports", "data", "sources", "followup", "script", "insights"}

def _allowed_broken(token: str) -> bool:
    """token 是否命中白名单（等值 / 前缀 / 后缀三种形态）。"""
    return any(
        token == a or token.startswith(a + "/") or token.endswith("/" + a)
        for a in ALLOWED_BROKEN
    )


def _allowed_prefix(token: str) -> bool:
    """token 是否位于运行期产出目录（前缀匹配）。"""
    return any(token == p or token.startswith(p + "/") for p in ALLOWED_PREFIXES)


# 不参与判定的文件：派生状态（重生成，含历史快照字段）
SKIP_FILES = {
    "engine/vocabulary/data/sync-state.json",
    # 本文件自带路径白名单字面量，自扫描会误判
    "engine/tools/check_links.py",
}

# 特定文件的相对路径基准目录（缺省 = 文件所在目录）。
# sync.json 的 target.path 按约定相对 vocabulary/ 根，而非 config/ 所在目录。
BASE_DIR_OVERRIDES = {
    "engine/vocabulary/config/sync.json": "engine/vocabulary",
    "engine/vocabulary/config/topics.json": "engine/vocabulary",
    "engine/vocabulary/script/sync_vocab.py": "engine/vocabulary",
    "engine/vocabulary/script/vocab_tool.py": "engine/vocabulary",
}

# 运行期产出目录（前缀匹配）：业务线采集 / 清洗落盘与词汇库同步备份，基线可缺
ALLOWED_PREFIXES = {
    "data/processed/economy/dubai/apartment",
    "data/processed/economy/insight",
    "data/processed/economy/trends",
    "data/processed/tech/ai-security/competitive-intelligence/dubai",
    "data/processed/tech/ai-security/industry-research/dubai",
    "data/processed/tech/ai-security/dubai",
    "data/processed/tech/ai-application/competitive-intelligence/dubai",
    "data/processed/tech/ai-application/industry-research/dubai",
    "data/processed/tech/ai-application/dubai",
    "data/sync-backups",
}

# 有意保留的不可解析引用（文档明确声明为可选或占位）
ALLOWED_BROKEN = {
    "engine/docs/adr",      # domain.md：文件不存在时 "proceed silently"，不标记缺失
    "GLOSSARY.md",       # 同上
    "GLOSSARY-MAP.md",   # 同上
    "reports/archives",  # 按需创建（archive_reports.py 首次归档时建立）
    # 已删除的历史业务线（回滚时移除）：仅在历史审计记录中引用，不得作为活跃链接
    "content/economy/real-estate/dubai/market-sizing",
    "content/economy/real-estate/dubai/policy-analysis",
    # 空主题占位（空目录不入 git）
    "content/education/.gitkeep",
    "content/international/.gitkeep",
    "content/political/.gitkeep",
    "content/society/.gitkeep",
    # 概念性默认路径（模板占位；实际登记按业务线落 data/processed/）
    "data/source_registry.json",
    # 已合并 / 已拆分 / 已迁移 / 已停用的历史业务线（仅在历史审计记录中引用，不得作为活跃链接）：
    # trends/ai-security、trends/ai-agent → content/tech/weekly-roundup → 拆分为 ai-security / ai-application（已停用）；
    # content/tech/{security,competitive-intelligence,industry-research}/dubai → content/tech/ai-security/...；
    # content/tech/ai-security/security/dubai → content/tech/ai-security/dubai。
    "trends/ai-security",
    "trends/ai-agent",
    "content/tech/weekly-roundup",
    "content/tech/security/dubai",
    "content/tech/competitive-intelligence/dubai",
    "content/tech/industry-research/dubai",
    "content/tech/ai-security/weekly-roundup",
    "content/tech/ai-application/weekly-roundup",
    "content/tech/ai-security/security/dubai",
    "data/processed/tech/security/dubai",
    "data/processed/tech/competitive-intelligence/dubai",
    "data/processed/tech/industry-research/dubai",
    "data/processed/tech/weekly-roundup",
    "data/processed/tech/ai-security/security/dubai",
    "data/processed/tech/ai-security/weekly-roundup",
    "data/processed/tech/ai-application/weekly-roundup",
    "content/tech/ai-application/trends",
    "data/processed/tech/ai-application/trends",
    "data/raw/tech/competitive-intelligence/dubai",
    "data/raw/tech/industry-research/dubai",
    # 已删除的未来周期月报（落款晚于产出当月、数据窗口越界，2026-11-21 清理）：
    # 仅在历史审计记录中引用，不得作为活跃链接
    "content/economy/dubai/apartment/reports/2026-12_monthly.html",
    "content/economy/dubai/apartment/reports/2027-01_monthly.html",
}
ALLOWED_TOKENS = {
    "./business-config.md",  # 泛用模板占位：实例化时替换为业务线 business-config.md
}


def is_frozen(rel: str) -> bool:
    """冻结留痕文件（历史备份 / 日志 / 冻结文档 / 夹具与派生状态）不参与断链判定。

    按路径段精确匹配，避免 `.git` 子串误伤 `.github/`。
    """
    if rel in FROZEN_DOCS or rel in SKIP_FILES or rel.startswith("engine/tests/"):
        return True
    if rel.startswith("engine/audit/records/"):
        return True  # 机器生成留痕（历史路径快照），不参与断链判定
    parts = rel.split("/")
    if any(p in SKIP_DIR_MARKERS for p in parts):
        return True
    return rel.endswith(".log")


def iter_files():
    """产出仓库内全部待扫描文本文件（绝对路径, 相对路径）。"""
    for f in sorted(ROOT.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in SCAN_SUFFIXES:
            continue
        rel = f.relative_to(ROOT).as_posix()
        if is_frozen(rel):
            continue
        yield f, rel


def _has_glob(token: str) -> bool:
    return any(ch in token for ch in GLOB_CHARS)


def _truncated_by_glob(line: str, m: re.Match) -> bool:
    """token 是否被通配/占位符截断（如 prompt-{...}.md、registry_*.xlsx）。"""
    return m.end() < len(line) and line[m.end()] in GLOB_CHARS


def _case_ok(path: Path) -> bool:
    """逐段校验大小写与磁盘实际条目一致（Windows 不敏感、Linux 敏感）。"""
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return True
    cur = ROOT
    for part in rel.parts:
        if not cur.is_dir():
            return True
        try:
            if part not in {e.name for e in cur.iterdir()}:
                return False
        except OSError:
            return True
        cur = cur / part
    return True


def _resolves(token: str, base_dir: Path) -> bool:
    """token 是否可达：仓库根 / 基准目录 / 任一业务线根；含大小写校验与白名单判定。"""
    for cand in (ROOT / token, base_dir / token):
        if cand.exists():
            return _case_ok(cand)
    if _allowed_prefix(token) or _allowed_broken(token):
        return True
    # 业务目录相对引用（如 prompts/business-config.md）：任一条业务线存在即视为可达
    if token.split("/")[0] in BUSINESS_SUBDIRS:
        for b in iter_business_dirs():
            cand = b.path / token
            if cand.exists():
                return _case_ok(cand)
    return False


def check_file(path: Path, rel: str, roots: set[str]) -> list[tuple[int, str, str]]:
    """-> [(行号, 引用原文, 解析目标)]，仅包含断链项。"""
    broken: list[tuple[int, str, str]] = []
    if rel in BASE_DIR_OVERRIDES:
        base_dir = ROOT / BASE_DIR_OVERRIDES[rel]
    elif rel.startswith(".github/workflows/"):
        base_dir = ROOT
    else:
        base_dir = path.parent
    text = path.read_text(encoding="utf-8", errors="replace")
    # data-search 为小写化搜索索引（非真实路径引用），不参与判定
    text = re.sub(r'data-search="[^"]*"', 'data-search=""', text)
    for lineno, line in enumerate(text.splitlines(), start=1):
        if "{{" in line and "}}" in line:
            continue  # 变量行整体跳过（如 {{REPO_RAW_URL_BASE}} = https://…/blob/main/…）

        # 1) 仓库相对路径（首段为已知根条目）
        for m in PATH_RE.finditer(line):
            token = m.group(0)
            if token.split("/")[0] not in roots or _has_glob(token):
                continue
            if _truncated_by_glob(line, m):
                continue
            if _resolves(token, base_dir):
                continue
            broken.append((lineno, token, token))

        # 2) 相对链接（./ 与 ../）
        for rx in (DOT_RE, DOTDOT_RE):
            for m in rx.finditer(line):
                token = m.group(0)
                if _has_glob(token) or _truncated_by_glob(line, m):
                    continue
                resolved = (base_dir / token).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    continue  # 指向仓库之外，不判定
                if not resolved.exists() or not _case_ok(resolved):
                    rel = resolved.relative_to(ROOT).as_posix()
                    if (
                        token not in ALLOWED_TOKENS
                        and not _allowed_prefix(rel)
                        and not _allowed_broken(rel)
                    ):
                        broken.append((lineno, token, rel))

        # 3) GitHub blob/main URL
        for m in BLOB_RE.finditer(line):
            token = m.group(1)
            if _has_glob(token) or _truncated_by_glob(line, m):
                continue
            target = ROOT / token
            if not target.exists() or not _case_ok(target):
                # 历史 blob URL（已迁移 / 已拆分业务线）经白名单放行
                if not _allowed_broken(token):
                    broken.append((lineno, f"blob/main/{token}", token))
    return broken


def main() -> int:
    ap = argparse.ArgumentParser(description="路径引用可达性校验")
    ap.add_argument("--verbose", action="store_true", help="列出扫描文件数")
    args = ap.parse_args()

    roots = known_roots()
    broken_all: list[tuple[str, int, str, str]] = []
    n_files = 0
    for f, rel in iter_files():
        n_files += 1
        for lineno, token, target in check_file(f, rel, roots):
            broken_all.append((rel, lineno, token, target))

    if args.verbose:
        print(f"已扫描 {n_files} 个文件；断链 {len(broken_all)} 条")

    for rel, lineno, token, target in broken_all:
        print(f"[BROKEN] {rel}:{lineno} -> {token}（目标不存在: {target}）")

    if broken_all:
        print(f"链接校验失败：{len(broken_all)} 条断链")
        return 1
    print("链接校验通过：全部仓库路径引用可达")
    return 0


if __name__ == "__main__":
    if ROOT.is_dir():
        sys.exit(main())
    sys.exit(1)
