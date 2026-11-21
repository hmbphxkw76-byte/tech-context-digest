# 迪拜长期居留签证台账（活值）

> **指针**：本文件是 `content/international/immigration/dubai` 业务线的政策台账活值载体；来源分级与逐条核验状态见 `data/processed/international/immigration/dubai/source_registry.json`。业务参数（口径、来源优先级、触发器）以 `content/international/immigration/dubai/prompts/business-config.md` 为单一事实源。
> **读数时点**：2026-11（基线首期）。核验 / 收敛型运行不升级版本号。
> **核验状态枚举**：`verified` = 已实际打开官方 URL 并读到内容；`snippet` = 仅搜索结果摘要，未打开原文；`unverified` = 无来源 / 仅凭记忆。

---

## 一、字段定义

| 字段 | 定义 | 口径 / 示例 |
|---|---|---|
| 通道编号 | G01–Gxx（黄金）/ N01–Nxx（绿卡），分组 | 一一对应，不混用 |
| 通道 | 英文原名 + 中文译名 | 官方页面标题为准 |
| 类别 | 投资者 / 企业家 / 杰出人才 / 科学家·专家 / 优秀学生 / 人道主义 / 前线 / 技术工人 / 自雇 / 投资者·合伙人 | 按官方定义归类 |
| 核心条件 | 学历 / 技能 / 职业级别 / 工作经验 / 推荐信 / 投资 | 逐条摘编 |
| 门槛 | 数值 + 币种 + 年 / 月口径 + 适用年份 | AED / 月毛；AED / 年 |
| 有效期 | 许可有效期 | 5 / 10 年 |
| 续期 / 境外 | 续期条件 + 境外停留上限 | 条件 + 月 |
| 担保 | 自担保 / 雇主担保 | 黄金 / 绿卡为自担保 |
| 官方 URL | 官方条款 / 细则页 | 优先公报 / 法规库 / 移民局官方页 |
| 核验状态 | verified / snippet / unverified | 见 source_registry |
| 是否更新 | 是 / 否 + 更新时间 | 核验型运行不升级版本号 |

---

## 二、黄金签证登记（G01–G08，Golden Residence）

> 联邦层面由 ICP 主管；迪拜申请经 GDRFA Dubai。有效期以官方页为准；**u.ae 与 ICP 对「房地产投资 / 企业家」年限口径不一致，见第四节与第八节 U-01**。

