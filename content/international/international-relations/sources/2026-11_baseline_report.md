# 全球 · 国际关系与外交 · 首期基线报告（2026-11）

### 九节固化锚 · 政策法规解读型 · 预校准（ex-ante）

<div class="delta-strip">
  <div class="d add"><div class="n">全量</div><div class="l">本期新增（基线首期 = 全部基线项）</div></div>
  <div class="d fix"><div class="n">0 条</div><div class="l">修正（已修正事实清单见第八节）</div></div>
  <div class="d same"><div class="n">0 条</div><div class="l">无变化（无上期报告）</div></div>
  <div class="d hyp"><div class="n">0/7</div><div class="l">假设核验进度（已登记 7 条假设/缺口）</div></div>
</div>

<p class="small muted">基线首期：本期新增 = 全部基线项；「已修正事实清单」为空，产生修正后逐条补记。本报告为后续事件解读与年度台账的<strong>滚动基线</strong>（对比锚），基线本身永不重跑。</p>

<h2 id="s1">一、执行摘要</h2>

<div class="card leadbox">
<h3>核心判断</h3>
<ol class="tight">
<li><b>机制基线</b>：以《联合国宪章》（1945-06-26 签署、1945-10-24 生效）为顶层法律框架的联合国体系是国际关系监测主干；六大主要机关与 ICJ 规约（构成宪章组成部分）为机制锚。<span class="lvl lvl-verified">已核验</span> [G03][G04]</li>
<li><b>条约基线</b>：外交/领事两公约（1961/1963）、UNCLOS（1982）、NPT（1968）、巴黎协定（2015）构成高普遍性基线；实时缔约方数以 UN Treaty Collection 状态页为准。<span class="lvl lvl-verified">已核验</span> [G03]</li>
<li><b>监测节拍</b>：事件触发单份解读 + 年度台账复盘；K01–K08 信号阈值与 RL-01–RL-05 红线为 ex-ante 预校准，首次中期回测 2027-06。<span class="lvl lvl-verified">已核验</span> [K01][RL-01]</li>
<li><b>数据缺口</b>：UN Treaty Collection 状态页、ICC/ICJ 官网、非英语官方原文本期未能自动核验，登记未核验清单 7 项。<span class="lvl lvl-partial">部分核验</span> [G02]</li>
<li><b>结论边界</b>：只给框架性说明与可核验信息，不构成外交、法律或安全建议，不预测他国政策意图。<span class="lvl lvl-verified">已核验</span> [K07]</li>
<li><b>场景切片</b>：主场景政策制定、次场景合规应对；本期为机制建立，事件解读待触发后启动。<span class="lvl lvl-verified">已核验</span> [G01]</li>
</ol>
<p><b>一句话定位</b>：国际关系与外交监测以官方文本为唯一采信层，基线锁定机制框架与条约状态，事件解读与年度台账在基线之上滚动。</p>
<p class="small muted">来源与时点：数据截止 2026-11；分级见第八节、URL 见第九节。</p>
</div>

<div class="preline">阈值与信号规则为「预校准（ex-ante）」；首次中期回测 2027-06。</div>

<h2 id="s2">二、政策台账与监测机制</h2>

<h3>2.1 台账结构（字段定义）</h3>

<p>台账为活值登记载体（<code>data/processed/international/international-relations/international_relations_ledger.md</code>），来源登记为 <code>source_registry.json</code>。字段如下：</p>

<div class="tblwrap"><table>
<thead><tr><th style="width:16%">字段</th><th style="width:44%">定义</th><th style="width:40%">口径 / 示例</th></tr></thead>
<tbody>
<tr><td>指标编号</td><td>K01–K08（信号）/ RL-01–RL-05（红线）/ G01–G05（政策框架）</td><td>一一对应，不混用</td></tr>
<tr><td>上期值 / 本期值 / 变化</td><td>滚动基线对比</td><td>基线首期无上期值</td></tr>
<tr><td>来源</td><td>官方原文 URL + 版本日期</td><td>媒体转述仅作线索，标「需核实原文」</td></tr>
<tr><td>口径</td><td>签署 / 批准 / 生效分列；制裁 / 出口管制 / 投资限制分列</td><td>外交关系级别 ≠ 外交承认</td></tr>
<tr><td>是否更新</td><td>是 / 否 + 更新时间</td><td>核验型运行不升级版本号</td></tr>
<tr><td>已修正事实清单</td><td>防回退：与清单冲突的旧结论不得复活</td><td>首期为空</td></tr>
</tbody>
</table></div>

<h3>2.2 监测节拍与触发器</h3>

<ul class="tight">
<li><b>主节拍（事件触发单份解读）</b>：各国外交部声明 / 发言人表态 → 外交关系专题；制裁、出口管制、投资限制新规 → 制裁合规专题；条约签署 / 批准 / 退出 → 条约专题；国际组织峰会、决议、席位变动 → 多边机制专题；冲突升级 / 停火谈判 → 冲突专题（并列多方口径）。</li>
<li><b>年度</b>：UN Treaty Collection 年度更新 → 条约状态基线；各国外交政策白皮书 / 战略文件 → 政策基线；国际组织年度报告 → 机制运行基线；台账年度复核 → 口径冲突与已修正事实清单更新。</li>
<li><b>先行信号标准矩阵</b>：① 官方声明与公报；② 条约与决议文本；③ 制裁与合规清单；④ 组织席位与投票记录；⑤ 使领馆与人员往来；⑥ 冲突与停火动态。</li>
<li><b>失真信号清单</b>：匿名消息、单一媒体爆料、把表态当政策、把签署当生效、把智库报告当官方立场。</li>
</ul>

