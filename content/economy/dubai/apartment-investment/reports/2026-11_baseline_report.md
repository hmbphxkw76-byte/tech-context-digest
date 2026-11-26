# 迪拜（阿联酋）公寓住宅市场 · 首期投资覆盖报告

### 投资分析与尽调型 · 基线（首次覆盖）· 版本 v1.0 · 数据截止 / 本期读数时点 2026-11-26

<div class="delta-strip">
  <div class="d add"><div class="n">全量</div><div class="l">本期新增（基线首期 = 全部基线项，八节骨架 + 估值模型）</div></div>
  <div class="d fix"><div class="n">0 条</div><div class="l">修正（已修正事实清单见第七节）</div></div>
  <div class="d same"><div class="n">0 条</div><div class="l">无变化（无上期报告）</div></div>
  <div class="d hyp"><div class="n">0/8</div><div class="l">假设核验进度（8 项估值假设已登记，待 2027-06 回测校准）</div></div>
</div>

<p class="small muted">基线首期：本期新增 = 全部基线项；「已修正事实清单」为空，产生修正后逐条补记。本报告为后续季度 / 年度复核与事件触发的<strong>滚动基线</strong>（对比锚），基线本身永不重跑。</p>

<div class="note correct"><b>决策件索引（v1.3）</b>：本基线的可执行升级版见《PRIME 城市评估 × MST + 决策纪律》专项（同目录 <code>2026-11_baseline_prime-quant-alignment.html</code>），含决策状态机、否决清单 K1–K5、关键假设边际排序、触发器日历、行为护栏与 comps 模板；配套标的档案见 <code>data/processed/economy/dubai/apartment-investment/</code>。</div>

## 一、投资要点（决策摘要）

<div class="card leadbox">
<h3>核心判断</h3>
<ol class="tight">
<li><b>收益定位</b>：毛收益率 6.0–6.6%，高于 3M EIBOR 4.36%（利差 +1.6～+2.2pp）；净中位 5.4%。<span class="lvl lvl-verified">已核验</span> [R10][R11][M02]</li>
<li><b>价格位置</b>：成交中位价 1,659 AED/sqft（2026-10），混合调整指数同比 −5.5%，价格端连续负增。<span class="lvl lvl-partial">部分核验</span> [P03][P04][FC-APT-002][FC-APT-003]</li>
<li><b>估值区间</b>（假设乘积，收益法 / 可比法）：1,430–1,840 AED/sqft，与现价 1,659–1,817 吻合。[R10][R11][R03]</li>
<li><b>需求侧</b>：常住人口 4.58m（+7.5%）、FDI 流入 48.2 亿美元（2025）、国际游客 6.97m（2026 1–8 月）。<span class="lvl lvl-verified">已核验</span> [S09][M12][M17]</li>
<li><b>主要风险</b>：EIBOR 距硬红线约 10.6bp；降租续约占比 21.4%；交付兑现率 41.3% 低位。<span class="lvl lvl-partial">部分核验</span> [M02][R06][S06]</li>
<li><b>结论</b>：以「正利差 + 价格回落」为框架的选择性持有——等待租金与供给信号确认，不给买卖价位。<b>有条件结论</b>：净收益率口径与持有成本明细未核验（第五 / 七节）。</li>
</ol>
<p><b>一句话定位</b>：美元收益型资产，利差为正、价格回落、供给放量；价值取决于「租金稳定性 × 供给消化」验证。</p>
<p><b>场景切片</b>：主场景「投资决策」；次场景「置产研究 / 比较」。</p>
<p class="small muted">来源与时点：数据截止 2026-11-26；指标指针见第三 / 四节，URL 见第八节。</p>
</div>

<div class="preline">阈值与信号规则为「预校准（ex-ante）」；首次中期回测 2027-06。</div>

