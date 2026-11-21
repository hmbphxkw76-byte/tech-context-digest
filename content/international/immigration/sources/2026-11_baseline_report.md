# 九国 · 高技能移民政策 · 首期基线报告（2026-11）

### 九节固化锚 · 政策法规解读型 · 预校准（ex-ante）

<div class="delta-strip">
  <div class="d add"><div class="n">全量</div><div class="l">本期新增（基线首期 = 全部基线项，46 条通道）</div></div>
  <div class="d fix"><div class="n">0 条</div><div class="l">修正（已修正事实清单见第八节）</div></div>
  <div class="d same"><div class="n">0 条</div><div class="l">无变化（无上期报告）</div></div>
  <div class="d hyp"><div class="n">0/12</div><div class="l">假设核验进度（已登记 12 项未核验清单）</div></div>
</div>

<p class="small muted">基线首期：本期新增 = 全部基线项；「已修正事实清单」为空，产生修正后逐条补记。本报告为后续月度监测与事件解读的<strong>滚动基线</strong>（对比锚），基线本身永不重跑。</p>

<h2 id="s1">一、执行摘要</h2>

<div class="card leadbox">
<h3>核心判断</h3>
<ol class="tight">
<li><b>框架基线</b>：九国通道可归四类——雇主担保 / 积分制 / 人才 / 留学生过渡；EB-1A、ONE Pass、澳大利亚 NIV 属人才类，Express Entry、SMC、189、德国机会卡属积分制类。<span class="lvl lvl-verified">已核验</span> [C01–C46]</li>
<li><b>薪资门槛分化</b>：雇主担保类普遍设最低薪资门槛，口径分年毛 / 月毛 / 小时且逐年调整（新西兰 NZD 35.00/小时、新加坡 EP S$6,000/月、荷兰 HSM €5,942/月）。<span class="lvl lvl-verified">已核验</span> [C04][C05][C31]</li>
<li><b>永居路径</b>：雇主担保类多经「工签 → 永居」两步（澳大利亚 186、爱尔兰 Stamp 4）；人才类多直接永居（EB-1A、ONE Pass）；积分制类直接 PR（Express Entry、SMC、189）。<span class="lvl lvl-verified">已核验</span> [C09][C15][C23]</li>
<li><b>STEM / AI 定向</b>：新加坡 5 年 EP、ONE Pass「AI and Tech」、加拿大 STEM 类别、美国 STEM OPT 构成定向；加拿大 STEM 类别未含软件开发人员大类，属结构性缺口。<span class="lvl lvl-partial">部分核验</span> [C16][C29][C32][C34]</li>
<li><b>监测节拍</b>：基线 + 月度主更新 + 事件触发解读；K01–K08 信号阈值与 RL-01–RL-05 红线为 ex-ante 预校准，首次中期回测 2027-06。<span class="lvl lvl-verified">已核验</span> [K01][RL-01]</li>
<li><b>数据缺口</b>：澳大利亚 immi、德国 make-it-in-germany、美国 travel.state.gov 访问受限，相关条目标 snippet（U-01–U-12）。<span class="lvl lvl-partial">部分核验</span> [U-01][U-02][U-04]</li>
<li><b>结论边界</b>：只给框架性说明与可核验信息，不构成法律意见，不承诺签证结果；政策以各国官方原文为准。<span class="lvl lvl-verified">已核验</span> [K07]</li>
</ol>
<p><b>一句话定位</b>：以官方原文为唯一采信层，基线锁定通道地图与门槛口径，月度监测在基线之上滚动。</p>
<p><b>场景切片</b>：主场景「就业决策」；次场景「政策制定」。</p>
<p class="small muted">来源与时点：数据截止 2026-11；分级见第八节、URL 见第九节。</p>
</div>

<div class="preline">阈值与信号规则为「预校准（ex-ante）」；首次中期回测 2027-06。</div>

<h2 id="s2">二、政策台账与监测机制</h2>

<h3>2.1 台账结构（字段定义）</h3>

<p>台账为活值登记载体（<code>data/processed/international/immigration/immigration_ledger.md</code>），来源登记为 <code>source_registry.json</code>。字段如下：</p>

<div class="tblwrap"><table>
<thead><tr><th style="width:16%">字段</th><th style="width:44%">定义</th><th style="width:40%">口径 / 示例</th></tr></thead>
<tbody>
<tr><td>通道编号</td><td>C01–C46，按国别分组</td><td>一一对应，不混用</td></tr>
<tr><td>国家</td><td>九国之一</td><td>新西兰 / 荷兰 / 澳大利亚 / 爱尔兰 / 加拿大 / 美国 / 新加坡 / 德国 / 法国</td></tr>
<tr><td>类别</td><td>雇主担保 / 积分制 / 人才类 / 留学生过渡 / 创业</td><td>按官方定义归类</td></tr>
<tr><td>薪资门槛</td><td>数值 + 币种 + 年 / 月 / 小时口径 + 适用年份</td><td>年毛 / 月毛 / 小时；本币</td></tr>
<tr><td>转永居</td><td>转永居 / 长期居留路径</td><td>居住年限 + 条件</td></tr>
<tr><td>是否更新</td><td>是 / 否 + 更新时间</td><td>核验型运行不升级版本号</td></tr>
</tbody>
</table></div>

<h3>2.2 监测节拍与触发器</h3>

<ul class="tight">
<li><b>主节拍（月度）</b>：逐国检测通道新增 / 关闭 / 改名、薪资门槛与配额、职业清单、积分 / 抽签规则、永居 / 居住年限、STEM / AI / IT 定向、官方统计更新；仅变更项展开解读。</li>
<li><b>事件触发解读</b>：单一重大政策变更（如通道关闭、门槛大幅上调）另出 <code>YYYY-MM-DD-&lt;slug&gt;</code> 解读件。</li>
<li><b>先行信号标准矩阵</b>：① 官方公报 / 法规数据库；② 移民局官方页；③ 职业清单与配额；④ 官方统计与处理时长；⑤ 欧盟框架（蓝卡）；⑥ 英文媒体（只作线索）。</li>
<li><b>失真信号清单</b>：匿名消息、单一媒体爆料、把政策公布当生效、把拟调整当已生效、把清单讨论当清单调整。</li>
</ul>

