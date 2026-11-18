# 词汇库子系统（vocabulary）· 标准操作流程（SOP）

> **一句话定位**：仓库级、主题无关的标准化动态词汇子系统。首期落地 **AI 安全词汇**（红队/蓝队、AI 红队认证考试、攻击技术、防御检测、工具平台、框架标准、基准评估，共 7 分类 47 条种子）；新增任意领域词汇仅需在配置文件登记一个主题，**零代码修改**。

---

## 一、架构与目录

```
vocabulary/
├── README.md                          # 本文件：标准操作流程（SOP）
├── INDEX.md                           # 全主题索引（index 命令自动生成，勿手工编辑）
├── config/
│   ├── topics.json                    # 主题注册表（扩展唯一改动点，单一事实源）
│   └── sync.json                      # 词条 → 业务提示词自动同步绑定
├── script/
│   ├── vocab_tool.py                  # 核心脚本（主题无关，仅依赖 Python 标准库）
│   └── sync_vocab.py                  # 词条自动同步脚本
├── prompts/                           # 多主题提示词库（与 data/<theme> 同主题对齐，见第十节）
│   ├── README.md                      # 总览：分类 / 原则 / 扩展
│   └── <theme>/                       # economy / tech / education / international / political / society
│       ├── README.md                  # 主题库：定义边界 / 术语对齐 / 场景词汇 / 索引 / 核验 / 缺口
│       └── prompt-<slug>.md            # 可复用提示词（work/life/research/learning-brief、skeleton）
└── data/
    └── <theme>/                        # 每主题一个数据目录（与 content/ 六主题同名，由 init 创建）
        ├── terms.md                   # 结构化存储（9 列 md-table 契约，脚本统一读写）
        ├── imports/                   # 批量导入文件暂存（保留留痕）
        │   └── 2026-11-18_merge-from-financial-markets.md
        └── exports/                   # 导出产物（json / csv / jsonl，供上层对接）
```

**主题与目录对齐（硬性）**：`data/<theme>/` 与 `prompts/<theme>/` 的主题名必须与 `content/` 六主题（`economy` / `tech` / `education` / `international` / `political` / `society`）及 `engine/tools/layout.json` 的 `themes` 一致；新增主题须先登记 `layout.json` 与 `topics.json`。

**三层解耦设计**（主题与实现完全分离的保证）：

| 层 | 载体 | 职责 | 变更频率 |
|---|---|---|---|
| 配置层 | `config/topics.json` | 主题 ID、名称、ID 前缀、三类路径、受控分类词表 | 新增领域时改这里（唯一） |
| 实现层 | `script/vocab_tool.py` | init/import/check/tag/export/index 全部逻辑，不含任何主题知识 | 极少（功能演进才改） |
| 数据层 | `data/<topic>/` | 词库存储、导入留痕、导出产物 | 每次词汇更新 |

**核心不变量**：脚本代码中不出现任何主题名、分类名、词条内容；数据文件中不出现流程逻辑。二者仅通过 `topics.json` 连接。

## 二、快速开始（AI 安全词汇已就位）

```powershell
python engine/vocabulary/script/vocab_tool.py topics                                          # 查看已注册主题（当前 6 个）
python engine/vocabulary/script/vocab_tool.py check --topic economy                           # 质量校验（当前 97 条，0 错误 0 警告）
python engine/vocabulary/script/vocab_tool.py export --topic economy --format all             # 一键导出 json/csv/jsonl
python engine/vocabulary/script/vocab_tool.py index                                           # 重新生成全主题索引
python engine/vocabulary/script/vocab_tool.py topic-check                                     # 注册表与目录一致性审计
```

提示词库入口：[prompts/README.md](./prompts/README.md)（总览）与各主题 `prompts/<theme>/README.md`。

## 三、全链路标准操作流程（六步）

所有命令在仓库根目录执行；退出码约定（对齐 `engine/tools` 工具链）：**0=通过，1=错误（阻断），2=警告（有产出但有瑕疵）**。

### S1 词汇收集

| 项 | 规范 |
|---|---|
| 来源要求 | 对齐仓库来源分级：官方一手优先；无法当场核验的来源填「需核实原文」；每条必须有来源（缺失时 import 自动补标「需核实原文」并告警） |
| 文件落位 | 导入文件放 `data/<topic>/imports/`，命名 `YYYY-MM-DD_说明.md`（或 `.csv` / `.json`） |
| 格式契约 | 6 列：`词条 / 别名 / 分类 / 标签 / 定义 / 来源`（表头中英文均可识别）；别名与标签用半角分号 `;` 分隔；单元格内禁止竖线与换行 |
| 增量语义 | import 天然增量：已存在的词条/别名自动跳过并计数，可安全重跑（幂等） |

