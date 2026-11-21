# 迪拜长期居留签证（黄金签证 / 绿卡签证）· 首期基线报告（2026-11）

### 九节固化锚 · 政策法规解读型 · 预校准（ex-ante）

<div class="delta-strip">
  <div class="d add"><div class="n">全量</div><div class="l">本期新增（基线首期 = 全部基线项，11 条通道）</div></div>
  <div class="d fix"><div class="n">0 条</div><div class="l">修正（已修正事实清单见第八节）</div></div>
  <div class="d same"><div class="n">0 条</div><div class="l">无变化（无上期报告）</div></div>
  <div class="d hyp"><div class="n">0/5</div><div class="l">假设核验进度（已登记 5 项未核验清单）</div></div>
</div>

<p class="small muted">基线首期：本期新增 = 全部基线项；「已修正事实清单」为空，产生修正后逐条补记。本报告为后续月度监测与事件解读的<strong>滚动基线</strong>（对比锚），基线本身永不重跑。</p>

<h2 id="s1">一、执行摘要</h2>

<div class="card leadbox">
<h3>核心判断</h3>
<ol class="tight">
<li><b>框架基线</b>：迪拜（UAE）长期居留以「黄金签证」（5 / 10 年）与「绿卡签证」（5 年）为两条主线，均以<b>自担保、免境内担保人</b>为核心特征；蓝色居留（10 年，环保与可持续发展）为第三类。<span class="lvl lvl-verified">已核验</span> [G01–G08][N01–N03]</li>
<li><b>门槛分化</b>：黄金房地产投资门槛 AED 2,000,000；黄金专业人士月薪 AED 30,000；绿卡技术工月薪 AED 15,000、自雇前两年年收入 AED 360,000；企业家年营收 AED 1,000,000。<span class="lvl lvl-verified">已核验</span> [G02][G03][G05][N01][N02]</li>
<li><b>家庭与续期</b>：黄金可担保配偶、子女（不限年龄）与父母，并担保家政工；绿卡可担保配偶、子女；两者均 5 / 10 年可续期。<span class="lvl lvl-verified">已核验</span> [G01–G08][N01–N03]</li>
<li><b>永久居留口径</b>：UAE 联邦制度中<b>无美国式「永久居留（PR）」类别</b>；黄金 / 绿卡 / 蓝色均为可续期长期居留许可，「绿卡」一词易被误读为永久居留，须严格区分。<span class="lvl lvl-verified">已核验</span> [S-001][S-002][S-003]</li>
<li><b>口径冲突</b>：u.ae 黄金签证页（2026-07-28 版）称房地产投资、企业家为 5 年；ICP 黄金居留指南称两者均 10 年，已并列呈现并列入未消号项。<span class="lvl lvl-partial">部分核验</span> [U-01]</li>
<li><b>监测节拍</b>：基线 + 月度主更新 + 事件触发解读；K01–K08 信号阈值与 RL-01–RL-05 红线为 ex-ante 预校准，首次中期回测 2027-06。<span class="lvl lvl-verified">已核验</span> [K01][RL-01]</li>
</ol>
<p><b>一句话定位</b>：以官方原文为唯一采信层，基线锁定「黄金 / 绿卡」类别地图与门槛口径，月度监测在基线之上滚动。</p>
<p><b>场景切片</b>：主场景「赴迪拜长期居留 / 投资决策」；次场景「签证研究 / 比较」。</p>
<p class="small muted">来源与时点：数据截止 2026-11；分级见第八节、URL 见第九节。</p>
</div>

<div class="preline">阈值与信号规则为「预校准（ex-ante）」；首次中期回测 2027-06。</div>

<h2 id="s2">二、政策台账与监测机制</h2>

<h3>2.1 台账结构（字段定义）</h3>

<p>台账为活值登记载体（<code>data/processed/international/immigration/dubai/dubai_visa_ledger.md</code>），来源登记为 <code>source_registry.json</code>。字段如下：</p>

<div class="tblwrap"><table>
<thead><tr><th style="width:16%">字段</th><th style="width:44%">定义</th><th style="width:40%">口径 / 示例</th></tr></thead>
<tbody>
<tr><td>通道编号</td><td>G01–G08（黄金）/ N01–N03（绿卡）</td><td>一一对应，不混用</td></tr>
<tr><td>通道</td><td>英文原名 + 中文译名</td><td>Golden Residence / Green Residence</td></tr>
<tr><td>类别</td><td>投资者 / 企业家 / 科学家·专家 / 杰出人才 / 学生 / 人道主义 / 前线 / 技术工人 / 自雇</td><td>按官方定义归类</td></tr>
<tr><td>门槛</td><td>数值 + 币种 + 年 / 月口径 + 适用年份</td><td>AED 2,000,000；AED 30,000/月；AED 360,000/年</td></tr>
<tr><td>有效期</td><td>许可有效期</td><td>5 年 / 10 年</td></tr>
<tr><td>续期 / 境外</td><td>续期条件 + 境外停留上限</td><td>条件 + 月</td></tr>
<tr><td>是否更新</td><td>是 / 否 + 更新时间</td><td>核验型运行不升级版本号</td></tr>
</tbody>
</table></div>