<h3>2.3 官方发布渠道清单（P0–P5）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:8%">优先级</th><th style="width:20%">渠道</th><th style="width:34%">官方 URL</th><th style="width:20%">更新机制</th><th style="width:18%">本期核验</th></tr></thead>
<tbody>
<tr><td>P0</td><td>UN Treaty Collection</td><td><a href="https://treaties.un.org/">https://treaties.un.org/</a></td><td>保管国通知 / 状态页</td><td>已核验（首页抓取）</td></tr>
<tr><td>P0</td><td>联合国宪章与公约页</td><td><a href="https://www.un.org/en/about-us/un-charter">https://www.un.org/en/about-us/un-charter</a></td><td>静态 + 修正案</td><td>已核验</td></tr>
<tr><td>P0</td><td>UNFCCC（巴黎协定）</td><td><a href="https://unfccc.int/process-and-meetings/the-paris-agreement">https://unfccc.int/process-and-meetings/the-paris-agreement</a></td><td>批准状态页</td><td>已核验</td></tr>
<tr><td>P0</td><td>UNODA（NPT）</td><td><a href="https://www.un.org/disarmament/wmd/nuclear/npt/">https://www.un.org/disarmament/wmd/nuclear/npt/</a></td><td>审议大会周期</td><td>已核验</td></tr>
<tr><td>P0</td><td>中国外交部</td><td><a href="https://www.mfa.gov.cn/eng/">https://www.mfa.gov.cn/eng/</a></td><td>声明 / 例行记者会</td><td>已核验（入口）</td></tr>
<tr><td>P0</td><td>美国 OFAC</td><td><a href="https://ofac.treasury.gov/">https://ofac.treasury.gov/</a></td><td>Recent Actions / 清单</td><td>已核验（入口）</td></tr>
<tr><td>P0</td><td>美国国务院</td><td><a href="https://www.state.gov/">https://www.state.gov/</a></td><td>声明 / 简报</td><td>未核验（未抓取）</td></tr>
<tr><td>P0</td><td>英国 FCDO</td><td><a href="https://www.gov.uk/government/organisations/foreign-commonwealth-and-development-office">https://www.gov.uk/government/organisations/foreign-commonwealth-and-development-office</a></td><td>声明 / 指南</td><td>未核验</td></tr>
<tr><td>P0</td><td>日本外务省</td><td><a href="https://www.mofa.go.jp/">https://www.mofa.go.jp/</a></td><td>声明 / 演説</td><td>未核验</td></tr>
<tr><td>P0</td><td>韩国外交部</td><td><a href="https://www.mofa.go.kr/eng/index.do">https://www.mofa.go.kr/eng/index.do</a></td><td>声明 / 记者会</td><td>未核验</td></tr>
<tr><td>P0</td><td>欧盟 EEAS</td><td><a href="https://www.eeas.europa.eu/">https://www.eeas.europa.eu/</a></td><td>声明 / 制裁</td><td>未核验（入口临时不可用）</td></tr>
<tr><td>P1</td><td>UN Digital Library</td><td><a href="https://digitallibrary.un.org/">https://digitallibrary.un.org/</a></td><td>决议 / 文件</td><td>未核验</td></tr>
<tr><td>P1</td><td>国际法院 ICJ</td><td><a href="https://www.icj-cij.org/en">https://www.icj-cij.org/en</a></td><td>判决 / 命令</td><td>未核验（反爬）</td></tr>
<tr><td>P1</td><td>国际刑事法院 ICC</td><td><a href="https://www.icc-cpi.int/about/the-court">https://www.icc-cpi.int/about/the-court</a></td><td>裁决 / 状态</td><td>未核验（反爬）</td></tr>
<tr><td>P2</td><td>WTO 法律文本</td><td><a href="https://www.wto.org/english/docs_e/legal_e/legal_e.htm">https://www.wto.org/english/docs_e/legal_e/legal_e.htm</a></td><td>协定 / 争端</td><td>未核验</td></tr>
<tr><td>P2</td><td>ICRC</td><td><a href="https://www.icrc.org/">https://www.icrc.org/</a></td><td>条约与习惯法</td><td>未核验</td></tr>
<tr><td>P4</td><td>ICG / Chatham House / IISS / CFR</td><td>各机构官网</td><td>分析报告</td><td>本基线未引用</td></tr>
</tbody>
</table></div>

<div class="note">渠道分级按业务配置第四节：P0 官方声明 / 条约文本 / 官方公报为唯一可直接采信层；P1 官方 PDF / 会议纪要 / 决议文本；P2 国际组织数据库；P3 英文媒体（只作线索）；P4 智库与行业机构（交叉验证方向）；P5 官方条约集 / 法律文本（最终裁决条约状态与效力口径）。</div>

<h3>2.4 信号规则阈值（K01–K08，ex-ante 预校准）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:7%">编号</th><th style="width:17%">监测对象</th><th style="width:7%">等级</th><th style="width:15%">绿灯</th><th style="width:15%">黄灯</th><th style="width:19%">预警红线</th><th style="width:14%">硬红线</th><th style="width:6%">基线状态</th></tr></thead>
<tbody>
<tr><td>K01</td><td>外交关系级别变动</td><td>一级</td><td>无变更</td><td>领导人表态</td><td>召回大使 / 降级</td><td>断交</td><td>未触发</td></tr>
<tr><td>K02</td><td>制裁 / 出口管制</td><td>一级</td><td>无新增</td><td>名单扩充讨论</td><td>新增单边制裁</td><td>全面制裁 / 二级制裁</td><td>未触发</td></tr>
<tr><td>K03</td><td>条约签署 / 退出</td><td>一级</td><td>无</td><td>谈判启动</td><td>签署待批准</td><td>批准生效或正式退出</td><td>未触发</td></tr>
<tr><td>K04</td><td>国际组织席位 / 投票</td><td>二级</td><td>正常</td><td>成员资格争议</td><td>暂停权利</td><td>退出组织</td><td>未触发</td></tr>
<tr><td>K05</td><td>使领馆与外交机构变动</td><td>二级</td><td>无变更</td><td>临时关闭</td><td>撤馆</td><td>大规模闭馆</td><td>未触发</td></tr>
<tr><td>K06</td><td>重大峰会 / 联合声明</td><td>二级</td><td>例行</td><td>议题争议</td><td>无联合公报</td><td>公开分歧</td><td>未触发</td></tr>
<tr><td>K07</td><td>冲突 / 停火</td><td>一级</td><td>无升级</td><td>局部摩擦</td><td>全面冲突</td><td>停火破裂</td><td>未触发</td></tr>
<tr><td>K08</td><td>国际司法 / 仲裁裁决</td><td>三级</td><td>无</td><td>程序启动</td><td>临时措施</td><td>实体裁决</td><td>未触发</td></tr>
</tbody>
</table></div>