**校验标准**：每条必须有词条、分类、定义三要素，否则该行计为无效并告警；import 汇总「新增 / 跳过重复 / 无效」三计数。

### S2 分类归档

| 项 | 规范 |
|---|---|
| 分类 | 必须取自 `topics.json` 该主题的 `categories` 受控词表；词表调整属配置层变更，随主题演进维护 |
| 标签 | 自由自定义（自定义标签分类），分号分隔，一个词条建议 1–3 个；用 `tag` 命令增删 |
| 归档 | 导入文件永久保留在 `imports/` 作为来源留痕，不删除 |

**校验标准**：`check` 对分类越界（不在受控词表）给警告（exit 2），不阻断；正式发布前警告应清零或确认合理。

### S3 去重校验

| 项 | 规范 |
|---|---|
| 归一化规则 | NFKC 折叠 + 空白折叠（多空格合一）+ 忽略大小写 + 全角分号折半 |
| 唯一性范围 | **词条 + 全部别名**共同构成全局唯一索引；词条与自身别名重复视为冗余（警告），跨条目冲突视为错误 |
| 双重防线 | import 时逐条比对已有索引，冲突即跳过（exit 2）；`check` 全库扫描兜底，跨条目重复=错误（exit 1 阻断） |

**校验标准**：`check` 报告「0 项错误」方可交付；冗余别名警告应清理。

### S4 结构化存储

| 项 | 规范 |
|---|---|
| 唯一存储 | `data/<topic>/terms.md`，9 列 md-table 契约：`ID / 词条 / 别名 / 分类 / 标签 / 定义 / 来源 / 首次登记 / 最近更新` |
| ID 规则 | `{id_prefix}-{三位序号}`（如 AIS-001），脚本自动分配、递增不复用 |
| 编辑纪律 | **词汇表禁止手工编辑**——一律走 `import`（新增）/ `tag`（标签）；单元格内竖线写入时自动转全角斜杠「／」 |
| 骨架生成 | `init` 创建空词库（v1.0）与 imports/exports 目录；已存在则跳过（幂等） |

**校验标准**：`check` 校验表头契约、ID 唯一性与序号连续性（不连续仅警告）。

### S5 索引生成与上层对接

| 项 | 规范 |
|---|---|
| 全主题索引 | `index` 命令 → `engine/vocabulary/INDEX.md`（主题 × 词条数 × 分类分布 × 版本 × 存储路径），自动生成勿手工编辑 |
| 结构化导出 | `export` 命令 → `exports/{topic}_{YYYY-MM-DD}_export.{json,csv,jsonl}`；jsonl 每行一个词条对象，适合检索系统逐行摄取 |
| 对接建议 | 以词条 ID 为主键；别名与标签作索引字段；分类作过滤面；JSON 顶层含 `topic / version / generated_at / count / categories` 元数据 |

**校验标准**：每次词汇变更后重跑 `index` + `export`，保证索引与产物同步；导出文件行数 = 词条数。

### S6 版本管理

| 项 | 规范 |
|---|---|
| 词库版本 | `terms.md` 尾部「版本记录」表由脚本自动追加：init 建 v1.0，每次 import / tag 自动递增小版本号并留痕计数 |
| 配置版本 | `topics.json` 的 `version` 字段由 `topic-add` / `topic-remove` 自动递增（每次操作自动备份到 `data/topic-backups/`），并更新 `updated` 日期 |
| git 纪律 | 一次词汇变更一个 commit（含 terms.md + imports 新文件 + 重新生成的 exports/INDEX.md）；提交前 `check` 须 0 错误 |

**校验标准**：任意词条可回溯「首次登记日期 + 引入它的导入文件 + 版本记录行」三要素。

## 四、新增主题扩展指南（一条命令，自动目录关联）

新增主题**无需手工编辑注册表**（topics.json 已降级为脚本托管文件），一条命令完成全部目录关联：

```powershell
python engine/vocabulary/script/vocab_tool.py topic-add --topic financial-markets --name 金融市场 --prefix FIN --categories "宏观与经济指标;金融机构与组织;金融工具与产品;市场机制与交易;监管与政策;估值与风险" --description "金融市场全领域词汇"
```