<h3>2.3 官方发布渠道清单（P0–P5）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:8%">优先级</th><th style="width:20%">渠道</th><th style="width:34%">官方 URL</th><th style="width:20%">更新机制</th><th style="width:18%">本期核验</th></tr></thead>
<tbody>
<tr><td>P0</td><td>新西兰移民局 INZ</td><td><a href="https://www.immigration.govt.nz/">https://www.immigration.govt.nz/</a></td><td>签证页 / 工资页</td><td>已核验</td></tr>
<tr><td>P0</td><td>荷兰 IND</td><td><a href="https://ind.nl/en">https://ind.nl/en</a></td><td>居留许可页 / 收入页</td><td>已核验</td></tr>
<tr><td>P0</td><td>澳大利亚 Home Affairs</td><td><a href="https://www.homeaffairs.gov.au/trav/work/skil">homeaffairs.gov.au/trav/work/skil</a></td><td>签证清单页</td><td>部分核验（immi 子域被拦截）</td></tr>
<tr><td>P0</td><td>爱尔兰 DETE</td><td><a href="https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/">enterprise.gov.ie/employment-permits</a></td><td>许可类型页 / MAR 页</td><td>已核验</td></tr>
<tr><td>P0</td><td>加拿大 IRCC</td><td><a href="https://www.canada.ca/en/immigration-refugees-citizenship.html">canada.ca</a></td><td>Express Entry / 项目页</td><td>已核验</td></tr>
<tr><td>P0</td><td>美国 USCIS</td><td><a href="https://www.uscis.gov/">https://www.uscis.gov/</a></td><td>签证页 / 政策手册</td><td>已核验</td></tr>
<tr><td>P0</td><td>美国国务院</td><td><a href="https://travel.state.gov/content/travel/en/us-visas/employment/treaty-trader-investor-visa-e.html">travel.state.gov</a></td><td>E 类签证页</td><td>未核验（Cloudflare）</td></tr>
<tr><td>P0</td><td>新加坡 MOM</td><td><a href="https://www.mom.gov.sg/">https://www.mom.gov.sg/</a></td><td>准证页 / 资格页</td><td>已核验</td></tr>
<tr><td>P0</td><td>德国 Make it in Germany</td><td><a href="https://www.make-it-in-germany.com/en/visa-recognition/visa-types">make-it-in-germany.com</a></td><td>签证类型页 / glossary</td><td>部分核验（机器人防护）</td></tr>
<tr><td>P0</td><td>德国法规库</td><td><a href="https://www.gesetze-im-internet.de/aufenthg_2004/__18b.html">gesetze-im-internet.de</a></td><td>AufenthG 条文</td><td>已核验</td></tr>
<tr><td>P0</td><td>法国 Service-Public</td><td><a href="https://www.service-public.fr/particuliers/vosdroits/F16922?lang=en">service-public.fr/F16922</a></td><td>Talent Passport 页</td><td>已核验</td></tr>
<tr><td>P1</td><td>荷兰政府</td><td><a href="https://www.government.nl/latest/news/2025/07/04/government-to-tighten-up-highly-skilled-migrant-scheme">government.nl</a></td><td>政策公告</td><td>已核验</td></tr>
<tr><td>P1</td><td>Business.gov.nl</td><td><a href="https://business.gov.nl/amendment/rules-highly-skilled-migrants-change/">business.gov.nl</a></td><td>30% ruling 变更</td><td>已核验</td></tr>
<tr><td>P2</td><td>EU 官方</td><td><a href="https://europa.eu/">europa.eu</a></td><td>蓝卡框架</td><td>未核验</td></tr>
<tr><td>P4</td><td>OECD / 智库</td><td>各机构官网</td><td>比较报告</td><td>本基线未引用</td></tr>
</tbody>
</table></div>

<div class="note">渠道分级按业务配置第四节：P0 官方公报 / 法规数据库 / 移民局官方页为唯一可直接采信层；P1 官方政策公告与门户；P2 国际组织与数据库；P3 英文媒体（只作线索）；P4 智库与行业机构（交叉验证方向）；P5 最终裁决口径。</div>

<h3>2.4 信号规则阈值（K01–K08，ex-ante 预校准）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:7%">编号</th><th style="width:17%">监测对象</th><th style="width:7%">等级</th><th style="width:15%">绿灯</th><th style="width:15%">黄灯</th><th style="width:19%">预警红线</th><th style="width:14%">硬红线</th><th style="width:6%">基线状态</th></tr></thead>
<tbody>
<tr><td>K01</td><td>通道新增 / 关闭 / 改名</td><td>一级</td><td>无变更</td><td>拟调整讨论</td><td>正式公布</td><td>生效</td><td>未触发</td></tr>
<tr><td>K02</td><td>薪资门槛调整</td><td>一级</td><td>无调整</td><td>拟调整</td><td>公布新标准</td><td>生效</td><td>未触发</td></tr>
<tr><td>K03</td><td>配额 / 抽签规则</td><td>一级</td><td>无变更</td><td>规则讨论</td><td>公布新规则</td><td>生效</td><td>未触发</td></tr>
<tr><td>K04</td><td>职业清单调整</td><td>一级</td><td>无变更</td><td>审查启动</td><td>公布变更</td><td>生效</td><td>未触发</td></tr>
<tr><td>K05</td><td>积分计分规则</td><td>二级</td><td>无变更</td><td>讨论</td><td>公布</td><td>生效</td><td>未触发</td></tr>
<tr><td>K06</td><td>永居 / 居住年限</td><td>一级</td><td>无变更</td><td>讨论</td><td>公布</td><td>生效</td><td>未触发</td></tr>
<tr><td>K07</td><td>STEM / AI / IT 定向</td><td>一级</td><td>无新增</td><td>政策讨论</td><td>专项通道公布</td><td>生效</td><td>未触发</td></tr>
<tr><td>K08</td><td>官方统计年度更新</td><td>三级</td><td>无</td><td>发布</td><td>数据更新</td><td>—</td><td>未触发</td></tr>
</tbody>
</table></div>

<h3>2.5 结构红线登记簿（RL-01–RL-05）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:16%">监测对象</th><th style="width:33%">硬阈值</th><th style="width:28%">触发后动作</th><th style="width:14%">基线状态</th></tr></thead>
<tbody>
<tr><td>RL-01</td><td>主要通道</td><td>通道关闭或暂停</td><td>重算九国路径优先级</td><td>未触发</td></tr>
<tr><td>RL-02</td><td>永居路径</td><td>永居路径中断</td><td>重算长期定居假设</td><td>未触发</td></tr>
<tr><td>RL-03</td><td>配额</td><td>配额耗尽致通道实际关闭</td><td>重算可申请窗口</td><td>未触发</td></tr>
<tr><td>RL-04</td><td>薪资门槛</td><td>单次上调 &gt;30%</td><td>重算雇主成本与资格</td><td>未触发</td></tr>
<tr><td>RL-05</td><td>排期 / 积压</td><td>积压超阈值</td><td>重算时间线</td><td>未触发</td></tr>
</tbody>
</table></div>

<h3>2.6 政策框架复核清单（G01–G05）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:22%">政策项</th><th style="width:45%">官方入口</th><th style="width:24%">复核周期</th></tr></thead>
<tbody>
<tr><td>G01</td><td>各国移民局 / 内政部</td><td>九国官方页</td><td>事件触发 + 月度</td></tr>
<tr><td>G02</td><td>官方公报 / 法规数据库</td><td>各国公报 / 法规库</td><td>事件触发 + 月度</td></tr>
<tr><td>G03</td><td>职业清单与配额</td><td>各国官方清单</td><td>月度 + 年度</td></tr>
<tr><td>G04</td><td>欧盟蓝卡框架</td><td>EU 官方（europa.eu）</td><td>月度</td></tr>
<tr><td>G05</td><td>官方统计与处理时长</td><td>各国官方统计</td><td>月度 + 年度</td></tr>
</tbody>
</table></div>

<p class="small muted">规则：未取得官方原文的标「未核验」；入口页 ≠ 条款页；任一变更 → 立即重算受影响结论。</p>

<h2 id="s3">三、高技能移民框架总览</h2>