<h3>2.5 结构红线登记簿（RL-01–RL-05）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:16%">监测对象</th><th style="width:33%">硬阈值</th><th style="width:28%">触发后动作</th><th style="width:14%">基线状态</th></tr></thead>
<tbody>
<tr><td>RL-01</td><td>外交关系</td><td>断交或外交关系降级至代办级</td><td>重算双边合作与人员往来假设</td><td>未触发</td></tr>
<tr><td>RL-02</td><td>制裁合规</td><td>全面制裁 / 二级制裁生效</td><td>重算贸易、金融与供应链合规边界</td><td>未触发</td></tr>
<tr><td>RL-03</td><td>条约效力</td><td>正式退出已生效多边条约</td><td>重算相关权利义务与替代机制</td><td>未触发</td></tr>
<tr><td>RL-04</td><td>冲突状态</td><td>全面冲突或停火破裂</td><td>重算人员安全与运营连续性</td><td>未触发</td></tr>
<tr><td>RL-05</td><td>国际司法</td><td>不利实体裁决且无上诉救济</td><td>重算法律风险与合规应对</td><td>未触发</td></tr>
</tbody>
</table></div>

<h3>2.6 政策框架复核清单（G01–G05）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:22%">政策项</th><th style="width:45%">官方入口</th><th style="width:24%">复核周期</th></tr></thead>
<tbody>
<tr><td>G01</td><td>外交关系与使领馆</td><td>各国外交部</td><td>事件触发 + 年度</td></tr>
<tr><td>G02</td><td>制裁与出口管制</td><td>各国政府 + OFAC / EU 官方清单</td><td>事件触发 + 年度</td></tr>
<tr><td>G03</td><td>条约与多边机制</td><td>UN Treaty Collection</td><td>年度</td></tr>
<tr><td>G04</td><td>国际组织与席位</td><td>各组织官方站</td><td>事件触发 + 年度</td></tr>
<tr><td>G05</td><td>国际法与仲裁</td><td>国际法院 / 仲裁庭官方文本</td><td>事件触发 + 年度</td></tr>
</tbody>
</table></div>

<p class="small muted">规则：未取得官方原文的标「未核验」；入口页 ≠ 条款页；任一变更 → 立即重算受影响结论。</p>

<h2 id="s3">三、国际机制框架总览</h2>

<h3>3.1 层级地图</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:14%">层级</th><th style="width:30%">代表文件</th><th style="width:26%">效力</th><th style="width:30%">监测要点</th></tr></thead>
<tbody>
<tr><td>L1 宪章 / 多边公约</td><td>《联合国宪章》；外交 / 领事两公约；UNCLOS；NPT；巴黎协定</td><td>对缔约国法律约束</td><td>签署 / 批准 / 生效 / 保留分列</td></tr>
<tr><td>L2 组织决议 / 规则</td><td>安理会决议、联大决议、WTO 专家组报告、UNFCCC 决定</td><td>视授权与章程</td><td>决议号、表决、执行与后续</td></tr>
<tr><td>L3 官方声明 / 指南</td><td>外交部声明、发言人表态、制裁指南、白皮书</td><td>政策信号，非法律约束</td><td>与政策文件区分；不把表态当政策</td></tr>
</tbody>
</table></div>

<h3>3.2 机制地图</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:15%">机制</th><th style="width:22%">法律基础</th><th style="width:27%">官方入口</th><th style="width:36%">监测要点</th></tr></thead>
<tbody>
<tr><td>联合国</td><td>《联合国宪章》</td><td><a href="https://www.un.org/en/about-us/un-charter">un.org/en/about-us/un-charter</a></td><td>六大主要机关；第 7 章强制行动、第 8 章区域安排</td></tr>
<tr><td>国际法院 ICJ</td><td>ICJ 规约（宪章附件）</td><td><a href="https://www.icj-cij.org/en">icj-cij.org</a></td><td>案件、咨询意见、判决执行（本期未核验）</td></tr>
<tr><td>国际刑事法院 ICC</td><td>《罗马规约》</td><td><a href="https://www.icc-cpi.int/about/the-court">icc-cpi.int</a></td><td>缔约国、管辖与调查（本期未核验）</td></tr>
<tr><td>国际海洋法法庭 ITLOS</td><td>UNCLOS 附件六</td><td><a href="https://www.itlos.org/">itlos.org</a></td><td>深海采矿争端专属管辖（本期未核验）</td></tr>
<tr><td>WTO</td><td>Marrakesh 协定 / WTO 协定</td><td><a href="https://www.wto.org/english/docs_e/legal_e/legal_e.htm">wto.org 法律文本</a></td><td>争端解决、上诉机构（本期未核验）</td></tr>
<tr><td>气候机制</td><td>UNFCCC / 巴黎协定</td><td><a href="https://unfccc.int/process-and-meetings/the-paris-agreement">unfccc.int</a></td><td>NDC 五年周期、全球盘点</td></tr>
<tr><td>东盟</td><td>《东盟宪章》</td><td><a href="https://asean.org/asean-charter/">asean.org</a></td><td>三大共同体、峰会与声明</td></tr>
<tr><td>非盟</td><td>《非盟组织法》</td><td><a href="https://au.int/en/constitutive-act">au.int</a></td><td>和平安全架构（本期未核验）</td></tr>
<tr><td>阿盟</td><td>阿盟宪章</td><td><a href="https://www.leagueofarabstates.net/">leagueofarabstates.net</a></td><td>成员国声明（本期未核验）</td></tr>
<tr><td>人道法</td><td>日内瓦四公约</td><td><a href="https://www.icrc.org/">icrc.org</a></td><td>普遍批准、共同第 1 条（本期未核验）</td></tr>
</tbody>
</table></div>

<h3>3.3 框架演变脉络</h3>

