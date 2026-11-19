# 教育词汇库（education）

> **定位**：vocabulary 子系统主题词库，由 `script/vocab_tool.py` 统一管理；词汇表请勿手工编辑，变更一律走 `import` / `tag` 命令。
> **主题配置**：`config/topics.json` → `education`（教育主题词汇：教育体系与制度、院校与机构、专业与课程、教育政策法规、评价认证、教育技术、国际教育、终身学习（骨架，待采集））
> **去重规范**：词条与别名经归一化（NFKC + 空白折叠 + 忽略大小写）后全局唯一；别名/标签分隔符为半角 `;`。

## 词汇表

| ID | 词条 | 别名 | 分类 | 标签 | 定义 | 来源 | 首次登记 | 最近更新 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EDU-001 | 学历 | Education Level Attained | 教育体系与制度 | 口径;层次 | 个人受教育的最高阶段（education level attained），与「学位」分列，不得互相替代 | UNESCO UIS / business-config 第三节 | 2026-11-19 | 2026-11-19 |
| EDU-002 | 学位 | Degree Awarded | 教育体系与制度 | 口径;层次 | 教育机构授予的学术资格（degree awarded），与「学历」分列 | UNESCO UIS / business-config 第三节 | 2026-11-19 | 2026-11-19 |
| EDU-003 | 高等教育 | Higher Education | 教育体系与制度 | 层次 | 中等教育之后的高等教育阶段，含专科、本科与研究生层次 | UNESCO UIS / ISCED 2011 | 2026-11-19 | 2026-11-19 |
| EDU-004 | 义务教育 | Compulsory Education;九年义务教育 | 教育政策与法规 | 制度;年限 | 国家法律强制实施的特定年限教育；中国《义务教育法》确立九年义务教育 | 中国教育部《义务教育法》 | 2026-11-19 | 2026-11-19 |
| EDU-005 | 义务教育年限 | Compulsory Education Duration | 教育体系与制度 | 口径;年限 | 义务教育的持续年数，须区分「学年口径」（如 9 年）与「年龄口径」（如 6–15 岁）并注明来源国定义 | business-config 第三节 | 2026-11-19 | 2026-11-19 |
| EDU-006 | 义务教育法 | 中华人民共和国义务教育法;Compulsory Education Law | 教育政策与法规 | 法规;中国 | 中国确立九年义务教育制度与年满 6 周岁入学年龄的法律（1986 通过、2006 修订、2015 / 2018 修正） | 中国教育部法规页 | 2026-11-19 | 2026-11-19 |
| EDU-007 | 学制 | School System | 教育体系与制度 | 制度 | 国家规定的学校层级结构与修业年限安排，如韩国 6-3-3 学制 | UNESCO UIS / 各国教育部 | 2026-11-19 | 2026-11-19 |
| EDU-008 | 6-3-3 学制 | 6-3-3 School System | 教育体系与制度 | 制度;韩国 | 小学 6 年、初中 3 年、高中 3 年的学制结构 | 韩国教育部 | 2026-11-19 | 2026-11-19 |
| EDU-009 | 毛入学率 | GER;Gross Enrolment Ratio | 教育评价与认证 | 指标;口径 | 某级教育在学人数占相应学龄人口的比例，含超龄与低龄人口，与净入学率口径不同 | UNESCO UIS / OECD EAG | 2026-11-19 | 2026-11-19 |
| EDU-010 | 高等教育毛入学率 | Higher Education GER | 教育评价与认证 | 指标;口径 | 高等教育阶段的毛入学率（GER），跨国对照须与净入学率并列 | OECD EAG / UNESCO UIS | 2026-11-19 | 2026-11-19 |
| EDU-011 | 净入学率 | NER;Net Enrolment Rate | 教育评价与认证 | 指标;口径 | 仅统计相应学龄人口的在学比例，不含超龄与低龄人口，与毛入学率禁止合并或互相折算 | UNESCO UIS / OECD EAG | 2026-11-19 | 2026-11-19 |
| EDU-012 | 入园率 | Early Childhood Enrolment Rate | 教育评价与认证 | 指标;学前 | 3–5 岁学前阶段入园比例（如 OECD 2024 年读数 86%） | OECD EAG | 2026-11-19 | 2026-11-19 |
| EDU-013 | 毕业率 | Graduation Rate | 教育评价与认证 | 指标;学业完成 | 完成某级教育并获得证书的比例，各国定义不同 | UNESCO UIS | 2026-11-19 | 2026-11-19 |
| EDU-014 | 辍学率 | Dropout Rate | 教育评价与认证 | 指标;学业完成 | 在学期间中途退出某级教育的比例，与毕业率、完成率口径不同 | UNESCO UIS | 2026-11-19 | 2026-11-19 |
| EDU-015 | 师生比 | Pupil-Teacher Ratio;Student-Teacher Ratio | 教育评价与认证 | 指标;投入 | 学生数与教师数之比，衡量教育资源配置 | UNESCO UIS | 2026-11-19 | 2026-11-19 |
| EDU-016 | 教育支出占 GDP 比 | Education Expenditure as Share of GDP | 教育评价与认证 | 指标;支出 | 公共与私人教育支出合计占 GDP 的比重（如 OECD 国家 2023 年均值 4.2%） | UNESCO UIS / World Bank EdStats / OECD EAG | 2026-11-19 | 2026-11-19 |
| EDU-017 | 教育支出 | Education Expenditure | 教育评价与认证 | 支出;口径 | 公共与私人教育支出，须并列口径（公共 / 私人、GDP 占比 / 人均），不取单一值 | UNESCO UIS / OECD EAG | 2026-11-19 | 2026-11-19 |
| EDU-018 | 教育统计 | Educational Statistics | 教育评价与认证 | 方法;数据 | 教育指标的采集与发布口径体系，跨国对照须注明版本与提取日期 | UNESCO UIS | 2026-11-19 | 2026-11-19 |
| EDU-019 | ISCED 2011 | ISCED;国际教育标准分类 2011;International Standard Classification of Education 2011 | 教育评价与认证 | 分类;国际标准 | UNESCO 统计研究所发布的 9 级（0–8）教育分类框架，为跨国教育对照的分类锚 | UNESCO UIS | 2026-11-19 | 2026-11-19 |
| EDU-020 | PISA | Programme for International Student Assessment;国际学生评估项目 | 教育评价与认证 | 测评;OECD | OECD 对 15 岁学生阅读、数学与科学素养的三年一度测评，结果仅作线索 | OECD PISA | 2026-11-19 | 2026-11-19 |
| EDU-021 | TIMSS | Trends in International Mathematics and Science Study;国际数学与科学趋势研究 | 教育评价与认证 | 测评;IEA | 对 4 / 8 年级学生数学与科学成就的国际测评 | IEA TIMSS | 2026-11-19 | 2026-11-19 |
| EDU-022 | PIRLS | Progress in International Reading Literacy Study;国际阅读素养进展研究 | 教育评价与认证 | 测评;IEA | 对 4 年级学生阅读素养的国际测评 | IEA PIRLS | 2026-11-19 | 2026-11-19 |
| EDU-023 | ICILS | International Computer and Information Literacy Study | 教育评价与认证 | 测评;IEA | 对 8 年级学生信息与计算机素养的国际测评 | IEA ICILS | 2026-11-19 | 2026-11-19 |
| EDU-024 | 国际教育成就评价协会 | IEA（教育测评）;International Association for the Evaluation of Educational Achievement | 院校与机构 | 组织;测评 | 主导 TIMSS / PIRLS / ICILS 等国际教育测评的机构；与 economy 主题「IEA（国际能源署）」区分 | IEA | 2026-11-19 | 2026-11-19 |
| EDU-025 | UNESCO | 联合国教科文组织;United Nations Educational, Scientific and Cultural Organization | 国际教育 | 组织;联合国 | 联合国教育、科学及文化组织，发布 ISCED 与全球互认公约 | UNESCO | 2026-11-19 | 2026-11-19 |
| EDU-026 | UNESCO UIS | 联合国教科文组织统计研究所;UNESCO Institute for Statistics | 国际教育 | 组织;统计 | UNESCO 下属教育统计机构，负责 ISCED 分类与 UIS.stat 数据 | UNESCO UIS | 2026-11-19 | 2026-11-19 |
| EDU-027 | OECD | 经济合作与发展组织;Organisation for Economic Co-operation and Development | 国际教育 | 组织 | 发布 Education at a Glance 与 PISA 的经济合作与发展组织 | OECD | 2026-11-19 | 2026-11-19 |
| EDU-028 | Education at a Glance | EAG;OECD 教育概览 | 国际教育 | 报告;指标 | OECD 年度教育指标报告，为支出与结构基线主源 | OECD EAG | 2026-11-19 | 2026-11-19 |
| EDU-029 | 全球高等教育学历资格认可公约 | UNESCO Global Convention on the Recognition of Qualifications concerning Higher Education;全球公约 | 国际教育 | 公约;互认 | 2019-11-25 由 UNESCO 大会通过的首个全球范围高等教育互认联合国条约，2023 年生效 | UNESCO | 2026-11-19 | 2026-11-19 |
| EDU-030 | 里斯本区域公约 | 里斯本公约;Lisbon Recognition Convention | 国际教育 | 公约;互认 | 1997-04-11 采纳的欧洲区域高等教育学历互认基础性公约，与全球公约并行 | UNESCO | 2026-11-19 | 2026-11-19 |
| EDU-031 | 学历互认 | 学历资格互认;Recognition of Education Level | 教育评价与认证 | 互认;口径 | 对境外学历（education level）的承认，与学位互认分列，须逐条核对协议名称与覆盖层级 | UNESCO / business-config 第三节 | 2026-11-19 | 2026-11-19 |
| EDU-032 | 学位互认 | Recognition of Degree | 教育评价与认证 | 互认;口径 | 对境外学位（degree）的承认，与学历互认分列 | UNESCO / business-config 第三节 | 2026-11-19 | 2026-11-19 |
| EDU-033 | 认证 | Accreditation | 教育评价与认证 | 质量;口径 | 官方或授权机构对院校 / 专业教育资格的认定状态，不等同于教育质量评价 | 各国官方认证机构名录 | 2026-11-19 | 2026-11-19 |
| EDU-034 | 质量保障 | Quality Assurance | 教育评价与认证 | 质量 | 保障教育质量的制度与程序体系，与认证状态口径不同 | UNESCO / 各国认证机构 | 2026-11-19 | 2026-11-19 |
| EDU-035 | 国际学生流动 | International Student Mobility | 国际教育 | 流动;指标 | 学生跨国接受教育的规模与方向，须并列来源国 / 目的国口径 | UNESCO UIS / OECD | 2026-11-19 | 2026-11-19 |
| EDU-036 | 终身学习 | Lifelong Learning | 终身学习 | 理念 | 贯穿一生的学习与教育机会体系 | UNESCO | 2026-11-19 | 2026-11-19 |
| EDU-037 | 教育政策 | Education Policy | 教育政策与法规 | 政策 | 政府或主管机关对教育制度、投入与改革的决定与行动 | 各国教育部 | 2026-11-19 | 2026-11-19 |
| EDU-038 | 课程 | Curriculum | 专业与课程 | 教学 | 学校实施的课程方案与内容体系 | UNESCO UIS | 2026-11-19 | 2026-11-19 |
| EDU-039 | MEXT | 文部科学省;日本文部科学省;Ministry of Education, Culture, Sports, Science and Technology | 院校与机构 | 机构;日本 | 日本主管教育、文化与科技的中央行政机关 | MEXT | 2026-11-19 | 2026-11-19 |
| EDU-040 | DfE | 英国教育部;Department for Education | 院校与机构 | 机构;英国 | 英国主管教育、技能与儿童服务的政府部门 | gov.uk | 2026-11-19 | 2026-11-19 |
| EDU-041 | OfS | 英国学生事务办公室;Office for Students | 院校与机构 | 机构;英国;认证 | 英国高等教育监管机构，负责院校注册与质量监管 | officeforstudents.org.uk | 2026-11-19 | 2026-11-19 |
| EDU-042 | NCES | 美国国家教育统计中心;National Center for Education Statistics | 院校与机构 | 机构;美国;统计 | 美国教育部下属教育统计机构 | nces.ed.gov | 2026-11-19 | 2026-11-19 |
| EDU-043 | KMK | 德国各州文教部长联席会议;Standing Conference of the Ministers of Education and Cultural Affairs | 院校与机构 | 机构;德国 | 德国各州教育部长协调机构，主管学制与教育协定 | kmk.org | 2026-11-19 | 2026-11-19 |
| EDU-044 | Eurydice | 欧洲教育信息网络;EU Eurydice | 院校与机构 | 机构;欧盟;信息 | EU 下属欧洲各国教育制度与政策信息网络 | eurydice.eacea.ec.europa.eu | 2026-11-19 | 2026-11-19 |
| EDU-045 | CERI | OECD 教育研究与创新中心;Centre for Educational Research and Innovation | 院校与机构 | 机构;OECD | OECD 教育研究与政策创新中心 | OECD CERI | 2026-11-19 | 2026-11-19 |

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
| --- | --- | --- | --- |
| v1.0 | 2026-11-18 | 首建词库 | topic-add/init 创建空词库骨架 |
| v1.1 | 2026-11-19 | 批量补录 | 新增 45 条 / 跳过重复 0 条 / 无效 0 条；来源：business-config、基线提示词与基线报告 |