<div class="decision-card">
  <div class="dc-head"><span class="dc-title">核心判断：正利差 + 价格回落 + 供给放量 → 选择性持有</span><span class="suff need">信息充分度：中</span></div>
  <div class="dc-grid">
    <div><span class="k">结论：</span>毛收益率 6.0–6.6% 对 EIBOR 4.36% 利差为正，估值区间与现价吻合；信号确认前只给条件化结论，不给方向性看多。</div>
    <div><span class="k">证据强度：</span><span class="ev-strong">强</span>（DLD / CBUAE / Savills / Peak Trust）</div>
    <div><span class="k">触发条件：</span>I01–I08 任一黄灯及以上；K / RL 系任一红线。</div>
    <div><span class="k">反向证据：</span>2027–2030 管道 &gt;52.5 万套；同质化新签租金 −15.3%；交付兑现率 41.3%；净收益率口径未核验。</div>
    <div><span class="k">信息充分度：</span>收益率与价格充分；净收益率、持有成本、空置率不足。</div>
    <div><span class="k">置信度：</span>0.7（Kent：中高）</div>
    <div><span class="k">行动：</span>见第六节行动协议卡。</div>
  </div>
</div>

## 二、标的概况

标的为**迪拜公寓资产类别（市场级标的）**，非单一开发商或项目。投资者通过持有物业获得租金收益与资本利得，暴露于价格、租金、利率、供给与政策五类风险。

<table>
<thead><tr><th>要素</th><th>口径 / 内容</th><th>来源</th></tr></thead>
<tbody>
<tr><td>产权制度</td><td>freehold 指定区域可外籍持有；其余为 leasehold / 长期租赁口径，区域清单以 DLD 官方页为准</td><td>DLD [S-072]</td></tr>
<tr><td>交易机制</td><td>过户登记（Property Sale Registration）、期房 Oqood 登记、按揭受 CBUAE 房贷规则约束</td><td>DLD [S-083]；CBUAE [S-085]</td></tr>
<tr><td>签证门槛</td><td>黄金签证房地产投资者门槛 AED 2,000,000（房产总价值 / 净资产口径，含贷款与期房规则以官方页为准）</td><td>UAE Government [S-082]</td></tr>
<tr><td>存量</td><td>≈977,000 套（2026，ValuStrat 全市住宅口径）</td><td>[S08]</td></tr>
<tr><td>成交结构</td><td>2026Q3 住宅成交 34,500 笔 / 70.8 AED bn；期房成交占比 72.2%（笔数）</td><td>Savills [P07]；Cavendish Maxwell [P08]</td></tr>
<tr><td>新推盘</td><td>2026 年 1–9 月新推盘 ≈50,000 套</td><td>Savills [S07]</td></tr>
<tr><td>价格水平</td><td>成交均价 1,817 AED/sqft（2026Q3，Savills）；中位价 1,659 AED/sqft（2026-10，DLD 登记）</td><td>[P01][FC-APT-001]；[P03][FC-APT-002]</td></tr>
</tbody>
</table>

<p class="small muted">口径提示：均价 / 中位价 / 混合调整指数三者不可混用；存量与成交为全市住宅口径，公寓专属口径以指标台账为准（指针 P / S 系）。</p>

## 三、行业与市场输入

本节只取**决策相关输入**，不重复市场全景；监测明细见公寓监测线 `content/economy/dubai/apartment`（月 / 季 / 年报告）与指标台账。

<table>
<thead><tr><th>维度</th><th>关键读数</th><th>时点</th><th>来源 / 指针</th></tr></thead>
<tbody>
<tr><td>价格</td><td>均价 1,817 AED/sqft（环比 −4.8%）；PIX 203.7 点（−0.9% MoM / −5.5% YoY，连续 2 月负增）</td><td>2026Q3 / 2026-10</td><td>Savills [P01]；PropertyIndex [P04][FC-APT-003]</td></tr>
<tr><td>租金</td><td>新签公寓租金中位 65,000 AED/年；平均租金 77.3 AED/sqft/年；降租续约占比 21.4%（2026Q1 为 4.8%）</td><td>2026-10 / 2026-09 / 2026Q3</td><td>Peak Trust [R01][FC-APT-006]；CM [R03][R06][FC-APT-005]</td></tr>
<tr><td>收益率</td><td>毛收益率 6.0–6.6%（DRED / Peak Trust / CM）；净收益率中位 5.4%（仅扣物业费）</td><td>2026Q3 / TTM</td><td>[R10][R11]</td></tr>
<tr><td>供给</td><td>9M 交付 40,400 套；2027 计划 60,000–162,500 套；2027–2030 管道 &gt;525,000 套</td><td>2026 1–9月 / 2027 / 2027–2030</td><td>C&W Core [S01]；[S03]；Savills [S05]</td></tr>
<tr><td>融资成本</td><td>3M EIBOR 4.3648%；CBUAE 基准利率 3.900%；Fed 目标区间 3.75–4.00%</td><td>2026-11-10 / 2026-10-28</td><td>CBUAE [M02][M01]；Federal Reserve [M05]</td></tr>
<tr><td>宏观与外需</td><td>CPI 2026F 1.8% / 2027F 2.5%；实际 GDP 2026F 3.1%；Brent 2026F 96 / 2027F 84 US$/bbl</td><td>2026F / 2027F</td><td>CBUAE / IMF [M14][M15]；EIA STEO [M16]</td></tr>
<tr><td>需求侧</td><td>人口 4.58m（2025 年末，+7.5%）；FDI 48,243 US$m（2025）；游客 6.97m（2026 1–8 月）；酒店入住率 66%</td><td>2025 / 2026</td><td>DDSE [S09]；UNCTAD [M12]；DET [M17][M18]</td></tr>
</tbody>
</table>