<div class="timeline">
  <div class="tl-item"><div class="tl-date">1945</div><div class="tl-body"><div class="t">《联合国宪章》签署并生效</div><div class="d">1945-06-26 旧金山签署；1945-10-24 生效；1963 / 1965 / 1973 三次修正。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">1949</div><div class="tl-body"><div class="t">日内瓦四公约</div><div class="d">1949-08-12 通过；普遍批准（国数未核验）。<span class="lvl lvl-partial">部分核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">1961 / 1963</div><div class="tl-body"><div class="t">维也纳外交 / 领事两公约</div><div class="d">外交 1961-04-18 通过、1964-04-24 生效；领事 1963-04-24 通过、1967-03-19 生效。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">1968 / 1970</div><div class="tl-body"><div class="t">《不扩散核武器条约》</div><div class="d">1968 开放签署、1970 生效；1995-05-11 无限期延长；191 国。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">1982 / 1994</div><div class="tl-body"><div class="t">《联合国海洋法公约》</div><div class="d">1982-12-10 蒙特哥贝开放签署；1994-11-16 生效；320 条 + 9 附件。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2008</div><div class="tl-body"><div class="t">《东盟宪章》生效</div><div class="d">2008-12-15 生效；10 个成员国全部批准；2025-10-26 东帝汶加入（第 11 个成员国）。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2015 / 2016</div><div class="tl-body"><div class="t">《巴黎协定》</div><div class="d">2015-12-12 195 方通过；2016-11-04 生效；194 方（截至 2026-01-27）。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2023 / 2026</div><div class="tl-body green"><div class="t">BBNJ 协定</div><div class="d">2023-06-19 通过；2025-09-19 生效条件满足；2026-01-17 生效。<span class="lvl lvl-verified">已核验</span></div></div></div>
</div>

<h3>3.4 术语口径区分（不得混用）</h3>

<div class="term"><b>外交关系级别 ≠ 外交承认</b>：建交 / 代办级 / 大使级 / 断交须逐条核对官方表述。<br>
<b>制裁 ≠ 出口管制 ≠ 投资限制</b>：法律工具与适用对象不同，分列。<br>
<b>条约签署 ≠ 批准 ≠ 生效</b>：三阶段分列，附各自日期。<br>
<b>国际组织成员 ≠ 观察员 ≠ 对话伙伴</b>：地位与权利不同。<br>
<b>停火 ≠ 和平协议 ≠ 终战宣言</b>：法律效力不同。<br>
<b>声明 ≠ 联合公报 ≠ 行动计划</b>：约束力不同。</div>

<h2 id="s4">四、重点条约与机制逐条解读</h2>

<h3>4.1 《联合国宪章》</h3>

<p><b>条款摘编</b>：第 2(4) 条禁止使用武力或威胁使用武力；第 2(7) 条不干涉内政原则；第 51 条单独或集体自卫之固有权利；第 7 章（第 39–51 条）安全理事会对和平之威胁、破坏及侵略行为之行动；第 8 章（第 52–54 条）区域办法。宪章于 1945-06-26 签署、1945-10-24 生效，1963 / 1965 / 1973 三次修正；ICJ 规约构成宪章组成部分。<span class="lvl lvl-verified">已核验</span></p>
<p><b>解读</b>：监测上以「第 7 章强制行动」与「第 8 章区域安排」区分强制力层级；决议类信号须记录决议号、表决情况与执行条款，文本依据回溯至 UN Digital Library 或官方公报。</p>
<p><b>官方答问 / 配套</b>：宪章全文、修正案页、ICJ 规约页。<span class="src-inline">来源：<a href="https://www.un.org/en/about-us/un-charter">https://www.un.org/en/about-us/un-charter</a>；<a href="https://www.un.org/en/about-us/un-charter/full-text">https://www.un.org/en/about-us/un-charter/full-text</a></span></p>

<h3>4.2 《维也纳外交关系公约》</h3>

<p><b>条款摘编</b>：第 2 条（外交关系及常设使馆之建立以协议为之）；第 22 条（使馆馆舍不得侵犯）；第 29 条（外交代表人身不得侵犯）；第 31 条（刑事管辖豁免及民事 / 行政管辖豁免之例外）；第 45 条（断交或使馆撤退时对馆舍、财产与档案之保护）。1961-04-18 通过并开放签署，1964-04-24 依第 51 条生效。<span class="lvl lvl-verified">已核验</span></p>
<p><b>解读</b>：本公约是 K01（外交关系级别变动）与 K05（使领馆变动）的条款基准；「不受欢迎的人」（第 9 条）与豁免放弃（第 32 条）须逐条核对官方表述。</p>
<p><b>官方答问 / 配套</b>：两任择议定书（取得国籍、强制解决争端）；实时缔约方数与保留声明以 UN Treaty Collection 状态页为准（本期未核验）。<span class="src-inline">来源：<a href="https://www.un.org/zh/documents/treaty/UNCITRAL-1961">https://www.un.org/zh/documents/treaty/UNCITRAL-1961</a>；状态页 <a href="https://treaties.un.org/pages/ViewDetails.aspx?src=TREATY&amp;mtdsg_no=III-3&amp;chapter=3&amp;clang=_en">treaties.un.org III-3</a></span></p>

<h3>4.3 《维也纳领事关系公约》</h3>

<p><b>条款摘编</b>：第 2 条（领事关系以协议建立；<b>断绝外交关系不当然断绝领事关系</b>）；第 5 条（领事职务）；第 36 条（与派遣国国民通讯及会见之自由，含拘禁情形通知与探视）；第 27 条（断绝领事关系时对馆舍与档案之保护）。1963-04-24 通过，1967-03-19 依第 77 条生效。<span class="lvl lvl-verified">已核验</span></p>
<p><b>解读</b>：第 36 条领事通知与探视是公民服务与合规要点；K05 使领馆变动须区分「临时关闭 / 撤馆 / 大规模闭馆」并评估对公民服务的影响。</p>
<p><b>官方答问 / 配套</b>：实时缔约方数与保留声明以 UN Treaty Collection 状态页为准（本期未核验）。<span class="src-inline">来源：<a href="https://www.un.org/zh/node/182171">https://www.un.org/zh/node/182171</a>；状态页 <a href="https://treaties.un.org/pages/ViewDetails.aspx?src=TREATY&amp;mtdsg_no=III-4&amp;chapter=3&amp;clang=_en">treaties.un.org III-4</a></span></p>

