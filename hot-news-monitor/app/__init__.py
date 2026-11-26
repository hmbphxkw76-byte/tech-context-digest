"""hot-news-monitor：英文权威信源热点新闻实时追踪报告系统。

子模块：
- models：数据模型（NewsItem / HotEvent / Snapshot）
- store：运行时存储（state.json 快照 + fetch_log/items JSONL 台账）
- fetch：RSS/Atom 抓取与来源可达性探测
- aggregate：去重、事件聚类、热度计算、分类标签
- seed：离线示例数据（合成占位，非真实新闻）
- pipeline：抓取 → 聚合 → 落盘编排（CLI 与服务共用）
- scheduler：固定周期调度（默认 21600 秒 / 6 小时）
- server：本地 HTTP 服务（看板静态页 + /api/state 等接口）
"""