<p><b>行业机构定性输入</b>：CBRE《UAE Real Estate Market Review Q3 2026》（2026-11-03）指出迪拜住宅进入「normalization（常态化）」阶段——成交、价格与租金涨幅随供给上升而放缓；阿布扎比受期房需求与总体规划社区支撑仍强。[Source: <a href="https://www.cbre.ae/insights/figures/uae-real-estate-market-review-q3-2026" target="_blank" rel="noopener">cbre.ae</a>, 2026]</p>

<p><b>周期定位</b>：基准判断为「常态化早期」——价格端连续负增（[P04]）、成交增速放缓、租金要价走弱，但登记口径收益率维持 6.0–6.6%（[R10]），处于「利差为正 + 价格回落」的组合窗口。<b>传导量化</b>：利率 → 估值的弹性为负且直接（EIBOR ±50bp 对应估值区间约 ∓7%～8%，假设乘积）；供给 → 价格的传导存在时滞（规划 → 许可 → 交付约 2–4 年，[S01][S03]），故 2027 供给潮的价格压力将滞后显化。<b>政策入模</b>：LTV 与签证门槛作为需求侧参数进入情景假设（G01 / G02），当前仅作方向性处理，未量化乘数（待核实）。<span class="lvl lvl-partial">部分核验</span></p>

## 四、财务分析与估值模型

### 4.1 市场序列（估值输入）

<table>
<thead><tr><th>指标</th><th>数值</th><th>单位</th><th>时点</th><th>来源</th></tr></thead>
<tbody>
<tr><td>[P01] 公寓成交均价</td><td>1,817</td><td>AED/sqft</td><td>2026Q3</td><td>Savills</td></tr>
<tr><td>[P03] 公寓成交中位价</td><td>1,659</td><td>AED/sqft</td><td>2026-10</td><td>PropertyIndex（DLD）</td></tr>
<tr><td>[R01] 新签公寓租金中位</td><td>65,000</td><td>AED/年</td><td>2026-10</td><td>Peak Trust（Ejari）</td></tr>
<tr><td>[R03] 平均租金</td><td>77.3</td><td>AED/sqft/年</td><td>2026-09</td><td>Cavendish Maxwell</td></tr>
<tr><td>[R10] 公寓毛收益率</td><td>6.0 / 6.2 / 6.6</td><td>%</td><td>2026Q3 / TTM</td><td>DRED / Peak Trust / CM</td></tr>
<tr><td>[R11] 净收益率（仅扣物业费）</td><td>5.4</td><td>% 中位</td><td>2026Q3</td><td>Peak Trust</td></tr>
<tr><td>[M01] CBUAE 基准利率</td><td>3.900</td><td>%</td><td>2026-11-10</td><td>CBUAE</td></tr>
<tr><td>[M02] 3M EIBOR</td><td>4.3648</td><td>%</td><td>2026-11-10</td><td>CBUAE</td></tr>
<tr><td>[M05] Fed 目标区间</td><td>3.75–4.00</td><td>%</td><td>2026-10-28</td><td>Federal Reserve</td></tr>
</tbody>
</table>

### 4.2 收益法（直接资本化）