<h3>4.4 《联合国海洋法公约》与 BBNJ 协定</h3>

<p><b>条款摘编</b>：UNCLOS 1982-12-10 于牙买加蒙特哥贝开放签署，1994-11-16 依第 308 条生效；含 320 条与 9 个附件，确立领海、专属经济区（200 海里）、大陆架与公海制度；争端可提交国际海洋法法庭、国际法院或仲裁。<span class="lvl lvl-verified">已核验</span></p>
<p><b>解读</b>：海洋权益主张与争端解决程序启动属 K03 / K08 监测对象；BBNJ 协定（国家管辖范围以外区域海洋生物多样性养护与可持续利用）2023-06-19 通过，2025-09-19 生效条件满足，2026-01-17 生效，为基线期内新增机制。<span class="lvl lvl-verified">已核验</span></p>
<p><b>官方答问 / 配套</b>：UNCLOS 概览与全文；BBNJ 生效公告见 UN Treaty Collection 首页。<span class="src-inline">来源：<a href="https://www.un.org/depts/los/convention_agreements/convention_overview_convention.htm">https://www.un.org/depts/los/convention_agreements/convention_overview_convention.htm</a>；<a href="https://treaties.un.org/">https://treaties.un.org/</a></span></p>

<h3>4.5 《不扩散核武器条约》（NPT）</h3>

<p><b>条款摘编</b>：NPT 1968 年开放签署、1970 年生效；1995-05-11 依第 10 条第 2 款无限期延长；191 个缔约国（含五个核武器国家）。三大支柱：防止核扩散、推动核裁军、促进和平利用核能；IAEA 负责保障监督。<span class="lvl lvl-verified">已核验</span></p>
<p><b>解读</b>：NPT 审议大会每五年一次，是机制运行基线的年度锚；2026 年第十一次审议大会于 2026-04-27 至 05-22 在纽约举行，其结果文件与共识情况须逐条核对（本期未跟踪，待事件解读）。<span class="lvl lvl-verified">已核验</span></p>
<p><b>官方答问 / 配套</b>：UNODA 条约页与 2026 审议大会页。<span class="src-inline">来源：<a href="https://www.un.org/disarmament/wmd/nuclear/npt/">https://www.un.org/disarmament/wmd/nuclear/npt/</a></span></p>

<h3>4.6 《巴黎协定》</h3>

<p><b>条款摘编</b>：2015-12-12 在 COP21 由 195 个方通过；2016-11-04 生效；截至 2026-01-27 共 194 个缔约方。核心目标为将全球平均气温升幅控制在远低于 2°C 并努力限制在 1.5°C；建立 NDC（国家自主贡献）五年周期与全球盘点。<span class="lvl lvl-verified">已核验</span></p>
<p><b>解读</b>：气候外交与贸易、制裁工具交叉（如碳边境调节机制），属 K02 / K03 的交叉监测对象；缔约方批准状态以 UNFCCC 状态页与 UN Treaty Collection 为准。<span class="lvl lvl-partial">部分核验</span></p>
<p><b>官方答问 / 配套</b>：UNFCCC 巴黎协定页、批准状态页。<span class="src-inline">来源：<a href="https://unfccc.int/process-and-meetings/the-paris-agreement">https://unfccc.int/process-and-meetings/the-paris-agreement</a>；<a href="https://unfccc.int/process/the-paris-agreement/status-of-ratification">https://unfccc.int/process/the-paris-agreement/status-of-ratification</a></span></p>

<h3>4.7 《东盟宪章》（区域机制示例）</h3>

<p><b>条款摘编</b>：《东盟宪章》2008-12-15 生效，对在 10 个成员国间构成有法律约束力的协定；东盟现设政治安全、经济、社会文化三大共同体。东盟 1967-08-08 成立，东帝汶于 2025-10-26 加入，成员国增至 11 个。<span class="lvl lvl-verified">已核验</span></p>
<p><b>解读</b>：区域机制的法律化程度与成员口径需分开登记（成员数与宪章批准数口径不同）；本基线仅作区域机制示例，不展开区域内事件。<span class="lvl lvl-partial">部分核验</span></p>
<p><b>官方答问 / 配套</b>：东盟宪章页。<span class="src-inline">来源：<a href="https://asean.org/asean-charter/">https://asean.org/asean-charter/</a></span></p>

<h3>4.8 日内瓦四公约（1949）与《罗马规约》（1998）</h3>

<p><b>条款摘编</b>：日内瓦四公约 1949-08-12 通过，普遍批准（具体国数本期未核验）；共同第 1 条规定各缔约国承诺在一切情况下尊重并保证公约被尊重。《罗马规约》1998-07-17 通过、2002-07-01 生效，收录于《联合国条约汇编》第 2187 卷；缔约国数与管辖现状本期未核验。<span class="lvl lvl-partial">部分核验</span></p>
<p><b>解读</b>：人道法与国际刑事司法属 K07 / K08 的条款基础；因 ICC 与 ICJ 官网本期反爬，相关实时状态登记为未核验（U-03 / U-04），待人工原文回溯后回填。</p>
<p><b>官方答问 / 配套</b>：ICRC 日内瓦四公约出版物；ICC 官网。<span class="src-inline">来源：<a href="https://www.icrc.org/en/doc/assets/files/publications/icrc-002-0173.pdf">ICRC 日内瓦四公约</a>；<a href="https://www.icc-cpi.int/about/the-court">https://www.icc-cpi.int/about/the-court</a></span></p>

<h2 id="s5">五、影响对象矩阵</h2>

<p>矩阵按「机制 / 条款 × 受影响主体 × 影响方向」展开，逐格附条款依据与指标指针；本期为基线，影响量级待事件触发后回填。</p>

