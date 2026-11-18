# 科技主题提示词库（tech）

> **词库**：`../../data/tech/terms.md`（v1.3，272 条 / 18 分类，ID 前缀 TEC）
> **规范形**：正文术语一律用词库「词条」；同义/近义表达取自词库「别名」，不得自造。
> **归并说明**：本主题由原 `ai-agent`（AI Agent 与大模型）、`ai-security`（AI 安全）、`cybersecurity`（网络安全）三库归并，分类保持领域边界（AI 类 12 类 / 网络类 6 类）。
> **上游**：分类与 `content/tech/` 业务线一致（`layout.json`：category 优先，region 可选）。

---

## 一、主题定义与使用边界

**定义**：研究大模型与 Agent 技术、AI 安全攻击与防御、网络安全技术与合规，以及三者交叉的评估基准、框架标准与组织实践。

| 项 | 内容 |
|---|---|
| 覆盖 | 模型与厂商、Agent 技术与框架、AI 编码工具、AI 应用与产品、AI 攻击与防御、网络安全技术与运营、密码与身份、框架与合规、认证与岗位、基准与评估 |
| 不覆盖 | 非 AI 的传统软件功能细节；纯经济变量归 `economy`；纯政治/国际关系归 `political` |
| 与 `economy` 界线 | AI 产业的经济影响（融资、定价、商业化）可交叉引用，但经济变量本体归 `economy` |
| 子领域界线 | **AI 类**（模型/Agent/AI 安全/AI 编码/AI 应用/AI 框架）与**网络类**（通用攻防/漏洞/密码/等保/GDPR 等）分属不同分类，输出时须标明所属子领域，不混用 |
| 结论边界 | 只给「条件 → 判读 → 框架性含义 → 风险提示」，不给具体买卖价位 |

---

## 二、术语对齐

### 2.1 分类总览

| 子领域 | 分类 | 词条数 | 代表术语 |
|---|---|---|---|
| AI | 模型与厂商 | 19 | 大语言模型、推理模型、OpenAI、Anthropic、DeepSeek |
| AI | Agent 技术与框架 | 13 | AI Agent、多智能体系统、工具调用、MCP、A2A |
| AI | 编码工具与 IDE | 13 | AI IDE、Cursor、GitHub Copilot、Claude Code、Vibe Coding |
| AI | 应用与产品 | 15 | ChatGPT、Perplexity、Deep Research、AI 搜索 |
| AI | 概念与评估 | 11 | 生成式 AI、上下文窗口、Token、幻觉、微调、RLHF |
| AI | 攻击技术 | 12 | 提示注入、间接提示注入、越狱、数据投毒、模型窃取 |
| AI | 防御与检测 | 11 | 护栏、提示注入检测、RAG 安全、DLP、零信任 |
| AI | 工具与平台 | 3 | PyRIT、promptfoo、garak |
| AI | 框架与标准 | 8 | OWASP LLM Top 10、OWASP Agentic Top 10、NIST AI RMF、EU AI Act |
| AI | 认证与资质 | 4 | AI 红队认证、AAIS、AIGP、CISSP |
| AI | 组织与岗位 | 5 | 红队、蓝队、紫队、AI 红队、SOC |
| AI | 基准与评估 | 5 | SWE-bench、OSWorld、HarmBench、人类基线、基准饱和 |
| 网络 | 网络攻击技术 | 44 | 拒绝服务攻击、勒索软件、钓鱼攻击、SQL 注入、跨站脚本 |
| 网络 | 防御与安全运营 | 47 | 防火墙、WAF、IDS/IPS、SIEM、SOAR、沙箱 |
| 网络 | 漏洞与漏洞管理 | 11 | CVE、CVSS、负责任披露、补丁管理、CWE |
| 网络 | 密码与身份认证 | 20 | 对称/非对称加密、哈希、PKI、TLS、MFA |
| 网络 | 框架与合规 | 19 | ISO/IEC 27001、NIST CSF、网络安全等级保护、GDPR、UAE PDPL |
| 网络 | 认证与岗位 | 12 | OSCP、CEH、CISM、SOC 分析师、CISA |

### 2.2 核心术语对齐表