命令自动完成（实时同步主题↔目录映射）：

1. **注册表登记**：写入 topics.json（自动备份到 `data/topic-backups/`、注册表版本号自动递增）；`--prefix` 缺省自动派生并查重。同时须在 `engine/tools/layout.json` 登记主题与维度、在 `prompts/<theme>/` 建提示词库（见第十节）。
2. **目录结构创建**：`data/<topic>/` 三件套（terms.md 词库骨架 + imports/ + exports/）；若同名目录已存在则**孤儿纳管**（不覆盖既有内容）。
3. **索引同步**：INDEX.md 自动重建。
4. **操作日志**：`data/topic-ops.log` 逐条留痕（动作 / 前缀 / 分类 / 备份文件名 / 结果）。
5. **失败回滚**：任何一步异常自动恢复注册表备份并清理本次新建目录，现有结构不受影响，给出明确错误提示。

辅助命令：

- `topic-check`：一致性审计（前缀冲突、注册缺目录、孤儿目录、缺分类词表），错误 exit 1 / 警告 exit 2。
- `topic-remove [--force] [--delete-data]`：移除注册（词库非空须 `--force` 确认；数据默认保留，`--delete-data` 才删除）；自动提示 sync.json 残留绑定。

⚠️ **手工维护入口已移除**：直接编辑 topics.json 或 terms.md 不再是支持的操作方式；词条级新增仍按第三节 S1 走 `import`（自动触发提示词同步，见第九节）。

## 五、命令参考

| 命令 | 参数 | 用途 | 退出码 |
|---|---|---|---|
| `topics` | `--config`（可选） | 列出已注册主题 | 0 |
| `init` | `--topic` | 创建主题目录与词库骨架（幂等） | 0 |
| `import` | `--topic` `--file` | 批量导入（增量、自动去重跳过） | 0/1/2 |
| `check` | `--topic` | 全库去重与结构校验 | 0/1/2 |
| `tag` | `--topic` `--id` `--add` `--remove` | 词条标签增删（分号分隔，可只给其一） | 0/1 |
| `export` | `--topic` `--format` `--out` | 导出 json/csv/jsonl/all | 0/1 |
| `index` | `--config`（可选） | 生成全主题索引 INDEX.md | 0 |
| `topic-add` | `--topic` `--name` `--prefix` `--categories` `--description` | 注册新主题并自动创建目录结构（备份回滚 + 日志） | 0/1 |
| `topic-remove` | `--topic` `--force` `--delete-data` | 移除主题注册（数据默认保留） | 0/1 |
| `topic-check` | — | 注册表与目录结构一致性审计 | 0/1/2 |

通用参数：`--config` 指定备用主题注册表（默认 `engine/vocabulary/config/topics.json`）；导入文件路径支持相对仓库根或 engine/vocabulary/ 根书写。

## 六、数据契约（上层系统对接）

导出 JSON 顶层结构：

```json
{
  "topic": "ai-security",
  "name": "AI 安全",
  "version": "v1.1",
  "generated_at": "2026-11-13T12:00:00",
  "count": 47,
  "categories": {"攻击技术": 11, "防御与检测": 11},
  "terms": [
    {"id": "AIS-001", "term": "红队", "aliases": ["Red Team", "攻击模拟队"],
     "category": "组织与岗位", "tags": ["红队", "安全测试"],
     "definition": "…", "source": "NIST SP 800-115",
     "first_added": "2026-11-13", "last_updated": "2026-11-13"}
  ]
}
```

- **jsonl**：每行一个 `terms[]` 元素（UTF-8），适合 ES / 向量库逐行摄取。
- **csv**：与存储同列（UTF-8 BOM，Excel 直接可开），适合人工审阅。
- 字段语义以本节为准；`aliases` / `tags` 恒为数组，不存在缺省为 null 的情形。

## 七、质量标准（验收清单）

| 维度 | 标准 | 验证方式 |
|---|---|---|
| 无重复 | 词条+别名归一化后全局唯一，跨条目冲突=0 | `check`（exit 1 即存在重复） |
| 分类准确 | 全部词条分类在受控词表内，越界=0 | `check` 警告清零 |
| 字段完整 | 词条/分类/定义三要素齐全，来源非空 | `import` 无效计数=0 |
| 检索高效 | 导出 jsonl/json 可供检索系统直接摄取；ID 为主键 | `export` 产物行数=词条数 |
| 可追溯 | 每条可回溯引入文件与版本；索引同步 | `terms.md` 版本记录 + `INDEX.md` 更新时间 |
| 幂等安全 | 重复 import 零新增；init 重复执行零覆盖 | 重跑 `import`/`init` 观察输出 |

