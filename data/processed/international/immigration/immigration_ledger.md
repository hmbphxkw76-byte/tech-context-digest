# 高技能移民政策台账（活值）

> **指针**：本文件是 `content/international/immigration` 业务线的政策台账活值载体；来源分级与逐条核验状态见 `data/processed/international/immigration/source_registry.json`。业务参数（口径、来源优先级、触发器）以 `content/international/immigration/prompts/business-config.md` 为单一事实源。
> **读数时点**：2026-11（基线首期）。核验 / 收敛型运行不升级版本号。
> **核验状态枚举**：`verified` = 已实际打开官方 URL 并读到内容；`snippet` = 仅搜索结果摘要，未打开原文；`unverified` = 无来源 / 仅凭记忆。

---

## 一、字段定义

| 字段 | 定义 | 口径 / 示例 |
|---|---|---|
| 通道编号 | C01–C46，按国别分组 | 一一对应，不混用 |
| 国家 | 九国之一 | 新西兰 / 荷兰 / 澳大利亚 / 爱尔兰 / 加拿大 / 美国 / 新加坡 / 德国 / 法国 |
| 通道 | 英文原名 + 中文译名 | 官方页面标题为准 |
| 类别 | 雇主担保 / 积分制 / 人才类 / 留学生过渡 / 创业 | 按官方定义归类 |
| 核心条件 | 学历 / 技能 / 语言 / 工作经验 / 担保 | 逐条摘编 |
| 薪资门槛 | 数值 + 币种 + 年 / 月 / 小时口径 + 适用年份 | 年毛 / 月毛 / 小时；本币 |
| 有效期 | 许可有效期 | 年 / 月 |
| 转永居 | 转永居 / 长期居留路径 | 居住年限 + 条件 |
| 官方 URL | 官方条款 / 细则页 | 优先公报 / 法规数据库 / 移民局官方页 |
| 核验状态 | verified / snippet / unverified | 见_source_registry |
| 是否更新 | 是 / 否 + 更新时间 | 核验型运行不升级版本号 |

---

## 二、九国通道登记（C01–C46）

### 新西兰（C01–C04）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛 | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C01 | Accredited Employer Work Visa (AEWV) 认证雇主工签 | 雇主担保 | 认证雇主全职 offer；2 年相关经验或 NZQCF 4 级 + 学历；技能 3–5 级需英语；雇主须认证 + job check | 不低于市场工资 + 法定最低工资（2025-03-10 起取消中位数要求） | 最长 5 年（ANZSCO 4–5 级为 3 年） | 可经 SMC / 绿名单 | https://www.immigration.govt.nz/new-zealand-visas/visas/visa/accredited-employer-work-visa | verified |
| C02 | Straight to Residence（绿名单 Tier 1）直通永居 | 人才类 / 雇主 | 绿名单 Tier1 职业、55 岁以下；认证雇主全职、英语、职业注册 / 学历 | 绿名单指定薪资，或当前中位工资 | 永居 | 直接永居 | https://www.immigration.govt.nz/visas/straight-to-residence-visa | snippet |
| C03 | Work to Residence（绿名单 Tier 2）工签转永居 | 雇主担保 | 绿名单 Tier2 职业；在认证雇主处工作满 24 个月 | 绿名单 Tier2 指定薪资 | 永居 | 24 个月后转永居 | https://www.immigration.govt.nz/visas/work-to-residence-visa | snippet |
| C04 | Skilled Migrant Category (SMC) 技术移民（6 分制） | 积分制 | 认证雇主 offer、55 岁以下；3 路径：积分制 6 分 / 技能工作经验 5 年（含 2 年新）/ 技工 4 年（含 18 个月新）；英语 | 现行门槛 NZD 35.00/小时（2026-03-09 起）；2025-08-18 至 2026-03-08 为 33.56；收入积分 3 倍 = 105.00 | 永居 | 直接永居 | https://www.immigration.govt.nz/visas/skilled-migrant-category-resident-visa | verified |

