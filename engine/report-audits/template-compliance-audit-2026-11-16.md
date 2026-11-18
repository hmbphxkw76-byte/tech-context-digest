# 模板合规性校验报告（engine/templates 全类型）

> **审计日期**：2026-11-16
> **审计范围**：`engine/templates/` 根部共享层（7 份）+ 14 个类型目录全部模板文件（31 份 `prompt-*-template.md` + 4 份配套 README/operations-guide）
> **审计依据**：通用基座（prompt-generic-base.md）、监测报告通用规范（monitoring-common-spec.md）、行业分类体系（report-classification.md）、信息分层规范（information-layering-spec.md）、决策交付规范（decision-delivery-spec.md）、compliance-rules.json、template-registry.md，以及各类型对应的行业主流专业报告范式
> **审计方法**：逐文件通读 → 骨架节数/节名与 compliance-rules.json 交叉核对 → 与 `_common.py` / `validate.py` / `compliance_check.py` 工具登记交叉核对 → 与 `engine/prompts/` 泛用版交叉核对 → 逐类型比对行业最佳实践的章节结构 / 内容模块 / 数据维度 / 呈现逻辑 / 格式规范
> **性质**：只读审计，未改动任何模板；修改建议按 P0/P1/P2 分级汇总于第五节

---

## 一、总体结论

| 维度 | 结论 |
|---|---|
| 骨架节数 vs compliance-rules.json | **31 份模板中 27 份完全一致；4 份运行期模板未显式声明骨架继承（见 P0-3）** |
| 骨架节数 vs 模板自述 | market-monitoring 三份周期模板的**版本记录**陈旧（9/12/11 节 vs 现行 8/11/10），骨架表本身正确 |
| 根部共享规范 | 发现 2 处规范断裂：① 通用规范第 5 节无「基线特例」条款但被 10+ 份基线模板引用；② `REQUIRED_TEMPLATE_FILES` 漏登 2 份根部规范 |
| 注册表层 | 泛用版提示词计数「23 份」与实际 24 份不符；其余登记与实际一致 |
| 行业最佳实践对齐 | 14 个类型**主体结构全部对齐**同类型专业报告范式；缺口集中在「运行期模板的骨架显式性」「个别行业特色字段」（催化剂、comps 表、危机分级、敏感性等） |
| 输出规范统一性 | 四层继承声明、来源分级、信息分层强制块、命名与导航规则**全类型统一**；存在模板层重复编码与版本号口径张力 |

**总评**：模板体系成熟度高于一般内部报告体系（信号规则、五态、红线归一化、假设审计、盲区消号等已是行业领先设计）。本次审计未发现会导致报告无法产出或合规校验误判的阻断级结构缺陷；需要处理的是**规范一致性与骨架显式性**问题，以及少量行业特色字段的补强。

---

## 二、骨架交叉核对表（模板 vs compliance-rules.json）

| 类型 | 周期 | 模板骨架 | rules 期望 | 结论 |
|---|---|---|---|---|
| market-monitoring | baseline | 10 节 | 10 | ✅ |
| market-monitoring | monthly | 8 节 | 8 | ✅ |
| market-monitoring | quarterly | 11 节（第 11 节为页脚 footer） | 10（注释：页脚非 h2） | ✅（模板宜标注） |
| market-monitoring | annual | 10 节 | 10 | ✅ |
| employment-research | baseline | 9 节 | 9 | ✅ |
| employment-research | monthly / quarterly / annual | 「结构逐字继承基线」9 节 | 9 | ✅ |
| competitive-intelligence | baseline | 9 节 | 9 | ✅ |
| competitive-intelligence | monthly | 9 节（逐字继承） | 9 | ✅ |
| sentiment-monitoring | baseline | 9 节 | 9 | ✅ |
| sentiment-monitoring | monthly | 9 节（逐字继承） | 9 | ✅ |
| consumer-research | baseline | 8 节 | 8 | ✅ |
| consumer-research | study | **未显式给出骨架，也未写「逐字继承基线」** | 8 | ⚠ P0-3 |
| industry-research | baseline | 9 节 | 9 | ✅ |
| industry-research | annual | 「九节逐字继承基线」 | 9 | ✅ |
| market-sizing | baseline | 9 节 | 9 | ✅ |
| market-sizing | annual | **未显式声明骨架继承** | 9 | ⚠ P0-3 |
| investment-research | baseline | 8 节 | 8 | ✅ |
| investment-research | target_update | 「八节逐字继承首次覆盖」 | 8 | ✅（命名周期映射见 P1-7） |
| policy-analysis | baseline | 9 节 | 9 | ✅ |
| policy-analysis | review | **未显式声明骨架继承** | 9 | ⚠ P0-3 |
| feasibility-study | baseline | 9 节 | 9 | ✅ |
| feasibility-study | study | **未显式给出骨架，也未写「逐字继承基线」** | 9 | ⚠ P0-3 |
| flash-commentary | baseline | 8 节 | 8 | ✅ |
| flash-commentary | flash_note | 四段式 | 4 | ✅ |
| whitepaper | baseline | 8 节 | 8 | ✅ |
| whitepaper | topic_study | **未显式给出骨架，也未写「逐字继承基线」** | 8 | ⚠ P0-3 |
| trend-weekly | baseline | 9 节 | 9 | ✅ |
| trend-weekly | weekly | 8 节 | 8（另含 1 条业务 override = 10 节） | ✅ |
| decision-dashboard | baseline | 9 节 | 9 | ✅ |
| decision-dashboard | quarterly | 9 节（同一模板） | 9 | ✅ |

