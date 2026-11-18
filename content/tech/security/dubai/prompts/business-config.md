# 迪拜 AI 网络安全 · 业务专属配置（business-config）

> **定位**：本文件是 `content/tech/security/dubai` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、受众定位、术语口径、触发器、指标追踪清单、已修正事实清单全部集中于此。周期提示词（基线 / 月 / 季 / 年）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [类型模板](../../../../../engine/templates/employment-research/)（职业就业调研型）× 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 网络安全
{{REPORT_TYPE}}          = employment-research
{{BASELINE_DATE}}        = 2026-11-11（基线报告完稿日期）
{{REGISTRY_PATH}}        = data/processed/tech/security/dubai/ai_cybersecurity_indicator_registry.md
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/security/dubai/source_registry.json
{{BASELINE_REPORT_PATH}} = sources/2026-11_baseline_report.md
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（全部取自英文网站，严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/security/dubai
```

**各周期落盘规则**（employment-research 类型模板第四节的实例化；命名对齐仓库工具链，版本号写入报告内）：

| 节拍 | 输出路径 | 定位 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-11_baseline_report.html`（md 源稿存 `sources/`） | 对比锚，常驻顶层 | 无 |
| 月度 | `reports/{{YYYY-MM}}_monthly.html`（md 源稿存 `sources/`） | 核验型轻运行，无触发不启动新报告 | 登记册更新记录 |
| 季度 | `reports/{{YYYY-Qn}}_quarterly.html`（md 源稿存 `sources/`） | 主更新节拍，九节全模块刷新 | 最近一期季度报告 + 基线 |
| 年度 | `reports/{{YYYY}}_annual.html`（md 源稿存 `sources/`） | 复盘：预测对照 + 清单复审 + 路线图重排 | 最近一期季度报告 + 基线 |

**输出格式**：纯 HTML 交付（业务配置声明，走 monitoring-common-spec 第 1 节例外条款）：canonical 富样式自包含 HTML 为主交付物，落盘 `reports/{{周期}}.html`；md 源稿存 `sources/` 同名存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。

## 二、受众定位

面向「拟赴迪拜从事 AI 网络安全就业」的读者，兼具行业分析与职业规划顾问视角。报告允许给出框架性求职路径建议（标「建议 / 推断」），不承诺就业结果、不保证薪资水平。

## 三、术语口径区分（表格与正文中不得混用）

- 基本工资 ≠ 总额（总包）：黄金签证门槛、离职补偿（Gratuity）、ILOE 分档均以**基本工资**计
- 名义薪资 ≠ 净薪（阿联酋 0% 个税、外籍 0% 社保，ILOE 为唯一强制扣减）≠ 总包价值（含房补 / 教育 / 机票 / 奖金）
- MENA 信息安全**终端支出**（Gartner）≠ 阿联酋市场**含服务总收入**（Mordor / GMI），口径不同不可直接比较
- 招聘机构抽样 ≠ 薪酬指南官方年版（前者标注「抽样」并谨慎引用）
- 汇率固定：1 USD = 3.6725 AED（钉住）

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① 阿联酋/迪拜政府官方（u.ae、desc.gov.ae、tdra.gov.ae、mediaoffice.ae、icp.gov.ae、added.gov.ae、WAM 英文、各自由区官网）
＞ ② 国际权威组织（ISC2、ISACA、Gartner、IDC、SANS/GIAC、MITRE、OWASP、NIST）
＞ ③ 头部薪酬指南与招聘平台抽样（Hays、Robert Half、Cooper Fitch、Michael Page、Charterhouse；LinkedIn、Bayt、GulfTalent、Naukrigulf、foundit Gulf——仅作市场信号，不与官方 / 行业机构同等采信）
＞ ④ 英文行业/主流媒体（Khaleej Times、The National、Gulf News、Zawya、Reuters、Arab News——只用于发现线索，数值须回官方/原始页校验）

**来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}）；若某数据点仅在中文源出现，标注「未找到英文权威来源，已剔除」并说明。Hays 与 GulfTalent 的原始网络安全分表若仅能经由非英文或二手摘要获取，须排除其未核实数字。

## 五、重大事件触发器（事件 → 受影响模块）

| 触发事件 | 受影响模块 |
|---|---|
| GITEX Global / GISEC Global 新一届举办（日期、主题、官方发布） | 市场趋势、雇主生态、落地路径 |
| ISC2《Cybersecurity Workforce Study》新年版发布 | 人才供需与薪酬 |
| Gartner 中东与北非信息安全支出预测更新（通常 4 月） | 市场趋势 |
| 阿联酋/迪拜新网络安全法规或 AI 安全政策生效 | 市场趋势、雇主生态、落地路径 |
| 任一头部薪酬指南发布新年版 | 人才供需与薪酬 |
| 黄金签证 / 阿化（Emiratisation）规则变更 | 人才供需与薪酬、落地路径 |
| 新 AI 安全证书发布或 SANS 海湾日程更新 | 技能要求、证书、落地路径 |