### 荷兰（C05–C07）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛（2026，税前月毛薪） | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C05 | Highly Skilled Migrant (kennismigrant / KMS) 高技术移民 | 雇主担保 | IND 认可担保方；雇佣合同；薪资符合市场水平 | ≥30 岁 €5,942；<30 岁 €4,357；毕业生降低标准 €3,122 | 同合同，最长 5 年 | 连续 5 年可申欧盟永居 | https://ind.nl/en/residence-permits/work/highly-skilled-migrant | verified |
| C06 | Orientation Year (zoekjaar) 搜索年 | 留学生过渡 | 毕业 / 博士 / 研究结束 3 年内；或指定海外院校（TOP200）硕士 | 无薪资门槛（可自由工作） | 1 年 | 可衔接 HSM 降低标准 | https://ind.nl/en/residence-permits/work/residence-permit-for-orientation-year | verified |
| C07 | EU Blue Card 欧盟蓝卡 | 雇主 / 高学历 | 高学历（≥3 年）或 5 年相关经验（IT 为 3 年 / 7 年内）；合同 ≥6 个月；无需认可担保 | 标准 €5,942；毕业生降低 €4,754 | 页面未明列 | 部分情况 2 年可申欧盟永居 | https://ind.nl/en/residence-permits/work/european-blue-card-residence-permit | verified |

### 澳大利亚（C08–C11）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛 | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C08 | National Innovation visa (subclass 858) 国家创新签证 | 人才类 | 国际公认卓越成就者；EOI 邀请制；需国家声誉提名人；费用 AUD 6,235 | 无 | 永居 | 直接永居 | https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/national-innovation-visa-858 | snippet |
| C09 | Employer Nomination Scheme (ENS / 186) 雇主提名 | 雇主担保 | TRT 类：持 457 / 482 并为提名雇主全职工作满 2 年；费用 AUD 6,140 | 不低于 TSMIT / 市场工资 | 永居 | 直接永居 | https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/employer-nomination-scheme-186/temporary-residence-transition-stream | snippet |
| C10 | Skills in Demand (SID / 482) 技能需求签证（取代 TSS） | 雇主担保 | Core Skills：CSOL 职业 + 1 年经验 + 英语；Specialist Skills：高薪、无清单 | Core Skills ≥ CSIT；Specialist ≥ SSIT | 最长 4 年（香港 5 年） | 可申 186 | https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/skills-in-demand-visa-subclass-482/core-skills-stream | snippet |
| C11 | Skilled Independent (189) 独立技术移民 | 积分制 | SkillSelect EOI 获邀；积分制 65 分起评 | 无明文 | 永居 | 直接永居 | https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/skilled-independent-189/points-table | snippet |

### 爱尔兰（C12–C14）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛（2026-03 起） | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C12 | Critical Skills Employment Permit (CSEP) 关键技能就业许可 | 雇主担保 | CSOL 上高技能紧缺职业（ICT、工程、科技等）；2 年 job offer；相关学位；免劳动力市场测试（LMNT）；50:50 规则（初创 2 年内豁免） | 有相关学位 €40,909；无相关学位 €68,911；应届（12 个月内）€36,849 | 2 年 | 期满可直接向司法部申 Stamp 4，2 年一续；满 60 个月可申长期居留 | https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/Critical-Skills-Employment-Permit/ | verified |
| C13 | General Employment Permit (GEP) 一般就业许可 | 雇主担保 | 广泛职业（除 Ineligible List）；12 个月合同亦可；多数需 LMNT；50:50 规则 | 一般 €36,605；HCA / 护工 / 肉类 / 园艺 €32,691；爱尔兰毕业生 €34,009 | 首次 ≤2 年，可续 3 年 | 连续 5 年可申长期居留 / Stamp 4 | https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/General-Employment-Permit/ | verified |
| C14 | Intra-Company Transfer 跨国公司调派 | 雇主担保 | 跨国企业高管 / 关键人员 / 培训生；海外关联公司调派 | €49,522（2026） | — | — | https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/Intra-Company-Transfer-Employment-Permit/ | verified（入口） |

### 加拿大（C15–C20）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛 | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C15 | Express Entry（FSW / CEC / FST + 类别抽签） | 积分制 | 入池 + CRS 排名；类别轮次需满足该类别条件 | 无统一门槛 | PR 直接获批 | 即永居 | https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations/category-based-selection.html | verified |
| C16 | └ STEM 类别 | 积分制 | STEM 职业；过去 3 年内 12 个月全职经验（境内外均可），职业在清单内 | — | — | — | 同上 | verified |
| C17 | Global Talent Stream (GTS) | 雇主担保 | A 类需指定推荐伙伴；B 类需在全球人才职业清单 | — | 工签 | 可转 PR | https://www.canada.ca/en/employment-social-development/services/foreign-workers/global-talent.html | snippet |
| C18 | Global Skills Strategy (GSS) | 高技能 | 完整申请 2 周处理 | — | — | — | https://www.canada.ca/en/employment-social-development/services/foreign-workers/global-skills-strategy/2-week-processing.html | verified |
| C19 | Tech Talent Strategy：H-1B 持有者开放工签 | 高技能 | 美国 H-1B 持有人；几乎可为任意加拿大雇主工作 3 年；带直系亲属 | — | 3 年 | — | https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/tech-talent.html | verified（状态 Closed） |
| C20 | Start-up Visa (SUV) | 创业 | 指定机构背书 | — | — | 直接 PR | https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/start-visa.html | snippet |