<h3>2.2 监测节拍与触发器</h3>

<ul class="tight">
<li><b>主节拍（月度）</b>：逐类检测类别新增 / 关闭 / 改名、投资门槛、薪资门槛、职业级别、企业家营收门槛、境外停留 / 续期 / 宽限期、申请材料 / 认证 / 费用、官方统计更新；仅变更项展开解读。</li>
<li><b>事件触发解读</b>：单一重大政策变更（如门槛大幅上调、类别关闭）另出 <code>YYYY-MM-DD-&lt;slug&gt;</code> 解读件。</li>
<li><b>先行信号标准矩阵</b>：① 官方公报 / 法规数据库；② 移民局官方页（ICP / GDRFA）；③ 地方执行口径（DLD / MOHRE）；④ 官方统计与处理时长；⑤ 英文媒体（只作线索）。</li>
<li><b>失真信号清单</b>：匿名消息、单一媒体爆料、把政策公布当生效、把拟调整当已生效、把中介口径当官方门槛。</li>
</ul>

<h3>2.3 官方发布渠道清单（P0–P5）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:8%">优先级</th><th style="width:22%">渠道</th><th style="width:34%">官方 URL</th><th style="width:20%">更新机制</th><th style="width:16%">本期核验</th></tr></thead>
<tbody>
<tr><td>P0</td><td>UAE 联邦政府门户 u.ae</td><td><a href="https://u.ae/en/information-and-services/visa-and-emirates-id/Types-of-visas/golden-visa">u.ae golden visa</a></td><td>签证页 / 类别页</td><td>已核验</td></tr>
<tr><td>P0</td><td>联邦身份与公民局 ICP</td><td><a href="https://icp.gov.ae/en/services/uae-golden-residency/">ICP Golden Residency Guide</a></td><td>类别 / 门槛页</td><td>已核验</td></tr>
<tr><td>P0</td><td>联邦身份与公民局 ICP</td><td><a href="https://icp.gov.ae/en/services/uae-green-residency/">ICP Green Residence Guide</a></td><td>类别 / 门槛页</td><td>已核验</td></tr>
<tr><td>P0</td><td>GDRFA Dubai</td><td><a href="https://www.gdrfad.gov.ae/">gdrfad.gov.ae</a></td><td>服务入口 / 预约</td><td>已核验</td></tr>
<tr><td>P1</td><td>UAE 通讯社 WAM</td><td><a href="https://wam.ae/en/details/1395303040263">WAM 执行条例公告</a></td><td>政策公告</td><td>未核验（抓取失败）</td></tr>
<tr><td>P2</td><td>联邦法规库</td><td><a href="https://icp.gov.ae/en/about-icp/laws-and-legislation/">uaelegislation 入口</a></td><td>法规原文</td><td>已核验（入口）</td></tr>
<tr><td>P3</td><td>英文媒体（Arab News 等）</td><td><a href="https://www.arabnews.com/node/2066256/business-economy">Arab News 新规转述</a></td><td>只作线索</td><td>需核实原文</td></tr>
</tbody>
</table></div>

<div class="note">渠道分级按 business-config 第四节：P0 官方页为唯一可直接采信层；P1 官方公告与法规原文；P2 官方统计与清单；P3 英文媒体（只作线索）；P4 其他英文行业机构；P5 最终以 P0 裁决，冲突并列。</div>

<h3>2.4 信号规则阈值（K01–K08，ex-ante 预校准）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:7%">编号</th><th style="width:20%">监测对象</th><th style="width:7%">等级</th><th style="width:14%">绿灯</th><th style="width:14%">黄灯</th><th style="width:19%">预警红线</th><th style="width:13%">硬红线</th><th style="width:6%">基线状态</th></tr></thead>
<tbody>
<tr><td>K01</td><td>类别新增 / 关闭 / 改名</td><td>一级</td><td>无变更</td><td>拟调整讨论</td><td>正式公布</td><td>生效</td><td>未触发</td></tr>
<tr><td>K02</td><td>房产投资门槛 / 贷款·期房口径</td><td>一级</td><td>无调整</td><td>拟调整</td><td>公布新标准</td><td>生效</td><td>未触发</td></tr>
<tr><td>K03</td><td>薪资门槛（AED 30,000 / 15,000）</td><td>一级</td><td>无调整</td><td>拟调整</td><td>公布新标准</td><td>生效</td><td>未触发</td></tr>
<tr><td>K04</td><td>职业级别分类（MOHRE 1–3 级）</td><td>二级</td><td>无变更</td><td>审查启动</td><td>公布变更</td><td>生效</td><td>未触发</td></tr>
<tr><td>K05</td><td>企业家营收 / 出售价值门槛</td><td>二级</td><td>无变更</td><td>讨论</td><td>公布</td><td>生效</td><td>未触发</td></tr>
<tr><td>K06</td><td>境外停留 / 续期 / 宽限期</td><td>一级</td><td>无变更</td><td>讨论</td><td>公布</td><td>生效</td><td>未触发</td></tr>
<tr><td>K07</td><td>申请材料 / 认证 / 费用</td><td>二级</td><td>无变更</td><td>拟调整</td><td>公布</td><td>生效</td><td>未触发</td></tr>
<tr><td>K08</td><td>官方统计年度更新</td><td>三级</td><td>无</td><td>发布</td><td>数据更新</td><td>—</td><td>未触发</td></tr>
</tbody>
</table></div>