<h3>3.1 层级地图</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:16%">层级</th><th style="width:30%">代表通道</th><th style="width:24%">效力</th><th style="width:30%">监测要点</th></tr></thead>
<tbody>
<tr><td>L1 人才类永居</td><td>EB-1A / EB-1B、NIW、ONE Pass、澳大利亚国家创新签证</td><td>直接 / 可转永居</td><td>成就标准、自申与否、排期</td></tr>
<tr><td>L2 积分制永居</td><td>Express Entry、SMC、189、德国机会卡</td><td>计分获邀</td><td>计分维度、门槛分、类别轮次</td></tr>
<tr><td>L3 雇主担保工签</td><td>H-1B、AEWV、SID 482、EP、HSM、CSEP、Talent</td><td>有条件工作权</td><td>担保义务、薪资门槛、有效期</td></tr>
<tr><td>L4 留学生过渡</td><td>F-1 OPT / STEM OPT、Orientation Year、§20 求职</td><td>过渡居留</td><td>衔接通道、时限</td></tr>
</tbody>
</table></div>

<h3>3.2 国别对比矩阵</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">国家</th><th style="width:22%">代表通道</th><th style="width:26%">薪资门槛（本币）</th><th style="width:16%">转永居</th><th style="width:17%">STEM / AI 定向</th><th style="width:10%">核验</th></tr></thead>
<tbody>
<tr><td>新西兰</td><td>SMC / AEWV / 绿名单</td><td>NZD 35.00/小时（2026-03）</td><td>直接 / 24 个月</td><td>绿名单 Tier1/2</td><td>已核验</td></tr>
<tr><td>荷兰</td><td>HSM / 蓝卡 / Orientation Year</td><td>€5,942/月（≥30 岁，2026）</td><td>连续 5 年</td><td>IT 经验折抵</td><td>已核验</td></tr>
<tr><td>澳大利亚</td><td>189 / 186 / SID 482 / NIV 858</td><td>CSIT AUD 76,515（2025-07）</td><td>直接 / 2 年后</td><td>NIV（原 GTV）</td><td>部分核验</td></tr>
<tr><td>爱尔兰</td><td>CSEP / GEP</td><td>€40,909/年（有学位，2026-03）</td><td>Stamp 4 / 60 个月</td><td>CSOL 含 ICT</td><td>已核验</td></tr>
<tr><td>加拿大</td><td>Express Entry / GTS</td><td>无统一门槛</td><td>直接 PR</td><td>STEM 类别</td><td>已核验</td></tr>
<tr><td>美国</td><td>H-1B / EB-1A / NIW / O-1A</td><td>现行工资（prevailing wage）</td><td>EB 类排期</td><td>STEM OPT / NIW</td><td>已核验</td></tr>
<tr><td>新加坡</td><td>EP / 5 年 EP / ONE Pass</td><td>S$5,600/月（2025 新申请）</td><td>可申 PR</td><td>5 年 EP / ONE「AI and Tech」</td><td>已核验</td></tr>
<tr><td>德国</td><td>蓝卡 / §18b / Chancenkarte</td><td>2025/2026 数值未核验</td><td>蓝卡加速 / 5 年</td><td>IT 无学位通道</td><td>部分核验</td></tr>
<tr><td>法国</td><td>Talent / 蓝卡</td><td>€39,582/年（2026）</td><td>5 年连续居住</td><td>暂无专门通道</td><td>已核验</td></tr>
</tbody>
</table></div>

<h3>3.3 框架演变脉络</h3>

<div class="timeline">
  <div class="tl-item"><div class="tl-date">2024-12</div><div class="tl-body"><div class="t">澳大利亚 SID 取代 TSS 482</div><div class="d">Skills in Demand（SID）签证取代 TSS 482；国家创新签证（858）取代 Global Talent visa。<span class="lvl lvl-partial">部分核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2024-12</div><div class="tl-body"><div class="t">美国 H-1B 现代化最终规则</div><div class="d">89 FR 103054，2025-01-17 生效：澄清专业职业定义、受益人自雇、cap-gap、注册诚信。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2025-03</div><div class="tl-body"><div class="t">新西兰取消中位数工资要求</div><div class="d">AEWV / SPWV 改为「市场工资 + 最低工资」；申请时工作经验由 3 年降为 2 年。<span class="lvl lvl-partial">部分核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2025-07</div><div class="tl-body"><div class="t">澳大利亚技能签证收入门槛上调</div><div class="d">CSIT 由 AUD 73,150 升至 76,515；SSIT 由 135,000 升至 141,210。<span class="lvl lvl-partial">部分核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2025-09</div><div class="tl-body"><div class="t">美国 H-1B 加收费用公告</div><div class="d">2025-09-21 起部分申请加收 $100,000；2026-06-08 联邦法院撤销该指引，2026-07-24 上诉法院拒绝暂停。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2026-03</div><div class="tl-body"><div class="t">新西兰中位工资升至 NZD 35.00</div><div class="d">SMC / 绿名单基准工资 2026-03-09 起 35.00/小时（此前 33.56）。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2026-03</div><div class="tl-body"><div class="t">爱尔兰新 MAR 生效</div><div class="d">CSEP 有学位 €40,909、应届 €36,849；GEP 一般 €36,605。<span class="lvl lvl-verified">已核验</span></div></div></div>
  <div class="tl-item"><div class="tl-date">2027-01</div><div class="tl-body green"><div class="t">新加坡 ONE Pass 新增「AI and Tech」</div><div class="d">2027-01-28 起可申请；EP 2027 新申请门槛升至 S$6,000。<span class="lvl lvl-verified">已核验</span></div></div></div>
</div>

<h3>3.4 术语口径区分（不得混用）</h3>

<div class="term"><b>工作许可 ≠ 永居 ≠ 入籍</b>：三者法律地位与权利不同，逐条分列。<br>
<b>雇主担保类 ≠ 积分制类 ≠ 人才类</b>：担保义务、计分维度与提名要求不同，不得合并登记。<br>
<b>薪资门槛 ≠ 市场工资 ≠ 现行工资</b>：门槛口径（年毛 / 月毛 / 小时）与适用年份必须标注。<br>
<b>职业清单 ≠ 紧缺清单</b>：SOL / Green List / CSOL / STEM 类别口径不同，分列。<br>
<b>通道生效 ≠ 政策公布 ≠ 实施细则</b>：公布、生效、配套细则三阶段分列，附各自日期。</div>

<h2 id="s4">四、重点国家政策逐条解读</h2>

<h3>4.1 新西兰</h3>

<p><b>通道</b>：AEWV（C01，最长 5 年）、Straight to Residence（C02，绿名单 Tier1 直接永居）、Work to Residence（C03，Tier2 满 24 个月转永居）、SMC（C04，6 分制直接永居）。</p>
<p><b>解读</b>：2025-03-10 起 AEWV / SPWV 取消中位数工资要求，改为「市场工资 + 法定最低工资」，申请时工作经验由 3 年降为 2 年；SMC 现行 3 路径（积分制 6 分 / 技能工作经验 5 年含 2 年新 / 技工 4 年含 18 个月新），门槛工资 2026-03-09 起 NZD 35.00/小时。绿名单 Tier1/Tier2 提供直通与 24 个月转永居两条快速路径。<span class="lvl lvl-verified">已核验</span> [C01][C04]</p>
<p><b>2024–2026 变化</b>：中位工资 2024-02-28 起 31.61 → 2025-08-18 起 33.56 → 2026-03-09 起 35.00；2025-08-18 起绿名单新增 10 类制造工种进入 Tier2（snippet）。</p>
<p><b>缺口</b>：绿名单逐职业调整公告页未找到（U-08）。</p>