<p><b>模型</b>：资产价值 = 净营运收入 / 资本化率。分子取 [R03] 平均租金 77.3 AED/sqft/年；净收益率 = 毛收益率 − 持有成本差（物业费 / 空置 / 维修等代理）。<span class="lvl lvl-partial">部分核验</span> [R03][R10][R11]</p>

<table>
<thead><tr><th>参数</th><th>取值</th><th>依据</th></tr></thead>
<tbody>
<tr><td>毛收益率</td><td>6.0–6.6%</td><td>[R10]（DRED / Peak Trust / CM 并列）</td></tr>
<tr><td>持有成本差（毛 − 净）</td><td>1.2–1.8pp</td><td>[I05] 业务配置阈值区间；[R11] 净中位 5.4% 与毛下限 6.0% 差 0.6pp，实际差高于代理下限</td></tr>
<tr><td>净收益率（净口径）</td><td>4.2–5.4%</td><td>假设（毛减持有成本差；净口径仅扣物业费，不含空置 / 维修 / 中介 / 利息）</td></tr>
<tr><td>估值（=R03 ÷ 净收益率）</td><td>1,430–1,840</td><td>假设乘积（区间）</td></tr>
</tbody>
</table>

### 4.3 可比法（价格租金比）

<p>以毛收益率倒数构造价格租金比：1 ÷ 6.6% ≈ 15.2x，1 ÷ 5.4% ≈ 18.5x；乘以 [R03] 平均租金 77.3 AED/sqft/年，得 <b>1,175–1,430 AED/sqft</b>（假设乘积，区间）。该口径使用毛收益率，未扣持有成本，与收益法净口径并列呈现、不取均值。相对位置校验：现价 1,659–1,817 AED/sqft 对应毛收益率约 4.2–4.7%（自算，假设乘积，区间），低于 [R10] 登记口径 6.0–6.6%，差异来自价格口径（中位价 / 均价 / 混合指数）与样本结构，正文并列不静默择一。</p>

### 4.4 利差定位（交叉校验）

<ul class="tight">
<li>毛收益率 − 3M EIBOR = <b>+1.6～+2.2pp</b>（[R10] 对 [M02]）；对 CPI 2026F 1.8%（[M14]）实际利差约 +4.2～+4.8pp（自算，假设乘积，区间）。</li>
<li>AED 钉住美元（1 USD = 3.6725 AED，CBUAE [S-057]），利差性质为美元利率资产对美元负债；对人民币投资者的汇率风险为 USD/CNY，正文不作换算结论。</li>
</ul>

### 4.5 估值区间（多方法并列）

<table>
<thead><tr><th>方法</th><th>区间（AED/sqft）</th><th>口径说明</th></tr></thead>
<tbody>
<tr><td>收益法（净收益率 4.2–5.4%）</td><td>1,430–1,840</td><td>假设乘积；净口径仅扣物业费</td></tr>
<tr><td>可比法（价格租金比 15.2–18.5x）</td><td>1,175–1,430</td><td>假设乘积；毛口径未扣持有成本</td></tr>
<tr><td>市场现价（对照）</td><td>1,659–1,817</td><td>[P03] 中位价 / [P01] 均价</td></tr>
</tbody>
</table>

<p><b>结论</b>：三种口径区间相互重叠于 1,430–1,840；现价位于重叠区上沿。定价既不显著高估，也未出现收益安全垫大幅走阔的折让。情景区间见第六节。</p>

## 五、风险清单

<table>
<thead><tr><th>风险</th><th>触发条件</th><th>影响量级</th><th>缓解依赖</th></tr></thead>
<tbody>
<tr><td>融资成本上行</td><td>3M EIBOR ≥4.50%（I01 硬红线）</td><td>月供与可负担性恶化，利差收窄</td><td>Fed 路径（[M05]）、CBUAE 政策</td></tr>
<tr><td>租金下行</td><td>同质化新签租约同比转负（[R09] 已 −15.3%）</td><td>毛收益率下修，估值承压</td><td>人口 / 就业流入（[S09]）、旅游（[M17]）</td></tr>
<tr><td>供给集中兑现</td><td>2027 计划 60,000–162,500 套（[S03]）</td><td>空置与去化压力</td><td>交付兑现率（[S06] 41.3% 低位）</td></tr>
<tr><td>期房交付与开发商信用</td><td>交付兑现率 &lt;45% 且计划量创高（I06）</td><td>资本利得实现推迟</td><td>DLD / Oqood 托管机制 [S-065]</td></tr>
<tr><td>房东定价权弱化</td><td>降租续约占比超过 25%（RL-02，公寓监测线阈值，指针）</td><td>租金与净收益率下修</td><td>Ejari 登记结构（[R06]）</td></tr>
<tr><td>政策门槛调整</td><td>黄金签证门槛 / LTV 规则变更（G01 / G02）</td><td>需求结构变化</td><td>u.ae / CBUAE 官方页 [S-082][S-085]</td></tr>
<tr><td>数据盲区</td><td>净收益率、持有成本、空置率缺同口径双源</td><td>估值区间不确定性</td><td>盲区台账（P0 四类 + 本线三项）</td></tr>
</tbody>
</table>