<div class="tblwrap"><table>
<thead><tr><th style="width:19%">机制 / 条款</th><th style="width:17%">受影响主体</th><th style="width:30%">影响方向</th><th style="width:34%">依据 / 指针</th></tr></thead>
<tbody>
<tr><td>外交关系级别（K01 / RL-01）</td><td>政策制定者</td><td>断交或降级 → 重算双边合作与人员往来假设</td><td>维也纳外交公约第 2 / 45 条；[G01]</td></tr>
<tr><td>制裁 / 出口管制（K02 / RL-02）</td><td>涉外合规团队</td><td>新增单边制裁 / 名单扩充 → 重算贸易、金融与供应链合规边界</td><td>OFAC 清单 / 欧盟限制措施；[G02]</td></tr>
<tr><td>条约签署 / 批准 / 退出（K03 / RL-03）</td><td>研究人员 / 合规团队</td><td>签署 ≠ 生效；保留条款影响权利义务</td><td>两维也纳公约、UNCLOS、NPT；[G03]</td></tr>
<tr><td>国际组织席位 / 投票（K04）</td><td>政策制定者</td><td>成员 / 观察员 / 对话伙伴权利差异</td><td>各组织章程；[G04]</td></tr>
<tr><td>使领馆变动（K05）</td><td>公民 / 企业</td><td>临时关闭 / 撤馆 → 领事服务与人员往来受阻</td><td>维也纳领事公约第 27 条；[G01]</td></tr>
<tr><td>峰会 / 联合声明（K06）</td><td>研究人员</td><td>仅作线索，不单独下结论</td><td>声明 ≠ 联合公报 ≠ 行动计划</td></tr>
<tr><td>冲突 / 停火（K07 / RL-04）</td><td>合规 / 安全团队</td><td>全面冲突或停火破裂 → 重算人员安全与运营连续性</td><td>并列多方口径，不采信单方；[G05]</td></tr>
<tr><td>国际司法 / 仲裁（K08 / RL-05）</td><td>法律合规团队</td><td>临时措施 / 实体裁决 → 重算法律风险</td><td>ICJ / ICC / ITLOS 官方文本；[G05]</td></tr>
</tbody>
</table></div>

<div class="decision-card">
  <div class="dc-head"><span class="dc-title">核心判断：机制框架已锁定，事件解读待触发</span><span class="suff need">信息充分度：中</span></div>
  <div class="dc-grid">
    <div><span class="k">结论：</span>以《联合国宪章》为顶层的联合国体系与高普遍性多边条约构成监测基线；事件触发解读与年度台账在此之上滚动。</div>
    <div><span class="k">证据强度：</span><span class="ev-strong">强</span>（官方原文 / 条约文本）</div>
    <div><span class="k">触发条件：</span>K01–K08 任一黄灯及以上；RL-01–RL-05 任一红线。</div>
    <div><span class="k">反向证据：</span>官方状态页与保留条款未核验（U-01 / U-07）；非英语原文缺口（U-02）。</div>
    <div><span class="k">信息充分度：</span>机制框架充分；实时状态与事件层面不足。</div>
    <div><span class="k">行动：</span>见第六节行动协议卡。</div>
  </div>
</div>

<h2 id="s6">六、合规应对建议（建议章）</h2>

<div class="note correct"><b>结论边界</b>：本章为「建议」，与事实分离；不构成外交、法律或安全建议；重大合规决策须咨询执业法律专业人士。原文有歧义处并列多解，不静默择一。</div>

<h3>6.1 建议清单</h3>

<ul class="tight">
<li><b>官方原文回溯 SOP</b>（建议）：条约状态一律以 UN Treaty Collection 状态页为准；声明与政策文件分列，入口页不等于条款页。</li>
<li><b>法律工具分列</b>（建议）：制裁、出口管制、投资限制逐条记录法律依据、适用对象、生效日与例外条款，不得合并登记。</li>
<li><b>关系级别与承认分列</b>（建议）：建交 / 代办级 / 大使级 / 断交逐条核对官方表述；使领馆变动影响公民服务时即升级复核（K05）。</li>
<li><b>条约三阶段分列</b>（建议）：签署、批准、生效各附日期；保留条款单列，不把签署当生效（K03 / RL-03）。</li>
<li><b>冲突多方口径</b>（建议）：并列当事方与第三方监测口径，不采信单方；停火、和平协议、终战宣言分开登记（K07）。</li>
</ul>

<h3>6.2 行动协议卡</h3>

<div class="action-card immediate">
  <div class="a-head"><span class="prio immediate">立即</span><span class="a-title">RL 红线触发</span></div>
  <div class="a-meta"><b>触发条件：</b>任一 RL-01–RL-05 红线触发。<b>动作：</b>24 小时内重算受影响结论并回写台账。<b>责任角色：</b>业务线负责人。<b>验证指标：</b>台账更新记录 + 已修正事实清单。</div>
</div>

<div class="action-card watch">
  <div class="a-head"><span class="prio watch">跟踪</span><span class="a-title">K01–K03 黄灯</span></div>
  <div class="a-meta"><b>触发条件：</b>外交关系表态、制裁名单扩充讨论、条约谈判启动。<b>动作：</b>48 小时内完成官方原文回溯，决定是否升级为事件解读。<b>责任角色：</b>监测岗。<b>验证指标：</b>原文 URL 与核验状态登记。</div>
</div>

<div class="action-card archive">
  <div class="a-head"><span class="prio archive">归档</span><span class="a-title">年度台账复核</span></div>
  <div class="a-meta"><b>触发条件：</b>年度复核节点。<b>动作：</b>刷新条约状态基线与政策框架，更新已修正事实清单并归档。<b>责任角色：</b>年度复盘。<b>验证指标：</b>台账版本与归档记录。</div>
</div>

<h2 id="s7">七、生效时间线</h2>