<h3>2.5 结构红线登记簿（RL-01–RL-05）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:16%">监测对象</th><th style="width:33%">硬阈值</th><th style="width:28%">触发后动作</th><th style="width:14%">基线状态</th></tr></thead>
<tbody>
<tr><td>RL-01</td><td>主要类别</td><td>黄金 / 绿卡主要类别关闭或暂停</td><td>重算迪拜长期居留路径优先级</td><td>未触发</td></tr>
<tr><td>RL-02</td><td>自担保资格</td><td>自担保资格收紧（如改为需担保）</td><td>重算长期居留假设</td><td>未触发</td></tr>
<tr><td>RL-03</td><td>投资门槛</td><td>单次上调 &gt;30%</td><td>重算投资门槛与资格</td><td>未触发</td></tr>
<tr><td>RL-04</td><td>处理时长 / 积压</td><td>积压超阈值</td><td>重算时间线</td><td>未触发</td></tr>
<tr><td>RL-05</td><td>口径冲突</td><td>u.ae 与 ICP 年限口径冲突未消号</td><td>并列呈现并升级复核</td><td>未消号（U-01）</td></tr>
</tbody>
</table></div>

<h3>2.6 政策框架复核清单（P01–P05）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:24%">政策项</th><th style="width:43%">官方入口</th><th style="width:24%">复核周期</th></tr></thead>
<tbody>
<tr><td>P01</td><td>黄金居留类别与门槛</td><td>ICP Golden Residency Guide</td><td>事件触发 + 月度</td></tr>
<tr><td>P02</td><td>绿卡类别与门槛</td><td>ICP Green Residence Guide</td><td>事件触发 + 月度</td></tr>
<tr><td>P03</td><td>联邦入境与居留法令及执行条例</td><td>uaelegislation / ICP Laws</td><td>事件触发</td></tr>
<tr><td>P04</td><td>迪拜申请与材料口径（GDRFA）</td><td>gdrfad.gov.ae</td><td>事件触发 + 月度</td></tr>
<tr><td>P05</td><td>房产投资认定（DLD / Oqood）</td><td>dubailand.gov.ae</td><td>事件触发</td></tr>
</tbody>
</table></div>

<p class="small muted">规则：未取得官方原文的标「未核验」；入口页 ≠ 条款页；任一变更 → 立即重算受影响结论。</p>

<h2 id="s3">三、迪拜长期居留框架总览</h2>

<h3>3.1 层级地图</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:16%">层级</th><th style="width:30%">代表通道</th><th style="width:24%">效力</th><th style="width:30%">监测要点</th></tr></thead>
<tbody>
<tr><td>L1 黄金居留（10 年为主）</td><td>G01 公共投资、G02 房地产、G03 企业家、G05 科学家·专家、G07 学生、G08 杰出人才、G06 人道主义、G04 前线</td><td>长期居留，自动续期</td><td>类别有效期、投资 / 薪资门槛、推荐主体</td></tr>
<tr><td>L2 绿卡居留（5 年）</td><td>N01 技术工人、N02 自雇、N03 投资者·合伙人</td><td>自担保居留，可续期</td><td>职业级别、薪资 / 年收入门槛、许可类型</td></tr>
<tr><td>L3 蓝色居留（10 年）</td><td>环保与可持续发展领域杰出贡献者</td><td>长期居留</td><td>贡献认定、推荐主体</td></tr>
<tr><td>L4 普通居留（雇主担保）</td><td>工作签证、家属居留、退休居留</td><td>有条件居留</td><td>担保义务、合同、居住年限</td></tr>
</tbody>
</table></div>