<div class="note correct"><b>重大未决事项</b>：① 净收益率仅 Peak Trust 单源中位 5.4%，持有成本明细未核验；② 交付兑现率 41.3% 为二手转载单源，需同口径双源；③ 2027 供给区间上下限相差 2.7 倍（60,000 vs 162,500），口径未对齐。</div>

<div class="note correct"><b>反向声音（至少两条，不静默择一）</b>：
<ul class="tight">
<li><b>供应过剩论 vs 需求流入</b>：看空方强调 2027–2030 管道 &gt;52.5 万套（[S05]）；看多方强调人口 4.58m（+7.5%）、FDI 48.2 亿美元、游客 6.97m（[S09][M12][M17]）。本报告并列，倾向于「供给压力真实、需求侧有支撑但弹性未知」。</li>
<li><b>租金口径分裂</b>：要价口径同质化新签较 1 月 −15.3%（[R09]，fäm / DLD），而登记口径显示租赁市场「稳定轨迹」（DLD 官方新闻 [S-062]）。两者口径不同，本报告以登记口径为锚、要价为先行信号。</li>
<li><b>整体回落 vs 高端韧性</b>：整体均价环比 −4.8%（[P01]），而 Knight Frank 跟踪的 US$10m+ 豪宅市场保持活跃（[S-050]）——结构性分层，不能用整体口径代表 prime 资产。</li>
</ul></div>

## 六、情景与敏感性

<table>
<thead><tr><th>情景</th><th>假设组合</th><th>估值区间（AED/sqft）</th><th>触发条件</th></tr></thead>
<tbody>
<tr><td>乐观</td><td>租金 +3～+5%；净收益率压缩至 4.0–4.5%（需求强 + 供给消化）</td><td>1,800–2,030（假设乘积，区间）</td><td>人口 / 就业持续净流入；EIBOR 下行</td></tr>
<tr><td>基准</td><td>租金 0～+2%；净收益率 4.2–5.4%</td><td>1,430–1,840（假设乘积，区间）</td><td>常态化延续（CBRE 定性）</td></tr>
<tr><td>悲观</td><td>租金 −5～−8%；净收益率扩张至 5.6–6.2%（供给冲击 + 利率高企）</td><td>1,180–1,310（假设乘积，区间）</td><td>I01 硬红线 + 供给集中兑现</td></tr>
</tbody>
</table>

<table>
<thead><tr><th>敏感性参数</th><th>变动</th><th>对估值的影响（基准租金 77.3）</th></tr></thead>
<tbody>
<tr><td>净收益率</td><td>±0.5pp</td><td>估值约 ∓7%～8%（假设乘积）</td></tr>
<tr><td>租金</td><td>±5%</td><td>估值同向 ±5%（假设乘积）</td></tr>
<tr><td>利率（EIBOR）</td><td>+50bp 且全额传导</td><td>利差收窄约 0.5pp，估值区间下移（假设乘积，区间）</td></tr>
</tbody>
</table>

<div class="note correct"><b>结论变化方向声明</b>：基线结论为「选择性持有（有条件）」；若 I01 触发硬红线且 I08 租金同比转负，结论下调为「减持观望」；若 I03 价格企稳且 I02 毛收益率 >7.0%，上调为「积极配置」。</div>

<h3>6.1 行动协议卡</h3>