| 编号 | 通道 | 类别 | 核心条件 | 门槛 | 有效期 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|
| G01 | Investors in Public Investments 公共投资投资者 | 投资者 | 投资基金 / 国家银行财务存款；或设立公司资本；或合伙份额；或所属企业年缴联邦税 ≥ AED 250,000；资本须自有、非贷款；本人及家人健康保险 | AED 2,000,000（存款 / 资本 / 份额）；AED 250,000/年（税） | 10 年 | https://icp.gov.ae/en/services/uae-golden-residency/ | verified |
| G02 | Real Estate Investors 房地产投资者 | 投资者 | 自有房产总价值 ≥ AED 2,000,000（可经获批本地银行贷款）；或期房 ≥ AED 2,000,000（获批本地房企）；本人及家人健康保险 | AED 2,000,000（总价值） | 5 年（u.ae）/ 10 年（ICP），口径冲突 | https://icp.gov.ae/en/services/uae-golden-residency/ | verified |
| G03 | Entrepreneurs 企业家 | 企业家 | 注册于 UAE 的 SME（批准领域）年营收 ≥ AED 1,000,000；或获认可孵化器 / 经济部 / ICP / 地方当局批准；或曾创办并出售企业总价值 ≥ AED 7,000,000；健康保险 | AED 1,000,000/年；AED 7,000,000（出售价值） | 5 年（u.ae）/ 10 年（ICP），口径冲突 | https://icp.gov.ae/en/services/uae-golden-residency/ | verified |
| G04 | First Line of Defence 第一线防卫人员 | 前线 | 从事前线防卫工作 | — | 10 年 | https://icp.gov.ae/en/services/uae-golden-residency/ | verified |
| G05 | Scientists and Specialists 科学家与专家 | 科学家·专家 | Emirates Scientists Council 推荐；或文化部·青年部 / 工业与先进技术部 / 卫生与预防部 / 教育部推荐；高级职业级别（level 1 董事长·CEO、level 2 专家）；有效工作许可；≥本科；健康保险 | 月薪 ≥ AED 30,000 | 10 年 | https://icp.gov.ae/en/services/uae-golden-residency/ | verified |
| G06 | Humanitarian Pioneers 人道主义先驱 | 人道主义 | 国际组织 / 区域组织成员或雇员；公益组织成员；人道主义奖项；杰出志愿者；人道主义工作资助者 | — | 10 年 | https://icp.gov.ae/en/services/uae-golden-residency/ | verified |
| G07 | Outstanding Students 优秀学生 | 学生 |  UAE 高中 ≥ 95%；或国际 top100 大学学士 GPA ≥ 3.5 且毕业 ≤ 2 年；或 UAE A 类大学 GPA ≥ 3.5 / B 类 ≥ 3.8 且毕业 ≤ 2 年；学历认证 | 95% / GPA 3.5 / 3.8 | 10 年 | https://icp.gov.ae/en/services/uae-golden-residency/ | verified |
| G08 | Exceptional Talents 杰出人才 | 杰出人才 | 文化·艺术（国际级奖项 / 提名 / 认可；或 5 年专业经验等）；创新者·发明家；运动员；数字技术人才；其他经政府认定 | — | 10 年 | https://icp.gov.ae/en/services/uae-golden-residency/ | verified |

**黄金签证通用权益**：免担保人；可担保配偶、子女（不限年龄）与父母；可担保家政工；境外申请人获 6 个月多次入境签证（可再续 6 个月）以完成手续；担保人去世时家属可在许可有效期内继续留 UAE；无担保人；可生活 / 工作 / 学习 / 投资。

---

## 三、绿卡签证登记（N01–N03，Green Residence）

> 5 年可续期自担保居留；面向技术工人、自由职业者·自雇、投资者·合伙人。

| 编号 | 通道 | 类别 | 核心条件 | 门槛 | 有效期 | 官方 URL | 核验 |
|---|---|---|---|---|---|---|---|
| N01 | Skilled Workers 技术工人 | 技术工人 | UAE 有效雇佣合同；MOHRE 职业分类 1–3 级；≥本科 | 月薪 ≥ AED 15,000 | 5 年 | https://icp.gov.ae/en/services/uae-green-residency/ | verified |
| N02 | Freelancers and Self-employed 自由职业者·自雇 | 自雇 | MOHRE 自由职业 / 自雇许可；≥本科 / 专门文凭；稳定年收入或财务偿付能力证明 | 前两年自雇年收入 ≥ AED 360,000 | 5 年 | https://icp.gov.ae/en/services/uae-green-residency/ | verified |
| N03 | Investors and Business Partners 投资者·合伙人 | 投资者·合伙人 | 投资 / 入股 UAE 企业证明；相关牌照与批准 | 未明列 | 5 年 | https://icp.gov.ae/en/services/uae-green-residency/ | verified |

**绿卡通用权益**：免担保人；可担保配偶、子女（按批准要求）；许可到期后有特定期限的宽限期（grace period）。

---

## 四、信号规则（K01–K08，ex-ante 预校准）

