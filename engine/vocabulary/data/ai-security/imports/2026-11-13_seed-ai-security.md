# AI 安全词汇 · 种子导入文件（47 条）

> **用途**：vocabulary 子系统首批 AI 安全词汇种子，走标准 import 流程入库（不直接写 terms.md）。
> **格式契约**：6 列 md 表格（词条 / 别名 / 分类 / 标签 / 定义 / 来源）；别名与标签用半角分号 `;` 分隔；单元格内禁止竖线。
> **来源规则**：官方一手优先；无法当场核验的标注「需核实原文」，入库后由后续运行回溯升级。

| 词条 | 别名 | 分类 | 标签 | 定义 | 来源 |
|---|---|---|---|---|---|
| 红队 | Red Team;攻击模拟队 | 组织与岗位 | 红队;安全测试 | 模拟真实攻击者手法对系统实施对抗性测试的团队，用于验证防御有效性与检测响应能力 | NIST SP 800-115 |
| 蓝队 | Blue Team;防御团队 | 组织与岗位 | 蓝队;防御运营 | 负责识别、防护、检测、响应与恢复网络攻击的安全运营团队（含 SOC 与事件响应职能） | NIST CSF |
| 紫队 | Purple Team | 组织与岗位 | 红队;蓝队;协同机制 | 红蓝队协同工作方式：红队攻击手法持续反馈蓝队，转化为检测规则与防御改进 | 行业实践（需核实原文） |
| AI 红队 | AI Red Team;LLM 红队;AI Red Teaming | 组织与岗位 | 红队;AI 安全 | 针对 AI/ML 系统的对抗性测试实践与团队职能，覆盖提示注入、越狱、投毒、Agent 滥用等 AI 特有攻击面 | Microsoft AI Red Team |
| SOC | Security Operations Center;安全运营中心 | 组织与岗位 | 蓝队;防御运营 | 集中承担安全监控、告警分诊与事件响应的组织职能 | NIST CSF |
| 威胁情报 | Threat Intelligence;CTI | 防御与检测 | 蓝队;情报 | 收集、分析攻击者 TTP（战术、技术与流程）并转化为防御与检测决策的证据过程 | NIST（需核实原文） |
| 提示注入 | Prompt Injection;PI | 攻击技术 | LLM 攻击;红队 | 通过构造输入覆盖或劫持 LLM 系统指令，使其偏离预期行为；OWASP LLM Top10 之 LLM01 | OWASP GenAI |
| 间接提示注入 | Indirect Prompt Injection;IPI | 攻击技术 | LLM 攻击;Agent | 恶意指令藏于模型检索的外部内容（网页、文档、邮件、工具输出）中间接触发注入 | OWASP GenAI |
| 越狱 | Jailbreak;LLM 越狱 | 攻击技术 | LLM 攻击;红队 | 绕过模型安全对齐与内容策略，诱导模型输出被禁止内容 | OWASP GenAI |
| 数据投毒 | Data Poisoning;训练数据投毒 | 攻击技术 | 投毒;供应链 | 污染训练或微调数据以植入恶意行为、后门或偏见 | Microsoft Security Blog |
| 模型投毒 | Model Poisoning;权重投毒 | 攻击技术 | 投毒;供应链 | 直接篡改模型权重或更新通道植入休眠后门，部署后由触发器激活 | Microsoft Security Blog（Trained to Betray / Sleeper Agents） |
| 后门攻击 | Backdoor Attack;木马化模型 | 攻击技术 | 投毒;检测对抗 | 在模型中植入由特定触发器激活的隐藏恶意行为，常规评估难以发现 | 行业综述（需核实原文） |
| 模型窃取 | Model Extraction;Model Theft;模型提取攻击 | 攻击技术 | 隐私;知识产权 | 通过大量查询近似复制目标模型的能力或参数 | OWASP GenAI（需核实原文） |
| 训练数据提取 | Training Data Extraction;模型反演;Model Inversion | 攻击技术 | 隐私 | 从模型输出中还原训练数据或敏感属性 | 行业综述（需核实原文） |
| 成员推断 | Membership Inference | 攻击技术 | 隐私 | 判定特定样本是否属于模型训练集的攻击，构成训练数据隐私风险 | 行业综述（需核实原文） |
| Agent 工具滥用 | Agent Tool Abuse;Confused Deputy;越权工具调用 | 攻击技术 | Agent;权限治理 | 诱导 AI Agent 滥用其工具与权限执行非授权操作（混淆代理人问题） | OWASP Agentic Top 10 |
| 多模态注入 | Multimodal Injection;跨模态注入 | 攻击技术 | LLM 攻击;多模态 | 经图像、音频、文档等非文本通道携带并触发恶意指令 | 行业综述（需核实原文） |
| 护栏 | Guardrails;LLM Guardrails;安全护栏 | 防御与检测 | 防御;LLM 安全 | 模型输入与输出侧的策略执行层，拦截违规内容、注入攻击与高危操作 | 行业实践 |
| 提示注入检测 | Prompt Injection Detection | 防御与检测 | 防御;蓝队;LLM 安全 | 识别输入与工具输出中注入意图的检测手段（分类器、规则、沙箱执行等） | 行业实践 |
| RAG 安全 | 检索增强生成安全;RAG Security | 防御与检测 | 防御;RAG | 检索源信任治理、外部内容消毒与引用隔离，防范间接注入与数据泄漏 | 行业实践 |
| DLP | Data Loss Prevention;数据防泄漏 | 防御与检测 | 防御;合规 | 防止敏感数据经 AI 应用、提示词或模型输出外泄的控制体系 | 行业实践 |
| DSPM | Data Security Posture Management;数据安全态势管理 | 防御与检测 | 防御;治理 | 发现、分类与治理数据资产安全态势的技术，AI 场景覆盖向量库与训练数据集 | 行业实践 |
| Shadow AI | 影子 AI;未申报 AI 使用 | 防御与检测 | 治理;风险 | 未经安全与合规治理即投入使用的 AI 工具与服务，构成数据与合规盲区 | 行业实践 |
| 零信任 | Zero Trust;ZT | 防御与检测 | 架构;防御 | 永不信任、持续验证的安全架构原则，适用于 Agent 权限与身份设计 | NIST SP 800-207 |
| EDR | Endpoint Detection and Response;端点检测与响应 | 防御与检测 | 蓝队;检测 | 端点侧持续监测、告警与响应能力 | 行业实践 |
| AI 事件响应 | AI Incident Response | 防御与检测 | 蓝队;响应 | 针对 AI 安全事件（投毒、越狱、数据泄漏、Agent 失控）的检测、遏制与恢复流程 | 行业实践 |
| 模型水印 | Model Watermarking;AI 内容溯源 | 防御与检测 | 溯源;治理 | 对 AI 生成内容或模型输出植入可验证标识以支持溯源 | 行业综述（需核实原文） |
| PyRIT | Microsoft PyRIT | 工具与平台 | 红队;工具链 | 微软开源的 AI 红队自动化框架，支持风险识别流水线与对抗提示编排 | github.com/Azure/PyRIT |
| promptfoo |  | 工具与平台 | 红队;评估 | 开源 LLM 评估与红队测试工具，支持用例化对抗测试与 CI 集成 | github.com/promptfoo/promptfoo |
| garak | LLM vulnerability scanner | 工具与平台 | 红队;扫描 | NVIDIA 开源 LLM 漏洞扫描器，探测越狱、注入、数据泄漏等模型弱点 | github.com/NVIDIA/garak |
| OWASP Top 10 for LLM Applications | LLM Top 10;OWASP LLM Top 10 | 框架与标准 | 标准;LLM 安全 | LLM 应用十大风险清单（2025 版 LLM01 为提示注入） | genai.owasp.org |
| OWASP Agentic Top 10 | Agentic AI Top 10 | 框架与标准 | 标准;Agent | Agentic AI 系统十大风险清单 | genai.owasp.org/agentic-top-10 |
| NIST AI RMF | AI 风险管理框架;AI Risk Management Framework | 框架与标准 | 标准;治理 | AI 风险的治理、映射、测量与管理框架 | nist.gov |
| EU AI Act | 欧盟人工智能法案;Regulation (EU) 2024/1689 | 框架与标准 | 法规;合规 | 欧盟按风险分级监管 AI 系统的法案 | EUR-Lex |
| ISO/IEC 42001 | AI 管理体系;AIMS | 框架与标准 | 标准;治理 | AI 管理体系国际标准 | iso.org |
| MITRE ATT&CK | ATT&CK | 框架与标准 | 标准;威胁情报 | 通用网络攻击战术与技术知识库，AI 相关攻击映射的基础框架 | attack.mitre.org |
| MITRE ATLAS | ATLAS;Adversarial Threat Landscape for AI Systems | 框架与标准 | 标准;AI 安全 | AI 系统对抗性威胁战术与技术知识库 | atlas.mitre.org |
| AI 红队认证考试 | AI Red Team Certification;AI 红队认证 | 认证与资质 | 认证;红队 | 面向 AI 红队从业者的认证考试统称；主流包括 ISACA AAIS、IAPP AIGP（治理向）、CREST AI 测试资质等，报考条件以颁发机构官方页为准 | 颁发机构官网（需核实原文） |
| AAIS | ISACA Advanced in AI Security;ISACA AI 安全高级认证 | 认证与资质 | 认证;AI 安全 | ISACA 面向 AI 安全的高级技术认证考试 | isaca.org（需核实原文） |
| AIGP | AI Governance Professional;IAPP AIGP | 认证与资质 | 认证;AI 治理 | IAPP 颁发的 AI 治理专业人员认证考试 | iapp.org |
| CISSP | 注册信息系统安全专家 | 认证与资质 | 认证;通用安全 | 通用信息安全认证，现行考纲已纳入 AI 安全相关内容 | isc2.org（需核实原文） |
| SWE-bench Verified | SWE-bench | 基准与评估 | 基准;代码 | 软件工程任务代码修复基准；Verified 为人工核验子集，2026-02 退役 | openai.com（需核实原文） |
| OSWorld | OSWorld 基准 | 基准与评估 | 基准;Agent | 计算机使用类 Agent 真实环境基准，人类基线 72.35% | Stanford HAI |
| HarmBench | HarmBench 基准 | 基准与评估 | 基准;红队 | 标准化红队攻击效果评测基准 | 行业综述（需核实原文） |
| 人类基线 | Human Baseline | 基准与评估 | 基准;评估 | 基准评估中人类表现的参照值，用于解读模型得分 | Stanford HAI |
| 幻觉 | Hallucination;模型幻觉 | 基准与评估 | 评估;风险 | 模型生成与事实不符或无依据内容的现象，是评估与风险治理的核心对象 | Stanford HAI |
| 基准饱和 | Benchmark Saturation | 基准与评估 | 评估;基准 | 基准得分逼近上限、失去模型区分度的状态，触发基准退役或换代 | OpenAI（需核实原文） |