<h3>3.2 类别对比矩阵</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">通道</th><th style="width:22%">类别</th><th style="width:26%">门槛（AED）</th><th style="width:16%">有效期</th><th style="width:17%">担保</th><th style="width:10%">核验</th></tr></thead>
<tbody>
<tr><td>G01</td><td>公共投资投资者</td><td>2,000,000 资本 / 250,000 年税</td><td>10 年</td><td>自担保</td><td>已核验</td></tr>
<tr><td>G02</td><td>房地产投资者</td><td>2,000,000 房产总价值</td><td>5 / 10 年（冲突）</td><td>自担保</td><td>部分核验</td></tr>
<tr><td>G03</td><td>企业家</td><td>1,000,000 年营收 / 7,000,000 出售价值</td><td>5 / 10 年（冲突）</td><td>自担保</td><td>部分核验</td></tr>
<tr><td>G05</td><td>科学家·专家</td><td>30,000/月</td><td>10 年</td><td>自担保</td><td>已核验</td></tr>
<tr><td>G07</td><td>优秀学生</td><td>95% / GPA 3.5 / 3.8</td><td>10 年</td><td>自担保</td><td>已核验</td></tr>
<tr><td>G08</td><td>杰出人才</td><td>奖项 / 推荐 / 5 年经验</td><td>10 年</td><td>自担保</td><td>已核验</td></tr>
<tr><td>N01</td><td>绿卡技术工人</td><td>15,000/月</td><td>5 年</td><td>自担保</td><td>已核验</td></tr>
<tr><td>N02</td><td>绿卡自雇</td><td>360,000/年（前两年）</td><td>5 年</td><td>自担保</td><td>已核验</td></tr>
<tr><td>N03</td><td>绿卡投资者·合伙人</td><td>未明列</td><td>5 年</td><td>自担保</td><td>已核验</td></tr>
</tbody>
</table></div>

<h3>3.3 框架演变脉络</h3>

<div class="timeline">
  <div class="tl-item"><div class="tl-date">2019</div><div class="tl-body"><div class="t">黄金居留计划启动</div><div class="d">UAE 启动黄金居留（Golden Residency），面向投资者、企业家、杰出人才与优秀学生，5 / 10 年长期居留。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2021-11</div><div class="tl-body"><div class="t">ICP 公布黄金居留服务</div><div class="d">ICP 官网公布黄金居留服务，明确 5–10 年长期居留、免担保人、自动续期。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2022-04</div><div class="tl-body"><div class="t">内阁批准执行条例</div><div class="d">UAE 内阁批准《外国人入境与居留联邦法令-法律》执行条例，修订黄金居留资格并新增绿卡（技术工人 / 自雇）等类别；房地产投资者门槛 AED 2,000,000。<span class="lvl lvl-partial">部分核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2022 起</div><div class="tl-body"><div class="t">绿卡（Green Residence）落地</div><div class="d">ICP 绿卡指南明确 5 年自担保居留，面向技术工人、自由职业者·自雇、投资者·合伙人。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2026-09</div><div class="tl-body green"><div class="t">ICP 指南更新</div><div class="d">ICP 黄金 / 绿卡指南更新（页面标注 2026-09-12），门槛与类别口径以该版为准。<span class="lvl lvl-verified">已核验</span></div></div></div>
</div>

<h3>3.4 术语口径区分（不得混用）</h3>

<div class="term"><b>黄金签证 ≠ 绿卡签证 ≠ 蓝色居留 ≠ 永久居留 ≠ 公民</b>：五者法律地位、有效期与权利不同，逐条分列。<br>
<b>长期居留 ≠ 永居</b>：UAE 联邦无美国式「永久居留（PR）」类别；黄金 / 绿卡 / 蓝色均为可续期长期居留许可，不得表述为「永居 / PR」。<br>
<b>自担保 ≠ 雇主担保</b>：黄金 / 绿卡核心特征是无境内担保人；普通工签需雇主担保。<br>
<b>门槛口径</b>：AED 2,000,000（房产总价值 / 净资产）、AED 30,000/月、AED 15,000/月、AED 360,000/年须标注币种与年 / 月口径。<br>
<b>通道生效 ≠ 政策公布 ≠ 实施细则</b>：公布、生效、配套细则三阶段分列，附各自日期。</div>

<h2 id="s4">四、重点政策逐条解读</h2>

<h3>4.1 黄金签证 · 投资者（G01 / G02）</h3>

<p><b>条款摘编</b>：公共投资投资者须在投资基金或国家银行有 ≥ AED 2,000,000 财务存款；或设立公司资本 ≥ AED 2,000,000；或合伙份额 ≥ AED 2,000,000；或所属企业年缴联邦税 ≥ AED 250,000；投资资本须自有、非贷款；本人及家人须有健康保险。房地产投资者须持有 UAE 房产总价值 ≥ AED 2,000,000（可经获批本地银行贷款），或期房 ≥ AED 2,000,000（获批本地房企）。<span class="lvl lvl-verified">已核验</span> [G01][G02]</p>
<p><b>解读</b>：投资类是迪拜置业的黄金通道；门槛口径为「房产总价值」，与「净资产（扣除按揭）」不同，正文须标注。房地产投资者有效期存在<u>官方口径冲突</u>：u.ae 页（2026-07-28）写 5 年，ICP 指南写 10 年，已并列。<span class="lvl lvl-partial">部分核验</span> [U-01]</p>
<p><b>缺口</b>：房地产「净资产认定」「夫妻份额合并」「期房 Oqood 计入」等迪拜本地执行细则未找到英文权威页（U-05）。</p>