| 编号 | 监测对象 | 等级 | 绿灯 | 黄灯 | 预警红线 | 硬红线 | 基线状态 |
|---|---|---|---|---|---|---|---|
| K01 | 类别新增 / 关闭 / 改名 | 一级 | 无变更 | 拟调整讨论 | 正式公布 | 生效 | 未触发 |
| K02 | 房产投资门槛 / 贷款·期房口径 | 一级 | 无调整 | 拟调整 | 公布新标准 | 生效 | 未触发 |
| K03 | 薪资门槛（AED 30,000 / 15,000） | 一级 | 无调整 | 拟调整 | 公布新标准 | 生效 | 未触发 |
| K04 | 职业级别分类（MOHRE 1–3 级） | 二级 | 无变更 | 审查启动 | 公布变更 | 生效 | 未触发 |
| K05 | 企业家营收 / 出售价值门槛 | 二级 | 无变更 | 讨论 | 公布 | 生效 | 未触发 |
| K06 | 境外停留 / 续期 / 宽限期 | 一级 | 无变更 | 讨论 | 公布 | 生效 | 未触发 |
| K07 | 申请材料 / 认证 / 费用 | 二级 | 无变更 | 拟调整 | 公布 | 生效 | 未触发 |
| K08 | 官方统计年度更新 | 三级 | 无 | 发布 | 数据更新 | — | 未触发 |

---

## 五、结构红线登记簿（RL-01–RL-05，ex-ante）

| 编号 | 监测对象 | 硬阈值 | 触发后动作 | 基线状态 |
|---|---|---|---|---|
| RL-01 | 主要类别 | 黄金 / 绿卡主要类别关闭或暂停 | 重算迪拜长期居留路径优先级 | 未触发 |
| RL-02 | 自担保资格 | 自担保资格收紧（如改为需担保） | 重算长期居留假设 | 未触发 |
| RL-03 | 投资门槛 | 单次上调 > 30% | 重算投资门槛与资格 | 未触发 |
| RL-04 | 处理时长 / 积压 | 积压超阈值 | 重算时间线 | 未触发 |
| RL-05 | 口径冲突 | u.ae 与 ICP 年限口径冲突未消号 | 并列呈现并升级复核 | **未消号（U-01）** |

---

## 六、政策框架复核清单（P01–P05）

| 编号 | 政策项 | 官方入口 | 复核周期 |
|---|---|---|---|
| P01 | 黄金居留类别与门槛 | `https://icp.gov.ae/en/services/uae-golden-residency/` | 事件触发 + 月度 |
| P02 | 绿卡类别与门槛 | `https://icp.gov.ae/en/services/uae-green-residency/` | 事件触发 + 月度 |
| P03 | 联邦入境与居留法令及执行条例 | `https://uaelegislation.gov.ae/` | 事件触发 |
| P04 | 迪拜申请与材料口径（GDRFA） | `https://www.gdrfad.gov.ae/` | 事件触发 + 月度 |
| P05 | 房产投资认定（DLD / Oqood） | `https://dubailand.gov.ae/` | 事件触发 |

规则：未取得官方原文的标「未核验」；入口页 ≠ 条款页；任一变更 → 立即重算受影响结论。

---

## 七、未核验清单（U-01–U-05）

| 编号 | 未核验项 | 影响与处置 |
|---|---|---|
| U-01 | u.ae 黄金签证页（2026-07-28 版）称房地产投资者 5 年、企业家 5 年；ICP 黄金居留指南称两者均 10 年 | 年限口径冲突，并列呈现；待 ICP / u.ae 版本对齐复核 |
| U-02 | 联邦《外国人入境与居留法令-法律》及其执行条例的**具体法令编号与条文**（2022-04 内阁批准执行条例，WAM 公告页多次抓取失败） | 法律依据名称待补全；以 u.ae / ICP 官方页为准 |
| U-03 | 黄金 / 绿卡处理时长与费用的官方数值（GDRFA / ICP 页面未明列） | 待官方服务卡复核 |
| U-04 | 境外停留上限的黄金签证具体口径（u.ae 表述为「超过通常 6 个月」；ICP 未给月数） | 待官方条款复核 |
| U-05 | 迪拜本地执行细则（房产净资产认定、夫妻份额合并、无犯罪记录认证批次） | 仅见非英文来源；**未找到英文权威来源，已剔除**，待英文官方页复核 |

---

## 八、计数

- 已登记黄金类别：8（G01–G08）
- 已登记绿卡类别：3（N01–N03）
- 未核验项：5（U-01–U-05）
- 已修正事实清单：首期为空