| 分类 | 术语 | 同义/近义表达 | 使用边界 | 常见误解 | 信息缺口 |
|---|---|---|---|---|---|
| 模型与厂商 | OpenAI | openai.com | 模型厂商；须注具体模型版本 | 把厂商名当模型名 | — |
| 模型与厂商 | DeepSeek | 深度求索 | 中国模型厂商；须注具体模型版本 | 把厂商名当模型名 | — |
| Agent 技术与框架 | AI Agent | 智能体、Agent | 与「模型」区分；须说明是否具工具调用/记忆 | 把聊天机器人当 Agent | — |
| Agent 技术与框架 | 工具调用 | Function Calling、Tool Use、函数调用 | 指模型调用外部函数；与 MCP 区分 | 把 MCP 当工具调用本身 | — |
| Agent 技术与框架 | 多智能体系统 | Multi-Agent System、MAS、多智能体协作 | 多 Agent 协同；须注编排方式 | 把单 Agent 当多智能体 | — |
| 编码工具与 IDE | Cursor | Cursor IDE、Anysphere Cursor | AI 原生 IDE；须注版本 | 把工具名当概念 | — |
| 编码工具与 IDE | Claude Code | Claude Code CLI | 命令行编码 Agent | 与「Claude 模型」混用 | — |
| 应用与产品 | ChatGPT | chatgpt.com | 对话产品；须注版本与订阅层 | 把产品名当模型名 | — |
| 应用与产品 | AI 搜索 | AI Search、答案引擎 | 搜索引擎形态；须注厂商 | 把 AI 搜索当独立模型 | — |
| 概念与评估 | 大语言模型 | LLM、Large Language Model、大模型 | 与「多模态模型」区分；须注上下文窗口 | 把 LLM 当通用人工智能 | — |
| 概念与评估 | 幻觉 | Hallucination、模型幻觉 | 指与事实不符的生成；评估与治理对象 | 把幻觉当随机错误 | 度量方法未统一 |
| 概念与评估 | 微调 | Fine-tuning、SFT、监督微调 | 作用于预训练模型；须注数据 | 把微调当从头训练 | — |
| 概念与评估 | Token | 词元 | 模型计费/上下文单位；与分词器相关 | 把 Token 当字数 | 分词器差异 |
| 攻击技术 | 提示注入 | Prompt Injection、PI | 针对模型指令层；与间接提示注入区分 | 把提示注入当传统注入（SQLi） | — |
| 攻击技术 | 间接提示注入 | Indirect Prompt Injection、IPI | 通过外部数据/工具间接生效 | 与直接提示注入混用 | 检测覆盖率 |
| 攻击技术 | 越狱 | Jailbreak、LLM 越狱 | 针对安全对齐的绕过 | 把越狱当漏洞利用（CVE） | — |
| 攻击技术 | 数据投毒 | Data Poisoning、训练数据投毒 | 作用于训练数据；与模型投毒区分 | 把推理期注入当投毒 | — |
| 攻击技术 | 模型窃取 | Model Extraction、Model Theft、模型提取攻击 | 黑盒查询重建；与训练数据提取区分 | 与「模型反演」混用 | — |
| 攻击技术 | 后门攻击 | Backdoor Attack、木马化模型 | 触发器驱动；与投毒区分 | 把后门当硬件木马 | — |
| 防御与检测 | 护栏 | Guardrails、LLM Guardrails、安全护栏 | 输入/输出侧的约束机制 | 把护栏当万无一失 | 误拒率数据 |
| 防御与检测 | 提示注入检测 | Prompt Injection Detection | 检测类；须注召回/误报 | 把检测当消除 | — |
| 防御与检测 | 零信任 | Zero Trust、ZT | 访问控制范式；非单一产品 | 把零信任当产品名 | — |
| 工具与平台 | PyRIT | Microsoft PyRIT | 红队测试框架 | 把工具名当概念 | — |
| 工具与平台 | garak | LLM vulnerability scanner | LLM 漏洞扫描器 | 与 PyRIT 混用 | — |
| 框架与标准 | 模型上下文协议 | MCP、Model Context Protocol | 开放协议；既属 Agent 框架也是攻击面 | 把 MCP 当某厂商私有协议 | 版本演进节奏 |
| 框架与标准 | OWASP Top 10 for LLM Applications | LLM Top 10、OWASP LLM Top 10 | 应用层风险清单；与 Agentic Top 10 区分 | 把两份 Top 10 合并使用 | 版本年份 |
| 框架与标准 | MITRE ATLAS | ATLAS、Adversarial Threat Landscape for AI Systems | AI 对抗威胁知识库；与 ATT&CK 区分 | 把 ATLAS 当 ATT&CK 子集 | — |
| 认证与资质 | AI 红队认证考试 | AI Red Team Certification、AI 红队认证 | 认证考试；须注发证机构 | 把认证当能力等价物 | — |
| 认证与资质 | AIGP | AI Governance Professional、IAPP AIGP | IAPP 治理认证 | 与 CISSP 混用 | — |
| 组织与岗位 | AI 红队 | AI Red Team、LLM 红队、AI Red Teaming | 组织/岗位；须注职能边界 | 把红队当攻击者 | — |
| 组织与岗位 | SOC | Security Operations Center、安全运营中心 | 安全运营中心；非个人岗位 | 把 SOC 当个人岗位 | — |
| 基准与评估 | SWE-bench | SWE-bench Verified、SWE-bench 基准 | Verified 为人工核验子集（已退役，须注时点） | 把子集当全集 | 退役后替代基准 |
| 基准与评估 | 基准饱和 | Benchmark Saturation | 指基准区分度下降 | 把分数上升当能力同比例提升 | 退役时间表 |
| 基准与评估 | OSWorld | OSWorld 基准 | 操作系统环境 Agent 基准 | 把基准分当真实能力 | — |
| 网络攻击技术 | 勒索软件 | Ransomware | 加密勒索；须注家族 | 把勒索软件当普通恶意软件 | — |
| 网络攻击技术 | 钓鱼攻击 | Phishing、鱼叉钓鱼、Spear Phishing | 社会工程；鱼叉为定向子类 | 把钓鱼当技术漏洞 | — |
| 防御与安全运营 | 防火墙 | Firewall | 网络边界访问控制 | 把 WAF 当防火墙 | — |
| 防御与安全运营 | IDS/IPS | 入侵检测/防御系统、IDS、IPS | 检测与防御一体两面 | 把 IDS 当 IPS | — |
| 防御与安全运营 | SIEM | 安全信息与事件管理、Security Information and Event Management | 日志聚合与关联分析 | 把 SIEM 当自动化响应 | — |
| 防御与安全运营 | SOAR | 安全编排自动化与响应、Security Orchestration, Automation and Response | 编排自动化；与 SIEM 区分 | 把 SOAR 当 SIEM 替代 | — |
| 漏洞与漏洞管理 | CVE | Common Vulnerabilities and Exposures、公共漏洞披露 | 漏洞编号；与 CWE 区分 | 把 CVE 当漏洞分类 | — |
| 漏洞与漏洞管理 | CVSS | 通用漏洞评分系统、Common Vulnerability Scoring System | 严重度评分；须注版本 | 把 CVSS 当可利用性 | — |
| 漏洞与漏洞管理 | CWE | 通用缺陷枚举、Common Weakness Enumeration | 缺陷分类；与 CVE 区分 | 把 CWE 当漏洞实例 | — |
| 密码与身份认证 | MFA | 多因素认证、Multi-Factor Authentication、2FA | 身份认证增强；2FA 为子集 | 把 2FA 当 MFA 同义 | — |
| 密码与身份认证 | 对称加密 | Symmetric Encryption | 加解密同钥；与非对称加密区分 | 把对称加密当「加密」全部 | — |
| 密码与身份认证 | TLS | 传输层安全、Transport Layer Security | 传输加密；须注版本 | 把 TLS 当 VPN | — |
| 框架与合规 | 网络安全等级保护 | 等保、MLPS | 中国合规框架 | 与 ISO/IEC 27001 混用 | — |
| 框架与合规 | GDPR | 通用数据保护条例、General Data Protection Regulation | 欧盟个人数据 | 与 UAE PDPL 混用 | — |
| 框架与合规 | EU AI Act | 欧盟人工智能法案、Regulation (EU) 2024/1689 | 风险分级监管 | 把「AI 法案」当已全面生效 | 各章生效节点 |
| 框架与合规 | ISO/IEC 27001 | 信息安全管理体系、ISMS | 信息安全管理体系标准 | 与等保混用 | — |
| 框架与合规 | NIST CSF | 网络安全框架、Cybersecurity Framework | 美国网络安全框架 | 与 ISO/IEC 27001 混用 | — |
| 认证与岗位 | OSCP | 攻击性安全认证专业人员、Offensive Security Certified Professional | 攻防认证；须注发证机构 | 把认证当能力等价物 | — |
| 认证与岗位 | CISM | 注册信息安全管理师、Certified Information Security Manager | 管理类认证；与 CISSP 区分 | 把 CISM 当技术认证 | — |