### 美国（C21–C30）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛 | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C21 | H-1B | 雇主担保 | 本科 + 相关学位；LCA；年度抽签 | 现行工资 prevailing wage | 3 + 3 年 | 可申 EB 类 | https://www.uscis.gov/working-in-the-united-states/h-1b-specialty-occupations | verified |
| C22 | O-1A | 人才类 | 持续国内 / 国际声誉；8 项满足 3 项或重大奖项 | 无 | 3 年初始 + 1 年延，无上限 | 可转 EB-1A | https://www.uscis.gov/working-in-the-united-states/temporary-workers/o-1-visa-individuals-with-extraordinary-ability-or-achievement | verified |
| C23 | EB-1A | 人才类 | 10 项满足 3 项或一次性大奖；可自申 | 无 | 直接绿卡 | 即永居 | https://www.uscis.gov/working-in-the-united-states/employment-based-immigration-first-preference-eb-1 | verified |
| C24 | EB-1B | 人才类 | 3 年经验；6 项满足 2 项；雇主 offer | 无 | 直接绿卡 | 即永居 | 同上 | verified |
| C25 | NIW (EB-2) | 人才类 | 高等学位 / 特殊能力；国家利益；可自申 | 无 | 直接绿卡 | 即永居 | https://www.uscis.gov/working-in-the-united-states/employment-based-immigration-second-preference-eb-2 | snippet |
| C26 | L-1A / L-1B | 雇主担保 | 3 年内 1 年海外；高管 / 专门知识 | 无 | 7 年 / 5 年 | 可转 EB-1C | https://www.uscis.gov/working-in-the-united-states/temporary-workers/l-1a-intracompany-transexecutive-or-manager | verified |
| C27 | E-3 | 雇主担保 | 澳大利亚公民；专业职业 | — | — | — | https://travel.state.gov/content/travel/en/us-visas/employment/treaty-trader-investor-visa-e.html | snippet |
| C28 | TN | 雇主担保 | 加 / 墨公民；USMCA 职业清单 | — | 3 年 + 无限 3 年延 | — | https://www.uscis.gov/working-in-the-united-states/temporary-workers/tn-usmca-professionals | verified |
| C29 | F-1 OPT / STEM OPT | 留学生过渡 | STEM 学位 + E-Verify 雇主 | 无 | 12 + 24 = 36 月 | — | https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-extension-for-stem-students-stem-opt | verified |
| C30 | International Entrepreneur Parole | 创业 | 重大公共福利 | 无 | 初次最长 30 个月 | — | https://www.uscis.gov/policy-manual/volume-3-part-g | snippet |

### 新加坡（C31–C34）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛 | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C31 | Employment Pass (EP) | 雇主担保 | 两阶段：①达 qualifying salary；②通过 COMPASS（40 分） | 2025 新申请 / 2026 续签：一般 S$5,600/月（23 岁起递增，45+ 至 S$10,700）；金融 S$6,200（45+ S$11,800）。2027 新申请 / 2028 续签：S$6,000（45+ S$11,500）；金融 S$6,600（45+ S$12,700） | 首次 ≤2 年，续签 ≤3 年 | 可申请 PR（须 ICA 审批） | https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility | verified |
| C32 | EP（科技紧缺 5 年） | 雇主担保 | COMPASS 短缺职业清单（SOL）上的资深科技人员；通过 COMPASS 且 C3（多样性）≥10 分；属 SOL 职业 | 2025 新申请 / 2026 续签：≤36 岁 S$10,700，45+ 至 S$14,270；2027 / 2028：S$11,500 至 S$15,499 | 最长 5 年 | 同 EP | https://www.mom.gov.sg/passes-and-permits/employment-pass/experienced-tech-professionals-with-skills-in-shortage | verified |
| C33 | S Pass | 雇主担保 | 中级技术（APT）；配额 + 征费；须 MyCareersFuture 广告 | S$3,300/月（45 岁中旬至 S$4,800）；2027 新申请 / 2028 续签升至 S$3,600 | 首次 ≤2 年，续签 ≤3 年 | 可申请 PR | https://www.mom.gov.sg/passes-and-permits/s-pass/key-facts | verified |
| C34 | ONE Pass | 人才类 | 顶级人才（商业 / 艺术 / 体育 / 学研 / AI 与科技）；过去 12 个月或未来雇主固定月薪 ≥S$30,000；或杰出成就 | S$30,000/月 | 首次及续签各 ≤5 年 | 可申请 PR | https://www.mom.gov.sg/passes-and-permits/overseas-networks-expertise-pass/key-facts | verified |