## 七·补、术语策略（缩写 vs 中文规范形）

- **规范形优先中文全称**：词条 `canonical` 默认使用中文全称（如「贷款市场报价利率」），缩写（LPR）入 `aliases`；报告与提示词正文引用规范形，缩写仅在括号注或空间受限时使用。
- **跨语言词条**：英文专有名词（机构 / 产品 / 基准名）保留原文规范形（如 `SWE-bench Verified`），中文译名录入 `aliases`，不强制翻译。
- **缩写收敛**：同一缩写对应多个全称时（如「CPI」），须按主题 / 口径拆分词条并在 `aliases` 中显式区分，不得共用规范形。
- **单一事实源**：规范形只定义于 `data/<theme>/terms.md`；提示词与报告只引用，不复制定义（见第三节）。

---

## 八、异常排查

| 现象 | 原因 | 处置 |
|---|---|---|
| import 报「词库不存在」 | 未初始化 | 先 `init --topic <主题>` |
| import 报「主题未注册」 | topics.json 无该条目 | 按第四节登记后再 init |
| 大量「与已有条目重复，已跳过」 | 重复导入同一文件 | 正常幂等行为（exit 2），确认无新增即结束 |
| check 报跨条目重复 | 不同词条的词条名/别名归一化后相同 | 判定保留方，修正导入文件重新入库（冗余方不再导入） |
| check 报「分类不在受控词表」 | categories 词表滞后于词汇演进 | 核对后二选一：改词条分类，或更新 topics.json 词表 |
| 单元格出现「／」 | 原文含竖线被自动转写 | 属预期消毒；如需保留竖线请改写措辞 |
| INDEX.md 导出时间过期 | 变更后未重跑 index | 重跑 `export` + `index` |
| topic-add 报「ID 前缀冲突」 | 自动派生前缀已被占用 | 换 `--prefix` 指定其他 2–4 位大写字母前缀 |
| topic-check 报「孤儿数据目录」 | data/ 下存在未注册目录 | 确认无用后删除，或用 `topic-add` 纳管（不覆盖既有内容） |
| topic-remove 报「词库含 N 条词条」 | 防误删保护 | 确认后加 `--force`（数据仍保留）；连数据一起删加 `--delete-data` |
| PowerShell 下 `--delete-data` 等开关传参报「缺少参数」 | PS 5.1 对连续 `--` 开关的解析怪癖 | 开关参数放命令最前，或用引号包裹（`"--delete-data"`） |

## 九、自动同步（sync_vocab.py）— 词汇库更新后自动写入业务提示词

词汇库与业务提示词的绑定由 [script/sync_vocab.py](./script/sync_vocab.py) 自动完成：词条以标记区间（`<!-- VOCAB-SYNC:BEGIN topic=... -->` … `<!-- VOCAB-SYNC:END -->`）写入目标提示词文件，**区间外内容字节级零触碰**；增量检测（逐词条 sha256 比对，仅变更条目触发写盘）、写后校验（区间完整性 + 词条覆盖 + 区间外内容与写入前逐字节一致），校验失败**自动回滚备份**。

### 9.1 部署方式（三选一或组合）

| 方式 | 操作 | 适用场景 |
|---|---|---|
| 自动钩子（默认，推荐） | 无需部署：`vocab_tool.py` 的 `import` / `tag` 成功写盘后自动调用同步（`sync.json` 的 `auto_trigger: true` 时生效） | Agent 驱动的常规词汇维护 |
| 常驻监听 | `python engine/vocabulary/script/sync_vocab.py watch`（`--interval N` 调轮询间隔，默认取配置 `watch_interval_sec`） | 词汇库可能被脚本外手段直接修改时 |
| 手动/定时 | `sync` 子命令（也是失败后的重试入口）；可挂 Schedule 定期执行 `sync` | 一次性接入、兜底对账 |

### 9.2 触发条件与配置

- 触发条件：词汇库 `terms.md` 内容发生变化（新增/修改/删除词条，含标签调整），或目标提示词区间被外部改动（结构漂移自动修复）。
- 绑定配置在 [config/sync.json](./config/sync.json)：`bindings[].topic`（须已在 topics.json 注册）、`targets[].path`（目标提示词，相对 engine/vocabulary/ 根）、`insert_before`（区块缺失时的插入锚点，须为目标文件内唯一文本）、`format`（`digest` 按分类紧凑速览 / `table` 三列表格）、`categories_include` / `tags_include`（可选过滤，空 = 全量）。
- 新增绑定只需在 `sync.json` 追加一个 target；词汇库侧零改动。

