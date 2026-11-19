# 社会词汇库（society）

> **定位**：vocabulary 子系统主题词库，由 `script/vocab_tool.py` 统一管理；词汇表请勿手工编辑，变更一律走 `import` / `tag` 命令。
> **主题配置**：`config/topics.json` → `society`（社会主题词汇：社会结构与分层、人口与家庭、社会保障与福利、文化与价值观、城市化与社区、风险与公共危机、媒体与传播（骨架，待采集））
> **去重规范**：词条与别名经归一化（NFKC + 空白折叠 + 忽略大小写）后全局唯一；别名/标签分隔符为半角 `;`。

## 词汇表

| ID | 词条 | 别名 | 分类 | 标签 | 定义 | 来源 | 首次登记 | 最近更新 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SOC-001 | 人口动态 | 人口動態;population dynamics | 人口与家庭 | 人口 | 出生、死亡与迁移三要素引起的人口规模与结构变动；须并列出生、死亡、迁移口径。 | 総務省統計局 人口推計 https://www.stat.go.jp/data/jinsui/ | 2026-11-19 | 2026-11-19 |
| SOC-002 | 老龄化率 | 高齢化率;aging rate | 人口与家庭 | 老龄化 | 65 岁及以上人口占总人口比例；与总抚养比（少儿加老年）分列。 | 総務省統計局 https://www.stat.go.jp/ | 2026-11-19 | 2026-11-19 |
| SOC-003 | 总抚养比 | 総扶養比;total dependency ratio | 人口与家庭 | 抚养 | 0–14 岁与 65 岁及以上人口之和占 15–64 岁劳动年龄人口的比例。 | World Bank WDI https://data.worldbank.org/ | 2026-11-19 | 2026-11-19 |
| SOC-004 | 总和生育率 | 合計特殊出生率;TFR | 人口与家庭 | 生育 | 育龄妇女平均生育子女数；低于 2.1 为低于更替水平。 | 国立社会保障・人口問題研究所 https://www.ipss.go.jp/ | 2026-11-19 | 2026-11-19 |
| SOC-005 | 家庭户 | 家庭戸;household | 人口与家庭 | 家庭 | 共同居住与生活单位的统计口径；与常住人口、户籍人口分列。 | 中国国家统计局 https://www.stats.gov.cn/ | 2026-11-19 | 2026-11-19 |
| SOC-006 | 基尼系数 | Gini coefficient | 社会结构与分层 | 不平等 | 按家庭可支配收入计算的分配不平等度量（0–1）；与收入五等分比口径不同。 | OECD Income Distribution Database https://data.oecd.org/inequality/income-inequality.htm | 2026-11-19 | 2026-11-19 |
| SOC-007 | 劳动参与率 | 労働力率;labor force participation rate | 社会结构与分层 | 就业 | 15 岁及以上经济活动人口（就业加失业）占工作年龄人口比例；与失业率分列。 | ILO https://www.ilo.org/ | 2026-11-19 | 2026-11-19 |
| SOC-008 | 城镇化率 | 都市化率;urbanization rate | 城市化与社区 | 城镇化 | 城镇常住人口占总人口比例；各国城乡划分标准不同，跨国对照须注明定义。 | UN World Urbanization Prospects https://population.un.org/wup/ | 2026-11-19 | 2026-11-19 |
| SOC-009 | 社会保障覆盖率 | 社会保障カバー率;social protection coverage | 社会保障与福利 | 社保 | 享受法定社会保障险种待遇的人口比例；与社会保障支出占比分列。 | ILO World Social Protection Report https://www.ilo.org/ | 2026-11-19 | 2026-11-19 |
| SOC-010 | 单人家庭 | 1人世帯;single-person household | 人口与家庭 | 家庭;老龄化 | 由一名成员构成的家庭户；与家庭户总数、户均规模分列。 | 韓国行政安全部 居民登记人口统计 https://www.mois.go.kr/ | 2026-11-19 | 2026-11-19 |

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
| --- | --- | --- | --- |
| v1.0 | 2026-11-18 | 首建词库 | topic-add/init 创建空词库骨架 |
| v1.1 | 2026-11-19 | 批量导入 | 新增 10 条 / 跳过重复 0 条 / 无效 0 条；文件 2026-11-18_seed-social-structure.md |