---

## 三、根部共享层问题

### P0-1 通用规范第 5 节缺「基线特例」条款，被多处引用的条款不存在

- **事实**：`monitoring-common-spec.md` 第 5 节规定「全部报告统一采用 canonical 结构（`header.report-head` + `nav.report-nav` + `main.wrap`）」，**没有**任何基线例外条款。
- **影响**：14 份基线模板中 10+ 份写明「基线导航采用简化锚点目录，不强制升级为 `.report-nav`」（如 consumer-research、industry-research、market-sizing、investment-research、policy-analysis、feasibility-study、flash-commentary、whitepaper、sentiment-monitoring、competitive-intelligence、employment-research）；`market-monitoring/prompt-baseline-setup-template.md` 第 54 行更直接引用「通用规范第 5 节『基线特例』」——该引用为**断头引用**。
- **建议**：在 `monitoring-common-spec.md` 第 5 节补写基线特例条款，例如：「基线报告（含机制文档、首次覆盖、一次性深度件）允许使用简化锚点目录（`<nav>` 不含 `.report-nav` 组件），不强制 `.nav-url`；自首个周期报告起强制 canonical 结构」。同步在 `market-monitoring` baseline 模板中保留引用。

### P0-2 `REQUIRED_TEMPLATE_FILES` 漏登两份根部规范

- **事实**：`engine/tools/_common.py` 第 188–194 行 `REQUIRED_TEMPLATE_FILES` 仅含 5 份（generic-base / monitoring-common-spec / template-registry / report-classification / compliance-rules）；而 `information-layering-spec.md` 与 `decision-delivery-spec.md` 被全部 31 份模板的信息分层强制块与通用基座第十节引用，却未纳入 `validate.py` 的必备文件校验。
- **影响**：两份规范若被误删/改名，`validate.py` 不会报错，直到模板引用断链才暴露。
- **建议**：将两份规范加入 `REQUIRED_TEMPLATE_FILES`（属新增文件登记，不动既有 5 份）。

### P1-1 通用规范开头措辞陈旧

- **事实**：`monitoring-common-spec.md` 第 3 行「四份类型模板与本文件冲突时，以类型模板及业务提示词为准」——当前注册类型 14 个、模板 31 份，「四份」为 v1.0 时代（仅 4 类型）遗留措辞。
- **建议**：改为「各类型模板与本文件冲突时，以类型模板及业务提示词为准」。

### P1-2 注册表泛用版计数错误

- **事实**：`template-registry.md` 第 80 行与 v1.5 变更记录称「共 23 份独立泛用版业务提示词」；实际 `engine/prompts/` 11 个目录共 **24 份**（trend-weekly 2 + competitive-intelligence 3 + sentiment-monitoring 3 + 其余 8 类型各 2）。
- **建议**：改为 24 份，并在注册表目录树中标注「共 24 份」。

### P1-3 模板层重复编码：信息分层强制块逐字复制通用基座第十一节