<div class="tblwrap"><table>
<thead><tr><th style="width:26%">政策 / 机制</th><th style="width:22%">关键节点</th><th style="width:16%">日期</th><th style="width:36%">依据</th></tr></thead>
<tbody>
<tr><td>《联合国宪章》</td><td>签署 / 生效</td><td>1945-06-26 / 1945-10-24</td><td>UN 宪章页</td></tr>
<tr><td>日内瓦四公约</td><td>通过</td><td>1949-08-12</td><td>ICRC</td></tr>
<tr><td>《维也纳外交关系公约》</td><td>通过 / 生效</td><td>1961-04-18 / 1964-04-24</td><td>UN 条约页</td></tr>
<tr><td>《维也纳领事关系公约》</td><td>通过 / 生效</td><td>1963-04-24 / 1967-03-19</td><td>UN 条约页</td></tr>
<tr><td>《不扩散核武器条约》</td><td>开放签署 / 生效 / 无限期延长</td><td>1968 / 1970 / 1995-05-11</td><td>UNODA</td></tr>
<tr><td>《联合国海洋法公约》</td><td>开放签署 / 生效</td><td>1982-12-10 / 1994-11-16</td><td>UN DOALOS</td></tr>
<tr><td>《东盟宪章》</td><td>生效</td><td>2008-12-15</td><td>ASEAN</td></tr>
<tr><td>《巴黎协定》</td><td>通过 / 生效</td><td>2015-12-12 / 2016-11-04</td><td>UNFCCC</td></tr>
<tr><td>BBNJ 协定</td><td>通过 / 条件满足 / 生效</td><td>2023-06-19 / 2025-09-19 / 2026-01-17</td><td>UN Treaty Collection</td></tr>
<tr><td>联合国可转让货物单证公约（阿克拉）</td><td>通过 / 开放签署</td><td>2025-12-15 / 2026-10-26</td><td>UN Treaty Collection</td></tr>
<tr><td>船舶司法出售国际效力公约（北京）</td><td>通过 / 生效</td><td>2022-12-07 / 2026-02-17</td><td>UN Treaty Collection</td></tr>
<tr><td>联合国打击网络犯罪公约</td><td>通过 / 开放签署</td><td>2024-12-24 / 待保管国通知</td><td>UN Treaty Collection</td></tr>
</tbody>
</table></div>

<h3>7.1 待生效与待细则清单</h3>

<ul class="tight">
<li><b>BBNJ 协定</b>：2026-01-17 生效后的机构安排与首批决定（未核验）。</li>
<li><b>NPT 2026 年审议大会</b>（2026-04-27 至 05-22，纽约）：结果文件与共识情况待跟踪。</li>
<li><b>联合国打击网络犯罪公约</b>：开放签署日期与签署安排待保管国通知。</li>
<li><b>巴黎协定全球盘点与 NDC 周期</b>：下一轮 NDC 提交与盘点结果待跟踪。</li>
</ul>

<h2 id="s8">八、数据治理与局限</h2>

<h3>8.1 来源分级</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:10%">层级</th><th style="width:22%">类型</th><th style="width:40%">使用规则</th><th style="width:28%">本基线处理</th></tr></thead>
<tbody>
<tr><td>T1</td><td>官方一手（政府 / 多边机构 / 官方发布）</td><td>唯一可直接采信层，标「已核验」</td><td>主要采信</td></tr>
<tr><td>T2</td><td>行业机构（研究 / 数据 / 咨询）</td><td>交叉验证方向，不替代官方</td><td>未引用</td></tr>
<tr><td>T3</td><td>挂牌门户（数据库 / 统计）</td><td>用于状态快照与线索</td><td>UN Treaty Collection / UN Digital Library 入口</td></tr>
<tr><td>T4</td><td>媒体转述</td><td>只用于发现线索，标「需核实原文」</td><td>本基线未直引</td></tr>
</tbody>
</table></div>

<h3>8.2 文本时效与版本治理</h3>

<ul class="tight">
<li><b>读数时点</b>：2026-11；条约与机制状态以官方页面为准，动态状态须回溯状态页。</li>
<li><b>版本治理</b>：本报告 v1.0（首期基线固定）；核验 / 收敛型运行不升级版本号，只标注「本期读数时点」。</li>
<li><b>基线属性</b>：本报告为后续事件解读与年度台账的对比锚；基线永不重跑，结构变更只影响后续新基线。</li>
</ul>

<h3>8.3 未核验清单（U-01–U-07）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:55%">未核验项</th><th style="width:36%">影响与处置</th></tr></thead>
<tbody>
<tr><td>U-01</td><td>UN Treaty Collection 各条约实时缔约方数与保留条款（状态页为动态页，本期未自动抓取）</td><td>条约状态只能给结构性结论；须人工核对状态页</td></tr>
<tr><td>U-02</td><td>非英语官方原文（中文 / 日文 / 韩文 / 阿文外交部一手文本）未覆盖</td><td>非英语声明须标注原文语言并附官方 URL</td></tr>
<tr><td>U-03</td><td>ICC《罗马规约》缔约国数与管辖现状（官网反爬）</td><td>待人工回溯 ICC 官方文本</td></tr>
<tr><td>U-04</td><td>ICJ 案件与判决执行现状（官网 Cloudflare 验证）</td><td>待人工回溯 ICJ 官方文本</td></tr>
<tr><td>U-05</td><td>区域组织（非盟 / 阿盟 / 欧盟 EEAS）官方页面本期未成功抓取</td><td>仅登记入口，未作事实引用</td></tr>
<tr><td>U-06</td><td>2026 年重大峰会 / 事件后续口径（事件触发解读尚未启动）</td><td>待事件触发后逐条解读</td></tr>
<tr><td>U-07</td><td>条约保留条款逐条核对未完成</td><td>保留条款影响权利义务口径</td></tr>
</tbody>
</table></div>

<h3>8.4 解读局限</h3>

<ul class="tight">
<li>本基线只处理官方文本与机制框架，不采集舆论反应；不做预测，不引用匿名消息。</li>
<li>机制框架的「影响量级」需事件触发后回填，本期矩阵只给方向与条款依据。</li>
<li>「已修正事实清单」首期为空；产生修正后逐条补记，防回退。</li>
</ul>

<h2 id="s9">九、参考来源清单</h2>