<h3>4.2 荷兰</h3>

<p><b>通道</b>：Highly Skilled Migrant（C05，KMS）、Orientation Year（C06，搜索年）、EU Blue Card（C07）。</p>
<p><b>解读</b>：HSM 由 IND 认可担保方聘用，2026 年门槛 ≥30 岁 €5,942/月、&lt;30 岁 €4,357、毕业生降低 €3,122；蓝卡无需认可担保，标准 €5,942、毕业生降低 €4,754，IT 经验折抵（3 年 / 7 年内）。Orientation Year 无薪资门槛，毕业后 3 年内可申。<span class="lvl lvl-verified">已核验</span> [C05][C06][C07]</p>
<p><b>2024–2026 变化</b>：2026-01-01 起执行新版 HSM / 蓝卡薪资；2025-07-04 政府宣布收紧 HSM（拟将 &lt;30 岁门槛升至全国平均年薪 1.1 倍、加强认可担保方审查）——<b>尚未生效</b>；30% ruling 自 2027-01-01 降至 27%；2026-05-22 起失业后求职期对持许可 ≥2 年者由 3 个月延至 6 个月。</p>
<p><b>缺口</b>：EU Blue Card 有效期页面未明列（U-11）。</p>

<h3>4.3 澳大利亚</h3>

<p><b>通道</b>：National Innovation visa（C08，858）、ENS（C09，186）、Skills in Demand（C10，482）、Skilled Independent（C11，189）。</p>
<p><b>解读</b>：SID 于 2024-12-07 取代 TSS 482，分 Core Skills（CSOL 职业 + 1 年经验）与 Specialist Skills（高薪、无清单）两档；NIV（858）为 EOI 邀请制人才类永居；186 经 TRT 类为持 482 为提名雇主全职满 2 年者；189 为积分制（65 分起评）。<span class="lvl lvl-partial">部分核验</span> [C08–C11]</p>
<p><b>2024–2026 变化</b>：2025-07-01 起 CSIT 由 AUD 73,150 升至 76,515、SSIT 由 135,000 升至 141,210；2026-07-01 起技能签证收入门槛按 AWOTE 年度指数化；2026-11-24 至 11-28 SkillSelect 迁移至 ImmiAccount。</p>
<p><b>缺口</b>：immi 子域被 Akamai 拦截，C08–C11 仅 snippet；NIV 取代 GTV 的确切日期待核（U-01）。</p>

<h3>4.4 爱尔兰</h3>

<p><b>通道</b>：CSEP（C12）、GEP（C13）、Intra-Company Transfer（C14）。</p>
<p><b>解读</b>：CSEP 面向 CSOL 上高技能紧缺职业（含 ICT），免劳动力市场测试，2 年后可直接申 Stamp 4；2026-03 起门槛有学位 €40,909、无学位 €68,911、应届 €36,849。GEP 覆盖广泛职业，一般 €36,605。ICT 门槛 €49,522。<span class="lvl lvl-verified">已核验</span> [C12–C14]</p>
<p><b>2024–2026 变化</b>：2024-09-02 Employment Permits Act 2024 生效；2025-01-17 HCA / 护工 MAR €27,000→€30,000；2025-04-28 新在线系统上线；2026-03-01 新 MAR 生效；2026-05-29 职业清单 2025 审查 32 项变更（6 项新增 CSEP 等）。</p>
<p><b>口径冲突</b>：MAR 页 CSEP 有学位 €40,909、应届 €36,849；CSEP 页 €40,904、€36,848（差 €1–5），已并列。</p>
<p><b>缺口</b>：CSOL 具体 ICT 条目为 docx 附件，未逐条核验（U-10）；任务所述「4 年 strategic roles permit」未在官方九类许可中找到。</p>

<h3>4.5 加拿大</h3>

<p><b>通道</b>：Express Entry（C15，含 STEM 类别 C16）、GTS（C17）、GSS（C18）、Tech Talent Strategy H-1B 开放工签（C19）、Start-up Visa（C20）。</p>
<p><b>解读</b>：Express Entry 为积分制（CRS）直接 PR，类别抽签含 STEM 类别（过去 3 年内 12 个月全职经验）；GTS 为雇主担保高技能工签；GSS 完整申请 2 周处理；Tech Talent Strategy 允许美国 H-1B 持有人为任意加拿大雇主工作 3 年（页面状态 Closed）。<span class="lvl lvl-verified">已核验</span> [C15][C18][C19]</p>
<p><b>2024–2026 变化</b>：2024-10-24 公布 2025–2027 水平计划（PR 目标 395,000 / 380,000 / 365,000）；2025-03-25 Express Entry 取消 job offer 加分（50 / 200 分）；2026 年 SUV 暂停、开放工签关闭新申请（snippet）。</p>
<p><b>定向</b>：STEM 类别清单偏工程 / 网络安全（如 21220 Cybersecurity specialists），未含「软件开发人员 / 程序员」大类，属结构性缺口。</p>
<p><b>缺口</b>：2026–2028 水平计划、PNP 技术类未核验（U-06）；SUV 状态为 snippet（U-07）。</p>

<h3>4.6 美国</h3>

<p><b>通道</b>：H-1B（C21）、O-1A（C22）、EB-1A（C23）、EB-1B（C24）、NIW（C25）、L-1A/L-1B（C26）、E-3（C27）、TN（C28）、F-1 OPT / STEM OPT（C29）、IEP（C30）。</p>
<p><b>解读</b>：H-1B 为专业职业工签（3+3 年，现行工资）；O-1A / EB-1A / EB-1B / NIW 为人才类（EB-1A 可自申，NIW 含 STEM 高学位优先）；L-1 为跨国调派；TN 限加 / 墨公民；STEM OPT 为留学生过渡（12+24 个月）。<span class="lvl lvl-verified">已核验</span> [C21–C24][C28][C29]</p>
<p><b>2024–2026 变化</b>：2024-12-18 H-1B 现代化最终规则（2025-01-17 生效）；2025-09-19 总统公告对部分 H-1B 加收 $100,000，2026-06-08 联邦法院撤销、2026-07-24 上诉法院拒绝暂停；2026-08-10 9-11 生物识别费最终规则（2026-09-09 生效）。</p>
<p><b>缺口</b>：H-1B 年度配额数字（65,000 / 20,000）未核验（U-03）；E-3 / IEP 仅 snippet（U-04）。</p>

<h3>4.7 新加坡</h3>

<p><b>通道</b>：EP（C31）、EP 科技紧缺 5 年（C32）、S Pass（C33）、ONE Pass（C34）。</p>
<p><b>解读</b>：EP 两阶段（qualifying salary + COMPASS 40 分），2025 新申请一般 S$5,600/月、金融 S$6,200；5 年 EP 面向 SOL 资深科技人员（须 C3 ≥10 分）；S Pass 为中级技术（配额 + 征费）；ONE Pass 为顶级人才（月薪 ≥S$30,000）。<span class="lvl lvl-verified">已核验</span> [C31–C34]</p>
<p><b>2024–2026 变化</b>：2024-03-04 宣布 EP 门槛自 2025-01-01 上调；2023-09 起资深科技人员可申 5 年 EP；2026 页面公布 2027–2028 门槛；ONE Pass 新增「AI and Tech」track（2027-01-28 起）。</p>
<p><b>缺口</b>：Tech.Pass 旧页 404，现行官方专页未找到（U-05）；COMPASS 各准则分值细节页面被截断。</p>