- **事实**：31 份模板尾部均逐字复制「信息分层与决策交付（强制，新报告 [E]）」8 条，与 `prompt-generic-base.md` 第十一节几乎完全相同。
- **影响**：与 `information-layering-spec.md` 1.3「共享 boilerplate 上移、消除重复编码」的目标在**模板层**未贯彻；通用基座更新时这 31 处副本不会自动同步，存在漂移风险（本次审计已发现各模板该块内容与通用基座一致，但无同步机制保障）。
- **建议**（二选一）：① 模板内改为指针：「信息分层与决策交付强制项见通用基座第十一节、information-layering-spec.md、decision-delivery-spec.md，本模板不复制」；② 保留清单但在维护规范中加「与通用基座第十一节同步」校验项，并在 `template-registry.md` 变更记录中登记。倾向 ①（与仓库既定的 boilerplate 上移纪律一致）。

### P1-4 版本号口径张力

- **事实**：各周期模板要求报告内写 `{{REPORT_VERSION}}`（vYYYY.MM.DD，每期不同）；`decision-delivery-spec.md` 第七节要求「核验 / 收敛型运行不新增独立版本号，统一标注读数时点；仅核心事实修正才升级版本号」，并禁止「无意义频繁刷新版本号」。
- **影响**：字面上「每期写新版本号」与「不升级版本号」冲突，业务提示词作者可能据此在收敛型运行时仍升版。
- **建议**：在 `decision-delivery-spec.md` 第七节或通用基座变量区明确：「周期报告的 `vYYYY.MM.DD` 为**读数时点标识**，不等同语义版本升级；仅核心事实修正升级语义版本号（如 v1.1 → v1.2）」。

### P1-5 market-monitoring 周期模板版本记录陈旧

- **事实**：monthly 版本记录「抽离 9 节骨架」（现行 8 节）、quarterly「抽离 12 节骨架」（现行 11 节）、annual「抽离 11 节骨架」（现行 10 节）。骨架表本身正确，仅历史说明文字未更新。
- **建议**：修订版本记录或在现行骨架表处加脚注「初版抽离口径为 N 节，现行以本表为准」。

### P1-6 quarterly 骨架第 11 节宜标注非 h2

- **事实**：`prompt-quarterly-analysis-template.md` 骨架表列 11 节，compliance-rules.json 注释说明「第 11 节页脚为 footer 元素（可选 h2），故 h2 期望值为 10」，但模板自身未标注。
- **建议**：在骨架表第 11 节标注「（footer 元素，不计入 h2 节数）」，与规则注释对齐，避免自检时误判。

---

## 四、逐类型审计（行业最佳实践对齐）

> 每类型结构：**行业范式 → 符合项 → 待调整项 → 建议**。行业范式指同类型主流专业报告（券商/咨询/智库/市场监管机构公开范式）的通用章节逻辑。

### 1. market-monitoring（市场指标监测型）——成熟度：高

- **行业范式**：执行摘要 / 指标总览看板 / 逐指标分析（环比+同比）/ 方法论与来源 / 异常与阈值预警 / 基线偏离 / 风险与局限 / 下期观察。
- **符合项**：baseline 10 节含机制设计、维度指标、先行指标判读、信号规则、监测日历、数据治理、盲区；monthly 8 节闭环完整；quarterly 含传导链、红线归一化、升级复核、供给情景重算；annual 含预测 vs 实际、五态回测、来源巡检、台账修订。信号五态与 ex-ante 标注为行业领先设计。
- **待调整项**：
  1. monthly 逐项对比表未固定「同比」列（行业月度跟踪惯例 MoM+YoY 并列）；
  2. quarterly 第 11 节页脚标注缺失（P1-6）；三份周期模板版本记录陈旧（P1-5）。
- **建议**：monthly 第 3 节列结构固定为「编号 / 指标 / 上期值 / 本期读数 / 环比 / 同比 / 方向 / 信号距离 / 来源」；处理 P1-5、P1-6。

### 2. employment-research（职业就业调研型）——成熟度：高