<h3>4.2 黄金签证 · 企业家（G03）</h3>

<p><b>条款摘编</b>：注册于 UAE 的 SME（批准领域）年营收 ≥ AED 1,000,000；或获认可孵化器 / 经济部 / ICP / 地方当局对创业计划的批准；或曾创办并出售企业总价值 ≥ AED 7,000,000；本人及家人健康保险。<span class="lvl lvl-verified">已核验</span> [G03]</p>
<p><b>解读</b>：企业家通道兼顾「在营 SME」与「退出创业者」两类；有效期同样存在 u.ae（5 年）与 ICP（10 年）口径冲突。<span class="lvl lvl-partial">部分核验</span> [U-01]</p>

<h3>4.3 黄金签证 · 科学家与专家（G05）</h3>

<p><b>条款摘编</b>：由 Emirates Scientists Council 推荐（科学家·研究人员）；或文化部·青年部 / 工业与先进技术部 / 卫生与预防部 / 教育部推荐；高级职业级别（level 1 董事长·CEO、level 2 专家）；有效工作许可；≥本科；月薪 ≥ AED 30,000；健康保险。<span class="lvl lvl-verified">已核验</span> [G05]</p>
<p><b>解读</b>：专业人才通道与 MOHRE 职业分类（ISCO）挂钩；薪资门槛 AED 30,000/月为本类核心量化口径。</p>

<h3>4.4 黄金签证 · 杰出人才与学生（G07 / G08）</h3>

<p><b>条款摘编</b>：杰出人才覆盖文化·艺术（国际级奖项 / 提名 / 认可，或 5 年专业经验等）、创新者·发明家、运动员、数字技术人才及其他经政府认定者。优秀学生：UAE 高中 ≥ 95%；国际 top100 大学学士 GPA ≥ 3.5 且毕业 ≤ 2 年；UAE A 类大学 GPA ≥ 3.5 / B 类 ≥ 3.8 且毕业 ≤ 2 年；学历认证。<span class="lvl lvl-verified">已核验</span> [G07][G08]</p>
<p><b>解读</b>：人才类以「推荐 / 奖项 / 成就」而非薪资为门槛；学生类以「排名 + GPA + 毕业年限」为门槛，两类均须标注学历认证要求。</p>

<h3>4.5 黄金签证 · 人道主义与前线（G04 / G06）</h3>

<p><b>条款摘编</b>：第一线防卫人员 10 年；人道主义先驱含国际组织 / 区域组织成员或雇员、公益组织成员、人道主义奖项、杰出志愿者、人道主义工作资助者，10 年。<span class="lvl lvl-verified">已核验</span> [G04][G06]</p>

<h3>4.6 绿卡 · 技术工人 / 自雇 / 投资者（N01–N03）</h3>

<p><b>条款摘编</b>：技术工人须有 UAE 有效雇佣合同、MOHRE 职业分类 1–3 级、≥本科、月薪 ≥ AED 15,000；自由职业者·自雇须有 MOHRE 自由职业 / 自雇许可、≥本科 / 专门文凭、稳定年收入或财务偿付能力证明、前两年自雇年收入 ≥ AED 360,000；投资者·合伙人须有投资 / 入股 UAE 企业证明及相关牌照与批准。<span class="lvl lvl-verified">已核验</span> [N01][N02][N03]</p>
<p><b>解读</b>：绿卡与黄金的核心差异是<b>有效期 5 年</b>与<b>门槛更低</b>（技术工 15,000/月 vs 黄金专家 30,000/月）；绿卡自雇通道的「前两年年收入 360,000」是审计口径，须标注。</p>

<h3>4.7 法律依据与执行条例</h3>

<p><b>法律依据</b>：联邦《外国人入境与居留法令-法律》及其执行条例（2022-04 内阁批准执行条例，WAM 公告）；ICP 依联邦法令主管黄金 / 绿卡 / 蓝色居留。<span class="lvl lvl-partial">部分核验</span> [U-02]</p>
<p><b>解读</b>：黄金 / 绿卡的资格与门槛由执行条例与 ICP 指南共同界定；具体法令编号与条文尚待官方英文法规库复核（U-02），本基线不作编号直引。</p>

<h2 id="s5">五、影响对象矩阵</h2>

<p>矩阵按「通道 / 条款 × 受影响主体 × 影响方向」展开，逐格附条款依据与指标指针；本期为基线，影响量级待月度监测回填。</p>