<h3>4.8 德国</h3>

<p><b>通道</b>：EU Blue Card（C35）、§18b（C36）、§18a（C37）、§19c(2)（C38）、IT 专门签证（C39）、Chancenkarte（C40）、§20 求职（C41）。</p>
<p><b>解读</b>：蓝卡面向高学历 + 最低毛薪合同；§18b 为高校学历者；§18a 为受认可职业资格者；§19c(2) 为无正式学历但有突出实践技能者；IT 专门签证可无正式高校学位；Chancenkarte 为无合同积分求职通道。<span class="lvl lvl-verified">已核验</span> [C36–C39][C41]</p>
<p><b>2024–2026 变化</b>：2024-11-18《技术移民法》首批修订生效（含蓝卡框架调整）——仅见非官方转述，<b>待核</b>；官方 visa-types 页确认蓝卡「快速进入劳动力市场、加速永居、简化家庭团聚」。</p>
<p><b>缺口</b>：蓝卡 2025 / 2026 薪资门槛、Chancenkarte 有效期与积分细则未核验（U-02）；2024 年蓝卡门槛 €45,300 / €41,041.80 来自大学页（非官方政府页，snippet）。</p>

<h3>4.9 法国</h3>

<p><b>通道</b>：Talent – salarié qualifié（C42）、entreprise innovante（C43）、salarié en mission（C44）、Carte bleue européenne（C45）、Talent famille（C46）。</p>
<p><b>解读</b>：Talent Passport 各子类年毛薪门槛 €39,582（最长 4 年）；法国蓝卡为 1.5× 平均年毛薪即 €59,373；雇主无需申请工作许可、免缴外国人就业税；居留卡税费 €350。<span class="lvl lvl-verified">已核验</span> [C42–C45]</p>
<p><b>2024–2026 变化</b>：F16922 页面 2026-06-01 核验版显示当前门槛 €39,582 / €59,373；2026 年 Smic 月毛 €1,823.03（时毛 €12.02），2025-01-01 未调。</p>
<p><b>缺口</b>：2024–2025 逐年门槛调整幅度未找到官方逐年对照页（U-09）；france-visas 对自动抓取返回 403；STEM / AI 专门通道未在官方页检索到（French Tech Visa 仅非官方转述）。</p>

<h2 id="s5">五、影响对象矩阵</h2>

<p>矩阵按「通道 / 条款 × 受影响主体 × 影响方向」展开，逐格附条款依据与指标指针；本期为基线，影响量级待月度监测回填。</p>

<div class="tblwrap"><table>
<thead><tr><th style="width:19%">通道 / 条款</th><th style="width:17%">受影响主体</th><th style="width:30%">影响方向</th><th style="width:34%">依据 / 指针</th></tr></thead>
<tbody>
<tr><td>雇主担保薪资门槛（K02 / RL-04）</td><td>雇主 / 技术求职者</td><td>门槛上调 → 重算雇主成本与资格</td><td>新西兰 SMC、荷兰 HSM、新加坡 EP、爱尔兰 CSEP；[C04][C05][C31][C12]</td></tr>
<tr><td>积分制类别轮次（K03 / K05）</td><td>海外技术工人</td><td>类别调整 → 改变可获邀路径</td><td>加拿大 Express Entry STEM、新西兰 SMC、澳大利亚 189；[C15][C04][C11]</td></tr>
<tr><td>人才类永居（K06）</td><td>高成就技术人才</td><td>直接永居 → 缩短定居周期</td><td>EB-1A / EB-1B、ONE Pass、澳大利亚 NIV；[C23][C24][C34][C08]</td></tr>
<tr><td>STEM / AI 定向（K07）</td><td>STEM / AI 从业者</td><td>定向通道 → 降低门槛或延长时限</td><td>新加坡 5 年 EP、美国 STEM OPT、加拿大 STEM 类别；[C32][C29][C16]</td></tr>
<tr><td>职业清单调整（K04）</td><td>清单外职业申请者</td><td>清单变化 → 改变资格</td><td>爱尔兰 CSOL、新加坡 SOL、澳大利亚 CSOL；[C12][C32][C10]</td></tr>
<tr><td>通道关闭 / 暂停（RL-01）</td><td>在途 / 拟申请人员</td><td>通道关闭 → 重算路径</td><td>加拿大 SUV、新加坡 Tech.Pass（待确认）；[C20]</td></tr>
</tbody>
</table></div>

<div class="decision-card">
  <div class="dc-head"><span class="dc-title">核心判断：九国通道地图已锁定，月度监测在基线之上滚动</span><span class="suff need">信息充分度：中</span></div>
  <div class="dc-grid">
    <div><span class="k">结论：</span>九国高技能移民通道可归四类；雇主担保类门槛分化、积分制类直接 PR、人才类永居路径清晰；月度监测聚焦变更检测。</div>
    <div><span class="k">证据强度：</span><span class="ev-strong">强</span>（官方原文 / 法规数据库）</div>
    <div><span class="k">触发条件：</span>K01–K08 任一黄灯及以上；RL-01–RL-05 任一红线。</div>
    <div><span class="k">反向证据：</span>澳大利亚 / 德国 / 美国部分官方页访问受限（U-01 / U-02 / U-04）；12 项未核验清单待消号。</div>
    <div><span class="k">信息充分度：</span>通道框架充分；实时数值与处理时长不足。</div>
    <div><span class="k">置信度：</span>0.7（Kent：中高）</div>
    <div><span class="k">行动：</span>见第六节行动协议卡。</div>
  </div>
</div>

<h2 id="s6">六、合规应对建议（建议章）</h2>

<div class="note correct"><b>结论边界</b>：本章为「建议」，与事实分离；不构成法律意见；重大合规决策须咨询执业移民法律专业人士。原文有歧义处并列多解，不静默择一。</div>

<h3>6.1 建议清单</h3>

<ul class="tight">
<li><b>官方原文回溯 SOP</b>（建议）：通道资格与门槛一律以各国移民局 / 法规数据库原文为准；入口页不等于条款页；拟调整 ≠ 已生效。</li>
<li><b>薪资门槛口径分列</b>（建议）：年毛 / 月毛 / 小时、本币与适用年份逐条标注；汇率换算只作参考，不作资格判断依据。</li>
<li><b>永居路径分列</b>（建议）：工作许可、永居、入籍分开登记；「可直接永居」「可转永居」「可申 PR」法律含义不同。</li>
<li><b>清单与类别动态跟踪</b>（建议）：CSOL / SOL / Green List / STEM 类别逐月比对版本与条目，清单外职业即时重算资格。</li>
<li><b>预留官方访问受限的复核通道</b>（建议）：对反爬 / 拦截页面（澳大利亚 immi、德国 make-it-in-germany、美国 travel.state.gov）建立人工复核清单，避免以 snippet 直引。</li>
</ul>