- **行业范式**：摘要 / 行业与政策环境 / 供需缺口 / 薪酬基准（岗位×职级×地区）/ 雇主画像 / 技能与资质 / 求职路径与建议 / 数据与局限。
- **符合项**：九节与范式一一对应；「岗位 × 职级」交叉分层表、净薪/总包模型、来源语言规则执行声明、登记册联动均优于一般就业调研报告。
- **待调整项**：
  1. 本类型在 `engine/prompts/` 无泛用版目录，README 新建业务线步骤指向 trend-weekly 泛用版作模式参考（可接受，但便利性差）；
  2. compliance-rules 给 monthly `nav=true`，但月度为核验轻运行不出报告，规则语义冗余（无害）。
- **建议**：在 engine/prompts/ 下补建 employment-research 泛用版目录（基线+三档），或在 README 明确「本类型无泛用版，按 trend-weekly 模式手工建立」；在 rules 注释说明 monthly nav 语义。

### 3. competitive-intelligence（竞争情报监测型）——成熟度：高

- **行业范式**：摘要 / 竞争格局（份额、集中度）/ 竞品档案卡 / 动态矩阵（动作流水）/ 信号与预警 / 对我方影响 / 来源治理 / 盲区。
- **符合项**：baseline 九节与范式完全对齐；多源交叉验证（关键动作 ≥2 源、单源待证）、公开信息边界、威胁/机会与事实分离均到位。
- **待调整项**：
  1. 月度更新要点未显式要求刷新「同维度横向对比矩阵」（第 5 节动态矩阵为「维度 × 玩家」，但月度框架第一条只提份额/格局，未提对比矩阵刷新）；
  2. 事件触发件仍要求九节全量，行业惯例事件触发可短（本仓库以「专项更新」承载，可接受）。
- **建议**：月度框架第一条补「动态矩阵与对比矩阵刷新」。

### 4. sentiment-monitoring（舆情传播监测型）——成熟度：高

- **行业范式**：摘要 / 声量趋势 / 情感分布 / 议题与热点榜 / KOL 观点 / 风险预警 / 方法论与局限 / 应对建议。
- **符合项**：舆论场结构、议题声量、情感信号规则、来源与研判治理、vocal minority / 水军干扰盲区均覆盖；「舆情热度 ≠ 市场事实」声明为行业必要条款。
- **待调整项**：
  1. 信号规则表缺「预警级别」维度（蓝/黄/橙/红或一级/二级），仅有阈值与动作；
  2. 缺「传播路径 / 关键扩散节点分析」模块（行业舆情报告常见）。
- **建议**：第 5 节信号规则表增列「预警级别」；第 3 节或第 5 节增「传播路径概览（首发→扩散→峰值）」。

### 5. trend-weekly（行业趋势周报型）——成熟度：高

- **行业范式**：Top 要点 / 分板块事实 / 数据看板（上期/本期/变化）/ 风险 / 行动启示 / 来源。
- **符合项**：八节骨架与范式完全一致；业务 override 机制支持板块扩展（content/tech/weekly-roundup 为 10 节）；operations-guide 与 README 通用层/业务层职责分离清晰；命名「数据截止日」规则明确。
- **待调整项**：未发现结构性缺口。
- **建议**：无需调整（保持）。

### 6. consumer-research（消费者·用户调研型）——成熟度：中高（study 骨架缺失）

- **行业范式**（ESOMAR 惯例）：摘要 / 方法论（抽样、样本、回收率、置信度）/ 样本画像 / 核心发现 / 交叉分析 / 人群细分与画像 / 建议 / 附录（问卷与数据表）。
- **符合项**：baseline 八节对齐；样本质量声明、显著性纪律、伦理与隐私、定性脱敏均到位。
- **待调整项**：
  1. **study 模板无显式报告骨架，也未写「逐字继承基线八节」**（P0-3）；
  2. 缺「附录：问卷 / 提纲（脱敏）+ 数据表」在骨架中的固定位置（项目交付包提到数据表附录，但未映射到报告结构）。
- **建议**：study 模板补「报告结构 = 基线八节逐字继承」声明；骨架第 8 节前增「附录（问卷/提纲脱敏、数据表）」。

### 7. industry-research（行业深度研究型）——成熟度：高

- **行业范式**：摘要 / 行业定义与范围 / 产业链 / 规模与格局 / 竞争格局 / 驱动与风险 / 趋势 / 风险提示 / 附录。
- **符合项**：九节对齐；「不含清单」、多口径并列、趋势推断与反向声音、中性边界（无评级无 Go/No-Go）均正确。
- **待调整项**：
  1. 缺「专家访谈执行披露」（访谈场数、匿名化口径）——第 2 节提到专家访谈但无披露要求。