### 9.3 校验与数据安全

- 同步前：`check` 输出「新增 / 修改 / 删除」逐条差异（含词条名），不写盘。
- 同步后：回读磁盘验证标记配对、词条全覆盖、区间外内容与写入前逐字节一致；任一失败自动回滚到 `data/sync-backups/` 备份（每目标保留最近 `backup_keep` 份）。
- 写入采用临时文件 + 原子替换（os.replace），不存在半写状态；保留原文换行风格（CRLF/LF 自适应）。
- 全部动作追加记录到 `data/sync.log`；同步状态（逐词条 hash）存 `data/sync-state.json`。

### 9.4 常见问题排查

| 现象 | 原因 | 处置 |
|---|---|---|
| `未找到插入锚点「…」` | 目标文件被重构，`insert_before` 文本不再存在 | 更新 sync.json 锚点后重试 `sync` |
| `结构漂移待修复` | 区间被手工编辑或部分删除 | 直接重跑 `sync`，脚本自动整块重写修复 |
| 自动同步提示「未成功（exit 1）」 | 见 `data/sync.log` 中 `[error]` 行 | 修复后手动重试：`sync_vocab.py sync --topic T` |
| `词条未覆盖 N 条`（verify） | 词汇库在同步后又变更 | 重跑 `sync` |
| 首次接入业务线 | 目标尚无标记区间 | 配置 `insert_before` 后跑一次 `sync`（自动插入区块）；并在目标文件版本记录人工登记机制接入（如 business-config v1.2） |
| 想临时停用自动同步 | — | `sync.json` 设 `auto_trigger: false`（watch/手动 sync 不受影响） |

### 9.5 已接入绑定

| 词汇库主题 | 目标提示词 | 接入日期 |
|---|---|---|
| tech（AI 类 12 分类，119 条） | `content/tech/weekly-roundup/prompts/business-config.md`「词汇速览 · 科技」区块（插于第八节版本记录之前） | 2026-11-18 |
| tech（网络类 6 分类，153 条） | `content/tech/security/dubai/prompts/business-config.md`「词汇速览」区块（插于第十节版本记录之前） | 2026-11-18 |
| economy（宏观经济 3 分类，48 条） | `content/economy/trends/prompts/business-config.md`「词汇速览」区块（插于第八节版本记录之前） | 2026-11-18 |
| economy（金融 6 分类，49 条） | `content/economy/dubai/apartment/prompts/business-config.md`「词汇速览」区块（插于第十四节版本记录之前） | 2026-11-18 |

> 归并后 `tech` / `economy` 各按 `categories_include` 拆分为不同业务线区块，各业务线原有词汇范围不变。

---

## 十、提示词库（prompts/）— 与词库同主题对齐的可复用提示词层

提示词库与词库**同主题、同目录名**管理，随词条演进维护；入口 [prompts/README.md](./prompts/README.md)。

### 10.1 目录与命名

| 位置 | 规则 | 示例 |
|---|---|---|
| `prompts/<theme>/README.md` | 主题库总览（定义边界 / 术语对齐 / 场景词汇 / 索引 / 核验 / 缺口） | `prompts/economy/README.md` |
| `prompts/<theme>/prompt-<slug>.md` | 可复用提示词；slug ∈ `work-brief` / `life-brief` / `research-brief` / `learning-brief` / `skeleton` | `prompt-work-brief.md` |

- `<theme>` 必须命中 `topics.json` 注册主题与 `content/` 六主题。
- 空主题仅交 `README.md` + `prompt-skeleton.md`（骨架），词库采集后补全。
- 上位规范 `engine/docs/structure-and-naming-spec.md` 第 7.2 节的位置登记待一次性同步补登（本节为该位置的现行规则）。

### 10.2 维护规则

