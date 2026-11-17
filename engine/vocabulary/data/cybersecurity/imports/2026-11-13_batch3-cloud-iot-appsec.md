# 网络安全词汇 · 第三批导入（36 条：云安全 / 物联网与无线 / 应用安全等新维度）

> **用途**：cybersecurity 主题第三批种子，走标准 import 流程入库（幂等）。入库后自动同步至 content/tech/security/dubai 业务提示词。
> **范围界定**：全部落入现有 6 分类；不与既有 90 条及 ai-security 主题重复。

| 词条 | 别名 | 分类 | 标签 | 定义 | 来源 |
|---|---|---|---|---|---|
| Evil Twin | 双胞胎热点;恶意热点 | 网络攻击技术 | 攻击;无线 | 伪装成合法 Wi-Fi 热点诱骗接入以窃取流量与凭据的无线攻击 | 行业综述（需核实原文） |
| ARP 欺骗 | ARP Spoofing;ARP 毒化 | 网络攻击技术 | 攻击;网络层 | 伪造 ARP 应答劫持局域网流量、支撑窃听与中间人攻击 | 行业综述（需核实原文） |
| DNS 劫持 | DNS Hijacking | 网络攻击技术 | 攻击;网络层 | 篡改 DNS 解析结果将用户引导至恶意站点的攻击 | 行业综述（需核实原文） |
| BGP 劫持 | BGP Hijacking | 网络攻击技术 | 攻击;路由 | 宣告虚假 BGP 路由劫持 IP 前缀、截获或黑洞流量的攻击 | 行业综述（需核实原文） |
| 命令注入 | Command Injection | 网络攻击技术 | 攻击;Web | 将操作系统命令注入应用输入并以应用权限执行的漏洞利用 | OWASP Top 10 |
| 不安全反序列化 | Insecure Deserialization;反序列化漏洞 | 网络攻击技术 | 攻击;应用 | 利用应用对不可信数据反序列化的缺陷实现代码执行或逻辑绕过 | OWASP Top 10 |
| XXE | XML 外部实体注入;XML External Entity | 网络攻击技术 | 攻击;应用 | 滥用 XML 解析器外部实体功能读取文件或发起 SSRF 的注入攻击 | OWASP（需核实原文） |
| SSRF | 服务端请求伪造;Server-Side Request Forgery | 网络攻击技术 | 攻击;应用 | 诱导服务端向任意地址发起请求、访问内网或云元数据的攻击 | OWASP Top 10 |
| 目录遍历 | Path Traversal;Directory Traversal | 网络攻击技术 | 攻击;应用 | 经特殊路径序列越权读取服务器任意文件的漏洞利用 | OWASP（需核实原文） |
| 越权访问 | Broken Access Control;访问控制失效 | 网络攻击技术 | 攻击;权限 | 绕过授权校验访问他人数据或高权限功能（水平/垂直越权） | OWASP Top 10 |
| CSPM | 云安全态势管理;Cloud Security Posture Management | 防御与安全运营 | 云;治理 | 持续发现与修复云资源配置错误的自动化治理平台 | Gartner（需核实原文） |
| CWPP | 云工作负载保护平台;Cloud Workload Protection Platform | 防御与安全运营 | 云;防护 | 面向虚拟机、容器与无服务器负载的工作负载安全防护平台 | Gartner（需核实原文） |
| SASE | 安全访问服务边缘;Secure Access Service Edge | 防御与安全运营 | 云;架构 | 融合网络与安全（SD-WAN、SWG、ZTNA 等）的云交付边缘架构 | Gartner（需核实原文） |
| CASB | 云访问安全代理;Cloud Access Security Broker | 防御与安全运营 | 云;防护 | 位于用户与云服务之间执行安全策略、发现影子 SaaS 的控制点 | Gartner（需核实原文） |
| 容器安全 | Container Security | 防御与安全运营 | 云;防护 | 覆盖镜像、运行时与编排层的容器化环境安全防护 | 行业实践 |
| Kubernetes 安全 | K8s 安全;K8s Security | 防御与安全运营 | 云;防护 | 面向 K8s 集群的 RBAC、策略、网络策略与镜像签名安全实践 | CNCF（需核实原文） |
| 物联网安全 | IoT Security | 防御与安全运营 | 防御;物联网 | 针对物联网设备的身份、固件、通信与生命周期安全防护 | NIST IR 8259（需核实原文） |
| 工控安全 | OT 安全;ICS Security;工业控制系统安全 | 防御与安全运营 | 防御;工控 | 面向工业控制与运营技术环境的可用性优先安全防护 | IEC 62443（需核实原文） |
| 无线安全 | Wireless Security;Wi-Fi 安全 | 防御与安全运营 | 防御;无线 | 无线网络接入认证与加密防护（WPA2/WPA3 等） | Wi-Fi Alliance（需核实原文） |
| SAST | 静态应用安全测试;Static Application Security Testing | 防御与安全运营 | 应用;DevSecOps | 不运行程序、基于源码/字节码分析发现安全缺陷的测试技术 | OWASP（需核实原文） |
| DAST | 动态应用安全测试;Dynamic Application Security Testing | 防御与安全运营 | 应用;DevSecOps | 运行态探测应用漏洞的黑盒安全测试技术 | OWASP（需核实原文） |
| 软件组成分析 | SCA;Software Composition Analysis | 防御与安全运营 | 供应链;DevSecOps | 识别开源与第三方组件及其已知漏洞的自动化分析 | 行业实践 |
| API 安全 | API Security | 防御与安全运营 | 防御;应用 | 面向 API 的认证、限流、Schema 校验与滥用防护 | OWASP API Top 10 |
| 攻防演练 | 红蓝对抗;实战攻防演练 | 防御与安全运营 | 评估;演练 | 在限定范围内组织攻防双方实战对抗以检验防御有效性的活动 | 行业实践 |
| 云配置错误 | Cloud Misconfiguration;配置漂移 | 漏洞与漏洞管理 | 云;风险 | 云资源策略偏离安全基线导致的暴露面（公开存储桶、裸奔端口等），云上事故首要诱因 | 行业综述（需核实原文） |
| 秘密管理 | Secrets Management;密钥管理服务;KMS | 密码与身份认证 | 密码学;云 | 集中存储、轮换与审计应用凭据（API Key、证书、密钥）的机制 | NIST SP 800-57（需核实原文） |
| 硬件安全模块 | HSM;Hardware Security Module | 密码与身份认证 | 密码学;硬件 | 提供密钥生成与密码运算的防篡改专用硬件 | NIST FIPS 140-3（需核实原文） |
| 零知识证明 | ZKP;Zero-Knowledge Proof | 密码与身份认证 | 密码学;前沿 | 证明者使验证者相信陈述为真而不泄露任何额外信息的密码协议 | 行业综述（需核实原文） |
| 后量子密码 | PQC;Post-Quantum Cryptography | 密码与身份认证 | 密码学;前沿 | 抵抗量子计算攻击的新一代公钥密码算法族（NIST 标准化中） | NIST PQC（需核实原文） |
| 共享责任模型 | Shared Responsibility Model | 框架与合规 | 云;治理 | 划分云厂商与租户安全责任边界的云服务模型框架 | AWS/微软官方文档（需核实原文） |
| DevSecOps | 开发安全运营;安全左移 | 框架与合规 | 方法;开发 | 将安全内嵌到开发运维全流程的文化与工程实践 | 行业实践 |
| 数据主权 | Data Sovereignty | 框架与合规 | 法规;数据 | 数据受其存储所在地司法管辖权约束的合规要求 | 行业综述（需核实原文） |
| 数据脱敏 | Data Masking;匿名化;Anonymization | 框架与合规 | 隐私;数据 | 以遮蔽、泛化或置换处理使数据无法关联到特定个人的技术 | ISO/IEC 20889（需核实原文） |
| CCSP | 认证云安全专家;Certified Cloud Security Professional | 认证与岗位 | 认证;云 | (ISC)2 与 CSA 联合颁发的云安全专业认证 | isc2.org |
| 云安全架构师 | Cloud Security Architect | 认证与岗位 | 岗位;云 | 负责云平台安全架构设计、治理与落地的技术岗位 | 行业通用惯例 |
| 应用安全工程师 | AppSec Engineer;安全开发工程师 | 认证与岗位 | 岗位;应用 | 负责应用安全评审、SAST/DAST 与安全编码推广的工程岗位 | 行业通用惯例 |