### 德国（C35–C41）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛 | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C35 | EU Blue Card | 雇主 / 高学历 | 德国 / 承认的外国高校学位 + 达到最低毛薪的工作合同 | 官方英文页被机器人防护拦截，2025 / 2026 数值未核验；一般规则见 glossary | 通常 4 年或合同期 + 3 个月 | 蓝卡加速通道（B1 21 个月 / A1 27 个月，须另核验） | https://www.make-it-in-germany.com/en/advice-support/glossary/glossary-detail/glossar/do/show/blaue-karte-eu | verified（仅一般规则） |
| C36 | §18b AufenthG 学术人才 | 高学历 | 高校学历者；合格学历即可从事任何合格工作 | 无固定门槛（按工资基准） | — | — | https://www.gesetze-im-internet.de/aufenthg_2004/__18b.html | verified |
| C37 | §18a AufenthG 职业资格人才 | 职业资格 | 受认可职业资格 | — | — | — | https://www.gesetze-im-internet.de/aufenthg_2004/__18a.html | verified |
| C38 | §19c(2) 经验丰富者 | 经验 | 无正式学历但有突出实践技能者；由《就业条例》规定可从事 | — | — | — | https://www.gesetze-im-internet.de/aufenthg_2004/__19c.html | verified |
| C39 | IT 专门签证 | 雇主 / 高技能 | IT 人才（可无正式高校学位） | 未核验 | — | — | https://www.make-it-in-germany.com/en/visa-recognition/visa-types | verified（条目存在） |
| C40 | Chancenkarte（机会卡） | 积分制 | 无雇主合同、积分达标者；积分制（学历 / 经验 / 语言 / 年龄等） | 无 | 未核验 | — | https://www.make-it-in-germany.com/en/visa-recognition/opportunity-card | snippet（页面被拦截） |
| C41 | §20 求职居留 | 留学生过渡 | 在德完成学业 / 研究 / 培训者；毕业后求职 | 须保障生活 | 最长 18 个月（研究 / 学历路径） | — | https://www.gesetze-im-internet.de/aufenthg_2004/__20.html | verified |

### 法国（C42–C46）

| 编号 | 通道 | 类别 | 核心条件 | 薪资门槛 | 有效期 | 转永居 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|---|
| C42 | Talent – salarié qualifié | 雇主 / 高技能 | 法国硕士同等学历或 CGE 标注 level 1 文凭；合同 >3 个月 | 年毛薪 ≥€39,582 | 同合同期，最长 4 年 | 可（5 年连续居住路径） | https://www.service-public.fr/particuliers/vosdroits/F16922?lang=en | verified |
| C43 | Talent – entreprise innovante | 雇主 / 高技能 | 创新企业（JEI / 获经济部认可）研发岗；岗位直接关联研发项目 | 年毛薪 ≥€39,582 | 最长 4 年 | 同上 | 同上 | verified |
| C44 | Talent – salarié en mission | 雇主 / 高技能 | 集团内派驻；同集团工龄 ≥3 个月；与法国雇主签约 | 年毛薪 ≥€39,582 | 最长 4 年 | 同上 | 同上 | verified |
| C45 | Talent – Carte bleue européenne（法国 EU 蓝卡） | 高技能 | ≥3 年高等教育学历，或 5 年可比经验（内政部法令职业为 7 年内 3 年）；合同 ≥6 个月 | 年毛薪 ≥1.5× 平均年毛薪，即 €59,373 | 合同 ≥2 年 → 同合同期，最长 4 年；合同 <2 年 → 合同期 + 3 个月，最长 2 年 | 可 | 同上 | verified |
| C46 | Talent famille | 家庭 | 配偶及未成年子女随主申请人 | — | 多年期 talent famille 卡 | — | https://www.service-public.fr/particuliers/vosdroits/F35792 | snippet |

---

## 三、信号规则阈值（K01–K08，ex-ante 预校准）