> 全量 272 条见词库 `terms.md`；上表为核心子集（覆盖全部 18 分类），新增术语同步补登。

---

## 三、场景词汇库

| 场景 | 典型提问句式 / 语料 | 必用术语 | 慎用 / 禁用表达 | 边界 |
|---|---|---|---|---|
| 工作 | 「这次模型发布对我们的红队清单意味着什么」「MCP 引入后攻击面怎么扩」 | 提示注入、间接提示注入、MCP、护栏、AI 红队 | 禁用「绝对安全」 | 只给攻击面/条件与缓解，不给具体配置 |
| 生活 | 「AI 搜索的结果能信吗」「怎么防钓鱼」 | 幻觉、钓鱼攻击、MFA、提示注入 | 禁用「点击链接就中毒」等恐吓式 | 不替代安全软件与专业咨询 |
| 研究 | 「越狱与提示注入的边界」「基准饱和的度量方法」 | 基准饱和、SWE-bench、提示注入、越狱、EU AI Act | 禁用无来源数字 | 须给口径并列与版本 |
| 学习 | 「Agent 和工具调用什么关系」「等保和 ISO27001 区别」 | 工具调用、MCP、等保、ISO/IEC 27001 | 禁用未经定义的缩写 | 给定义—机制—例子三步 |

