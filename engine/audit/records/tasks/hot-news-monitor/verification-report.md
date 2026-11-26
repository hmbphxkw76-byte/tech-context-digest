# hot-news-monitor 验证报告（2026-11-26）

验证口径（经用户确认的等价方案，替代字面 24 小时连续运行）：
每周更新频率下的抽样长跑 + 30–60 分钟连续运行 + 断点恢复；全部留存日志。

## 1. 长跑稳定性（soak）

- 命令：`python -m app soak --duration 1800 --interval 300`（分离进程真实运行）。
- 判据：每轮刷新输出快照可用（events/items 非空）；错误计数为 0。
- 结果：**ticks=6，errors=0，时长 1861s**（节拍稳定在约 305–320s；第 5 拍起因信源端 feed 变化 events 153→30、items 258→34，系统始终产出可用快照，未中断；日志 `soak-run.log`）。

## 2. 断点恢复

- 步骤：记录 `generated_at=2026-11-26T01:44:05Z` → `Stop-Process` 杀服务 → 连接拒绝（预期）→ 以 `--no-immediate` 重启 → `/api/health` 返回同一 `generated_at` 与 `mode=live`。
- 结论：状态从磁盘原子快照完整恢复，无丢失；写入采用 tmp + replace，`state.prev.json` 恒为最近成功快照。

## 3. 抽样准确性（sample-verify --n 100）

- 快照 mode=live，真实条目 34（不足 100，按总量全量核验；报告如实呈现）。
- 机器判定：34/34 通过（字段完整性 / 白名单命中 / 链接格式 / 热度重算一致 / 标签一致），0 失败。
- 语义准确性无法机器判定：输出 20 条人工复核清单（见 `sample-verify-raw.txt`），不冒充通过。

## 4. 交互流畅性（浏览器实测 + 静态检查）

- 真实点击：「按更新时间」排序切换生效；分类 chip「政治」筛选 → 卡片 1 张且标签全为「政治」；搜索 "tariff" → 3 张卡；折叠面板展开；时间线事件切换按钮 12 个；外链 34 个 `target=_blank rel=noopener`。
- 四模块齐备：热度趋势走势 / 核心热点事件实时动态 / 多信源交叉验证 / 事件发展时间线。
- 离线演示（`serve --demo`）：12 张事件卡、L1 高亮边框 + 置顶徽章 2 个、交叉表「已交叉」3 行；截图 `ui-demo-seed-full.png`。
- 响应式：桌面全页截图 `ui-desktop-full.png`；800px 视口实测无横向滚动。
- 已知限制：妙手浏览器守护进程拒绝 iPhone 14 设备模拟（socket closed），≤560px 断点仅由 CSS 媒体查询静态保证，未真机实测。

## 5. 自动化测试

- `python -m unittest discover -s tests`：17 项全过（聚合 / 抓取解析 / 存储回退 / 流水线 seed / API / 核验）。
- `ruff check hot-news-monitor`、`mypy hot-news-monitor/app`：通过。
- 仓库统一门禁 `optimization_gate.py --probe`：0 阻断（4 项既有基线警告）。

## 信源可达性（2026-11-26 probe-sources）

- 可达 2/12：france24-en、npr-world（系统 mode=live 即由二者驱动）。
- 超时/拒绝 10/12：bbc、guardian、nyt、wapo、dw、aljazeera、cnn、pbs、whitehouse(404)、imf(403)。
- 评级机构（S&P/Moody's/Fitch）与 World Bank/UN 列入 `pending_verification`，地址未核实前不启用，避免编造 URL。