<div class="tblwrap"><table>
<thead><tr><th style="width:19%">通道 / 条款</th><th style="width:17%">受影响主体</th><th style="width:30%">影响方向</th><th style="width:34%">依据 / 指针</th></tr></thead>
<tbody>
<tr><td>房产投资门槛（K02 / RL-03）</td><td>置业投资者</td><td>门槛调整 → 重算投资门槛与资格</td><td>黄金房地产 G02；ICP / u.ae</td></tr>
<tr><td>薪资门槛（K03）</td><td>技术 / 专业人才</td><td>门槛上调 → 重算资格</td><td>黄金专家 G05（AED 30,000）、绿卡 N01（AED 15,000）</td></tr>
<tr><td>自雇收入门槛（K03）</td><td>自由职业者 / 自雇</td><td>收入门槛 → 改变可申请性</td><td>绿卡 N02（AED 360,000/年）</td></tr>
<tr><td>企业家营收门槛（K05）</td><td>创业者 / SME 主</td><td>营收 / 出售价值 → 改变通道</td><td>黄金企业家 G03</td></tr>
<tr><td>职业级别分类（K04）</td><td>level 1–3 职业者</td><td>分类调整 → 改变绿卡资格</td><td>MOHRE 分类；绿卡 N01</td></tr>
<tr><td>自担保资格（RL-02）</td><td>全部长期居留申请人</td><td>收紧 → 重算定居路径</td><td>黄金 / 绿卡通用权益</td></tr>
<tr><td>口径冲突（RL-05）</td><td>房地产 / 企业家申请人</td><td>年限不确定 → 需复核</td><td>u.ae vs ICP；[U-01]</td></tr>
</tbody>
</table></div>

<div class="decision-card">
  <div class="dc-head"><span class="dc-title">核心判断：黄金 / 绿卡类别地图已锁定，门槛口径以 ICP 指南为准并并列 u.ae 冲突</span><span class="suff need">信息充分度：中</span></div>
  <div class="dc-grid">
    <div><span class="k">结论：</span>迪拜长期居留以黄金（5 / 10 年）与绿卡（5 年）两条主线承载，均自担保；门槛分化清晰，永久居留口径须纠正为「可续期长期居留」。</div>
    <div><span class="k">证据强度：</span><span class="ev-strong">强</span>（ICP / u.ae 官方页）</div>
    <div><span class="k">触发条件：</span>K01–K08 任一黄灯及以上；RL-01–RL-05 任一红线。</div>
    <div><span class="k">反向证据：</span>u.ae 与 ICP 对房地产 / 企业家年限口径冲突（U-01）；处理时长、境外停留上限、迪拜本地执行细则未核验（U-03–U-05）。</div>
    <div><span class="k">信息充分度：</span>类别与门槛充分；处理时长、费用与本地执行细则不足。</div>
    <div><span class="k">置信度：</span>0.7（Kent：中高）</div>
    <div><span class="k">行动：</span>见第六节行动协议卡。</div>
  </div>
</div>

<h2 id="s6">六、合规应对建议（建议章）</h2>

<div class="note correct"><b>结论边界</b>：本章为「建议」，与事实分离；不构成法律意见、不构成投资建议；重大合规决策须咨询执业移民法律专业人士。原文有歧义处并列多解，不静默择一。</div>

<h3>6.1 建议清单</h3>

<ul class="tight">
<li><b>官方原文回溯 SOP</b>（建议）：资格与门槛一律以 ICP / u.ae / GDRFA 官方页为准；入口页不等于条款页；拟调整 ≠ 已生效。</li>
<li><b>门槛口径分列</b>（建议）：AED 币种、年 / 月口径、净资产 / 总价值逐条标注；汇率换算只作参考，不作资格判断依据。</li>
<li><b>永久居留口径纠正</b>（建议）：对外沟通不得将黄金 / 绿卡表述为「永居 / PR」；UAE 长期居留为可续期许可，入籍依《联邦国籍与护照法》单独审批。</li>
<li><b>冲突口径复核</b>（建议）：房地产 / 企业家年限以 ICP 指南（10 年）与 u.ae（5 年）并列，申请前以 GDRFA 受理口径复核。</li>
<li><b>预留官方访问受限的复核通道</b>（建议）：对抓取失败 / 反爬页面（WAM 公告、GDRFA 服务卡）建立人工复核清单，避免以 snippet 直引。</li>
</ul>

<h3>6.2 行动协议卡</h3>

<div class="action-card immediate">
  <div class="a-head"><span class="prio immediate">立即行动</span><span class="a-title">RL-05 口径冲突消号</span></div>
  <div class="a-meta"><b>触发条件：</b>u.ae 与 ICP 年限口径冲突未消号。<b>阈值：</b>连续 2 期未对齐即升级。<b>责任角色：</b>业务线负责人。<b>时限：</b>24 小时内登记，1 个周期内复核。<b>验证指标：</b>台账 U-01 状态 + 已修正事实清单。</div>
</div>