| 编号 | 监测对象 | 等级 | 绿灯 | 黄灯 | 预警红线 | 硬红线 | 基线状态 |
|---|---|---|---|---|---|---|---|
| K01 | 通道新增 / 关闭 / 改名 | 一级 | 无变更 | 拟调整讨论 | 正式公布 | 生效 | 未触发 |
| K02 | 薪资门槛调整 | 一级 | 无调整 | 拟调整 | 公布新标准 | 生效 | 未触发 |
| K03 | 配额 / 抽签规则 | 一级 | 无变更 | 规则讨论 | 公布新规则 | 生效 | 未触发 |
| K04 | 职业清单调整 | 一级 | 无变更 | 审查启动 | 公布变更 | 生效 | 未触发 |
| K05 | 积分计分规则 | 二级 | 无变更 | 讨论 | 公布 | 生效 | 未触发 |
| K06 | 永居 / 居住年限 | 一级 | 无变更 | 讨论 | 公布 | 生效 | 未触发 |
| K07 | STEM / AI / IT 定向 | 一级 | 无新增 | 政策讨论 | 专项通道公布 | 生效 | 未触发 |
| K08 | 官方统计年度更新 | 三级 | 无 | 发布 | 数据更新 | — | 未触发 |

## 四、结构红线登记簿（RL-01–RL-05）

| 编号 | 监测对象 | 硬阈值 | 触发后动作 | 基线状态 |
|---|---|---|---|---|
| RL-01 | 主要通道 | 通道关闭或暂停 | 重算九国路径优先级 | 未触发 |
| RL-02 | 永居路径 | 永居路径中断 | 重算长期定居假设 | 未触发 |
| RL-03 | 配额 | 配额耗尽致通道实际关闭 | 重算可申请窗口 | 未触发 |
| RL-04 | 薪资门槛 | 单次上调 >30% | 重算雇主成本与资格 | 未触发 |
| RL-05 | 排期 / 积压 | 积压超阈值 | 重算时间线 | 未触发 |

## 五、政策框架复核清单（G01–G05）

| 编号 | 政策项 | 官方入口 | 复核周期 |
|---|---|---|---|
| G01 | 各国移民局 / 内政部 | 九国官方页 | 事件触发 + 月度 |
| G02 | 官方公报 / 法规数据库 | 各国公报 / 法规库 | 事件触发 + 月度 |
| G03 | 职业清单与配额 | 各国官方清单 | 月度 + 年度 |
| G04 | 欧盟蓝卡框架 | EU 官方（europa.eu） | 月度 |
| G05 | 官方统计与处理时长 | 各国官方统计 | 月度 + 年度 |

## 六、已修正事实清单

```
- 首期为空；后续运行产生修正后逐条补记（格式：❌ 不得再称「旧说法」——实际为「新说法」。[Source: URL, 年份]）。
```

## 七、未核验清单（U-01–U-12）

| 编号 | 未核验项 | 影响与处置 |
|---|---|---|
| U-01 | 澳大利亚 immi.homeaffairs.gov.au 全部页面（Akamai 拦截），C08–C11 仅 snippet | 薪资门槛与日期须人工官方页复核 |
| U-02 | 德国 make-it-in-germany 的 Blue Card / Chancenkarte 专页（机器人防护），C35 / C40 数值未核验 | 待 BAMF / arbeitsagentur 英文页补采 |
| U-03 | 美国 H-1B 年度配额数字（65,000 / 20,000）未核验 | 待联邦公报 / USCIS 官方页复核 |
| U-04 | 美国 E-3 / IEP 仅 snippet | 待 travel.state.gov / USCIS 原文复核 |
| U-05 | 新加坡 Tech.Pass 现行官方专页未找到（旧 URL 404） | 以 ONE Pass / EP 为准，待确认是否并入 |
| U-06 | 加拿大 2026–2028 水平计划与 PNP 技术类未核验 | 待 canada.ca 官方页复核 |
| U-07 | 加拿大 SUV 2026 暂停与开放工签关闭为 snippet | 待 canada.ca 官方公告复核 |
| U-08 | 新西兰绿名单逐职业调整公告页未找到 | 待 INZ 官方公告复核 |
| U-09 | 法国 2024–2025 Talent Passport 逐年门槛未找到官方对照页 | 待 service-public.fr 历史版复核 |
| U-10 | 爱尔兰 CSOL 具体 ICT 条目为 docx 附件，未逐条核验 | 待官方清单复核 |
| U-11 | 荷兰 EU Blue Card 有效期页面未明列 | 待 IND 页面复核 |
| U-12 | 德国《技术移民法》2024-11-18 修订生效仅见非官方转述 | 待官方英文页复核 |

## 八、计数

| 项 | 值 |
|---|---|
| 已登记通道 | 46（C01–C46） |
| verified | 27 |
| snippet | 17 |
| unverified | 2 |
| 待采集 | 0（基线九国已覆盖） |
| 信号 / 红线 / 框架 | K01–K08 / RL-01–RL-05 / G01–G05 |