<h3>6.2 行动协议卡</h3>

<div class="action-card immediate">
  <div class="a-head"><span class="prio immediate">立即行动</span><span class="a-title">RL 红线触发</span></div>
  <div class="a-meta"><b>触发条件：</b>任一 RL-01–RL-05 红线触发。<b>阈值：</b>RL-04 门槛单次上调 &gt;30%；RL-05 积压超阈值。<b>责任角色：</b>业务线负责人。<b>时限：</b>24 小时内。<b>验证指标：</b>台账更新记录 + 已修正事实清单。</div>
</div>

<div class="action-card watch">
  <div class="a-head"><span class="prio watch">持续观察</span><span class="a-title">K01–K03 黄灯</span></div>
  <div class="a-meta"><b>触发条件：</b>通道拟调整、门槛公布新标准、清单审查启动。<b>阈值：</b>K01–K03 进入黄灯。<b>责任角色：</b>监测岗。<b>时限：</b>48 小时内。<b>验证指标：</b>原文 URL 与核验状态登记。</div>
</div>

<div class="action-card archive">
  <div class="a-head"><span class="prio archive">仅记录存档</span><span class="a-title">月度监测</span></div>
  <div class="a-meta"><b>触发条件：</b>每自然月固定窗口。<b>阈值：</b>每自然月 1 次。<b>责任角色：</b>月度监测。<b>时限：</b>月度窗口内。<b>验证指标：</b>月度报告与台账「是否更新」记录。</div>
</div>

<h2 id="s7">七、生效时间线</h2>

<div class="tblwrap"><table>
<thead><tr><th style="width:24%">政策 / 通道</th><th style="width:22%">关键节点</th><th style="width:16%">日期</th><th style="width:38%">依据</th></tr></thead>
<tbody>
<tr><td>新西兰 AEWV / SPWV</td><td>取消中位数工资、经验降为 2 年</td><td>2025-03-10</td><td>INZ</td></tr>
<tr><td>新西兰中位工资</td><td>31.61 → 33.56 → 35.00</td><td>2024-02-28 / 2025-08-18 / 2026-03-09</td><td>INZ 工资页</td></tr>
<tr><td>荷兰 HSM / 蓝卡</td><td>新版薪资生效</td><td>2026-01-01</td><td>IND 收入页</td></tr>
<tr><td>荷兰 HSM 收紧</td><td>公布（拟收紧，尚未生效）</td><td>2025-07-04</td><td>government.nl</td></tr>
<tr><td>澳大利亚 SID / NIV</td><td>取代 TSS 482 / GTV</td><td>2024-12</td><td>Home Affairs</td></tr>
<tr><td>澳大利亚 CSIT / SSIT</td><td>上调</td><td>2025-07-01</td><td>Home Affairs</td></tr>
<tr><td>爱尔兰 Employment Permits Act</td><td>生效</td><td>2024-09-02</td><td>DETE</td></tr>
<tr><td>爱尔兰新 MAR</td><td>生效</td><td>2026-03-01</td><td>DETE MAR 页</td></tr>
<tr><td>美国 H-1B 现代化</td><td>最终规则生效</td><td>2025-01-17</td><td>89 FR 103054</td></tr>
<tr><td>美国 H-1B 加收费用</td><td>公告 / 撤销 / 拒绝暂停</td><td>2025-09-21 / 2026-06-08 / 2026-07-24</td><td>USCIS / 联邦法院</td></tr>
<tr><td>新加坡 EP 门槛</td><td>上调生效</td><td>2025-01-01（新申请）</td><td>MOM</td></tr>
<tr><td>新加坡 ONE Pass「AI and Tech」</td><td>开放申请</td><td>2027-01-28</td><td>MOM</td></tr>
<tr><td>德国《技术移民法》修订</td><td>首批生效（待核）</td><td>2024-11-18</td><td>待官方英文页</td></tr>
<tr><td>法国 Talent Passport</td><td>当前门槛核验版</td><td>2026-06-01</td><td>service-public.fr</td></tr>
</tbody>
</table></div>

<h3>7.1 待生效与待细则清单</h3>

<ul class="tight">
<li><b>荷兰 HSM 收紧</b>：2025-07-04 公布，拟将 &lt;30 岁门槛升至全国平均年薪 1.1 倍，尚未生效。</li>
<li><b>荷兰 30% ruling</b>：自 2027-01-01 降至 27%。[S-009]</li>
<li><b>新加坡 EP 2027 / 2028 门槛</b>：已公布（一般 S$6,000 / 金融 S$6,600）。</li>
<li><b>加拿大 SUV</b>：2026-01-01 起暂停，2025 年背书证书须于 2026-06-30 前递交（snippet）。</li>
<li><b>德国 Chancenkarte</b>：积分细则与有效期待官方页核验。</li>
</ul>

<h2 id="s8">八、数据治理与局限</h2>

<h3>8.1 来源分级</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:10%">层级</th><th style="width:22%">类型</th><th style="width:40%">使用规则</th><th style="width:28%">本基线处理</th></tr></thead>
<tbody>
<tr><td>T1</td><td>官方一手（政府 / 移民局 / 法规数据库）</td><td>唯一可直接采信层，标「已核验」</td><td>主要采信</td></tr>
<tr><td>T2</td><td>行业机构（研究 / 数据 / 咨询）</td><td>交叉验证方向，不替代官方</td><td>未引用</td></tr>
<tr><td>T3</td><td>挂牌门户（数据库 / 统计）</td><td>用于状态快照与线索</td><td>部分入口</td></tr>
<tr><td>T4</td><td>媒体转述</td><td>只用于发现线索，标「需核实原文」</td><td>本基线未直引</td></tr>
</tbody>
</table></div>

<h3>8.2 文本时效与版本治理</h3>

<ul class="tight">
<li><b>读数时点</b>：2026-11；通道状态与门槛以官方页面为准，动态状态须回溯状态页。</li>
<li><b>版本治理</b>：本报告 v1.0（首期基线固定）；核验 / 收敛型运行不升级版本号，只标注「本期读数时点」。</li>
<li><b>基线属性</b>：本报告为后续月度监测与事件解读的对比锚；基线永不重跑，结构变更只影响后续新基线。</li>
</ul>

<div class="note"><b>高影响披露（impact_tier: high）</b>：关键判断附置信区间（以信息等级 + 核验状态表达，不合成单一数值）；读数时点 2026-11；免责——不构成法律意见、不承诺签证结果；非专业建议——重大合规决策须咨询持牌专业人士。</div>

<h3>8.3 未核验清单（U-01–U-12）</h3>