<div class="action-card watch">
  <div class="a-head"><span class="prio watch">持续观察</span><span class="a-title">K02 / K03 门槛黄灯</span></div>
  <div class="a-meta"><b>触发条件：</b>房产投资门槛或薪资门槛公布新标准。<b>阈值：</b>K02 / K03 进入黄灯。<b>责任角色：</b>监测岗。<b>时限：</b>48 小时内。<b>验证指标：</b>原文 URL 与核验状态登记。</div>
</div>

<div class="action-card archive">
  <div class="a-head"><span class="prio archive">仅记录存档</span><span class="a-title">月度监测</span></div>
  <div class="a-meta"><b>触发条件：</b>每自然月固定窗口。<b>阈值：</b>每自然月 1 次。<b>责任角色：</b>月度监测。<b>时限：</b>月度窗口内。<b>验证指标：</b>月度报告与台账「是否更新」记录。</div>
</div>

<h2 id="s7">七、生效时间线</h2>

<div class="tblwrap"><table>
<thead><tr><th style="width:24%">政策 / 通道</th><th style="width:22%">关键节点</th><th style="width:16%">日期</th><th style="width:38%">依据</th></tr></thead>
<tbody>
<tr><td>黄金居留计划</td><td>启动</td><td>2019</td><td>ICP / u.ae</td></tr>
<tr><td>ICP 黄金居留服务</td><td>公布 5–10 年免担保自动续期</td><td>2021-11-22</td><td>ICP</td></tr>
<tr><td>入境与居留执行条例</td><td>内阁批准（待核编号）</td><td>2022-04</td><td>WAM（U-02）</td></tr>
<tr><td>绿卡（Green Residence）</td><td>落地，5 年自担保</td><td>2022 起</td><td>ICP</td></tr>
<tr><td>ICP 黄金 / 绿卡指南</td><td>更新（门槛与类别口径）</td><td>2026-09-12</td><td>ICP</td></tr>
</tbody>
</table></div>

<h3>7.1 待生效与待细则清单</h3>

<ul class="tight">
<li><b>房地产 / 企业家年限</b>：u.ae（5 年）与 ICP（10 年）口径待对齐（U-01）。</li>
<li><b>迪拜本地执行细则</b>：房产净资产认定、夫妻份额合并、无犯罪记录认证批次待英文官方页（U-05）。</li>
<li><b>处理时长与费用</b>：GDRFA / ICP 服务卡待复核（U-03）。</li>
<li><b>境外停留上限</b>：黄金签证「超过通常 6 个月」的具体月数待条款复核（U-04）。</li>
</ul>

<h2 id="s8">八、数据治理与局限</h2>

<h3>8.1 来源分级</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:10%">层级</th><th style="width:22%">类型</th><th style="width:40%">使用规则</th><th style="width:28%">本基线处理</th></tr></thead>
<tbody>
<tr><td>T1</td><td>官方一手（政府 / 移民局 / 法规数据库）</td><td>唯一可直接采信层，标「已核验」</td><td>主要采信（u.ae / ICP / GDRFA）</td></tr>
<tr><td>T2</td><td>行业机构（研究 / 数据 / 咨询）</td><td>交叉验证方向，不替代官方</td><td>未引用</td></tr>
<tr><td>T3</td><td>挂牌门户（数据库 / 统计）</td><td>用于状态快照与线索</td><td>未引用</td></tr>
<tr><td>T4</td><td>媒体转述</td><td>只用于发现线索，标「需核实原文」</td><td>Arab News 仅作线索（S-011）</td></tr>
</tbody>
</table></div>

<h3>8.2 文本时效与版本治理</h3>

<ul class="tight">
<li><b>读数时点</b>：2026-11；类别与门槛以官方页面为准，动态状态须回溯状态页。</li>
<li><b>版本治理</b>：本报告 v1.0（首期基线固定）；核验 / 收敛型运行不升级版本号，只标注「本期读数时点」。</li>
<li><b>基线属性</b>：本报告为后续月度监测与事件解读的对比锚；基线永不重跑，结构变更只影响后续新基线。</li>
</ul>

<div class="note"><b>高影响披露（impact_tier: high）</b>：关键判断附置信区间（以信息等级 + 核验状态表达，不合成单一数值）；读数时点 2026-11；免责——不构成法律意见、不构成投资建议、不承诺签证结果；非专业建议——重大合规决策须咨询持牌专业人士。</div>

