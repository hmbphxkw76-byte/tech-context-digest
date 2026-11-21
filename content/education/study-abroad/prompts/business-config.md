# 留学信息与决策 · 业务专属配置（business-config）

> **定位**：本文件是 `content/education/study-abroad` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、受众定位、术语口径、触发器、指标追踪清单、已修正事实清单全部集中于此。周期提示词（基线 / 月度）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../engine/templates/monitoring-common-spec.md) × [类型模板](../../../../engine/templates/employment-research/)（职业就业调研型）× 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 无（14 国横向：美国 / 新加坡 / 马来西亚 / 香港 / 新西兰 / 澳大利亚 / 加拿大 / 芬兰 / 爱尔兰 / 荷兰 / 丹麦 / 挪威 / 瑞典 / 法国）
{{TOPIC}}                = 留学信息与决策（海外升学）
{{REPORT_TYPE}}          = employment-research
{{BASELINE_DATE}}        = 2026-11-21（基线报告完稿日期）
{{REGISTRY_PATH}}        = data/processed/education/study-abroad/study_abroad_ledger.md
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/education/study-abroad/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/education/study-abroad
```

**覆盖矩阵（14 国 × 学位层级，共 29 个组合）**：

| 目的地 | 本科 | 硕士 | 博士 | 工程师学院 |
|---|---|---|---|---|
| 美国 | — | ✓ | ✓ | — |
| 新加坡 | — | ✓ | ✓ | — |
| 马来西亚 | ✓ | ✓ | — | — |
| 香港 | — | ✓ | ✓ | — |
| 新西兰 | — | ✓ | ✓ | — |
| 澳大利亚 | — | ✓ | ✓ | — |
| 加拿大 | — | ✓ | ✓ | — |
| 芬兰 | — | ✓ | ✓ | — |
| 爱尔兰 | — | ✓ | ✓ | — |
| 荷兰 | — | ✓ | ✓ | — |
| 丹麦 | — | ✓ | ✓ | — |
| 挪威 | — | ✓ | ✓ | — |
| 瑞典 | — | ✓ | ✓ | — |
| 法国 | — | ✓ | ✓ | ✓ |

**各周期落盘规则**（employment-research 类型模板第四节的实例化；命名对齐仓库工具链，版本号写入报告内）：

| 节拍 | 输出路径 | 定位 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-11_baseline_report.html`（md 源稿同目录） | 对比锚，常驻顶层 | 无 |
| 月度 | `reports/{{YYYY-MM}}_monthly.html`（md 源稿同目录） | 主更新节拍，九节全模块刷新 | 最近一期月度报告 + 基线 |
| 事件触发解读 | `reports/{{YYYY-MM-DD}}-<slug>.html`（md 源稿同目录） | 单国政策 / 项目变更解读 | 基线 + 相关月度 |

**输出格式**：md 源稿 + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须过 `lint_reports.py` 与 `page_build_check.py`。

## 二、受众定位

面向「拟赴 14 国攻读本科 / 硕士 / 博士 / 法国工程师学位」的读者，兼具留学研究与升学决策顾问视角。报告允许给出框架性路径建议（标「建议 / 推断」），不承诺录取结果、不保证签证结果、不构成升学 / 留学 / 认证个案意见。

## 三、术语口径区分（表格与正文中不得混用）