## 六、指标追踪表（14 项，活值维护于 {{REGISTRY_PATH}}）

| # | 监测指标 | 口径/单位 | 优先数据源（英文） |
|---|---|---|---|
| 1 | MENA 信息安全支出 & 增速 | 亿美元 / 同比 % | gartner.com/newsroom |
| 2 | 阿联酋网安市场规模 & CAGR | 亿美元 / % | mordorintelligence.com / gminsights.com |
| 3 | 日均攻击量 / 国家背景占比 | 次/日 / % | khaleejtimes.com / uaecsc.gov.ae |
| 4 | ISC2 人力研究（技能缺口/AI 占比） | % / 人数 | isc2.org/Insights |
| 5 | 五大薪酬指南最新年版网安分表 | 年版 | hays.ae / roberthalf.ae / cooperfitch.ae / michaelpage.ae / charterhouseme.ae |
| 6 | AI 安全岗薪资抽样 | AED/月 | hiredeveloper.ae / gulftalent.com / bayt.com |
| 7 | Numbeo 迪拜 vs 阿布扎比生活成本 | 含租等效月度 | numbeo.com |
| 8 | ILOE 费率 & 黄金签证门槛 | AED/月 / AED | iloe.ae / u.ae / icp.gov.ae |
| 9 | Stargate UAE 状态 | — | openai.com / coloprice.com |
| 10 | GISEC / GITEX 最新届次 | 日期 | gisec.ae / gitex.com |
| 11 | G42/Core42/CPX/e&/Moro Hub 动态 | — | 各公司官网 / WAM |
| 12 | OWASP LLM Top 10 / MITRE ATLAS 版本 | 版本/计数 | genai.owasp.org / atlas.mitre.org |
| 13 | 新发 AI 安全证书 & 本地考点 | — | giac.org / isc2.org / comptia.org / eccouncil.org / sans.org |
| 14 | DESC ISR v3.1 / ISR 审核员计划 | 版本/控制域 | desc.gov.ae |

## 七、已修正事实清单（基线锚，防回退；无来源不得追加）

```
- ❌ 不得再称"Black Hat MEA 在阿布扎比"——该会议 2025 年起已在沙特利雅得举办。[Source: https://www.blackhatmea.com/about-us/key-information, 2026]
- ❌ 不得再称 ILOE 失业险"每周 AED 5/10"——实为**每月** AED 5（基本≤1.6万）/ AED 10（基本>1.6万）+5% VAT。[Source: https://www.iloe.ae/pdf/Involuntary-Loss-of-Employment-Brochure-ILOE-V2.pdf, 2025]
- ❌ 不得再称"阿布扎比同岗薪资普遍高出迪拜 10–15%"——多数权威来源显示迪拜名义薪资更高，阿布扎比优势在生活成本低约 15–20%；结论是**净购买力大致相当**。[Source: https://www.numbeo.com/cost-of-living/compare_cities.jsp?city1=Dubai&city2=Abu+Dhabi, 2025]
- ❌ 不得再将 CPX 与 DarkMatter 绑定——CPX 为 2022 年成立的 G42 子公司，与 DarkMatter→Digital14 系不同实体。[Source: https://www.cpx.net, 2025]
- ❌ 不得再引用微软–G42「152 亿美元」broad 投资计划——经复核未获英文权威来源证实（微软官方仅确认 2024.4 的 **15 亿美元**股权注资与 10 亿美元开发者基金），按来源语言规则标注「未找到英文权威来源，已剔除」并列入待复核。[Source: https://blogs.microsoft.com/blog/2024/04/15/microsoft-and-g42-partner, 2024]
- ❌ 黄金签证门槛须以**基本工资**（非总额）计，并标注 2026-10 阿布扎比收紧动向待 ICP 最终确认。[Source: https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa, 2025]
```

## 八、基线九节结构固化锚

基线报告 `sources/2026-11_baseline_report.md` 九节结构为该业务线固化锚，后续报告逐字继承：

1. 核心结论（摘要）｜2. 市场发展趋势｜3. 人才供需状况与薪资（核心模块）｜4. 企业类型细分｜5. 岗位技能要求｜6. 行业认可的职业证书｜7. 就业落地建议（结论章）｜8. 数据可靠性与局限说明｜9. 参考来源清单（完整 URL）

---

## 九、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **事实卡片**：本业务线为共享事实域（SEC），正文以 `[FC-SEC-…]` 引用 `engine/fact_cards/security_fact_cards.json`，不复制卡片全文。
- **决策卡与行动协议**：核心判断输出决策卡（结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度）；行动项五要素 + 三档优先级。
- **阈值校准**：首次中期回测 2027-06；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **就业决策**；次场景 **政策制定**。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（就业 / 收入 / 空置 / 竣工）优先消号。