<h3>8.3 未核验清单（U-01–U-05）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:55%">未核验项</th><th style="width:36%">影响与处置</th></tr></thead>
<tbody>
<tr><td>U-01</td><td>u.ae 黄金页称房地产 / 企业家 5 年；ICP 指南称 10 年</td><td>年限口径冲突，并列；待版本对齐复核</td></tr>
<tr><td>U-02</td><td>联邦入境与居留法令及执行条例的具体编号与条文（WAM 公告抓取失败）</td><td>法律依据名称待补全；以 ICP / u.ae 为准</td></tr>
<tr><td>U-03</td><td>黄金 / 绿卡处理时长与费用官方数值</td><td>待 GDRFA / ICP 服务卡复核</td></tr>
<tr><td>U-04</td><td>黄金签证境外停留上限的具体月数</td><td>待官方条款复核</td></tr>
<tr><td>U-05</td><td>迪拜本地执行细则（房产净资产认定、夫妻份额合并、无犯罪记录认证）</td><td>未找到英文权威来源，已剔除；待英文官方页复核</td></tr>
</tbody>
</table></div>

<h3>8.4 解读局限</h3>
<ul class="tight">
<li><b>研究内核</b>：周期定位——本基线为 2026-11 滚动基线锚点；传导量化——门槛调整对申请量的弹性与时滞以官方统计为准，本基线不作估计；政策入模——政策变量以类别状态 / 门槛 / 材料要求三因子入模，政策乘数待校准。</li>
<li>本基线只处理官方文本与通道框架，不采集舆论反应；不做预测，不引用匿名消息。</li>
<li>通道「影响量级」需月度监测回填，本期矩阵只给方向与条款依据。</li>
<li>「已修正事实清单」首期为空；产生修正后逐条补记，防回退。</li>
<li>部分官方页存在访问限制（WAM 公告抓取失败），相关条目标 snippet / 未核验并列入未核验清单。</li>
</ul>

<h2 id="s9">九、参考来源清单</h2>

<div class="refs">
<h3>官方一手（P0 / P1）</h3>
<ol>
<li>UAE 联邦政府门户 · Golden visa — <a href="https://u.ae/en/information-and-services/visa-and-emirates-id/Types-of-visas/golden-visa">https://u.ae/en/information-and-services/visa-and-emirates-id/Types-of-visas/golden-visa</a> [Source: 完整URL, 2026]</li>
<li>ICP · Golden Residency Guide — <a href="https://icp.gov.ae/en/services/uae-golden-residency/">https://icp.gov.ae/en/services/uae-golden-residency/</a> [Source: 完整URL, 2026]</li>
<li>ICP · Green Residence Guide — <a href="https://icp.gov.ae/en/services/uae-green-residency/">https://icp.gov.ae/en/services/uae-green-residency/</a> [Source: 完整URL, 2026]</li>
<li>ICP · What is Golden Residency? — <a href="https://icp.gov.ae/en/golden-residence/">https://icp.gov.ae/en/golden-residence/</a> [Source: 完整URL, 2026]</li>
<li>ICP · Services — <a href="https://icp.gov.ae/en/services/">https://icp.gov.ae/en/services/</a> [Source: 完整URL, 2026]</li>
<li>ICP · Laws and Legislation — <a href="https://icp.gov.ae/en/about-icp/laws-and-legislation/">https://icp.gov.ae/en/about-icp/laws-and-legislation/</a> [Source: 完整URL, 2026]</li>
<li>GDRFA Dubai · Services — <a href="https://www.gdrfad.gov.ae/">https://www.gdrfad.gov.ae/</a> [Source: 完整URL, 2026]</li>
<li>u.ae · Types of visas / Residence visas — <a href="https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas">https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas</a> [Source: 完整URL, 2026]</li>
<li>u.ae · Residence visa — <a href="https://u.ae/en/information-and-services/visa-and-emirates-id/Types-of-visas/Residence-visa">https://u.ae/en/information-and-services/visa-and-emirates-id/Types-of-visas/Residence-visa</a> [Source: 完整URL, 2026]</li>
<li>WAM · UAE Cabinet approves Executive Regulations of Federal Decree-Law on Entry and Residence of Foreigners — <a href="https://wam.ae/en/details/1395303040263">https://wam.ae/en/details/1395303040263</a> [Source: 完整URL, 2026]</li>
</ol>
<h3>媒体线索（P3，须标「需核实原文」）</h3>
<ol>
<li>Arab News · UAE rolls out new visa rules: All you need to know — <a href="https://www.arabnews.com/node/2066256/business-economy">https://www.arabnews.com/node/2066256/business-economy</a> [Source: 完整URL, 2022；仅作线索]</li>
</ol>
</div>

<div class="disc">
<strong>结论边界与版本治理</strong>：本报告只给框架性说明与可核验信息，不构成法律意见、不构成投资建议，不承诺签证结果，不引用匿名消息。报告版本 v1.0（首期基线固定）；核验 / 收敛型运行不升级版本号，只标注「本期读数时点」。信号阈值与红线为「预校准（ex-ante）」，首次中期回测 2027-06。数据截止 2026-11；来源分级与未核验清单见第八节。
</div>

<footer>迪拜长期居留签证（黄金签证 / 绿卡签证）· 首期基线报告（2026-11）｜v1.0｜内容层：content/international/immigration/dubai/reports/2026-11_baseline_report.html</footer>