- **本科 / 硕士 / 博士**：按 ISCED 2011 等级（6 / 7 / 8）对照；各国本地称谓（美国 PhD、法国 Doctorat、荷兰 PhD、北欧 Licentiate/PhD 等）须括注本地名。
- **授课型 ≠ 研究型硕士**：taught（MSc / MA）与 research（MRes / MPhil）的路径、学制、毕业要求不同，分列。
- **工程师学院 ≠ 综合大学**：法国 Diplôme d'Ingénieur（CTI 认证，ISCED 7）与大学硕士分列。
- **学费 ≠ 总成本**：学费（tuition）与生活成本（living cost）分列；总成本为自算加总并标「自算」。
- **录取 ≠ 签证 ≠ 居留**：三者法律地位不同，逐条分列。
- **学历认证 ≠ 学位认证 ≠ 专业认证**：口径不同，逐条核对官方原文。
- **排名仅作线索**：商业排名（QS / THE / ARWU）不列入采信层级，须回官方页核验后再使用。

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① **官方一手**：各国官方（大学官网 / 教育部 / 移民局 / 官方留学门户：Education USA、Study in Sweden、Study in Finland、Campus France、Education New Zealand、Study Australia、EduCanada、Education in Norway、Study in Denmark、Study in Holland、Education in Ireland、MOE Singapore、Ministry of Higher Education Malaysia、HK UGC、INIS、IND、UDI、Migri、SIRI、Home Affairs、IRCC、ICA 等）+ 多边机构（UNESCO UIS、OECD、EU Eurydice、Eurostat、World Bank EdStats）
＞ ② **官方统计与认证机构**：各国认证 / 评估机构（CTI、NOKUT、QQI、TEQSA、NZQA、UGC 等）
＞ ③ **英文行业 / 专业媒体**（Times Higher Education、Study International、The Pie News——只用于发现线索，数值须回官方页校验）
＞ ④ **英文大众媒体转述**（只作线索，须标「需核实原文」）

**来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}），严禁中文来源；若某数据点仅在中文源出现，标注「未找到英文权威来源，已剔除」并说明。政策见 `engine/docs/source-language-policy.md`（门禁 `source_check` R9）。

## 五、重大事件触发器（事件 → 受影响模块）

| 触发事件 | 受影响模块 |
|---|---|
| 任一国学签 / 签证政策变更 | 全球趋势、逐国解读、落地路径 |
| 学费 / 奖学金政策调整生效 | 成本模块、逐国解读 |
| 学制 / 学位结构改革（如博洛尼亚进程调整） | 框架总览、逐国解读 |
| 学历互认 / 认证协议签署或退出 | 认证模块、逐国解读 |
| 汇率大幅波动（>10%） | 成本模块 |
| 官方国际学生统计年度更新 | 台账、趋势 |
| 院校认证资质撤销 / 名单变更 | 院校模块、认证模块 |

## 六、指标追踪表（14 项，活值维护于 {{REGISTRY_PATH}}）

| # | 监测指标 | 口径 / 单位 | 优先数据源（英文） |
|---|---|---|---|
| 1 | 14 国国际学生规模与增速 | 人 / 同比 % | UNESCO UIS、OECD EAG、各国官方 |
| 2 | 各目的地学费区间（本币 / USD） | 本币 / 年 | 各大学官网 / 官方留学门户 |
| 3 | 生活成本基准 | 含租等效月度 | Numbeo / 官方统计 |
| 4 | 申请轮次与截止日期 | 轮次 / 日期 | 各大学官网 / 申请系统 |
| 5 | 语言要求 | 雅思 / 托福 / 本地语 | 各大学官网 |
| 6 | 学签类型与处理时长 | 类型 / 工作日 | 各国移民局 |
| 7 | 毕业后工作 / 居留通道 | 类型 / 时限 | 各国移民局 |
| 8 | 学历 / 学位认证口径 | 机构 / 状态 | 认证机构、官方认证渠道 |
| 9 | 奖学金项目与额度 | 项目 / 金额 | 官方留学门户 |
| 10 | 汇率（本币 → USD） | 汇率 | 央行 / ECB / 官方统计 |
| 11 | 学制与学位结构 | 年 / ISCED | UNESCO UIS、EU Eurydice |
| 12 | 院校类型与数量 | 所 | 官方留学门户 / UIS |
| 13 | 入学门槛（GPA / 科研 / 经验） | 分 / 项 | 各大学官网 |
| 14 | 决策失败预警信号 | 触发计数 | 台账 + 官方原文 |

## 七、已修正事实清单（基线锚，防回退；无来源不得追加）

```
【已修正事实清单 — 首期为空，产生修正后逐条补记，格式如下】
- ❌ 不得再称"…"——正确结论为…。[Source: URL, 年份]
```

## 八、基线九节结构固化锚