| 项 | 规则 |
|---|---|
| 术语单一事实源 | 提示词中的术语规范形与同义表达**只引用** `data/<theme>/terms.md`，不复制定义 |
| 词条变更 | 走 `import` / `tag`；如影响提示词术语约束，同步更新 `prompts/<theme>/README.md` 第 2.2 节 |
| 新增场景提示词 | 复用四场景结构；正文含「适用 / 不适用 / 边界 / 常见误解 / 信息缺口」 |
| 核验 | 对照 `prompts/README.md` 第五节口径逐项自检；缺口显式登记于主题 README 第六节 |

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 子系统建立：SOP 六步流程 + vocab_tool.py（7 子命令）+ topics.json 主题注册 + AI 安全种子 47 条（7 分类）入库 v1.1；全链路含幂等/去重/错误路径自检通过 |
| v1.1 | 2026-11-13 | 新增 financial-markets 主题 | 金融市场主体接入：6 分类 49 条种子入库；topics.json v1.1 |
| v1.2 | 2026-11-13 | 自动同步机制 | 新增 sync_vocab.py（sync/check/verify/watch/status 五命令：标记区间保护 + 增量检测 + 写后校验自动回滚 + 日志）与 sync.json 绑定配置；vocab_tool import/tag 增加自动同步钩子；ai-security → business-config.md 绑定接入并实测通过（含 watch 轮询与错误路径自检） |
| v1.3 | 2026-11-13 | 主题管理自动化 | 新增 topic-add / topic-remove / topic-check：新增主题一条命令自动完成注册表登记 + 目录创建 + 索引重建（备份回滚 + topic-ops.log 操作日志，前缀自动派生查重、孤儿目录纳管）；手工编辑 topics.json 降级为非支持入口。正反路径与孤儿纳管实测通过 |
| v1.4 | 2026-11-13 | 新增 cybersecurity 主题与第二条绑定 | cybersecurity 主题接入（6 分类 90 条，两批种子）并绑定同步至 content/tech/regional/dubai/security/prompts/business-config.md（sync.json v1.1）；全库 3 主题 188 条 |
| v1.5 | 2026-11-13 | 第三条绑定（全量覆盖） | financial-markets 绑定同步至 content/economy/real-estate/apartment/prompts/business-config.md；至此三条业务线全部接入自动同步（49+90+49=188 条） |
| v1.6 | 2026-11-13 | 新增 economy 主题与第四条绑定 | economy（经济）主题接入：3 分类（经济体与国家 / 区域经济组织 / 经济概念），种子 17 条入库 + 并行批次扩展至 44 条 + 海湾补充批次 4 条（v1.3），ECO 前缀；绑定同步至 content/economy/trends/prompts/business-config.md（sync.json v1.2）；全库 4 主题 |
| v1.7 | 2026-11-13 | 新增 ai-agent 主题与第五条绑定 | ai-agent（AI Agent 与大模型）主题接入：5 分类（模型与厂商 / Agent 技术与框架 / 编码工具与 IDE / 应用与产品 / 概念与评估），两批种子共 73 条入库（v1.2），AAG 前缀；绑定同步至 content/tech/regional/global/trends/prompts/business-config.md（sync.json v1.3）；全库 5 主题 372 条 |
| v1.8 | 2026-11-14 | 绑定迁移（业务线合并） | trends/ai-security 与 trends/ai-agent 合并为 content/tech/regional/global/trends；两条词汇主题（ai-security 49 条、ai-agent 73 条）改绑定至 `content/tech/regional/global/trends/prompts/business-config.md`（两个「词汇速览」区块）；sync.json v1.4 |
| v1.9 | 2026-11-14 | 绑定路径更新（地区优先重构） | 地区维度优先级调整：`technology/ai/{sub_direction}/{region}` → `technology/ai/{region}/{sub_direction}`；ai-security / ai-agent 绑定改指 `content/tech/regional/global/trends/prompts/business-config.md`，cybersecurity 改指 `content/tech/regional/dubai/security/prompts/business-config.md`；sync.json v1.5 |
| v1.10 | 2026-11-17 | 绑定路径迁移（六主题回滚） | 内容结构回滚至 economy/tech 六主题：ai-security / ai-agent → `content/tech/weekly-roundup/...`，cybersecurity → `content/tech/security/dubai/...`，financial-markets → `content/economy/dubai/apartment/...`，economy → `content/economy/trends/...`；sync.json v1.6 |
| v1.11 | 2026-11-18 | 主题归并 + 提示词库 | `data/` 对齐 `content/` 六主题：economy（归并 financial-markets，97 条）、tech（归并 ai-agent / ai-security / cybersecurity，272 条）；新建 education / international / political / society 空主题；新增 `prompts/` 多主题提示词库；sync.json 改按 `categories_include` 拆分（v1.7） |