<div class="action-card immediate">
  <div class="a-head"><span class="prio immediate">立即行动</span><span class="a-title">净收益率口径消号</span></div>
  <div class="a-meta"><b>触发条件：</b>净收益率单源状态持续。<b>阈值：</b>连续 2 期未补齐同口径双源即升级。<b>责任角色：</b>业务线负责人。<b>时限：</b>24 小时内登记，1 个周期内复核。<b>验证指标：</b>registry 假设表状态 + 待核实清单。</div>
</div>

<div class="action-card watch">
  <div class="a-head"><span class="prio watch">持续观察</span><span class="a-title">I01 / I08 阈值跟踪</span></div>
  <div class="a-meta"><b>触发条件：</b>3M EIBOR 或租金同比接近阈值。<b>阈值：</b>以 business-config 第五节 I01 / I08 行为准（预校准）。<b>责任角色：</b>监测岗。<b>时限：</b>月度窗口内。<b>验证指标：</b>EIBOR 定盘与 Ejari 登记读数入库。</div>
</div>

<div class="action-card archive">
  <div class="a-head"><span class="prio archive">仅记录存档</span><span class="a-title">季度复核</span></div>
  <div class="a-meta"><b>触发条件：</b>每季度固定窗口。<b>阈值：</b>每季度 1 次。<b>责任角色：</b>业务线负责人。<b>时限：</b>季度窗口内。<b>验证指标：</b>季度复核报告与 registry 更新记录。</div>
</div>

## 七、合规与边界

<div class="note correct"><b>信息来源合法性声明</b>：本报告仅使用公开合法来源（政府 / 央行 / 统计机构 / 多边机构原始发布、行业机构英文研究、挂牌门户与媒体线索），不使用非公开信息；媒体转述仅作线索并标注「需核实原文」。</div>

<div class="note correct"><b>利益冲突声明</b>：本仓库为公开研究仓库，作者不持有本报告涉及的任何头寸，不存在与结论相关的经济利益；报告不接受任何机构的付费或定向委托。</div>

<div class="disc"><b>免责与非专业建议</b>：本报告不构成对不特定公众的投资邀约，不构成投资、法律、税务或持牌专业人士意见；读者须咨询持牌专业人士后独立决策。估值为模型输出（假设乘积，区间），不是买卖报价；数据截止 2026-11-26（本期读数时点），后续变化不在本报告覆盖范围内。置信区间：核心估值区间 1,430–1,840 AED/sqft；时效声明：读数时点 2026-11-26，复核节拍为季度 / 年度。</div>

<p><b>影响分级披露</b>：<code>impact_tier = high</code>（强制披露四要素：置信区间 / 时效声明 / 免责 / 非专业建议，已齐）。<b>盲区</b>：就业 / 收入 / 空置 / 竣工四类沿用共享盲区台账；本线新增净收益率口径、持有成本明细、USD/CNY 汇率路径三项，均在 registry 待核实清单列示。</p>

## 八、参考来源清单

<p class="small muted">分级：T1 官方一手；T2 行业机构；T3 挂牌门户；T4 媒体转述（须标「需核实原文」）。完整登记见 <code>data/processed/economy/dubai/apartment-investment/source_registry.json</code>。</p>