<div class="tblwrap"><table>
<thead><tr><th style="width:9%">编号</th><th style="width:55%">未核验项</th><th style="width:36%">影响与处置</th></tr></thead>
<tbody>
<tr><td>U-01</td><td>澳大利亚 immi.homeaffairs.gov.au 全部页面（Akamai 拦截），C08–C11 仅 snippet</td><td>薪资门槛与日期须人工官方页复核</td></tr>
<tr><td>U-02</td><td>德国 make-it-in-germany 的 Blue Card / Chancenkarte 专页（机器人防护）</td><td>待 BAMF / arbeitsagentur 英文页补采</td></tr>
<tr><td>U-03</td><td>美国 H-1B 年度配额数字（65,000 / 20,000）未核验</td><td>待联邦公报 / USCIS 官方页复核</td></tr>
<tr><td>U-04</td><td>美国 E-3 / IEP 仅 snippet</td><td>待 travel.state.gov / USCIS 原文复核</td></tr>
<tr><td>U-05</td><td>新加坡 Tech.Pass 现行官方专页未找到（旧 URL 404）</td><td>以 ONE Pass / EP 为准，待确认是否并入</td></tr>
<tr><td>U-06</td><td>加拿大 2026–2028 水平计划与 PNP 技术类未核验</td><td>待 canada.ca 官方页复核</td></tr>
<tr><td>U-07</td><td>加拿大 SUV 2026 暂停与开放工签关闭为 snippet</td><td>待 canada.ca 官方公告复核</td></tr>
<tr><td>U-08</td><td>新西兰绿名单逐职业调整公告页未找到</td><td>待 INZ 官方公告复核</td></tr>
<tr><td>U-09</td><td>法国 2024–2025 Talent Passport 逐年门槛未找到官方对照页</td><td>待 service-public.fr 历史版复核</td></tr>
<tr><td>U-10</td><td>爱尔兰 CSOL 具体 ICT 条目为 docx 附件，未逐条核验</td><td>待官方清单复核</td></tr>
<tr><td>U-11</td><td>荷兰 EU Blue Card 有效期页面未明列</td><td>待 IND 页面复核</td></tr>
<tr><td>U-12</td><td>德国《技术移民法》2024-11-18 修订生效仅见非官方转述</td><td>待官方英文页复核</td></tr>
</tbody>
</table></div>

<h3>8.4 解读局限</h3>
<ul class="tight">
<li><b>研究内核</b>：周期定位——本基线为 2026-11 滚动基线锚点；传导量化——政策门槛调整对申请量的弹性与时滞以官方统计为准，本基线不作估计；政策入模——政策变量以通道状态 / 门槛 / 清单三因子入模，政策乘数待校准。</li>
<li>本基线只处理官方文本与通道框架，不采集舆论反应；不做预测，不引用匿名消息。</li>
<li>通道「影响量级」需月度监测回填，本期矩阵只给方向与条款依据。</li>
<li>「已修正事实清单」首期为空；产生修正后逐条补记，防回退。</li>
<li>部分官方页存在访问限制（反爬 / Cloudflare / 机器人防护），相关数值已降级为 snippet 并列入未核验清单。</li>
</ul>

<h2 id="s9">九、参考来源清单</h2>