- **建议**：第 2 节或第 8 节增「访谈执行情况（N 场、匿名口径、执行窗口）」。

### 8. market-sizing（市场规模测算与预测型）——成熟度：高

- **行业范式**：摘要 / 方法论（自上而下/自下而上）/ 口径定义 / 基准年规模 / 预测与情景 / 敏感性 / 假设清单 / 局限。
- **符合项**：九节对齐；假设审计表、回测规则、三情景 + 区间、「假设乘积」纪律为行业必要设计；年度刷新的回测归因闭环完整。
- **待调整项**：
  1. annual refresh 未显式声明「九节逐字继承基线」（P0-3，轻度）。
- **建议**：节拍设计表下补一句结构继承声明。

### 9. investment-research（投资分析与尽调型）——成熟度：高

- **行业范式**：投资要点（评级/目标价/估值区间）/ 公司概况 / 行业与竞争 / 财务分析 / 估值（DCF、comps）/ 风险 / 情景 / 合规声明。
- **符合项**：八节对齐；「结论必须明确」、估值区间多方法并列、利益冲突与合法性声明、重大未决事项降级为有条件结论均符合行业规范。
- **待调整项**：
  1. 缺「关键催化剂与时点（catalysts）」字段（行业研报惯例）；
  2. 缺「可比公司明细表」固定结构（comps：公司/倍数/估值）；
  3. compliance-rules 未登记 quarterly/annual 周期，定期复核报告按命名会被回落到 baseline 规则校验（P1-7）。
- **建议**：第 1 节或第 6 节增「关键催化剂与时点」；第 4 节增 comps 明细表要求；rules 增周期映射。

### 10. policy-analysis（政策法规解读型）——成熟度：高

- **行业范式**：摘要 / 政策背景与原文 / 条款解读 / 影响矩阵 / 合规建议 / 生效时间线 / 来源。
- **符合项**：九节对齐；官方原文铁律、歧义多解并列、不构成法律意见声明均到位。
- **待调整项**：
  1. review 模板未显式声明「九节逐字继承基线」（P0-3，轻度）。
- **建议**：补结构继承声明。

### 11. feasibility-study（可行性与市场进入型）——成熟度：高

- **行业范式**：摘要 / 项目范围与评估框架 / 市场 / 技术与运营 / 财务（投资、回收期、IRR、NPV）/ 法规合规 / 风险与缓解 / Go/No-Go 与实施路线图。
- **符合项**：九节对齐；「必须收敛到单一决策」、综合集成引用纪律、有条件 Go 条件清单均符合可研报告规范。
- **待调整项**：
  1. **study 模板无显式报告骨架，也未写「逐字继承基线九节」**（P0-3）；
  2. 财务测算未强制「敏感性分析」（仅要求三情景；行业可研惯例含关键参数敏感性）。
- **建议**：补结构继承声明；第 5 节财务测算增「敏感性：关键参数 ±x% 对回收期/IRR 的影响」。

### 12. flash-commentary（快评·事件点评型）——成熟度：高

- **行业范式**（flash note）：事件 / 预期 vs 实际 / 影响判断 / 观察点。
- **符合项**：四段式完全对齐；72h 时效、预期台账、官方原文底线、单源直引禁令、事后补验均为行业必要设计。
- **待调整项**：未发现结构性缺口。
- **建议**：无需调整（保持）。

### 13. whitepaper（白皮书·专题深度型）——成熟度：高

- **行业范式**：摘要 / 问题定义 / 框架与方法 / 深度论证 / 案例 / 观点与倡议 / 审校 / 来源。
- **符合项**：八节对齐；观点与事实分离、原创框架登记、品牌与合规审校记录、勘误件机制均符合对外发布物规范。
- **待调整项**：
  1. **topic-study 模板无显式报告骨架，也未写「逐字继承基线八节」**（P0-3）。
- **建议**：补结构继承声明。

### 14. decision-dashboard（决策仪表盘型）——成熟度：高