---

## 四、可复用提示词索引

| 编号 | 文件 | 用途 | 适用场景 | 使用边界 | 常见误解 | 信息缺口 |
|---|---|---|---|---|---|---|
| TEC-W | [prompt-work-brief.md](./prompt-work-brief.md) | 从业者快速研判（攻击面 / 防御 / 合规） | 工作 | 不给具体产品采购与配置基线 | 把 AI 风险与传统漏洞混为一谈 | 厂商实现差异 |
| TEC-L | [prompt-life-brief.md](./prompt-life-brief.md) | 个人防护与 AI 使用避坑 | 生活 | 不替代安全产品与专业咨询 | 把 MFA 当万能 | 个人环境未知 |
| TEC-R | [prompt-research-brief.md](./prompt-research-brief.md) | 系统调研与框架对照 | 研究 | 不做能力预测 | 跨框架术语混用 | 标准版本/生效节点 |
| TEC-S | [prompt-learning-brief.md](./prompt-learning-brief.md) | 入门到进阶路径 | 学习 | 不替代认证考试 | 把工具名当概念 | 先修水平未知 |

---

## 五、核验清单

- [x] 定义清晰度：覆盖 / 不覆盖 / 与 `economy` 界线 / AI 与网络子领域界线齐备（第一节）
- [x] 覆盖完整性：18 分类全部出现在 2.1 与 2.2；2.2 核心子集均含同义表达
- [x] 表达精准度：4 条提示词均有适用 / 不适用 / 边界 / 误解 / 缺口
- [x] 无重复：AI 类与网络类近义分类（如「框架与标准」vs「框架与合规」）保持区分，未合并
- [x] 无漂移：归并后规范形统一（如「模型上下文协议」取代「MCP」为首现形；「多因素认证」用规范形「MFA」）
- [ ] 来源核验：词库中「需核实原文」条目清零（进行中）

---

## 六、信息缺口清单

| 缺口 | 影响 | 补采来源建议 | 状态 |
|---|---|---|---|
| 基准退役/版本演进（SWE-bench Verified 等） | 研究结论时效性 | 各基准官方页、OpenAI/Anthropic 公告 | 待采集 |
| EU AI Act 各章生效节点 | 合规判断 | EUR-Lex 官方文本 | 待采集 |
| 部分词条来源标「需核实原文」 | 定义权威性不足 | NIST/OWASP/ISO 官方页 | 待核验 |
| AI 与网络交叉术语（如 Shadow AI）归属 | 分类边界 | 词库分类维护 | 已归类（防御与检测） |
| 提示词实际复用效果未回测 | 无法量化价值 | 2027-06 首次中期回测 | 未启动 |

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-18 | 初始版本 | 归并 ai-agent / ai-security / cybersecurity 后建立完整提示词库（4 场景 + 核验 + 缺口） |
| v1.1 | 2026-11-18 | 覆盖补齐 | 2.2 增分类列，补齐 9 个缺失分类（模型与厂商 / 编码工具与 IDE / 应用与产品 / 组织与岗位 / 工具与平台 / 认证与资质 / 网络攻击技术 / 密码与身份认证 / 认证与岗位）；规范形修正「多因素认证」→「MFA」，移除分类名占位行 |