---

<!-- VOCAB-SYNC:BEGIN topic=tech do-not-edit -->
## 词汇速览（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 tech v1.3，共 153 条（同步于 2026-11-18T08:50:16）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **网络攻击技术**（44）：拒绝服务攻击（DoS、DDoS、分布式拒绝服务）；勒索软件（Ransomware）；钓鱼攻击（Phishing、鱼叉钓鱼、Spear Phishing）；中间人攻击（MITM、Man-in-the-Middle）；SQL 注入（SQLi、SQL Injection）；跨站脚本（XSS、Cross-Site Scripting）；跨站请求伪造（CSRF、XSRF）；远程代码执行（RCE、Remote Code Execution）；零日漏洞利用（Zero-Day、0-day）；横向移动（Lateral Movement）；高级持续性威胁（APT、Advanced Persistent Threat）；供应链攻击（Supply Chain Attack）；挖矿木马（Cryptojacking、挖矿程序）；水坑攻击（Watering Hole）；路过式下载（Drive-by Download）；键盘记录（Keylogger、键盘记录器）；木马（Trojan、特洛伊木马）；蠕虫（Worm、计算机蠕虫）；僵尸网络（Botnet）；Rootkit；无文件攻击（Fileless Attack、无文件恶意软件）；DNS 隧道（DNS Tunneling）；凭据填充（Credential Stuffing）；暴力破解（Brute Force、爆破）；口令喷洒（Password Spraying）；社会工程学（Social Engineering）；商业邮件欺诈（BEC、Business Email Compromise）；点击劫持（Clickjacking）；缓冲区溢出（Buffer Overflow）；Evil Twin（双胞胎热点、恶意热点）；ARP 欺骗（ARP Spoofing、ARP 毒化）；DNS 劫持（DNS Hijacking）；BGP 劫持（BGP Hijacking）；命令注入（Command Injection）；不安全反序列化（Insecure Deserialization、反序列化漏洞）；XXE（XML 外部实体注入、XML External Entity）；SSRF（服务端请求伪造、Server-Side Request Forgery）；目录遍历（Path Traversal、Directory Traversal）；越权访问（Broken Access Control、访问控制失效）；语音钓鱼（Vishing、电话钓鱼）；短信钓鱼（Smishing）；深度伪造（Deepfake、深度伪造攻击）；物理渗透（Physical Intrusion、物理入侵测试）；无线干扰（Jamming、无线拒绝服务）
- **防御与安全运营**（47）：防火墙（Firewall）；WAF（Web 应用防火墙、Web Application Firewall）；IDS/IPS（入侵检测/防御系统、IDS、IPS）；SIEM（安全信息与事件管理、Security Information and Event Management）；SOAR（安全编排自动化与响应、Security Orchestration, Automation and Response）；沙箱（Sandbox、动态分析沙箱）；蜜罐（Honeypot）；漏洞扫描（Vulnerability Scanning）；渗透测试（Penetration Testing、Pen Test）；攻击面管理（ASM、Attack Surface Management）；威胁狩猎（Threat Hunting）；事件响应（Incident Response、IR）；欺骗防御（Deception Technology、欺骗技术）；网络分段（Network Segmentation、微隔离、Microsegmentation）；邮件安全网关（SEG、Secure Email Gateway）；安全基线（Security Baseline、加固基线）；系统加固（Hardening、安全加固）；备份与容灾（Backup and Recovery、3-2-1 备份）；NDR（网络检测与响应、Network Detection and Response）；XDR（扩展检测与响应、Extended Detection and Response）；MDR（托管检测与响应、Managed Detection and Response）；UEBA（用户与实体行为分析、User and Entity Behavior Analytics）；数字取证（DFIR、数字取证与事件响应）；CSPM（云安全态势管理、Cloud Security Posture Management）；CWPP（云工作负载保护平台、Cloud Workload Protection Platform）；SASE（安全访问服务边缘、Secure Access Service Edge）；CASB（云访问安全代理、Cloud Access Security Broker）；容器安全（Container Security）；Kubernetes 安全（K8s 安全、K8s Security）；物联网安全（IoT Security）；工控安全（OT 安全、ICS Security、工业控制系统安全）；无线安全（Wireless Security、Wi-Fi 安全）；SAST（静态应用安全测试、Static Application Security Testing）；DAST（动态应用安全测试、Dynamic Application Security Testing）；软件组成分析（SCA、Software Composition Analysis）；API 安全（API Security）；攻防演练（红蓝对抗、实战攻防演练）；身份与访问管理（IAM、Identity and Access Management）；目录服务（AD、Active Directory、LDAP）；网络访问控制（NAC、Network Access Control）；统一端点管理（UEM、Unified Endpoint Management）；移动安全（Mobile Security）；应用加固（App Hardening、APP 加固）；告警分诊（Alert Triage）；攻击溯源（Attribution、攻击归因）；桌面推演（TTX、Tabletop Exercise）；韧性指标（RTO、RPO、恢复时间目标）
- **漏洞与漏洞管理**（11）：CVE（Common Vulnerabilities and Exposures、公共漏洞披露）；CVSS（通用漏洞评分系统、Common Vulnerability Scoring System）；负责任披露（Responsible Disclosure、漏洞披露）；补丁管理（Patch Management）；漏洞利用代码（Exploit、EXP、PoC）；CWE（通用缺陷枚举、Common Weakness Enumeration）；漏洞赏金（Bug Bounty）；SBOM（软件物料清单、Software Bill of Materials）；云配置错误（Cloud Misconfiguration、配置漂移）；漏洞管理平台（VM、漏洞生命周期管理）；安全公告（Advisory、漏洞预警）
- **密码与身份认证**（20）：对称加密（Symmetric Encryption）；非对称加密（Asymmetric Encryption、公钥加密）；哈希（Hash、散列）；PKI（公钥基础设施、Public Key Infrastructure）；TLS（传输层安全、Transport Layer Security）；MFA（多因素认证、Multi-Factor Authentication、2FA）；SSO（单点登录、Single Sign-On）；特权访问管理（PAM、Privileged Access Management）；端到端加密（E2EE、End-to-End Encryption）；数字签名（Digital Signature）；证书透明度（CT、Certificate Transparency）；密钥轮换（Key Rotation）；OAuth（开放授权、OAuth 2.0）；FIDO2（免密认证、Fast Identity Online）；秘密管理（Secrets Management、密钥管理服务、KMS）；硬件安全模块（HSM、Hardware Security Module）；零知识证明（ZKP、Zero-Knowledge Proof）；后量子密码（PQC、Post-Quantum Cryptography）；隐私计算（Privacy-Preserving Computation、隐私增强技术）；通行密钥（Passkey、同步通行密钥）
- **框架与合规**（19）：ISO/IEC 27001（信息安全管理体系、ISMS）；NIST CSF（网络安全框架、Cybersecurity Framework）；网络安全等级保护（等保、MLPS）；GDPR（通用数据保护条例、General Data Protection Regulation）；UAE PDPL（阿联酋个人数据保护法、Personal Data Protection Law）；SOC 2（服务组织控制 2、Service Organization Control 2）；PCI DSS（支付卡行业数据安全标准）；HIPAA（健康保险可携性与责任法案）；数据分类分级（Data Classification）；安全意识培训（Security Awareness Training）；共享责任模型（Shared Responsibility Model）；DevSecOps（开发安全运营、安全左移）；数据主权（Data Sovereignty）；数据脱敏（Data Masking、匿名化、Anonymization）；中国网络安全法（网络安全法、CSL）；中国数据安全法（数据安全法、DSL）；数据跨境传输（数据出境、Cross-Border Data Transfer）；业务连续性管理（BCM、BCP、业务连续性计划）；网络保险（Cyber Insurance、网络安全保险）
- **认证与岗位**（12）：OSCP（攻击性安全认证专业人员、Offensive Security Certified Professional）；CEH（道德黑客认证、Certified Ethical Hacker）；CISM（注册信息安全管理师、Certified Information Security Manager）；安全运营分析师（SOC Analyst、安全分析师）；CompTIA Security+（Security Plus）；CISA 认证（注册信息系统审计师、Certified Information Systems Auditor）；CCSP（认证云安全专家、Certified Cloud Security Professional）；云安全架构师（Cloud Security Architect）；应用安全工程师（AppSec Engineer、安全开发工程师）；首席信息安全官（CISO）；安全研究员（漏洞研究员、Security Researcher）；安全合规官（GRC 经理、治理风险合规岗）
<!-- VOCAB-SYNC:END -->

## 十、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 自 failed-project 迁移适配：四层继承体系改指向 employment-research 类型模板；补运行变量固定值、来源优先级实例化、触发器、14 项指标追踪表、已修正事实清单、九节固化锚 |
| v1.1 | 2026-11-13 | 来源口径对齐 | 已修正事实清单第 5 条改写：微软–G42「152 亿美元」经复核未获英文权威来源证实，按来源语言规则标注「已剔除、待复核」，仅保留已确认的 15 亿美元股权注资与 10 亿美元开发者基金 |
| v1.2 | 2026-11-13 | 词汇库绑定机制 | 接入 `engine/vocabulary/script/sync_vocab.py` 自动同步：新增「词汇速览（词汇库自动同步）」标记区间，由脚本维护（网络安全术语与别名的唯一速览源，与第三节术语口径区分互为补充）；区间外内容不受同步影响 |