<div class="refs">
<h3>官方一手（P0 / P1）</h3>
<ol>
<li>新西兰 AEWV — <a href="https://www.immigration.govt.nz/new-zealand-visas/visas/visa/accredited-employer-work-visa">https://www.immigration.govt.nz/new-zealand-visas/visas/visa/accredited-employer-work-visa</a> [Source: 完整URL, 2026]</li>
<li>新西兰 SMC — <a href="https://www.immigration.govt.nz/visas/skilled-migrant-category-resident-visa">https://www.immigration.govt.nz/visas/skilled-migrant-category-resident-visa</a> [Source: 完整URL, 2026]</li>
<li>新西兰 Straight to Residence — <a href="https://www.immigration.govt.nz/visas/straight-to-residence-visa">https://www.immigration.govt.nz/visas/straight-to-residence-visa</a> [Source: 完整URL, 2026]</li>
<li>新西兰 Work to Residence — <a href="https://www.immigration.govt.nz/visas/work-to-residence-visa">https://www.immigration.govt.nz/visas/work-to-residence-visa</a> [Source: 完整URL, 2026]</li>
<li>荷兰 Highly Skilled Migrant — <a href="https://ind.nl/en/residence-permits/work/highly-skilled-migrant">https://ind.nl/en/residence-permits/work/highly-skilled-migrant</a> [Source: 完整URL, 2026]</li>
<li>荷兰 Orientation Year — <a href="https://ind.nl/en/residence-permits/work/residence-permit-for-orientation-year">https://ind.nl/en/residence-permits/work/residence-permit-for-orientation-year</a> [Source: 完整URL, 2026]</li>
<li>荷兰 EU Blue Card — <a href="https://ind.nl/en/residence-permits/work/european-blue-card-residence-permit">https://ind.nl/en/residence-permits/work/european-blue-card-residence-permit</a> [Source: 完整URL, 2026]</li>
<li>荷兰政府 HSM 收紧公告 — <a href="https://www.government.nl/latest/news/2025/07/04/government-to-tighten-up-highly-skilled-migrant-scheme">https://www.government.nl/latest/news/2025/07/04/government-to-tighten-up-highly-skilled-migrant-scheme</a> [Source: 完整URL, 2026]</li>
<li>Business.gov.nl 30% ruling — <a href="https://business.gov.nl/amendment/rules-highly-skilled-migrants-change/">https://business.gov.nl/amendment/rules-highly-skilled-migrants-change/</a> [Source: 完整URL, 2026]</li>
<li>澳大利亚 Home Affairs 技能签证 — <a href="https://www.homeaffairs.gov.au/trav/work/skil">https://www.homeaffairs.gov.au/trav/work/skil</a> [Source: 完整URL, 2026]</li>
<li>澳大利亚 National Innovation visa 858 — <a href="https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/national-innovation-visa-858">https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/national-innovation-visa-858</a> [Source: 完整URL, 2026]</li>
<li>澳大利亚 ENS 186 — <a href="https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/employer-nomination-scheme-186/temporary-residence-transition-stream">https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/employer-nomination-scheme-186/temporary-residence-transition-stream</a> [Source: 完整URL, 2026]</li>
<li>澳大利亚 SID 482 — <a href="https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/skills-in-demand-visa-subclass-482/core-skills-stream">https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/skills-in-demand-visa-subclass-482/core-skills-stream</a> [Source: 完整URL, 2026]</li>
<li>澳大利亚 Skilled Independent 189 — <a href="https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/skilled-independent-189/points-table">https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/skilled-independent-189/points-table</a> [Source: 完整URL, 2026]</li>
<li>爱尔兰 Employment Permits — <a href="https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/">https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/</a> [Source: 完整URL, 2026]</li>
<li>爱尔兰 CSEP — <a href="https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/Critical-Skills-Employment-Permit/">https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/Critical-Skills-Employment-Permit/</a> [Source: 完整URL, 2026]</li>
<li>爱尔兰 GEP — <a href="https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/General-Employment-Permit/">https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/General-Employment-Permit/</a> [Source: 完整URL, 2026]</li>
<li>爱尔兰 ICT — <a href="https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/Intra-Company-Transfer-Employment-Permit/">https://www.enterprise.gov.ie/en/what-we-do/workplace-and-skills/employment-permits/Permit-Types/Intra-Company-Transfer-Employment-Permit/</a> [Source: 完整URL, 2026]</li>
<li>加拿大 Express Entry 类别抽签 — <a href="https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations/category-based-selection.html">https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations/category-based-selection.html</a> [Source: 完整URL, 2026]</li>
<li>加拿大 Global Talent Stream — <a href="https://www.canada.ca/en/employment-social-development/services/foreign-workers/global-talent.html">https://www.canada.ca/en/employment-social-development/services/foreign-workers/global-talent.html</a> [Source: 完整URL, 2026]</li>
<li>加拿大 Global Skills Strategy — <a href="https://www.canada.ca/en/employment-social-development/services/foreign-workers/global-skills-strategy/2-week-processing.html">https://www.canada.ca/en/employment-social-development/services/foreign-workers/global-skills-strategy/2-week-processing.html</a> [Source: 完整URL, 2026]</li>
<li>加拿大 Tech Talent Strategy — <a href="https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/tech-talent.html">https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/tech-talent.html</a> [Source: 完整URL, 2026]</li>
<li>加拿大 Start-up Visa — <a href="https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/start-visa.html">https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/start-visa.html</a> [Source: 完整URL, 2026]</li>
<li>美国 H-1B — <a href="https://www.uscis.gov/working-in-the-united-states/h-1b-specialty-occupations">https://www.uscis.gov/working-in-the-united-states/h-1b-specialty-occupations</a> [Source: 完整URL, 2026]</li>
<li>美国 O-1A — <a href="https://www.uscis.gov/working-in-the-united-states/temporary-workers/o-1-visa-individuals-with-extraordinary-ability-or-achievement">https://www.uscis.gov/working-in-the-united-states/temporary-workers/o-1-visa-individuals-with-extraordinary-ability-or-achievement</a> [Source: 完整URL, 2026]</li>
<li>美国 EB-1 — <a href="https://www.uscis.gov/working-in-the-united-states/employment-based-immigration-first-preference-eb-1">https://www.uscis.gov/working-in-the-united-states/employment-based-immigration-first-preference-eb-1</a> [Source: 完整URL, 2026]</li>
<li>美国 EB-2 — <a href="https://www.uscis.gov/working-in-the-united-states/employment-based-immigration-second-preference-eb-2">https://www.uscis.gov/working-in-the-united-states/employment-based-immigration-second-preference-eb-2</a> [Source: 完整URL, 2026]</li>
<li>美国 L-1A — <a href="https://www.uscis.gov/working-in-the-united-states/temporary-workers/l-1a-intracompany-transexecutive-or-manager">https://www.uscis.gov/working-in-the-united-states/temporary-workers/l-1a-intracompany-transexecutive-or-manager</a> [Source: 完整URL, 2026]</li>
<li>美国 TN — <a href="https://www.uscis.gov/working-in-the-united-states/temporary-workers/tn-usmca-professionals">https://www.uscis.gov/working-in-the-united-states/temporary-workers/tn-usmca-professionals</a> [Source: 完整URL, 2026]</li>
<li>美国 STEM OPT — <a href="https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-extension-for-stem-students-stem-opt">https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-extension-for-stem-students-stem-opt</a> [Source: 完整URL, 2026]</li>
<li>美国 E-3 — <a href="https://travel.state.gov/content/travel/en/us-visas/employment/treaty-trader-investor-visa-e.html">https://travel.state.gov/content/travel/en/us-visas/employment/treaty-trader-investor-visa-e.html</a> [Source: 完整URL, 2026]</li>
<li>美国 IEP 政策手册 — <a href="https://www.uscis.gov/policy-manual/volume-3-part-g">https://www.uscis.gov/policy-manual/volume-3-part-g</a> [Source: 完整URL, 2026]</li>
<li>新加坡 EP 资格 — <a href="https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility">https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility</a> [Source: 完整URL, 2026]</li>
<li>新加坡 5 年 EP（科技紧缺）— <a href="https://www.mom.gov.sg/passes-and-permits/employment-pass/experienced-tech-professionals-with-skills-in-shortage">https://www.mom.gov.sg/passes-and-permits/employment-pass/experienced-tech-professionals-with-skills-in-shortage</a> [Source: 完整URL, 2026]</li>
<li>新加坡 S Pass — <a href="https://www.mom.gov.sg/passes-and-permits/s-pass/key-facts">https://www.mom.gov.sg/passes-and-permits/s-pass/key-facts</a> [Source: 完整URL, 2026]</li>
<li>新加坡 ONE Pass — <a href="https://www.mom.gov.sg/passes-and-permits/overseas-networks-expertise-pass/key-facts">https://www.mom.gov.sg/passes-and-permits/overseas-networks-expertise-pass/key-facts</a> [Source: 完整URL, 2026]</li>
<li>德国签证类型 — <a href="https://www.make-it-in-germany.com/en/visa-recognition/visa-types">https://www.make-it-in-germany.com/en/visa-recognition/visa-types</a> [Source: 完整URL, 2026]</li>
<li>德国蓝卡 glossary — <a href="https://www.make-it-in-germany.com/en/advice-support/glossary/glossary-detail/glossar/do/show/blaue-karte-eu">https://www.make-it-in-germany.com/en/advice-support/glossary/glossary-detail/glossar/do/show/blaue-karte-eu</a> [Source: 完整URL, 2026]</li>
<li>德国机会卡 — <a href="https://www.make-it-in-germany.com/en/visa-recognition/opportunity-card">https://www.make-it-in-germany.com/en/visa-recognition/opportunity-card</a> [Source: 完整URL, 2026]</li>
<li>德国 AufenthG §18b — <a href="https://www.gesetze-im-internet.de/aufenthg_2004/__18b.html">https://www.gesetze-im-internet.de/aufenthg_2004/__18b.html</a> [Source: 完整URL, 2026]</li>
<li>德国 AufenthG §18a — <a href="https://www.gesetze-im-internet.de/aufenthg_2004/__18a.html">https://www.gesetze-im-internet.de/aufenthg_2004/__18a.html</a> [Source: 完整URL, 2026]</li>
<li>德国 AufenthG §19c — <a href="https://www.gesetze-im-internet.de/aufenthg_2004/__19c.html">https://www.gesetze-im-internet.de/aufenthg_2004/__19c.html</a> [Source: 完整URL, 2026]</li>
<li>德国 AufenthG §20 — <a href="https://www.gesetze-im-internet.de/aufenthg_2004/__20.html">https://www.gesetze-im-internet.de/aufenthg_2004/__20.html</a> [Source: 完整URL, 2026]</li>
<li>法国 Talent Passport — <a href="https://www.service-public.fr/particuliers/vosdroits/F16922?lang=en">https://www.service-public.fr/particuliers/vosdroits/F16922?lang=en</a> [Source: 完整URL, 2026]</li>
<li>法国 Talent Famille — <a href="https://www.service-public.fr/particuliers/vosdroits/F35792">https://www.service-public.fr/particuliers/vosdroits/F35792</a> [Source: 完整URL, 2026]</li>
</ol>
</div>

<div class="disc">
<strong>结论边界与版本治理</strong>：本报告只给框架性说明与可核验信息，不构成法律意见，不承诺签证结果，不引用匿名消息。报告版本 v1.0（首期基线固定）；核验 / 收敛型运行不升级版本号，只标注「本期读数时点」。信号阈值与红线为「预校准（ex-ante）」，首次中期回测 2027-06。数据截止 2026-11；来源分级与未核验清单见第八节。
</div>

<footer>九国 · 高技能移民政策 · 首期基线报告（2026-11）｜v1.0｜内容层：content/international/immigration/reports/2026-11_baseline_report.html</footer>