<h3>官方一手（T1）</h3>
<ul class="tight">
<li>Central Bank of the UAE（CBUAE）— EIBOR / 统计数据 / 统计公报：<a href="https://www.centralbank.ae/en/forex-eibor/eibor-rates/" target="_blank" rel="noopener">centralbank.ae/eibor</a>；<a href="https://centralbank.ae/media/cysbl3ar/statistical-bulletin-september-2026.pdf" target="_blank" rel="noopener">Statistical Bulletin Sep 2026</a>；<a href="https://rulebook.centralbank.ae/en/rulebook/regulations-regarding-mortgage-loans" target="_blank" rel="noopener">房贷规则</a></li>
<li>U.S. Federal Reserve — FOMC 声明（2026-10-28）：<a href="https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm" target="_blank" rel="noopener">federalreserve.gov</a></li>
<li>Dubai Land Department（DLD）— 指数 / 租赁指数 / 交易与租赁开放数据：<a href="https://dubailand.gov.ae/en/open-data/indexes-home/" target="_blank" rel="noopener">dubailand.gov.ae/indexes</a>；<a href="https://www.dubaipulse.gov.ae/data/dld-registration/dld_transactions-open" target="_blank" rel="noopener">Dubai Pulse · DLD Transactions</a>；<a href="https://www.dubaipulse.gov.ae/data/dld-registration/dld_rent_contracts-open" target="_blank" rel="noopener">Dubai Pulse · Rent Contracts</a></li>
<li>Digital Dubai / DDSE — 人口 4.580m（2025 年末）：<a href="https://www.digitaldubai.ae/" target="_blank" rel="noopener">digitaldubai.ae</a></li>
<li>Dubai Statistics Centre（DSC）：<a href="https://www.dsc.gov.ae/" target="_blank" rel="noopener">dsc.gov.ae</a></li>
<li>Government of Dubai Media Office — 旅游数据：<a href="https://mediaoffice.ae/en/news/2026/september/13-09/dubai-tourism-records-highest-visitor-numbers-since-february-as-atm-2026-opens" target="_blank" rel="noopener">mediaoffice.ae</a></li>
<li>UAE Government — 黄金签证：<a href="https://u.ae/en/information-and-services/visa-and-emirates-id/Types-of-visas/golden-visa" target="_blank" rel="noopener">u.ae</a></li>
<li>UNCTAD — WIR 2026（FDI）：<a href="https://unctad.org/" target="_blank" rel="noopener">unctad.org</a></li>
<li>International Monetary Fund（IMF）— UAE 国别页：<a href="https://imf.org/external/country/are/index.htm" target="_blank" rel="noopener">imf.org</a></li>
<li>U.S. Energy Information Administration — STEO：<a href="https://www.eia.gov/outlooks/steo/" target="_blank" rel="noopener">eia.gov/steo</a></li>
<li>Dubai Municipality — 建筑许可 / 竣工证书开放数据：<a href="https://dm.gov.ae/open-data/" target="_blank" rel="noopener">dm.gov.ae/open-data</a></li>
</ul>

<h3>行业机构（T2）</h3>
<ul class="tight">
<li>Savills Middle East — Dubai Residential Q3 2026：<a href="https://www.savills.ae/research_articles/379881/395342-0" target="_blank" rel="noopener">savills.ae</a></li>
<li>CBRE UAE — UAE Real Estate Market Review Q3 2026：<a href="https://www.cbre.ae/insights/figures/uae-real-estate-market-review-q3-2026" target="_blank" rel="noopener">cbre.ae</a></li>
<li>JLL — UAE Living / Market Dynamics：<a href="https://www.jll.com/en-ae/insights/market-dynamics/uae-living" target="_blank" rel="noopener">jll.com</a></li>
<li>Cushman & Wakefield — Residential Q3 2026 Dubai UAE：<a href="https://www.cushwake.ae/en/marketbeats/marketbeat-residential-q3-2026-dubai-uae" target="_blank" rel="noopener">cushwake.ae</a></li>
<li>Cavendish Maxwell：<a href="https://cavendishmaxwell.com/" target="_blank" rel="noopener">cavendishmaxwell.com</a></li>
<li>Peak Trust — Rent Yield Monitor：<a href="https://peaktrust.ae/insights/rent-yield-monitor/2026-10" target="_blank" rel="noopener">peaktrust.ae</a></li>
<li>ValuStrat — Dubai Real Estate Review Q3 2026：<a href="https://valustrat.com/products/dubai-real-estate-review-q3-2026" target="_blank" rel="noopener">valustrat.com</a></li>
<li>PropertyIndex.ae — Dubai Real Estate Price Index：<a href="https://www.propertyindex.ae/dubai-real-estate-price-index" target="_blank" rel="noopener">propertyindex.ae</a></li>
<li>DXBinteract — Market Reports Q3 2026：<a href="https://dxbinteract.com/market-reports/2026/Q3" target="_blank" rel="noopener">dxbinteract.com</a></li>
<li>Knight Frank — Dubai Residential / Prime：<a href="https://www.knightfrank.ae/newsroom/press-release" target="_blank" rel="noopener">knightfrank.ae</a></li>
</ul>

<h3>媒体线索（T4，须标「需核实原文」）</h3>
<ul class="tight">
<li>Khaleej Times — 租金与租客结构报道（线索，数值已回登记口径校验）</li>
<li>The Gulf Pulse / OffPlan Insider — 要价与推盘线索（仅作先行信号）</li>
</ul>