<div class="refs">
<h3>官方一手（P0 / P1）</h3>
<ol>
<li>联合国宪章 — <a href="https://www.un.org/en/about-us/un-charter">https://www.un.org/en/about-us/un-charter</a> [Source: 完整URL, 2026]</li>
<li>联合国宪章全文 — <a href="https://www.un.org/en/about-us/un-charter/full-text">https://www.un.org/en/about-us/un-charter/full-text</a> [Source: 完整URL, 2026]</li>
<li>维也纳外交关系公约（UN 条约页） — <a href="https://www.un.org/zh/documents/treaty/UNCITRAL-1961">https://www.un.org/zh/documents/treaty/UNCITRAL-1961</a> [Source: 完整URL, 2026]</li>
<li>维也纳领事关系公约（UN 条约页） — <a href="https://www.un.org/zh/node/182171">https://www.un.org/zh/node/182171</a> [Source: 完整URL, 2026]</li>
<li>UN Treaty Collection — <a href="https://treaties.un.org/">https://treaties.un.org/</a> [Source: 完整URL, 2026]</li>
<li>UN Treaty Collection 状态页（外交，III-3） — <a href="https://treaties.un.org/pages/ViewDetails.aspx?src=TREATY&amp;mtdsg_no=III-3&amp;chapter=3&amp;clang=_en">https://treaties.un.org/pages/ViewDetails.aspx?src=TREATY&amp;mtdsg_no=III-3&amp;chapter=3&amp;clang=_en</a> [Source: 完整URL, 2026]</li>
<li>UN Treaty Collection 状态页（领事，III-4） — <a href="https://treaties.un.org/pages/ViewDetails.aspx?src=TREATY&amp;mtdsg_no=III-4&amp;chapter=3&amp;clang=_en">https://treaties.un.org/pages/ViewDetails.aspx?src=TREATY&amp;mtdsg_no=III-4&amp;chapter=3&amp;clang=_en</a> [Source: 完整URL, 2026]</li>
<li>UNCLOS 概览 — <a href="https://www.un.org/depts/los/convention_agreements/convention_overview_convention.htm">https://www.un.org/depts/los/convention_agreements/convention_overview_convention.htm</a> [Source: 完整URL, 2026]</li>
<li>NPT（UNODA） — <a href="https://www.un.org/disarmament/wmd/nuclear/npt/">https://www.un.org/disarmament/wmd/nuclear/npt/</a> [Source: 完整URL, 2026]</li>
<li>巴黎协定（UNFCCC） — <a href="https://unfccc.int/process-and-meetings/the-paris-agreement">https://unfccc.int/process-and-meetings/the-paris-agreement</a> [Source: 完整URL, 2026]</li>
<li>巴黎协定批准状态 — <a href="https://unfccc.int/process/the-paris-agreement/status-of-ratification">https://unfccc.int/process/the-paris-agreement/status-of-ratification</a> [Source: 完整URL, 2026]</li>
<li>东盟宪章 — <a href="https://asean.org/asean-charter/">https://asean.org/asean-charter/</a> [Source: 完整URL, 2026]</li>
<li>中国外交部 — <a href="https://www.mfa.gov.cn/eng/">https://www.mfa.gov.cn/eng/</a> [Source: 完整URL, 2026]</li>
<li>美国 OFAC — <a href="https://ofac.treasury.gov/">https://ofac.treasury.gov/</a> [Source: 完整URL, 2026]</li>
<li>UN Digital Library — <a href="https://digitallibrary.un.org/">https://digitallibrary.un.org/</a> [Source: 完整URL, 2026]</li>
<li>UN News — <a href="https://news.un.org/en/">https://news.un.org/en/</a> [Source: 完整URL, 2026]</</ol>
<h3>国际组织 / 机制入口（P1 / P2）</h3>
<ol start="17">
<li>国际法院 ICJ — <a href="https://www.icj-cij.org/en">https://www.icj-cij.org/en</a> [Source: 完整URL, 2026]</li>
<li>国际刑事法院 ICC — <a href="https://www.icc-cpi.int/about/the-court">https://www.icc-cpi.int/about/the-court</a> [Source: 完整URL, 2026]</li>
<li>国际海洋法法庭 ITLOS — <a href="https://www.itlos.org/">https://www.itlos.org/</a> [Source: 完整URL, 2026]</li>
<li>WTO 法律文本 — <a href="https://www.wto.org/english/docs_e/legal_e/legal_e.htm">https://www.wto.org/english/docs_e/legal_e/legal_e.htm</a> [Source: 完整URL, 2026]</li>
<li>ICRC — <a href="https://www.icrc.org/">https://www.icrc.org/</a> [Source: 完整URL, 2026]</li>
<li>欧盟 EEAS — <a href="https://www.eeas.europa.eu/">https://www.eeas.europa.eu/</a> [Source: 完整URL, 2026]</li>
<li>美国国务院 — <a href="https://www.state.gov/">https://www.state.gov/</a> [Source: 完整URL, 2026]</li>
<li>英国 FCDO — <a href="https://www.gov.uk/government/organisations/foreign-commonwealth-and-development-office">https://www.gov.uk/government/organisations/foreign-commonwealth-and-development-office</a> [Source: 完整URL, 2026]</li>
<li>日本外务省 — <a href="https://www.mofa.go.jp/">https://www.mofa.go.jp/</a> [Source: 完整URL, 2026]</li>
<li>韩国外交部 — <a href="https://www.mofa.go.kr/eng/index.do">https://www.mofa.go.kr/eng/index.do</a> [Source: 完整URL, 2026]</li>
<li>非盟组织法 — <a href="https://au.int/en/constitutive-act">https://au.int/en/constitutive-act</a> [Source: 完整URL, 2026]</li>
<li>阿盟 — <a href="https://www.leagueofarabstates.net/">https://www.leagueofarabstates.net/</a> [Source: 完整URL, 2026]</li>
</ol>
</div>

<div class="disc">
<strong>结论边界与版本治理</strong>：本报告只给框架性说明与可核验信息，不构成外交、法律或安全建议，不预测他国政策意图，不引用匿名消息。报告版本 v1.0（首期基线固定）；核验 / 收敛型运行不升级版本号，只标注「本期读数时点」。信号阈值与红线为「预校准（ex-ante）」，首次中期回测 2027-06。数据截止 2026-11；来源分级与未核验清单见第八节。
</div>

<footer>全球 · 国际关系与外交 · 首期基线报告（2026-11）｜v1.0｜内容层：content/international/international-relations/reports/2026-11_baseline_report.html</footer>
