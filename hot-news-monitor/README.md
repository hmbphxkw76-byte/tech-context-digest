# hot-news-monitor · 热点新闻实时追踪报告系统

参照 `hormuzstraitmonitor.com` 的内容组织逻辑（状态总览 → 关键指标卡 → 影响分析 → 时间线）构建的
实时新闻追踪看板：英文权威信源 → 抓取 / 聚合 / 交叉验证 → 本地 API + 响应式前端。界面、内容与提示全部为中文。

> 注册信息：顶层受控目录（`engine/tools/layout.json` 的 `root_reserved`），不属六主题报告业务线。
> 运行时产物写入 `runtime/`，不入库（见 `.gitignore`）。

## 快速开始

```bash
cd hot-news-monitor
python -m app serve --host 127.0.0.1 --port 8765 --interval 300 --threshold 50
# 打开 http://127.0.0.1:8765/
```

子命令：

| 命令 | 作用 |
| --- | --- |
| `serve` | 调度（默认每 300s 全量刷新）+ 本地 HTTP 服务；加 `--demo` 为离线演示（仅合成示例数据，不联网） |
| `refresh` | 立即做一次全量刷新并输出摘要 |
| `probe-sources` | 探测白名单信源可达性，结果落 `runtime/source_probe.json` |
| `sample-verify --n 100` | 随机抽样机器核验（字段/来源/链接/热度重算） |
| `soak --duration 1800` | 长跑稳定性测试（默认 30 分钟，含刷新节拍核对） |

零第三方依赖（仅 Python 标准库）；单元测试：`python -m unittest discover -s tests`。

## 四大核心模块（固定存在）

1. **核心热点事件实时动态**：事件卡片流，含分类标签、热度值、独立信源数、迷你趋势；
2. **热度趋势走势**：Top 5 事件的热度采样折线（SVG，阈值虚线）；
3. **多信源交叉验证**：按事件列出独立信源数 / 最高信源层级 / 交叉结论（已交叉 / 双源互补 / 单源待补证）；
4. **事件发展时间线**：按时间正序还原单一事件节点，可切换事件。

排序与筛选：按热度降序 / 更新时间倒序 / 分类标签 + 分类 chips 筛选 + 标题搜索。
自动刷新：每 5 分钟 `GET /api/state`，顶部进度条 + 内容微透明过渡（无感加载），
保留当前筛选、排序与滚动位置，不打断浏览；「立即刷新」走 `POST /api/refresh`。

三级信息层级：L1 热度 ≥ 阈值 → 金色高亮边框 + 「置顶 · 高优先级」标识；
L2 每事件「背景溯源」折叠面板（覆盖结构与采信强度说明）；L3 每条报道「阅读原文 ↗」外链。

**热度展示口径**：界面只显示三档级别——`热`（≥ 阈值，默认 50）、`高`（≥ 25）、`中`（< 25）；悬停可见精确数值。排序、趋势与核验仍使用内部数值（API 字段不变）。

## 来源纪律（硬性）

- 白名单唯一事实源：`config/sources.json`；仅英文权威媒体 / 国际评级机构 / 官方公开资料；
- **禁止中文媒体**：`app/verify.py` 内置违禁域名黑名单做机器兜底；
- 未核验条目在配置中显式标 `status: unverified`；可达性以运行期 `probe-sources` 结果为准；
- 示例数据（`seed` 模式）全部合成、标注「示例」，不计入准确性核验通过口径；
- 引用格式 `[Source: URL, 抓取时间]` 由页面外链与快照时间共同承载。

### 信源现状（2026-11-26 探测）

- 可达：`france24-en`、`npr-world`（mode=live）；
- 超时 / 拒绝：bbc、guardian、nyt、wapo、dw、aljazeera、pbs、cnn（网络环境受限，程序降级为 hybrid/seed 并在状态栏如实标注）；
- 待接入（地址未核实，未启用）：S&P Global / Moody's / Fitch / World Bank / UN News（见配置 `pending_verification`）。

## 验证口径（等价方案，替代 24 小时连续运行）

- **长跑稳定性**：`python -m app soak --duration 1800`（30 分钟真实运行，逐拍核对快照可用）；
  断点恢复：写入采用 tmp + replace 原子替换，`state.prev.json` 恒为最近成功快照，进程被杀后重启自动续跑；
- **抽样准确性**：`sample-verify --n 100` 机器判定字段完整性、来源白名单命中、链接合规、热度重算一致；
  语义准确性无法机器判定，脚本输出人工复核清单（不冒充通过）；
- **交互流畅性**：浏览器实测各模块（见 `tests/` 与运行记录），静态检查覆盖响应式断点 / 可访问性底线。

## 目录

```
hot-news-monitor/
├── config/sources.json     # 信源白名单（单一事实源）
├── app/                    # models / store / fetch / aggregate / seed / pipeline / scheduler / server / verify
├── dashboard/index.html    # 单页看板（内联 CSS/JS + SVG 图表）
├── tests/                  # unittest：聚合 / 抓取解析 / 存储 / 流水线 / API / 核验
└── runtime/                # 运行时生成（不入库）
```