- **行业范式**（decision dashboard）：决策摘要 / 决策卡 / 证据强度 / 触发条件 / 缺失清单 / 行动协议 / 场景切片 / 盲区 / 读数时点。
- **符合项**：九节与 `decision-delivery-spec.md` 第三节骨架逐条对应；决策卡台账 JSON 格式、三档优先级、ex-ante 标注为强制项。
- **待调整项**：
  1. baseline 与 quarterly 共用同一模板，但两档 nav 期望不同（false/true），模板未区分渲染要求。
- **建议**：模板补一行「baseline 用简化锚点导航；quarterly 起强制 `.report-nav`」。

---

## 五、修改建议汇总（按优先级）

### P0（规范断裂，建议尽快处理）

| # | 问题 | 涉及文件 | 建议 |
|---|---|---|---|
| P0-1 | 通用规范第 5 节无「基线特例」条款，被 10+ 份基线模板引用；market-monitoring baseline 存在断头引用 | monitoring-common-spec.md 第 5 节 | 补写基线特例条款 |
| P0-2 | `REQUIRED_TEMPLATE_FILES` 漏登 information-layering-spec.md、decision-delivery-spec.md | engine/tools/_common.py | 补登两份根部规范 |
| P0-3 | 5 份运行期模板（consumer study、market-sizing annual、policy review、feasibility study、whitepaper topic-study）未显式声明骨架继承，业务提示词作者无结构依据 | 对应 5 份模板 | 各补「报告结构 = 基线 N 节骨架逐字继承」声明（market-monitoring 与 flash-commentary 已有先例） |

### P1（一致性与口径）

| # | 问题 | 建议 |
|---|---|---|
| P1-1 | 通用规范「四份类型模板」措辞陈旧 | 改为「各类型模板」 |
| P1-2 | 注册表泛用版计数 23 ≠ 实际 24 | 更正为 24 |
| P1-3 | 31 份模板尾部信息分层强制块逐字复制通用基座，存在漂移风险 | 改为指针或加同步校验 |
| P1-4 | 周期报告 vYYYY.MM.DD 与版本治理「不升级版本号」口径张力 | 明确 vYYYY.MM.DD = 读数时点标识 |
| P1-5 | market-monitoring 三份周期模板版本记录陈旧 | 修订或加脚注 |
| P1-6 | quarterly 骨架第 11 节宜标注非 h2 | 加标注 |
| P1-7 | investment-research 定期复核命名（quarterly/annual）在 rules 中无周期映射，校验回落 baseline | rules 增映射或模板声明命名预期 |

### P2（行业特色增强，按业务需要采纳）

| # | 类型 | 增强建议 |
|---|---|---|
| P2-1 | market-monitoring | monthly 逐项对比表固定同比列 |
| P2-2 | competitive-intelligence | 月度框架补「对比矩阵刷新」 |
| P2-3 | sentiment-monitoring | 信号规则增「预警级别」；增传播路径分析 |
| P2-4 | consumer-research | 骨架固定附录（问卷/提纲脱敏、数据表） |
| P2-5 | industry-research | 增专家访谈执行披露 |
| P2-6 | investment-research | 增关键催化剂与时点、comps 明细表 |
| P2-7 | feasibility-study | 财务测算增敏感性分析 |
| P2-8 | decision-dashboard | 区分 baseline / quarterly 渲染要求 |

---

## 六、结论

1. **结构合规**：31 份模板的骨架节数与 compliance-rules.json 全部可对齐（含 quarterly 页脚注释），未发现会导致合规校验误判的阻断级缺陷。
2. **行业对齐**：14 个类型的章节结构、内容模块、数据维度、呈现逻辑均与同类型主流专业报告范式对齐，market-monitoring / trend-weekly / flash-commentary / decision-dashboard 达到行业领先成熟度。
3. **主要风险**：集中在规范一致性（P0-1/2/3、P1 系列）而非模板设计本身；建议在下一维护窗口按 P0 → P1 顺序处理，P2 按业务需要排期。
4. **统一输出规范**：四层继承声明、来源分级、命名与导航、信息分层强制项已全类型统一；处理 P1-3/P1-4 后可实现模板层与规范层的单一事实源闭环。

---

*审计人：妙手（CatPaw）｜审计对象版本：template-registry v1.11 / compliance-rules v1.1 / 各模板 v1.0*
