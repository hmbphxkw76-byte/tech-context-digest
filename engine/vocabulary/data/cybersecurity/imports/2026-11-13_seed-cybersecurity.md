# 网络安全词汇 · 种子导入文件（48 条）

> **用途**：vocabulary 子系统 cybersecurity 主题首批种子，走标准 import 流程入库（不直接写 terms.md）。
> **范围界定**：传统/网络层安全词汇（非 AI 专项）；与 ai-security 主题重叠的词条（SOC、红队、零信任、EDR、MITRE ATT&CK 等）已在彼库登记，本库不再重复。
> **来源规则**：官方一手与标准机构优先；无法当场核验的标注「需核实原文」。

| 词条 | 别名 | 分类 | 标签 | 定义 | 来源 |
|---|---|---|---|---|---|
| 拒绝服务攻击 | DoS;DDoS;分布式拒绝服务 | 网络攻击技术 | 攻击;可用性 | 通过耗尽目标资源使其无法为正常用户提供服务的攻击，分布式形态为 DDoS | CISA（需核实原文） |
| 勒索软件 | Ransomware | 网络攻击技术 | 攻击;勒索 | 加密受害者数据并索要赎金（常伴数据窃取双重勒索）的恶意软件 | CISA（需核实原文） |
| 钓鱼攻击 | Phishing;鱼叉钓鱼;Spear Phishing | 网络攻击技术 | 攻击;社工 | 以伪装可信发件人诱导泄露凭据或执行恶意载荷的社会工程攻击，定向形态为鱼叉钓鱼 | CISA（需核实原文） |
| 中间人攻击 | MITM;Man-in-the-Middle | 网络攻击技术 | 攻击;网络层 | 攻击者秘密截获或篡改通信双方流量的攻击 | OWASP（需核实原文） |
| SQL 注入 | SQLi;SQL Injection | 网络攻击技术 | 攻击;Web | 将恶意 SQL 片段注入应用输入以操纵后端数据库的注入攻击 | OWASP Top 10 |
| 跨站脚本 | XSS;Cross-Site Scripting | 网络攻击技术 | 攻击;Web | 向页面注入恶意脚本在其他用户浏览器中执行的漏洞利用 | OWASP Top 10 |
| 跨站请求伪造 | CSRF;XSRF | 网络攻击技术 | 攻击;Web | 诱导已认证用户浏览器携带其凭据发起非预期请求的攻击 | OWASP（需核实原文） |
| 远程代码执行 | RCE;Remote Code Execution | 网络攻击技术 | 攻击;高危 | 使目标系统远程执行攻击者任意代码的严重漏洞利用 | CISA（需核实原文） |
| 零日漏洞利用 | Zero-Day;0-day | 网络攻击技术 | 攻击;漏洞 | 利用尚未公开或未发布补丁的漏洞的攻击 | CISA（需核实原文） |
| 横向移动 | Lateral Movement | 网络攻击技术 | 攻击;入侵后 | 攻击者立足后在内网扩展控制范围的手法集合 | MITRE ATT&CK |
| 高级持续性威胁 | APT;Advanced Persistent Threat | 网络攻击技术 | 攻击;组织化 | 具备长期驻留与定向目标能力的高水平攻击组织及其活动 | MITRE ATT&CK |
| 供应链攻击 | Supply Chain Attack | 网络攻击技术 | 攻击;供应链 | 经由软件依赖、更新通道或第三方服务商渗入目标的攻击 | CISA（需核实原文） |
| 挖矿木马 | Cryptojacking;挖矿程序 | 网络攻击技术 | 攻击;恶意软件 | 未经授权占用受害者算力进行加密货币挖掘的恶意软件 | 行业综述（需核实原文） |
| 防火墙 | Firewall | 防御与安全运营 | 防御;网络层 | 依安全策略控制进出网络流量的边界防护设备或功能 | NIST SP 800-41（需核实原文） |
| WAF | Web 应用防火墙;Web Application Firewall | 防御与安全运营 | 防御;Web | 针对 HTTP/HTTPS 流量按规则防护 Web 攻击（注入、XSS 等）的应用层防火墙 | OWASP（需核实原文） |
| IDS/IPS | 入侵检测/防御系统;IDS;IPS | 防御与安全运营 | 防御;检测 | 侦测（IDS）或侦测并阻断（IPS）恶意网络活动的设备与系统 | NIST（需核实原文） |
| SIEM | 安全信息与事件管理;Security Information and Event Management | 防御与安全运营 | 运营;检测 | 聚合关联全网安全日志与事件以支持检测、调查与合规的平台 | NIST（需核实原文） |
| SOAR | 安全编排自动化与响应;Security Orchestration, Automation and Response | 防御与安全运营 | 运营;自动化 | 以剧本编排自动化处置安全告警与响应流程的平台 | Gartner（需核实原文） |
| 沙箱 | Sandbox;动态分析沙箱 | 防御与安全运营 | 防御;分析 | 隔离环境中执行可疑文件并观测行为的安全分析机制 | 行业实践 |
| 蜜罐 | Honeypot | 防御与安全运营 | 防御;诱捕 | 伪装为真实目标的诱饵系统，用于吸引并研究攻击行为 | 行业实践 |
| 漏洞扫描 | Vulnerability Scanning | 防御与安全运营 | 运营;检测 | 自动探测主机与应用已知漏洞的周期性评估活动 | NIST（需核实原文） |
| 渗透测试 | Penetration Testing;Pen Test | 防御与安全运营 | 评估;攻击模拟 | 在授权范围内模拟攻击者验证系统安全性的评估服务 | NIST SP 800-115 |
| 攻击面管理 | ASM;Attack Surface Management | 防御与安全运营 | 运营;治理 | 持续发现、盘点与收敛互联网暴露资产的运营实践 | 行业综述（需核实原文） |
| 威胁狩猎 | Threat Hunting | 防御与安全运营 | 运营;主动检测 | 基于假设在环境内主动搜寻潜伏威胁的运营活动 | 行业实践 |
| 事件响应 | Incident Response;IR | 防御与安全运营 | 运营;响应 | 对安全事件进行准备、检测、遏制、根除与恢复的流程 | NIST SP 800-61（需核实原文） |
| CVE | Common Vulnerabilities and Exposures;公共漏洞披露 | 漏洞与漏洞管理 | 漏洞;编号 | MITRE 主持的公开信息安全漏洞统一编号体系 | cve.org |
| CVSS | 通用漏洞评分系统;Common Vulnerability Scoring System | 漏洞与漏洞管理 | 漏洞;评分 | FIRST 维护的漏洞严重程度量化评分标准（0–10 分） | FIRST |
| 负责任披露 | Responsible Disclosure;漏洞披露 | 漏洞与漏洞管理 | 漏洞;流程 | 向厂商协调报告漏洞并按约定时限公开的披露流程 | ISO/IEC 29147（需核实原文） |
| 补丁管理 | Patch Management | 漏洞与漏洞管理 | 运营;修复 | 获取、测试与部署软件补丁以修复漏洞的周期性流程 | NIST（需核实原文） |
| 漏洞利用代码 | Exploit;EXP;PoC | 漏洞与漏洞管理 | 漏洞;武器化 | 触发并利用特定漏洞的程序或技术验证代码 | 行业通用惯例 |
| 对称加密 | Symmetric Encryption | 密码与身份认证 | 密码学 | 加解密使用同一密钥的加密体制（如 AES） | NIST FIPS 197 |
| 非对称加密 | Asymmetric Encryption;公钥加密 | 密码与身份认证 | 密码学 | 使用公私钥对的加密体制（如 RSA、ECC） | NIST FIPS 186（需核实原文） |
| 哈希 | Hash;散列 | 密码与身份认证 | 密码学 | 将任意数据映射为固定长度摘要的单向函数（如 SHA-256） | NIST FIPS 180-4 |
| PKI | 公钥基础设施;Public Key Infrastructure | 密码与身份认证 | 密码学;证书 | 以数字证书与证书机构为核心的密钥管理与信任体系 | NIST SP 800-57（需核实原文） |
| TLS | 传输层安全;Transport Layer Security | 密码与身份认证 | 协议;加密 | 保障通信机密性与完整性的传输层协议（SSL 的继任者） | IETF RFC 8446 |
| MFA | 多因素认证;Multi-Factor Authentication;2FA | 密码与身份认证 | 身份 | 结合知识、持有物与生物特征中至少两类要素的认证机制 | NIST SP 800-63B（需核实原文） |
| SSO | 单点登录;Single Sign-On | 密码与身份认证 | 身份 | 一次认证访问多个应用系统的身份联合机制 | NIST（需核实原文） |
| 特权访问管理 | PAM;Privileged Access Management | 密码与身份认证 | 身份;权限 | 对高权限账号的管控、审计与临时授权机制 | 行业实践 |
| ISO/IEC 27001 | 信息安全管理体系;ISMS | 框架与合规 | 标准;合规 | 信息安全管理体系国际认证标准 | iso.org |
| NIST CSF | 网络安全框架;Cybersecurity Framework | 框架与合规 | 标准;治理 | 美国国家标准机构的网络安全治理框架（识别/防护/检测/响应/恢复） | nist.gov |
| 网络安全等级保护 | 等保;MLPS | 框架与合规 | 法规;合规 | 中国网络安全分等级保护监管制度（等保 2.0） | 全国信息安全标准化技术委员会（需核实原文） |
| GDPR | 通用数据保护条例;General Data Protection Regulation | 框架与合规 | 法规;隐私 | 欧盟个人数据处理的统一监管法规 | EUR-Lex |
| UAE PDPL | 阿联酋个人数据保护法;Personal Data Protection Law | 框架与合规 | 法规;隐私 | 阿联酋联邦第 45/2021 号个人数据保护法令 | 阿联酋数据办公室（需核实原文） |
| SOC 2 | 服务组织控制 2;Service Organization Control 2 | 框架与合规 | 审计;合规 | 针对 SaaS 服务商安全性、可用性与保密性的 AICPA 审计报告体系 | AICPA（需核实原文） |
| OSCP | 攻击性安全认证专业人员;Offensive Security Certified Professional | 认证与岗位 | 认证;渗透测试 | 以实操 24 小时考试著称的渗透测试技术认证 | offsec.com |
| CEH | 道德黑客认证;Certified Ethical Hacker | 认证与岗位 | 认证;攻防 | EC-Council 颁发的道德黑客知识与技能认证 | eccouncil.org |
| CISM | 注册信息安全管理师;Certified Information Security Manager | 认证与岗位 | 认证;管理 | ISACA 颁发的信息安全管理方向认证 | isaca.org |
| 安全运营分析师 | SOC Analyst;安全分析师 | 认证与岗位 | 岗位;蓝队 | 在安全运营中心承担告警分诊、调查与升级处置的一线岗位 | 行业通用惯例 |