1. 核心结论（摘要）｜2. 全球留学市场与政策趋势｜3. 目的地供需、费用与奖学金（核心模块）｜4. 院校与项目类型细分｜5. 申请要求与能力画像｜6. 学历认证与职业资质｜7. 留学落地路径建议（结论章）｜8. 数据可靠性与局限说明｜9. 参考来源清单

## 九、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **指针引用**：事实唯一定义于台账 / 登记册 / 事实卡片（`[FC-…]`），正文用「指标编号 + 指针」（K01–K14）。
- **决策卡与行动协议**：核心判断输出决策卡（结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度）；行动项五要素 + 三档优先级。
- **阈值校准**：首次中期回测 2027-06；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **升学决策**（关联 **就业决策**：毕业后工作 / 居留衔接）；次场景 **研究参考**。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：优先补齐非英语国家英文官方页与 ISCED 版本对照。

<!-- VOCAB-SYNC:BEGIN topic=education do-not-edit -->
## 词汇速览（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 education v1.1，共 45 条（同步于 2026-11-21T18:44:58）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **教育体系与制度**（6）：学历（Education Level Attained）；学位（Degree Awarded）；高等教育（Higher Education）；义务教育年限（Compulsory Education Duration）；学制（School System）；6-3-3 学制（6-3-3 School System）
- **院校与机构**（8）：国际教育成就评价协会（IEA（教育测评）、International Association for the Evaluation of Educational Achievement）；MEXT（文部科学省、日本文部科学省、Ministry of Education, Culture, Sports, Science and Technology）；DfE（英国教育部、Department for Education）；OfS（英国学生事务办公室、Office for Students）；NCES（美国国家教育统计中心、National Center for Education Statistics）；KMK（德国各州文教部长联席会议、Standing Conference of the Ministers of Education and Cultural Affairs）；Eurydice（欧洲教育信息网络、EU Eurydice）；CERI（OECD 教育研究与创新中心、Centre for Educational Research and Innovation）
- **专业与课程**（1）：课程（Curriculum）
- **教育政策与法规**（3）：义务教育（Compulsory Education、九年义务教育）；义务教育法（中华人民共和国义务教育法、Compulsory Education Law）；教育政策（Education Policy）
- **教育评价与认证**（19）：毛入学率（GER、Gross Enrolment Ratio）；高等教育毛入学率（Higher Education GER）；净入学率（NER、Net Enrolment Rate）；入园率（Early Childhood Enrolment Rate）；毕业率（Graduation Rate）；辍学率（Dropout Rate）；师生比（Pupil-Teacher Ratio、Student-Teacher Ratio）；教育支出占 GDP 比（Education Expenditure as Share of GDP）；教育支出（Education Expenditure）；教育统计（Educational Statistics）；ISCED 2011（ISCED、国际教育标准分类 2011、International Standard Classification of Education 2011）；PISA（Programme for International Student Assessment、国际学生评估项目）；TIMSS（Trends in International Mathematics and Science Study、国际数学与科学趋势研究）；PIRLS（Progress in International Reading Literacy Study、国际阅读素养进展研究）；ICILS（International Computer and Information Literacy Study）；学历互认（学历资格互认、Recognition of Education Level）；学位互认（Recognition of Degree）；认证（Accreditation）；质量保障（Quality Assurance）
- **国际教育**（7）：UNESCO（联合国教科文组织、United Nations Educational, Scientific and Cultural Organization）；UNESCO UIS（联合国教科文组织统计研究所、UNESCO Institute for Statistics）；OECD（经济合作与发展组织、Organisation for Economic Co-operation and Development）；Education at a Glance（EAG、OECD 教育概览）；全球高等教育学历资格认可公约（UNESCO Global Convention on the Recognition of Qualifications concerning Higher Education、全球公约）；里斯本区域公约（里斯本公约、Lisbon Recognition Convention）；国际学生流动（International Student Mobility）
- **终身学习**（1）：终身学习（Lifelong Learning）
<!-- VOCAB-SYNC:END -->

## 十、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 新增留学业务线：14 国 × 学位层级矩阵（29 组合）、14 项指标追踪表、九节固化锚；阈值为 ex-ante 预校准 |
