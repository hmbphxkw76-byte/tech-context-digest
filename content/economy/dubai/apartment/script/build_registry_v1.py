# -*- coding: utf-8 -*-
"""迪拜公寓住宅市场持续监测指标台账 — openpyxl 直写建表脚本

用法：python script/build_registry_v1.py [--force]

防覆盖保护：输出文件已存在时默认跳过；加 --force 才允许重写（重写前请确认
xlsx 无手工增量修订，否则会被本脚本的硬编码内容回滚）。
输出：data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_2026-11.xlsx（仓库相对）
"""
import importlib.util
import sys
from pathlib import Path

if importlib.util.find_spec("openpyxl") is None:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "openpyxl>=3.1.0"])

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

ROOT = Path(__file__).resolve().parents[5]  # 仓库根（content/<theme>/<region>/<category>/script/）
OUT = str(ROOT / "data" / "processed" / "economy" / "dubai" / "apartment"
         / "dubai_apartment_indicator_registry_2026-11.xlsx")

if Path(OUT).exists() and "--force" not in sys.argv:
    print("SKIP", OUT, "已存在（防覆盖保护；确认无手工增量后可用 --force 重写）")
    sys.exit(0)


def xl_color(css_hex: str) -> str:
    value = css_hex.removeprefix("#").upper()
    if len(value) != 6:
        raise ValueError(f"Expected #RRGGBB, got: {css_hex}")
    return "FF" + value


XL_PRIMARY = xl_color("#4472C4")
XL_DARK = xl_color("#2F5597")
XL_LIGHT = xl_color("#D9E2F3")
XL_PALE = xl_color("#F2F6FC")
XL_BORDER = xl_color("#BFBFBF")
XL_WHITE = xl_color("#FFFFFF")
XL_TEXT = xl_color("#1A1A1A")
XL_GREEN_BG = xl_color("#C6EFCE")
XL_GREEN_FG = xl_color("#006100")
XL_YELLOW_BG = xl_color("#FFEB9C")
XL_YELLOW_FG = xl_color("#9C6500")
XL_RED_BG = xl_color("#FFC7CE")
XL_RED_FG = xl_color("#9C0006")

thin = Side(style="thin", color=XL_BORDER)
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
H_FONT = Font(name="Microsoft YaHei", size=10, bold=True, color=XL_WHITE)
B_FONT = Font(name="Microsoft YaHei", size=10, color=XL_TEXT)
TITLE_FONT = Font(name="Microsoft YaHei", size=15, bold=True, color=XL_WHITE)
SUB_FONT = Font(name="Microsoft YaHei", size=9, color=XL_TEXT)

wb = Workbook()
wb.properties.title = "迪拜公寓住宅市场持续监测指标台账（2026年11月基线）"
wb.properties.subject = "Dubai Apartment Market Continuous Monitoring - Indicator Registry"
wb.properties.creator = "WorkBuddy Research"


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = H_FONT
        cell.fill = PatternFill("solid", fgColor=XL_PRIMARY)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = 32


def style_body(ws, start, end, ncols, wrap_cols=()):
    for r in range(start, end + 1):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = B_FONT
            cell.border = BORDER
            cell.alignment = Alignment(
                horizontal="left" if c in wrap_cols else "center",
                vertical="top",
                wrap_text=(c in wrap_cols),
            )
        if r % 2 == 0:
            for c in range(1, ncols + 1):
                ws.cell(row=r, column=c).fill = PatternFill("solid", fgColor=XL_PALE)


def set_widths(ws, widths):
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = w


def add_table(ws, headers, rows, title=None, widths=None, wrap_cols=(), hyperlink_col=None):
    """锚点：有 title 时 第1行标题 / 第2行表头 / 第3行起数据；否则 第1行表头 / 第2行起数据。"""
    ncols = len(headers)
    hdr_row = 2 if title else 1
    data_start = hdr_row + 1
    if title:
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
        t = ws.cell(row=1, column=1, value=title)
        t.font = TITLE_FONT
        t.fill = PatternFill("solid", fgColor=XL_DARK)
        t.alignment = Alignment(horizontal="left", vertical="center")
        ws.row_dimensions[1].height = 30
    for i, h in enumerate(headers, start=1):
        ws.cell(row=hdr_row, column=i, value=h)
    style_header(ws, hdr_row, ncols)
    for ri, row in enumerate(rows, start=data_start):
        for ci, val in enumerate(row, start=1):
            ws.cell(row=ri, column=ci, value=val)
    data_end = data_start + len(rows) - 1
    style_body(ws, data_start, data_end, ncols, wrap_cols)
    if hyperlink_col:
        for r in range(data_start, data_end + 1):
            cell = ws.cell(row=r, column=hyperlink_col)
            if isinstance(cell.value, str) and cell.value.startswith("http"):
                cell.hyperlink = cell.value
                cell.font = Font(name="Microsoft YaHei", size=9, color=XL_DARK, underline="single")
    if widths:
        set_widths(ws, widths)
    if len(rows) >= 10:
        ws.auto_filter.ref = f"A{hdr_row}:{get_column_letter(ncols)}{data_end}"
    ws.freeze_panes = f"C{data_start}" if ncols >= 8 else f"A{data_start}"
    return hdr_row, data_start, data_end


# ---------------------------------------------------------------- 看板
ws = wb.active
ws.title = "看板"
ws.sheet_properties.tabColor = XL_DARK
ws.merge_cells("A1:H1")
c = ws["A1"]
c.value = "迪拜公寓住宅市场持续监测 · 首期基线看板"
c.font = TITLE_FONT
c.fill = PatternFill("solid", fgColor=XL_DARK)
c.alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[1].height = 34
ws.merge_cells("A2:H2")
ws["A2"] = "基线日期 2026-11-10（北京时间）｜经济指标一律取自官方英文一手来源｜市场数据取自英文行业机构｜所有输出为中文"
ws["A2"].font = SUB_FONT
ws["A2"].alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[2].height = 22

kpis = [
    ("公寓成交中位价", "AED 1,659/sqft", "2026-10 · PropertyIndex/DLD 登记"),
    ("Q3 住宅成交量", "≈34,500 笔", "2026Q3 · Savills · 同比 −38%"),
    ("Q3 公寓毛收益率", "6.6%", "2026Q3 · Cavendish Maxwell · 毛口径"),
    ("9M 2026 已交付", "40,400 套", "C&W Core Q3 2026 · 同比大增"),
    ("CBUAE 基准利率", "3.900%", "2026-11-10 · 官方一手"),
    ("3 个月 EIBOR", "4.364820%", "2026-11-10 · 官方一手"),
    ("Fed 目标区间", "3.75%–4.00%", "2026-10-28 · 10-2 票维持，2 票主张加息"),
    ("UAE 2025 FDI 流入", "US$48,243m", "UNCTAD WIR 2026 · 同比 +5.7%"),
]
for i, (name, val, note) in enumerate(kpis):
    col = 1 + (i % 4) * 2
    row = 4 + (i // 4) * 3
    ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col + 1)
    ws.merge_cells(start_row=row + 1, start_column=col, end_row=row + 1, end_column=col + 1)
    ws.merge_cells(start_row=row + 2, start_column=col, end_row=row + 2, end_column=col + 1)
    a = ws.cell(row=row, column=col, value=name)
    a.font = Font(name="Microsoft YaHei", size=9, color=XL_TEXT)
    a.fill = PatternFill("solid", fgColor=XL_LIGHT)
    a.alignment = Alignment(horizontal="center", vertical="center")
    b = ws.cell(row=row + 1, column=col, value=val)
    b.font = Font(name="Microsoft YaHei", size=14, bold=True, color=XL_DARK)
    b.alignment = Alignment(horizontal="center", vertical="center")
    d = ws.cell(row=row + 2, column=col, value=note)
    d.font = Font(name="Microsoft YaHei", size=8, color=XL_TEXT)
    d.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for rr in (row, row + 1, row + 2):
        for cc in (col, col + 1):
            ws.cell(row=rr, column=cc).border = BORDER
ws.row_dimensions[4].height = 20
ws.row_dimensions[7].height = 20
ws.row_dimensions[5].height = 26
ws.row_dimensions[8].height = 26
ws.row_dimensions[6].height = 24
ws.row_dimensions[9].height = 24

ws.merge_cells("A10:H10")
ws["A10"] = "先行信号矩阵（首期判读）"
ws["A10"].font = Font(name="Microsoft YaHei", size=11, bold=True, color=XL_WHITE)
ws["A10"].fill = PatternFill("solid", fgColor=XL_PRIMARY)
ws["A10"].alignment = Alignment(horizontal="left", vertical="center")

sig_headers = ["先行指标", "最新读数", "方向", "信号灯", "传导链", "领先期", "对公寓市场的含义", "来源级别"]
for i, h in enumerate(sig_headers, start=1):
    ws.cell(row=11, column=i, value=h)
style_header(ws, 11, 8)
signals = [
    ("CBUAE 基准利率 / 3M EIBOR", "3.900% / 4.3648%", "上行后高位", "红灯", "利率→按揭月供→购买力→成交量→价格", "2–4 季", "融资成本抬升，压制杠杆买家与期房吸收", "官方一手"),
    ("Fed 政策倾向", "3.75–4.00%，2 票主张加息", "偏鹰", "红灯", "Fed→IORB→CBUAE→EIBOR→按揭", "2–4 季", "AED 盯住美元，迪拜无独立宽松空间", "官方一手"),
    ("建筑许可 / 许可建筑面积", "10,776 套许可 / +48% 面积", "扩张", "红灯", "许可→开工→2–4 年交付→租金与价格", "8–16 季", "中期供给压力源已形成", "官方一手"),
    ("新推盘量", "9M ≈50,000 套 / −64% 同比", "收缩", "绿灯", "推盘→3–4 年后交付 / 当期可售库存", "当期+长周期", "开发商主动刹车，缓冲 2028+ 供给", "行业机构"),
    ("FDI 流入", "US$48,243m（2025）/ +5.7%", "增长", "绿灯", "FDI→企业设立→外籍就业→家庭形成→需求", "2–6 季", "支撑长期自住与租赁需求", "官方一手"),
    ("人口 / 家庭形成", "4.580m（2025 末）/ +7.5%", "增长", "绿灯", "人口→家庭数→租赁需求→租金→价格", "1–4 季", "需求分母仍在扩张", "官方一手"),
    ("降租续约占比", "21.4%（Q3）vs 4.8%（Q1）", "恶化", "红灯", "交付→空置竞争→议价权→租金→收益率", "0–2 季", "房东定价权快速流失，租金领先转弱", "行业机构（媒体转述）"),
    ("就业 / 失业率", "2026 调查 10 月启动，结果未发布", "数据缺口", "灰灯", "就业→净迁入→家庭形成→租金", "1–3 季", "最大监测盲区，暂不可量化", "官方（无数值）"),
]
for r, row in enumerate(signals, start=12):
    for ci, val in enumerate(row, start=1):
        ws.cell(row=r, column=ci, value=val)
style_body(ws, 12, 19, 8, wrap_cols=(1, 5, 7))
for r in range(12, 20):
    cell = ws.cell(row=r, column=4)
    v = cell.value
    if v == "红灯":
        cell.fill = PatternFill("solid", fgColor=XL_RED_BG)
        cell.font = Font(name="Microsoft YaHei", size=10, bold=True, color=XL_RED_FG)
    elif v == "绿灯":
        cell.fill = PatternFill("solid", fgColor=XL_GREEN_BG)
        cell.font = Font(name="Microsoft YaHei", size=10, bold=True, color=XL_GREEN_FG)
    else:
        cell.fill = PatternFill("solid", fgColor=XL_YELLOW_BG)
        cell.font = Font(name="Microsoft YaHei", size=10, bold=True, color=XL_YELLOW_FG)
    ws.row_dimensions[r].height = 34

ws.merge_cells("A21:H21")
ws["A21"] = "综合判断：周期处于「高位放缓 → 结构性再平衡」过渡段。量跌远大于价跌，供给兑现率是关键缓冲；利率与租金议价权两项先行信号已转负，人口与 FDI 仍为正。2027 年是压力测试年。"
ws["A21"].font = Font(name="Microsoft YaHei", size=10, bold=True, color=XL_DARK)
ws["A21"].fill = PatternFill("solid", fgColor=XL_LIGHT)
ws["A21"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
ws.row_dimensions[21].height = 42
set_widths(ws, [24, 20, 15, 11, 34, 12, 34, 20])


# ---------------------------------------------------------------- 指标台账
headers = ["编号", "模块", "指标中文名", "英文名称 / Series", "时序属性", "领先期(月)",
           "来源机构", "来源级别", "官方/权威英文URL", "发布频率", "发布时滞", "单位",
           "最新值", "统计周期", "发布日期", "监测频次", "触发阈值 / 关注条件", "核验状态", "口径警示"]

CB = "https://centralbank.ae/en"
CBE = "https://www.centralbank.ae/en/forex-eibor/eibor-rates/"
CBFX = "https://centralbank.ae/en/forex-eibor/exchange-rates/"
CBMB = "https://centralbank.ae/en/research-and-statistics/latest-statistics/statistical-bulletin-banking-monetary-statistics/"
CBQR = "https://centralbank.ae/en/news-and-publications/publications/quarterly-reports/"
FED = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FEDOCT = "https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm"
DMO = "https://mediaoffice.ae/en/news/2026/march/25-03/dubai-records-strong-performance-in-the-construction-sector"
DMOT = "https://mediaoffice.ae/en/news/2026/september/13-09/dubai-tourism-records-highest-visitor-numbers-since-february-as-atm-2026-opens"
DD = "https://www.digitaldubai.ae/initiatives/paperless/dubai-digital-dubai's-population-tops-4.580-million-by-the-end-of-2025-recording-7.5-growth"
UNCTAD = "https://unctad.org/system/files/non-official-document/wir_fs_qa_en.pdf"
IMF = "https://imf.org/external/country/are/index.htm"
EIA = "https://www.eia.gov/outlooks/steo/report/global_oil.php"
DP_RENT = "https://www.dubaipulse.gov.ae/data/dld-registration/dld_rent_contracts-open"
DP_SALE = "https://www.dubaipulse.gov.ae/data/dld-transactions/dld_transactions-open"
DP_UNIT = "https://www.dubaipulse.gov.ae/data/dld-registration/dld_units-open"
DLD_IDX = "https://dubailand.gov.ae/en/open-data/indexes-home/"
DLD_RI = "https://dubailand.gov.ae/en/eservices/rental-index/rental-index/"
DLD_FAQ = "http://dubailand.gov.ae/en/frequently-asked-questions"
DSC = "https://www.dsc.gov.ae/en-us/Themes/Pages/Population-and-Vital-Statistics.aspx?Theme=42&year=2022"
DM_OPEN = "https://dm.gov.ae/open-data/"
DUBAI_OPEN = "https://www.dubai.ae/open-data"
SAV = "https://www.savills.ae/research_articles/379881/395342-0"
CW = "https://www.cushwake.ae/en/marketbeats/marketbeat-residential-q3-2026-dubai-uae"
CM = "https://www.zawya.com/en/press-release/research-studies/dubai-residential-sales-values-top-aed72.6-billion-in-q3-2026-cavendish-maxwell-1518343"
CMH1 = "https://zawya.com/en/press-release/research-studies/dubai-adds-24800-new-residential-units-in-h1-2026-as-market-shifts-from-launch-led-to-delivery-driven-says-cavendish-maxwell-414719"
VS = "https://valustrat.com/products/dubai-real-estate-review-q3-2026"
PIX = "https://www.propertyindex.ae/dubai-real-estate-price-index"
PEAK = "https://peaktrust.ae/insights/rent-yield-monitor/2026-09"
DRED = "https://www.dubairealestatedata.com/yields"
KT = "https://www.khaleejtimes.com/business/dubai-rents-1-in-5-tenants-now-pays-less-than-before-as-rentals-ease-on-new-supply"
KTF = "https://www.khaleejtimes.com/business/dubai-tenants-move-homes-as-new-leases-offer-rents-up-to-15-lower"
PF = "https://thegulfpulse.com/dubai-asking-rents-fall-up-to-22-in-tracked-areas"

V = "已核验"
PV = "部分核验"
UV = "未核验"

registry = [
    # 价格与成交
    ["P01", "价格", "公寓成交均价", "Average apartment price", "同步", "0", "Savills Middle East", "行业机构", SAV, "季度", "季末+约2周", "AED/sqft", "1,817（−4.8% QoQ）", "2026Q3", "2026-10-12", "季", "环比跌幅连续2季 >3% 视为转弱", V, "均价受成交结构影响，须与同质化口径并读"],
    ["P02", "价格", "公寓同质化价格变动", "Like-for-like apartment price change", "同步", "0", "Savills Middle East", "行业机构", SAV, "季度", "季末+约2周", "%", "−1.7% QoQ", "2026Q3", "2026-10-12", "季", "转负且连续2季 = 实质性回调", V, "比表观均价更接近真实资产价值变动"],
    ["P03", "价格", "公寓成交中位价", "Apartment median transacted price", "同步", "0", "PropertyIndex.ae（DLD 登记）", "行业机构", "https://www.propertyindex.ae/dubai-real-estate-prices", "月度", "次月上旬", "AED/sqft", "1,659（8,674 笔）", "2026-10", "2026-11-09", "月", "同比转负且连续3月 = 下行确认", PV, "原始登记中位率，非混合调整；与均价不可直接比较"],
    ["P04", "价格", "PIX© 混合调整价格指数", "PIX mix-adjusted price index", "同步", "0", "PropertyIndex.ae", "行业机构", PIX, "月度", "次月上旬", "指数点", "203.7（−0.9% MoM，−5.5% YoY）", "2026-10", "2026-11-02", "月", "同比 <−5% 且持续3月 = 红灯", PV, "10 月指数点位在 203.7/203.9/204.0 之间冲突，须取固定日期发布版"],
    ["P05", "价格", "ValuStrat 公寓资本价值指数", "ValuStrat Price Index (VPI) - Apartments", "同步", "0", "ValuStrat", "行业机构", VS, "月度/季度", "次月", "指数点", "公寓 168.1（−0.6% QoQ）；全市 218.6（−4.5% YoY）", "2026Q3", "2026-10", "月", "全市 VPI 同比 <−5% = 红灯", PV, "估值型指数（非成交均价），Q1 2021=100"],
    ["P06", "价格", "Property Monitor 城市指数", "Dubai City Index", "同步", "0", "Property Monitor", "行业机构", "https://www.sevencentury.com/market-insights/reports/monthly/dubai-property-market-report-september-2026", "月度", "滞后1月", "AED/sqft", "1,644（9月）；8月 1,632（−1.9% YoY）", "2026-09", "2026-10", "月", "距峰值跌幅 >5% = 黄灯", PV, "官方主站与方法论未取得，仅见英文经纪商转载，需核实原文"],
    ["P07", "成交", "住宅成交笔数与金额", "Residential transactions & value", "同步", "0", "DLD / Savills / Cavendish Maxwell", "行业机构", CM, "季度/月度", "季末+约2周", "笔 / AED bn", "Q3 ≈34,500 笔 / AED70.8bn（Savills）；≈33,949 笔 / AED72.58bn（DLD 口径）", "2026Q3", "2026-10", "月", "成交量同比 <−30% 连续2季 = 红灯", V, "各机构统计范围（住宅/全部物业）与截止日不同，不可混算"],
    ["P08", "成交", "期房成交占比", "Off-plan share of transactions", "领先", "3–9", "Cavendish Maxwell / Savills", "行业机构", CM, "季度", "季末+约2周", "%", "72.2%（笔数，Q3）", "2026Q3", "2026-11-02", "季", "占比快速下滑 >10pp = 投机退潮/现房转向", V, "期房≠一手、转售≠现房，登记程序口径"],
    ["P09", "成交", "二手/转售成交占比", "Secondary / resale share", "同步", "0", "DXBinteract / Savills", "行业机构", "https://dxbinteract.com/market-reports/2026/Q3", "季度", "季末+约2周", "%", "30.8%（笔数，Q3，DXBinteract 全物业）；≈29%（betterhomes）", "2026Q3", "2026-10-16", "季", "占比持续上升 = 流动性向现房集中", PV, "primary≠off-plan；resale≠ready"],
    ["P10", "成交", "豪宅成交量（>AED10m）", "Prime transactions above AED10m", "同步", "0", "Savills / Knight Frank", "行业机构", SAV, "季度", "季末+约2周", "笔", "669 笔（Q2 871 笔）", "2026Q3", "2026-10-12", "季", "连续2季下滑 >25% = 高端情绪转弱", V, "豪宅篮子各机构定义不同"],
    ["P11", "价格", "顶级公寓均价", "Prime apartment average price", "同步", "0", "Savills Middle East", "行业机构", SAV, "季度", "季末+约2周", "AED/sqft", "5,237（+4.0% YoY）", "2026Q3", "2026-10-12", "季", "同比转负 = 高端补跌信号", V, "与 ValuStrat prime VPI（−3.4% YoY）冲突，篮子不同"],
    ["P12", "价格", "门户挂牌要价指数", "Portal asking price index (Bayut / Property Finder)", "领先", "1–3", "Bayut / Property Finder", "挂牌门户", "https://offplaninsider.com/news/dubai-asking-prices-steady-q3-2026-bayut-56600-new-homes", "季度", "季末+约2周", "指数/%", "Q3 大体持平；部分板块 +1.55% YoY", "2026Q3", "2026-10-28", "季", "与登记价背离扩大 = 卖方预期未修正", PV, "挂牌价≠成交价；校正期以 DLD 登记为准；主报告 URL 未取得"],
    # 供需
    ["S01", "供需", "已交付住宅套数", "Residential units handed over", "同步", "0", "Cushman & Wakefield Core / Cavendish Maxwell", "行业机构", CW, "季度", "季末+约2周", "套", "9M 2026 累计 40,400（C&W）；CM 口径 38,000", "2026 9M", "2026-10-29", "季", "单季交付 >15,000 套 = 租金压力红灯", V, "各机构交付定义不同；无官方竣工登记，不可加总"],
    ["S02", "供需", "公寓占待交付比例", "Apartment share of scheduled supply", "领先", "0–6", "Cavendish Maxwell", "行业机构", CMH1, "半年度", "半年末+约4周", "%", "82.5%（H2 2026 计划交付）", "2026H2 计划", "2026-07-30", "季", ">80% = 中端公寓压力集中", V, "为计划口径，非实际交付"],
    ["S03", "供需", "2027 年计划交付", "Scheduled completions 2027", "领先", "12–24", "Cavendish Maxwell / C&W Core", "行业机构", CMH1, "半年度", "修订频繁", "套", "CM H1 版 162,500；CM Q1 版 146,400；C&W ≈60,000", "2027 计划", "2026-07-30", "季", "口径分歧 >20% 时以兑现率折算区间", PV, "同一机构半年内重设基线；三套口径不可比"],
    ["S04", "供需", "2028 年计划交付", "Scheduled completions 2028", "领先", "24–36", "Cavendish Maxwell", "行业机构", CMH1, "半年度", "修订频繁", "套", "CM H1 版 128,200；CM Q3 引述 155,700", "2028 计划", "2026-11-02", "年", "与上年版本偏离 >20% 需重算情景", PV, "计划量，非交付量"],
    ["S05", "供需", "2027–2030 管道总量", "Delivery pipeline 2027-2030", "领先", "24–48", "Savills Middle East", "行业机构", SAV, "季度", "季末+约2周", "套", ">525,000", "2027–2030 计划", "2026-10-12", "年", "仅作长期供给上限，不作短期预测", V, "为已公告/登记项目的 scheduled stock"],
    ["S06", "供需", "交付兑现率", "Materialisation rate (actual / scheduled)", "领先", "0–6", "Cavendish Maxwell / Knight Frank", "行业机构（二手转载）", "https://crescorealestate.ae/dubai-supply-2027-2028-handover-risk/", "季度/年度", "不定", "%", "41.3%（H1 2026）；48.9%（FY2025）；KF：2022–24 约 60%", "2026H1", "2026-08-07", "季", "兑现率 <45% = 供给冲击被显著推迟", PV, "CM 主报告 403；42.3% 可能与阿布扎比报告混淆，须核原文"],
    ["S07", "供需", "新推盘套数", "New project launches (units)", "领先", "当期+36", "Savills / Cavendish Maxwell", "行业机构", SAV, "季度", "季末+约2周", "套", "Q3 ≈5,000（Q2 ≈36,400）；9M ≈50,000（−64% YoY）", "2026Q3", "2026-10-12", "月", "同比 <−50% = 开发商主动收缩（缓冲未来供给）", V, "Savills Q2 36,400 与 CM H1 28,000 口径冲突"],
    ["S08", "供需", "住宅存量", "Residential stock", "同步", "0", "ValuStrat / DLD units register", "行业机构", DP_UNIT, "年度", "不定", "套", "≈977,000（ValuStrat 估算）；官方 dld_units 数据集", "2026", "2026-08-20", "年", "存量年增 >8% = 供给过剩风险", PV, "与 KF/REIDIN 635,319（2025F）统计域不同，不可并列"],
    ["S09", "供需", "常住人口", "Resident population", "领先", "3–12", "Dubai Data & Statistics Establishment (DDSE)", "官方一手", DD, "实时+年度基准", "年度基准滞后约7月", "百万人", "4.580（+7.5%）；日间峰值 6.392", "2025 年末", "2026-07-30", "季", "增速 <3% = 需求分母转弱", V, "行政登记式实时人口，非传统普查；≈4.8m（2026-09）仅媒体转述，官方未核验"],
    ["S10", "供需", "家庭户数", "Households", "领先", "3–12", "DDSE / Dubai Statistics Centre", "官方（数值未核验）", DSC, "年度", "滞后约9月", "户", "858,000（2025）vs 795,200（2024），+7.9%", "2025", "2026-09", "年", "家庭增速 <人口增速 = 居住密度上升、需求被高估", UV, "数值仅见英文媒体转述 DDSE；官方英文页面未取得"],
    ["S11", "供需", "建筑许可发放数", "Building permits issued", "领先", "24–48", "Dubai Municipality / Government of Dubai Media Office", "官方一手", DMO, "季度（不定期）", "季内发布", "份", "10,776（+12% YoY）", "2026Q1", "2026-03-25", "季", "同比 >+10% 连续2季 = 中期供给压力", V, "发布日期早于季末，属初步数据；Q2/Q3 2026 未检索到同类发布"],
    ["S12", "供需", "许可建筑面积", "Permitted built-up area", "领先", "24–48", "Dubai Municipality / Media Office", "官方一手", DMO, "季度（不定期）", "季内发布", "m²", "≈3.9 百万（+48% YoY）", "2026Q1", "2026-03-25", "季", "+48% 是比许可份数更强的远期供给信号", V, "同 S11，初步数据"],
    ["S13", "供需", "竣工证书", "Building completion certificates", "领先", "0–6", "Dubai Municipality / Media Office", "官方一手", DMO, "季度（不定期）", "季内发布", "份", "3,154", "2026Q1", "2026-03-25", "季", "环比大增 → 未来 1–2 季租金供应上行", V, "官方仅 Q1 发布被检索到"],
    ["S14", "供需", "住宅空置率", "Residential vacancy rate", "同步", "0", "无官方发布", "未取得", DUBAI_OPEN, "—", "—", "%", "无官方序列；第三方估算 4–8%（不可采信）", "2026", "—", "季", "无官方值时不进入信号合成", UV, "迪拜不发布全市统一官方空置率；第三方估算为营销模型"],
    ["S15", "供需", "DLD 单元登记数据集", "DLD Units open dataset", "同步", "0", "Dubai Pulse / DLD", "官方一手", DP_UNIT, "周度", "周", "条", "开放数据集（含户型、面积）", "持续", "持续", "季", "用于自建存量/户型结构口径", V, "CC BY 4.0；可用于交叉核验第三方存量估计"],
    ["S16", "供需", "DLD 成交登记数据集", "DLD Transactions open dataset", "同步", "0", "Dubai Pulse / DLD", "官方一手", DP_SALE, "周度", "周", "条", "自 2004 年起逐笔登记", "持续", "持续", "月", "一手校验所有第三方成交统计", V, "登记日期滞后于价格约定数周"],
    # 租赁
    ["R01", "租赁", "新签公寓租金中位数", "Median new apartment lease", "同步", "0", "DXBinteract / Peak Trust（DLD 登记）", "行业机构", PEAK, "月度/季度", "次月", "AED/年", "68,000（9月）；Q3 68,000 / 92 AED/sqft", "2026-09", "2026-10-06", "月", "连续3月下行 = 租金周期确认转弱", V, "2026-04 起 Ejari 不再记录卧室数，按面积段替代"],
    ["R02", "租赁", "续约公寓租金中位数", "Median renewed apartment lease", "同步", "0", "DXBinteract（DLD 登记）", "行业机构", "https://dxbinteract.com/market-reports/2026/Q3", "季度", "季末+约2周", "AED/年", "59,000 / 73 AED/sqft", "2026Q3", "2026-10-16", "季", "新签/续约价差收敛 = 搬家套利消失", PV, "页面更新日期自相矛盾（10-16 / 11-10），可能修订"],
    ["R03", "租赁", "平均租金", "Average residential rent", "同步", "0", "Cavendish Maxwell", "行业机构", KT, "月度", "次月上旬", "AED/sqft/年", "77.3（+5.5% YoY，2025-09 为 +11.5%）", "2026-09", "2026-11-02", "月", "同比增速跌破 0 = 红灯", PV, "全市住宅平均，非公寓专属；与新签中位 92 AED/sqft 口径不同"],
    ["R04", "租赁", "Ejari 登记合约总数", "Registered rental contracts", "同步", "0", "DLD / Cavendish Maxwell", "官方+行业", "https://dubailand.gov.ae/en/news-media/dubai-s-rental-market-charts-stable-trajectory-reflecting-integrated-regulatory-environment-and-sustained-public-confidence", "季度", "季末+约4周", "份", "Q3 >172,000；Q1 253,992（全物业，官方）", "2026Q3", "2026-11-02", "季", "总量连续2季下滑 >15% = 需求收缩", PV, "官方 Q1 为全物业口径；各来源统计域不同不可串成时间序列"],
    ["R05", "租赁", "新签 / 续约合约数", "New vs renewed contracts", "领先", "0–3", "Cavendish Maxwell / fäm", "行业机构", KT, "季度/月度", "次月", "份", "Q3 新签 77,700（+18.2% YoY）/ 续约 94,300（−10.6% YoY）", "2026Q3", "2026-11-02", "月", "新签连续超续约 = 租客迁移加速", PV, "2026-07 起新签 36 个月来首次超续约（fäm/DLD）"],
    ["R06", "租赁", "降租续约占比 ★", "Share of renewals with lower rent", "领先", "0–6", "Cavendish Maxwell", "行业机构（媒体转述）", KT, "季度", "季末+约4周", "%", "21.4%（Q3）vs 4.8%（Q1）", "2026Q3", "2026-11-02", "月", ">20% 红灯；>30% 且持续 = 租金下行加速", PV, "本机制最敏感的房东定价权指标；CM 原始 PDF 未取得"],
    ["R07", "租赁", "持平续约占比", "Share renewed at same rent", "同步", "0", "Cavendish Maxwell", "行业机构（媒体转述）", KT, "季度", "季末+约4周", "%", "38.7%", "2026Q3", "2026-11-02", "季", "与 R06 合并判读", PV, "Q2 数据未取得"],
    ["R08", "租赁", "涨租续约占比", "Share renewed with higher rent", "同步", "0", "Cavendish Maxwell", "行业机构（媒体转述）", KT, "季度", "季末+约4周", "%", "40.0%（Q1 为 59.4%）", "2026Q3", "2026-11-02", "季", "<40% = 定价权明显转弱", PV, "—"],
    ["R09", "租赁", "同质化新签租约价差", "Like-for-like new lease vs January", "领先", "0–3", "fäm Properties / DLD", "行业机构", KTF, "月度", "次月", "%", "−15.3%（8月）；续约仅约 −1%", "2026-08", "2026-09-23", "月", "价差 >10pp = 挂牌租金即将补跌", V, "RERA 指数允许低于基准的续约涨租，导致新签与续约背离"],
    ["R10", "租赁", "公寓毛收益率（登记口径）", "Gross apartment rental yield", "同步", "0", "Dubai Real Estate Data / Peak Trust", "行业机构", DRED, "滚动12月/季度", "次月", "%", "6.0%（登记 TTM）；6.2%（23 区中位，Q3）；6.6%（CM 问询口径）", "2026Q3", "2026-11-09", "月", "跌破 5.5% = 相对债券吸引力下降", PV, "三套口径并存；均为毛收益率，未扣空置/管理/融资"],
    ["R11", "租赁", "净收益率（仅扣物业费）", "Net yield after service charges", "同步", "0", "Peak Trust", "行业机构", PEAK, "季度", "次月", "%", "23 区中位 5.4%（区间 4.1–7.6%）", "2026Q3", "2026-10-06", "季", "毛净差 >1.5pp = 持有成本侵蚀", V, "仅扣 2023 Mollak 物业费；不含空置、维修、中介、利息"],
    ["R12", "租赁", "分区毛收益率", "Gross yield by community", "同步", "0", "Cavendish Maxwell / Bayut / DRED", "行业机构", DRED, "季度/月度", "次月", "%", "DIP 10.0｜国际城 9.0–9.3｜Production City 8.0–10.5｜JVC 7.1–7.4｜Business Bay 6.0–6.1｜Downtown 5.1–5.4｜Marina 5.0–5.5｜Palm 4.4–4.6", "2026Q3", "2026-11-02", "季", "价值区与核心区利差收窄 = 风险重定价", PV, "各来源口径（挂牌 vs 登记）不同，仅作横向分级"],
    ["R13", "租赁", "门户挂牌租金同比", "Asking rent change by community", "领先", "1–3", "Property Finder", "挂牌门户", PF, "季度", "季末+约2周", "%", "Downtown −21.7｜Marina −16.1｜Meydan −13.3｜Business Bay −12.5｜JVC −10.0｜Dubai Hills 0.0", "2026Q3", "2026-10-12", "季", "与登记租金背离 >10pp = 挂牌端仍未出清", PV, "挂牌≠签约；Downtown 登记口径仅 −11%"],
    ["R14", "租赁", "挂牌量 / 询盘比", "Listings vs enquiries per listing", "领先", "1–3", "Property Finder", "挂牌门户", PF, "月度", "次月", "%", "挂牌量 +55.1% YoY；询盘 +15.4%；单盘询盘 −23%", "2026-09", "2026-10-12", "月", "单盘询盘连续3月下行 = 租赁去化转弱", PV, "门户自有样本，非全市"],
    ["R15", "租赁", "Smart Rental Index 与法定涨幅上限", "DLD Smart Rental Index / rent cap", "同步", "0", "Dubai Land Department (RERA)", "官方一手", DLD_RI, "年度更新", "年度", "%", "低于指数 ≤10%→0%；11–20%→5%；21–30%→10%；31–40%→15%；>40%→20%", "现行", "官方 FAQ", "年", "规则修订 = 租金弹性结构性变化", PV, "官方 FAQ 称年度更新；商业来源称实时更新，以官方为准。无可下载指数时间序列"],
    ["R16", "租赁", "Ejari 租约开放数据集", "DLD rent contracts open dataset", "同步", "0", "Dubai Pulse / DLD", "官方一手", DP_RENT, "周度", "周", "条", "自 2001 年起逐笔登记，CC BY 4.0", "持续", "持续", "月", "自建新签/续约/降租占比，摆脱对媒体转述的依赖", V, "建议后续用此数据源自主复算 R06–R08"],
    ["R17", "租赁", "DLD 季度住宅价格指数", "DLD Residential Price Index (sales)", "同步", "0", "Dubai Land Department", "官方一手", DLD_IDX, "季度", "季末", "指数点", "官方季度销售价格指数", "持续", "持续", "季", "作为第三方价格指数的官方锚", V, "为销售价格指数，非租金指数"],
    # 宏观先行（官方英文）
    ["M01", "宏观先行", "CBUAE 基准利率", "CBUAE Base Rate (ODF)", "领先", "6–12", "Central Bank of the UAE", "官方一手", CB, "事件驱动（跟随 FOMC）", "0–1 日", "%", "3.900%", "2026-11-10", "2026-10-28（维持）", "月", "上调 25bp 即触发融资条件复核；转向降息为绿灯", V, "9 月由 3.65% 上调至 3.90%、9/17 生效仅见 WAM/媒体，官方页面未核验生效日"],
    ["M02", "宏观先行", "3 个月 EIBOR", "3-month EIBOR", "领先", "6–12", "Central Bank of the UAE", "官方一手", CBE, "每个工作日", "当日 12:15 UAE", "%", "4.364820%", "2026-11-10", "2026-11-10", "月", ">4.5% 红灯；<3.5% 绿灯", V, "浮动按揭定价基准；11/09 为 4.32138%，11/06 为 4.20677%"],
    ["M03", "宏观先行", "1 年期 EIBOR", "1-year EIBOR", "领先", "6–12", "Central Bank of the UAE", "官方一手", CBE, "每个工作日", "当日", "%", "4.603340%（11/02 曾达 5.222610）", "2026-11-10", "2026-11-10", "月", "与 3M 倒挂/跳升 = 银行资金压力", V, "11/02 单日异常值需关注"],
    ["M04", "宏观先行", "AED/USD 参考汇率", "AED/USD reference rate", "同步", "0", "Central Bank of the UAE", "官方一手", CBFX, "每日", "当日", "AED/USD", "3.6725", "2026-11-09", "2026-11-09", "年", "钉住汇率变动 = 系统性重定价", V, "迪拜资产对人民币投资者本质是美元资产"],
    ["M05", "宏观先行", "Fed 联邦基金目标区间", "Fed funds target range", "领先", "6–12", "U.S. Federal Reserve", "官方一手", FEDOCT, "每年 8 次", "决议当日 14:00 ET", "%", "3.75–4.00（维持，10-2 票；2 票主张加息 25bp）", "2026-10-28", "2026-10-28", "月", "点阵图/票型转鹰 = 红灯", V, "下次决议 2026-12-09；夏令时 22:00 迪拜 / 次日 02:00 北京；冬令时 23:00 迪拜 / 次日 03:00 北京"],
    ["M06", "宏观先行", "FOMC 会议与纪要日历", "FOMC calendar & minutes", "领先", "6–12", "U.S. Federal Reserve", "官方一手", FED, "每年 8 次", "纪要 +3 周", "—", "2026 剩余：12/08–09；纪要 12/30", "2026", "持续", "月", "会前一周预置监测窗口", V, "2027 首次暂定 01/26–27"],
    ["M07", "宏观先行", "银行信贷总额", "Gross bank credit", "领先", "6–12", "Central Bank of the UAE", "官方一手（数值经媒体转录）", CBMB, "月度", "约 5–6 周", "AED bn", "2,871.4（8月，+2.6% m/m）", "2026-08", "2026-10-06", "月", "同比转负 = 信用收缩红灯", PV, "CBUAE 页面数值未直接读取，采用 WAM 转录；无「房地产信贷」独立科目"],
    ["M08", "宏观先行", "银行存款总额", "Total bank deposits", "领先", "6–12", "Central Bank of the UAE", "官方一手（数值经媒体转录）", CBMB, "月度", "约 5–6 周", "AED bn", "3,534.8（8月，+0.7% m/m）", "2026-08", "2026-10-06", "月", "存款增速 <信贷增速 = 银行放贷能力受限", PV, "同上"],
    ["M09", "宏观先行", "货币供应 M1/M2/M3", "Money supply M1/M2/M3", "领先", "6–12", "Central Bank of the UAE", "官方一手（数值经媒体转录）", CBMB, "月度", "约 5–6 周", "AED bn", "1,038.9 / 2,919.9 / 3,465.6", "2026-08", "2026-10-06", "月", "M1 同比转负 = 流动性收缩", PV, "同上"],
    ["M10", "宏观先行", "季度经济评论 / 信贷景气调查", "Quarterly Economic Review / Credit Sentiment Survey", "领先", "6–12", "Central Bank of the UAE", "官方一手", CBQR, "季度", "季末前后", "—", "QER 2026-09（09/30）；CSS Q2（09/17）", "2026Q3", "2026-09-30", "季", "银行放贷标准收紧 = 领先负面", V, "QER 含 CPI/GDP 预测，与 IMF 口径需并列呈现"],
    ["M11", "宏观先行", "就业 / 失业率", "Employment / unemployment", "领先", "3–9", "DDSE / Digital Dubai；FCSC", "官方（无数值）", "https://www.digitaldubai.ae/newsroom/digital-dubai-launches-the-labour-force-survey-2026-to-strengthen-data-driven-labour-market-planning-and-decision-making", "不定期调查", "不定", "%", "2026 劳动力调查 10/13 启动（5,000 户），结果尚未发布", "2026", "2026-10-13", "季", "结果发布后立即纳入信号合成", UV, "最大数据盲区；市面「UAE 失业率 1.9%」无官方依据，禁止引用"],
    ["M12", "宏观先行", "UAE FDI 流入", "UAE inward FDI flows", "领先", "6–24", "UNCTAD (World Investment Report)", "官方一手（多边机构）", UNCTAD, "年度", "次年 6–7 月", "US$ m", "48,243（2025，+5.7%）；2024 45,637；2023 30,688", "2025", "2026-07", "年", "同比转负 = 中长期需求转弱", V, "WIR 2026 官方 PDF 直连受限，经官方 PDF 索引文本核验；绿地项目 1,562 个为政府新闻稿口径"],
    ["M13", "宏观先行", "FDI 存量与绿地项目", "FDI stock / greenfield projects", "领先", "6–24", "UAE Ministry of Investment（新闻稿）", "官方（经通讯社转载）", "https://www.zawya.com/en/press-release/government-news/uae-attracts-aed-1773bln-in-fdi-inflows-in-2025-ciq4f0bg", "年度", "次年", "AED / 个", "存量 AED1.171tn；绿地 1,562 个；就业 >65,000", "2025", "2026-07", "年", "绿地项目数下滑 = 外籍岗位创造放缓", PV, "非政府官网直发；与 UNCTAD 数值体系不同"],
    ["M14", "宏观先行", "CPI 通胀", "Consumer price inflation", "领先", "3–9", "CBUAE QER / IMF WEO", "官方一手", IMF, "季度 / 半年", "不定", "%", "CBUAE：2025 1.3%、2026F 1.8%、2027F 2.0%；IMF：2026F 2.5%", "2026F", "2026", "季", ">3% = 实际收益率受压", PV, "两套官方预测冲突，禁止合并为一个数值；FCSC 官方 CPI 序列未取得"],
    ["M15", "宏观先行", "实际 GDP 增长", "Real GDP growth", "领先", "3–9", "DDSE / CBUAE / IMF", "官方一手", IMF, "季度 / 半年 / 年度", "不定", "%", "迪拜 2025 +5.4%（DDSE）；UAE 2025 est. 5.6%、2026 ≈5.6%（CBUAE）；IMF 2026F 3.1%", "2025 / 2026F", "2026", "季", "官方预测分歧 >2pp 时采用区间而非点值", PV, "迪拜（emirate）与 UAE（federal）口径不同；IMF 与 CBUAE 分歧显著"],
    ["M16", "宏观先行", "Brent 原油价格", "Brent crude spot price", "领先", "6–18", "U.S. Energy Information Administration (EIA)", "官方一手", EIA, "月度 STEO", "每月上中旬", "US$/bbl", "2025 69；2026F 96；2027F 84（5月版 95 / 79）", "2026F", "2026", "季", "油价大跌 >25% = 财政与外籍就业风险", PV, "为年度均价与预测，非 2026-11-10 现货价；OPEC 官方序列未取得"],
    ["M17", "宏观先行", "国际过夜游客", "International overnight visitors", "领先", "3–9", "Dubai DET / Media Office", "官方一手", DMOT, "月度/不定期", "约 2 周", "百万人", "8月 0.869；1–8月 6.97；2025 全年 19.6（+5.0%）", "2026 1–8月", "2026-09-13", "季", "连续3月同比负增 = 短租收益与就业承压", V, "2026 处扰动修复期：3月酒店入住率仅 36%，8月 66%（为 2025-08 的 89%）"],
    ["M18", "宏观先行", "酒店入住率", "Hotel occupancy", "同步", "0", "Dubai DET / Media Office", "官方一手", DMOT, "月度/不定期", "约 2 周", "%", "66%（2026-08）；36%（2026-03）", "2026-08", "2026-09-13", "季", "<60% 且持续 = 短租需求红灯", V, "不宜用 2025 纪录外推 2026"],
    ["M19", "宏观先行", "迪拜实际 GDP（H1）", "Dubai real GDP H1", "同步", "0", "Digital Dubai", "官方（细节未取得）", "https://www.digitaldubai.ae/en/", "半年度", "约 1 月", "AED bn", "AED473bn（H1 2026 标题数据）", "2026H1", "2026-10-28", "半年", "增速转负 = 需求端红灯", UV, "仅取得标题，细项与增速未核验"],
    # 政策
    ["G01", "政策", "黄金签证房产门槛", "Golden Visa property threshold", "领先", "0–6", "UAE ICP / GDRFA / DLD（待核验）", "官方（未取得）", "https://u.ae/", "事件驱动", "不定", "AED", "常见引述 2,000,000；2026 放宽说法互相矛盾", "2026", "—", "年", "官方门槛调整即触发需求情景重算", UV, "仅见商业签证/中介网站且相互矛盾，禁止作为事实引用"],
    ["G02", "政策", "按揭 LTV 上限", "Mortgage LTV caps", "领先", "3–6", "Central Bank of the UAE（待核验）", "官方（未取得）", CB, "事件驱动", "不定", "%", "商业引述：首套 ≤AED5m 可至 80%，非居民 50–65%", "2026", "—", "年", "LTV 收紧 10pp 以上 = 成交量红灯", UV, "未取得 CBUAE 官方通告"],
    ["G03", "政策", "DLD 过户费与交易成本", "DLD transfer fee", "同步", "0", "Dubai Land Department（待核验）", "官方（未取得）", "https://dubailand.gov.ae/en/open-data/real-estate-data/", "事件驱动", "不定", "%", "常见引述 4%（未核验）", "2026", "—", "年", "费率变动影响短线交易成本", UV, "未取得官方英文页面"],
    ["G04", "政策", "期房资金托管制度", "Escrow / Oqood framework", "同步", "0", "Dubai Land Department / RERA（待核验）", "官方（未取得）", "https://dubailand.gov.ae/en/eservices/", "事件驱动", "不定", "—", "商业引述：2007 年第 8 号法", "现行", "—", "年", "监管收紧/放松影响开发商现金流与交付", UV, "未取得官方英文页面；不引用法条编号作为事实"],
    ["G05", "政策", "续约涨租 90 天通知规则", "90-day notice for contract changes", "同步", "0", "Dubai Land Department", "官方一手", DLD_FAQ, "事件驱动", "不定", "天", "90", "现行", "官方 FAQ", "年", "规则修订影响续约节奏", V, "官方 FAQ 明示；配合 Decree 43/2013 法定涨幅上限使用"],
]

ws = wb.create_sheet("指标台账")
ws.sheet_properties.tabColor = XL_PRIMARY
add_table(
    ws, headers, registry,
    title="指标台账｜四维体系（价格·供需·租赁·宏观先行）+ 政策｜基线 2026-11-10",
    widths=[8, 11, 24, 30, 10, 11, 26, 20, 46, 14, 14, 12, 34, 15, 16, 10, 40, 12, 44],
    wrap_cols=(3, 4, 7, 9, 13, 17, 19),
    hyperlink_col=9,
)
hdr_row, _d_start, d_end = 2, 3, 2 + len(registry)  # _d_start 保留解包位（当前未用）
ws.freeze_panes = "C3"
for col, options in {
    "E": '"领先,同步,滞后"',
    "H": '"官方一手,官方（无数值）,官方（数值未核验）,官方（经通讯社转载）,官方（细节未取得）,官方（未取得）,行业机构,行业机构（二手转载）,行业机构（媒体转述）,挂牌门户,官方+行业,未取得"',
    "P": '"月,季,半年,年"',
    "R": '"已核验,部分核验,未核验"',
}.items():
    dv = DataValidation(type="list", formula1=options, allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"{col}3:{col}{d_end}")
for txt, bg, fg in [("已核验", XL_GREEN_BG, XL_GREEN_FG), ("部分核验", XL_YELLOW_BG, XL_YELLOW_FG), ("未核验", XL_RED_BG, XL_RED_FG)]:
    ws.conditional_formatting.add(
        f"R3:R{d_end}",
        FormulaRule(formula=[f'$R3="{txt}"'], fill=PatternFill("solid", fgColor=bg), font=Font(color=fg, bold=True)),
    )


# ---------------------------------------------------------------- 官方来源清单
src_headers = ["序号", "机构（英文）", "机构中文", "来源级别", "数据类别", "官方英文URL", "发布频率", "典型时滞", "核验备注"]
sources = [
    [1, "Central Bank of the UAE (CBUAE)", "阿联酋央行", "官方一手", "基准利率/EIBOR/汇率/货币信贷/季度评论", CB, "日/月/季", "当日～6周", "已直连核验：Base Rate 3.900%、3M EIBOR 4.364820%、AED/USD 3.6725"],
    [2, "CBUAE – EIBOR Rates", "阿联酋央行 EIBOR", "官方一手", "各期限 EIBOR 每日定盘", CBE, "每个工作日", "当日 12:15 UAE", "已直连核验 2026-11-10 全期限"],
    [3, "CBUAE – Exchange Rates", "阿联酋央行汇率", "官方一手", "AED/USD 参考汇率", CBFX, "每日", "当日", "已核验"],
    [4, "CBUAE – Statistical Bulletin", "阿联酋央行统计公报", "官方一手", "银行资产/信贷/存款/M1-M3", CBMB, "月度", "约 5–6 周", "最新期 2026-08，发布 2026-10-06"],
    [5, "CBUAE – Banking Operations Statistics", "阿联酋银行业务统计", "官方一手", "银行业务分项", "https://centralbank.ae/en/research-and-statistics/latest-statistics/banking-operations-statistics/", "月度", "约 5–6 周", "与统计公报同期"],
    [6, "CBUAE – Quarterly Reports", "阿联酋央行季度报告", "官方一手", "QER、信贷景气调查、金融稳健指标", CBQR, "季度", "季末前后", "QER 2026-09 发布 09/30"],
    [7, "U.S. Federal Reserve – FOMC", "美联储 FOMC", "官方一手", "联邦基金目标区间/纪要/SEP/会议日历", FED, "每年 8 次", "决议当日", "已直连核验 2026-10-28 声明与 10-2 票型"],
    [8, "Government of Dubai Media Office", "迪拜政府媒体办公室", "官方一手", "建筑许可/竣工证书/游客与酒店数据", DMO, "不定期（季度）", "季内", "已直连核验 Q1 2026 许可 10,776 / +12%"],
    [9, "Government of Dubai Media Office – Tourism", "迪拜政府媒体办公室（旅游）", "官方一手", "国际过夜游客、入住率、客房夜", DMOT, "月度/不定期", "约 2 周", "已核验 2026 1–8 月 6.97m"],
    [10, "Digital Dubai / DDSE", "迪拜数字局 / 数据统计局", "官方一手", "实时人口、年度人口基准、GDP、家庭", DD, "实时+年度", "年度基准约 7 月", "已核验 4.580m（2025 末，+7.5%）"],
    [11, "Dubai Statistics Centre (DSC)", "迪拜统计中心", "官方一手", "人口与生命统计、住房与建筑年度表", DSC, "年度", "滞后约 1 年", "页面可见 2022 年度表；住房主题页可访问性未核验"],
    [12, "Dubai Municipality – Open Data", "迪拜市政厅开放数据", "官方一手", "建筑许可、项目、楼栋微观数据", DM_OPEN, "按数据集", "不定", "经 Dubai Pulse 提供，需查单数据集元数据"],
    [13, "Dubai Pulse / Dubai.ae Open Data", "迪拜开放数据门户", "官方一手", "数据集元数据、更新频率、使用条款", DUBAI_OPEN, "按数据集", "不定", "官方门户，英文"],
    [14, "Dubai Pulse – DLD rent contracts", "DLD 租约开放数据", "官方一手", "Ejari 逐笔租约（2001 起）", DP_RENT, "周度", "周", "CC BY 4.0；建议自主复算续约指标"],
    [15, "Dubai Pulse – DLD transactions", "DLD 成交开放数据", "官方一手", "逐笔成交登记（2004 起）", DP_SALE, "周度", "周", "CC BY 4.0；一手校验第三方统计"],
    [16, "Dubai Pulse – DLD units", "DLD 单元登记", "官方一手", "户型、面积、楼栋单元", DP_UNIT, "周度", "周", "存量/户型结构自建口径"],
    [17, "Dubai Land Department (DLD)", "迪拜土地局", "官方一手", "季度住宅价格指数、租金指数、FAQ、开放数据", DLD_IDX, "季度/事件", "季末/年度", "Smart Rental Index 官方称年度更新"],
    [18, "DLD – Rental Index e-service", "迪拜租金指数服务", "官方一手", "Smart Rental Index / 法定涨幅计算器", DLD_RI, "年度更新", "年度", "无公开可下载指数时间序列"],
    [19, "UNCTAD – World Investment Report", "联合国贸发会议", "官方一手（多边）", "UAE FDI 流入/流出/存量", UNCTAD, "年度", "次年 6–7 月", "WIR 2026：2025 流入 US$48,243m"],
    [20, "IMF – UAE country page", "国际货币基金组织", "官方一手（多边）", "实际 GDP / CPI 预测、Article IV", IMF, "半年/年度", "4月与10月 WEO", "2026F GDP 3.1%、CPI 2.5%"],
    [21, "U.S. EIA – Short-Term Energy Outlook", "美国能源信息署", "官方一手", "Brent 现货与预测", EIA, "月度", "每月上中旬", "2026F $96/b；为预测而非实时现货"],
    [22, "WAM (Emirates News Agency)", "阿联酋通讯社", "官方通讯社", "央行/人口/政策新闻稿", "https://www.wam.ae/en", "事件驱动", "当日", "9 月加息细节经 WAM 系英文转载，官方页面未直接检索到"],
    [23, "Federal Competitiveness & Statistics Centre (FCSC)", "阿联酋联邦竞争力与统计中心", "官方（URL 未取得）", "全国 CPI / GDP / 劳动力", "https://fcsc.gov.ae/en", "季度/月度", "未核验", "本次研究未取得官方英文序列 URL，标注为待补"],
]
ws = wb.create_sheet("官方来源清单")
add_table(ws, src_headers, sources, title="官方英文权威来源清单（经济指标唯一采信层）",
          widths=[7, 34, 24, 20, 36, 46, 14, 16, 46],
          wrap_cols=(2, 3, 5, 6, 9), hyperlink_col=6)
ws.freeze_panes = "C3"


# ---------------------------------------------------------------- 监测日历
cal_headers = ["周期", "时点", "监测任务", "需更新指标编号", "主要来源", "输出物", "升级/复核条件"]
calendar = [
    ["月度", "每月第 1 周", "抓取 EIBOR 全期限、基准利率、AED/USD", "M01–M04", "CBUAE", "月度简报·融资条件段", "3M EIBOR 月均变动 >25bp"],
    ["月度", "每月第 1 周", "读取 Fed 决议/纪要/票型与点阵图", "M05–M06", "Federal Reserve", "月度简报·外部利率段", "票型转鹰或 SEP 路径上移"],
    ["月度", "每月第 1 周", "CBUAE 货币与银行统计（滞后 5–6 周）", "M07–M09", "CBUAE Statistical Bulletin", "月度简报·信用段", "M1 同比转负 / 存贷增速倒挂"],
    ["月度", "每月第 2 周", "EIA STEO 油价与情景假设", "M16", "U.S. EIA", "月度简报·宏观段", "Brent 预测较上期调整 >15%"],
    ["月度", "每月第 2 周", "DLD 成交与 Ejari 开放数据增量", "S16 / R16", "Dubai Pulse / DLD", "月度数据底表", "成交登记连续 2 月同比 <−30%"],
    ["月度", "每月上旬", "月度价格指数（PIX© / ValuStrat / Property Monitor）", "P03–P06", "PropertyIndex / ValuStrat / Property Monitor", "月度简报·价格段", "≥2 个指数同时同比转负"],
    ["月度", "每月上旬", "登记租金中位、新签/续约、降租占比", "R01–R09", "Peak Trust / DXBinteract / CM", "月度简报·租赁段", "降租续约占比再升 >5pp"],
    ["月度", "每月中旬", "DET 游客与酒店入住率", "M17–M18", "Media Office / DET", "月度简报·需求段", "连续 3 月同比负增"],
    ["月度", "每月末", "生成《月度监测简报》并与上期逐项对比", "全部月度项", "本地台账 + 官方源", "reports/YYYY-MM_monthly.html", "任一红灯触发 → 专项复核"],
    ["季度", "季末+2 周", "Savills / CBRE / JLL / C&W / CM 季度报告交叉核验", "P01–P12 / S01–S08", "英文行业机构", "季度分析·市场段", "口径分歧 >20% 需列明并取 DLD 锚"],
    ["季度", "季末+2 周", "交付量、推盘量、兑现率重算", "S01–S07", "C&W Core / Cavendish Maxwell / Savills", "季度分析·供给段", "兑现率跌破 45% → 重算 2027 情景"],
    ["季度", "季末+2 周", "分区毛/净收益率与挂牌-登记背离", "R10–R14", "Peak Trust / Bayut / Property Finder", "季度分析·收益段", "毛净差 >1.5pp 或背离 >10pp"],
    ["季度", "季末+2 周", "Dubai Municipality 建筑许可/竣工证书发布", "S11–S13", "Government of Dubai Media Office", "季度分析·先行段", "许可面积同比 >+30%"],
    ["季度", "季末+2 周", "CBUAE 季度经济评论与信贷景气调查", "M10 / M14 / M15", "CBUAE Quarterly Reports", "季度分析·宏观段", "放贷标准收紧或 CPI 预测上修"],
    ["季度", "季末+3 周", "DLD 季度住宅价格指数与官方锚校验", "R17 / P07", "Dubai Land Department", "季度分析·官方锚", "官方指数与第三方方向相反"],
    ["季度", "季末+3 周", "先行信号矩阵重算与投资决策情景更新", "看板 / 信号规则", "本地台账", "reports/YYYY-Qn_quarterly.html", "信号矩阵由 3 绿 3 红转为红占多数"],
    ["年度", "每年 1 月", "上年度全年成交、交付、价格、租金复盘", "全部", "DLD / 行业机构 / 台账", "年度报告·复盘章", "实际交付与年初计划偏离 >30%"],
    ["年度", "每年 1 月", "重估交付兑现率与 3 年供给情景", "S03–S06", "CM / Savills / KF / C&W", "年度报告·供给情景", "2027/2028 计划量重设 >20%"],
    ["年度", "每年 4 月 / 10 月", "IMF WEO 与 Article IV 宏观基线更新", "M14–M15", "IMF", "年度报告·宏观段", "GDP 预测较上期调整 >1pp"],
    ["年度", "每年 6–7 月", "UNCTAD WIR：FDI 流入/存量/绿地项目", "M12–M13", "UNCTAD / UAE Ministry of Investment", "年度报告·资本流段", "FDI 同比转负"],
    ["年度", "每年 7–8 月", "DDSE 年度人口基准、家庭户数与劳动力调查", "S09–S10 / M11", "Digital Dubai / DSC / DDSE", "年度报告·需求段", "人口增速 <3% 或家庭增速 <人口增速"],
    ["年度", "每年 7–8 月", "DSC 住房与建筑年度统计（许可/竣工/存量）", "S08 / S11–S15", "Dubai Statistics Centre", "年度报告·供给存量段", "存量年增 >8%"],
    ["年度", "每年 12 月", "政策框架复核：签证、LTV、过户费、托管、租金规则", "G01–G05", "u.ae / CBUAE / DLD 官方英文页", "年度报告·政策段", "任一官方规则变更 → 立即重算需求情景"],
    ["年度", "每年 12 月", "信号阈值回测与指标增删、来源 URL 有效性巡检", "信号规则 / 官方来源清单", "本地台账", "reports/YYYY_annual.html + 台账新版", "阈值触发过密（>6 次/年）或过疏（0 次）"],
]
ws = wb.create_sheet("监测日历")
add_table(ws, cal_headers, calendar, title="月 / 季 / 年三级监测日历（自 2026 年 11 月起持续执行）",
          widths=[9, 16, 44, 24, 38, 40, 42], wrap_cols=(3, 4, 5, 6, 7))
ws.freeze_panes = "C3"
dv = DataValidation(type="list", formula1='"月度,季度,年度"', allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"A3:A{2 + len(calendar)}")


# ---------------------------------------------------------------- 信号规则
sig_rule_headers = ["编号", "监测对象", "绿灯（支持）", "黄灯（观察）", "红灯（警示）", "确认标准", "失真信号", "对应动作", "权重"]
rules = [
    ["K01", "3M EIBOR", "<3.50% 或连续 3 月下行", "3.50–4.50% 横盘", ">4.50% 或 3 月上行 >50bp", "月均连续 2 期同向，不用单日定盘", "季末/年末资金面扰动、单日跳价", "重算按揭月供与可负担性上限", "高"],
    ["K02", "Fed 票型 / 点阵图", "转向降息", "维持不变", "加息倾向或 2 票以上主张加息", "以 FOMC 声明与纪要双确认", "会议前媒体放风", "调整未来 4 季融资条件假设", "高"],
    ["K03", "许可建筑面积同比", "<0%", "0–30%", ">30% 连续 2 季", "以官方 Media Office 发布为准", "季内发布属初步数据，可能被修订", "上修 2–4 年后供给情景", "中"],
    ["K04", "交付兑现率", ">65%（供给被推迟）", "45–65%", "<45% 且计划量创高", "至少 2 家机构口径互证", "单机构重设基线", "重算 2027 实际交付区间", "高"],
    ["K05", "新推盘量同比", "<−50%（刹车）", "−50%～0%", ">+20% 连续 2 季", "Savills 与 CM 双源", "个别 mega-project 一次性入市", "调整 2029+ 供给压力", "中"],
    ["K06", "降租续约占比", "<10%", "10–20%", ">20% 或单季 +5pp 以上", "连续 2 季同向；优先用 Ejari 自主复算", "季末集中续约、样本切换", "下修租金与毛收益率预测", "高"],
    ["K07", "公寓成交中位价同比", ">+3%", "−3%～+3%", "<−5% 连续 3 月", "≥2 个独立指数同向", "成交结构变化（小户型占比）", "切换至同质化指数复核", "高"],
    ["K08", "成交量同比", ">−10%", "−10%～−30%", "<−30% 连续 2 季", "DLD 登记口径为准", "登记滞后数周、季末冲量", "下修去化速度与开发商现金流假设", "高"],
    ["K09", "现房成交金额占比", "持续上升", "横盘", "连续 2 季下滑", "以成交金额而非笔数", "个别大宗交易扰动", "评估流动性与期房溢价风险", "中"],
    ["K10", "登记口径毛收益率", ">7.0%", "5.5–7.0%", "<5.5%", "同一口径连续 2 期", "挂牌价估算与登记口径混用", "重算相对无风险利率的溢价", "中"],
    ["K11", "FDI 流入同比", ">+5%", "0–+5%", "<0%", "UNCTAD WIR 年度官方值", "绿地项目公告≠实际到账", "下修中长期外籍需求", "中"],
    ["K12", "人口 / 家庭户数增速", ">5%", "3–5%", "<3% 或家庭增速显著低于人口", "DDSE 官方年度基准", "实时人口 clock 与年度基准口径不同", "重估租赁需求分母", "高"],
    ["K13", "就业 / 失业", "就业净增", "数据待发布", "失业率上行", "2026 劳动力调查结果发布后立即纳入", "商业网站无官方依据的失业率", "补齐最大盲区并重跑信号合成", "中"],
    ["K14", "酒店入住率 / 游客", ">75% 且同比正增", "60–75%", "<60% 连续 3 月", "DET 官方月度/定期发布", "大型活动单月扰动", "下修短租与旅游就业假设", "低"],
    ["K15", "官方 GDP/CPI 预测分歧", "<1pp", "1–2pp", ">2pp 或方向相反", "CBUAE / IMF / DDSE 并列呈现", "emirate 与 federal 口径混用", "用区间而非点值，标注分歧", "中"],
]
ws = wb.create_sheet("信号规则")
add_table(ws, sig_rule_headers, rules, title="信号灯阈值与确认标准（含失真信号与动作）",
          widths=[8, 24, 26, 24, 30, 34, 34, 34, 9], wrap_cols=(2, 3, 4, 5, 6, 7, 8))
ws.freeze_panes = "C3"
dv = DataValidation(type="list", formula1='"高,中,低"', allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"I3:I{2 + len(rules)}")


# ---------------------------------------------------------------- 首期基线值
bl_headers = ["指标编号", "指标名称", "基线值", "单位", "统计周期", "来源机构", "来源级别", "发布日期", "核验状态", "备注"]
baseline = [
    ["P01", "公寓成交均价", "1,817", "AED/sqft", "2026Q3", "Savills", "行业机构", "2026-10-12", "已核验", "−4.8% QoQ"],
    ["P02", "公寓同质化价格变动", "−1.7", "% QoQ", "2026Q3", "Savills", "行业机构", "2026-10-12", "已核验", "真实贬值小于表观"],
    ["P03", "公寓成交中位价", "1,659", "AED/sqft", "2026-10", "PropertyIndex (DLD)", "行业机构", "2026-11-09", "部分核验", "8,674 笔"],
    ["P04", "PIX© 指数", "203.7", "点", "2026-10", "PropertyIndex", "行业机构", "2026-11-02", "部分核验", "−0.9% MoM / −5.5% YoY"],
    ["P05", "ValuStrat 全市 VPI", "218.6", "点", "2026Q3", "ValuStrat", "行业机构", "2026-10", "部分核验", "−4.5% YoY，首次年度下跌"],
    ["P07", "Q3 住宅成交", "34,500 / 70.8", "笔 / AED bn", "2026Q3", "Savills", "行业机构", "2026-10-12", "已核验", "−38% YoY / −46% YoY 金额"],
    ["P08", "期房成交占比", "72.2", "% 笔数", "2026Q3", "Cavendish Maxwell", "行业机构", "2026-11-02", "部分核验", "—"],
    ["P11", "顶级公寓均价", "5,237", "AED/sqft", "2026Q3", "Savills", "行业机构", "2026-10-12", "已核验", "+4.0% YoY"],
    ["S01", "9M 已交付住宅", "40,400", "套", "2026 1–9月", "C&W Core", "行业机构", "2026-10-29", "已核验", "CM 口径 38,000"],
    ["S05", "2027–2030 计划管道", ">525,000", "套", "2027–2030", "Savills", "行业机构", "2026-10-12", "已核验", "计划量，非交付量"],
    ["S06", "交付兑现率", "41.3", "%", "2026H1", "Cavendish Maxwell（二手）", "行业机构", "2026-08-07", "部分核验", "FY2025 为 48.9%"],
    ["S07", "9M 新推盘", "≈50,000", "套", "2026 1–9月", "Savills", "行业机构", "2026-10-12", "已核验", "−64% YoY"],
    ["S09", "常住人口", "4.580", "百万人", "2025 年末", "DDSE / Digital Dubai", "官方一手", "2026-07-30", "已核验", "+7.5% YoY"],
    ["S11", "建筑许可", "10,776", "份", "2026Q1", "Dubai Municipality", "官方一手", "2026-03-25", "已核验", "+12% YoY"],
    ["S12", "许可建筑面积", "≈3.9", "百万 m²", "2026Q1", "Dubai Municipality", "官方一手", "2026-03-25", "已核验", "+48% YoY"],
    ["S13", "竣工证书", "3,154", "份", "2026Q1", "Dubai Municipality", "官方一手", "2026-03-25", "已核验", "—"],
    ["R01", "新签公寓租金中位", "68,000", "AED/年", "2026-09", "Peak Trust (DLD)", "行业机构", "2026-10-06", "已核验", "同质化 +0.3% MoM"],
    ["R02", "续约公寓租金中位", "59,000", "AED/年", "2026Q3", "DXBinteract (DLD)", "行业机构", "2026-10-16", "部分核验", "—"],
    ["R03", "平均租金", "77.3", "AED/sqft/年", "2026-09", "Cavendish Maxwell", "行业机构", "2026-11-02", "部分核验", "+5.5% YoY（上年 +11.5%）"],
    ["R06", "降租续约占比", "21.4", "%", "2026Q3", "Cavendish Maxwell", "行业机构", "2026-11-02", "部分核验", "Q1 为 4.8%"],
    ["R09", "同质化新签租约 vs 1 月", "−15.3", "%", "2026-08", "fäm Properties / DLD", "行业机构", "2026-09-23", "已核验", "续约仅约 −1%"],
    ["R10", "公寓毛收益率", "6.0 / 6.2 / 6.6", "%", "2026Q3 / TTM", "DRED / Peak Trust / CM", "行业机构", "2026-11-02", "部分核验", "三套口径并列，均为毛口径"],
    ["R11", "净收益率（仅扣物业费）", "5.4", "% 中位", "2026Q3", "Peak Trust", "行业机构", "2026-10-06", "已核验", "区间 4.1–7.6%"],
    ["M01", "CBUAE 基准利率", "3.900", "%", "2026-11-10", "Central Bank of the UAE", "官方一手", "2026-10-28", "已核验", "维持；9 月加息细节未官方核验"],
    ["M02", "3M EIBOR", "4.364820", "%", "2026-11-10", "Central Bank of the UAE", "官方一手", "2026-11-10", "已核验", "11/09 为 4.321380"],
    ["M05", "Fed 目标区间", "3.75–4.00", "%", "2026-10-28", "U.S. Federal Reserve", "官方一手", "2026-10-28", "已核验", "10-2 票，2 票主张加息"],
    ["M07", "银行信贷总额", "2,871.4", "AED bn", "2026-08", "CBUAE（WAM 转录）", "官方一手", "2026-10-06", "部分核验", "+2.6% m/m"],
    ["M12", "UAE FDI 流入", "48,243", "US$ m", "2025", "UNCTAD WIR 2026", "官方一手", "2026-07", "已核验", "+5.7% YoY"],
    ["M15", "实际 GDP", "5.4 / 5.6 / 3.1", "%（迪拜2025 / UAE2025 / IMF2026F）", "2025 / 2026F", "DDSE / CBUAE / IMF", "官方一手", "2026", "部分核验", "三口径冲突，禁止合并"],
    ["M16", "Brent", "69 / 96 / 84", "US$/bbl（2025 / 2026F / 2027F）", "年度", "U.S. EIA STEO", "官方一手", "2026", "部分核验", "预测值，非现货"],
    ["M17", "国际游客", "6.97", "百万人（1–8月）", "2026 1–8月", "DET / Media Office", "官方一手", "2026-09-13", "已核验", "2025 全年 19.6m"],
    ["M18", "酒店入住率", "66", "%", "2026-08", "DET / Media Office", "官方一手", "2026-09-13", "已核验", "为 2025-08 的 89%"],
]
ws = wb.create_sheet("首期基线值")
add_table(ws, bl_headers, baseline, title="首期基线值（后续各期逐项对比的锚点｜2026-11-10）",
          widths=[11, 30, 22, 30, 18, 30, 18, 16, 12, 40], wrap_cols=(2, 4, 6, 10))
ws.freeze_panes = "C3"
dv = DataValidation(type="list", formula1='"已核验,部分核验,未核验"', allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"I3:I{2 + len(baseline)}")
for txt, bg, fg in [("已核验", XL_GREEN_BG, XL_GREEN_FG), ("部分核验", XL_YELLOW_BG, XL_YELLOW_FG), ("未核验", XL_RED_BG, XL_RED_FG)]:
    ws.conditional_formatting.add(
        f"I3:I{2 + len(baseline)}",
        FormulaRule(formula=[f'$I3="{txt}"'], fill=PatternFill("solid", fgColor=bg), font=Font(color=fg, bold=True)),
    )


# ---------------------------------------------------------------- 使用说明
ws = wb.create_sheet("使用说明")
ws.sheet_properties.tabColor = XL_LIGHT
notes = [
    ("文档定位", "本工作簿是「迪拜公寓住宅市场持续监测机制」的指标台账与数据字典，配套首期中文情报分析报告（HTML）与月/季/年三级自动化监测任务。"),
    ("基线日期", "2026-11-10（北京时间 / GMT+8）。所有「最新值」以该日可取得的最新已发布数据为准；当前周期未发布时使用最近已发布周期并标注数据时点。"),
    ("来源约束", "全部资料取自英文网站；经济指标数据一律取自官方英文权威渠道（CBUAE、Federal Reserve、Dubai Municipality / Media Office、Digital Dubai / DSC、DLD / Dubai Pulse、UNCTAD、IMF、U.S. EIA、DET）。中文来源一律排除。"),
    ("来源分级", "① 官方一手：政府/央行/统计机构/多边机构原始发布，可直接采信；② 行业机构：Savills、CBRE、JLL、C&W Core、Cavendish Maxwell、ValuStrat、Knight Frank 等英文报告；③ 挂牌门户：Bayut、Property Finder 仅作卖方预期；④ 媒体转述：须标注「需核实原文」，不得与官方一手同等处理。"),
    ("口径优先级", "成交登记（Dubai Pulse / DLD）> 同质化/混合调整指数 > 成交中位价 > 成交均价 > 挂牌要价指数。均价受成交结构影响；当口径冲突时以 DLD 登记与同质化指数为准，并显式列出分歧。"),
    ("核验状态", "已核验 = 官方或机构原始页面直连确认；部分核验 = 数值来自英文媒体/转载或官方页面未直接读取；未核验 = 官方确认未取得，不得作为事实引用。"),
    ("领先期定义", "「领先期」为分析性估计（非官方统计），指该指标变动传导至迪拜公寓价格/租金的典型时滞：利率 2–4 季、许可 8–16 季、就业/FDI 2–6 季、降租续约占比 0–2 季。"),
    ("更新流程", "每月/季/年自动化任务按「监测日历」抓取 → 回填「首期基线值」的对比列或新增期间行 → 按「信号规则」判定红黄绿灯 → 更新「看板」→ 生成中文 HTML 报告至 reports/ 目录。"),
    ("自动化任务", "三个循环任务：月度（每月 5 日 09:00 北京）、季度（1/4/7/10 月 8 日 09:00 北京）、年度（每年 1 月 15 日 09:00 北京）。任务提示词自带完整指标清单、官方英文源与输出路径，可独立运行。"),
    ("已知盲区", "① 无官方住宅空置率序列；② 2026 迪拜劳动力调查 10/13 才启动，就业/失业结果未发布；③ 迪拜无官方竣工登记，各机构交付口径不可加总；④ DLD Smart Rental Index 无可下载时间序列；⑤ 签证/LTV/过户费等政策阈值未取得官方英文页面；⑥ FCSC 官方 CPI/GDP 序列 URL 未取得。"),
    ("冲突处理", "同一指标多来源冲突时并列呈现、标注各自口径，禁止静默选取其一；官方 GDP 预测 CBUAE(~5.6%) 与 IMF(3.1%) 分歧显著，报告以区间呈现。"),
    ("版本记录", "v1.0 / 2026-11-10：首期基线，含 7 个工作表、69 项指标、23 个官方英文来源、24 条监测日历、15 条信号规则、32 项基线值。"),
]
ws.merge_cells("A1:B1")
ws["A1"] = "使用说明 · 迪拜公寓住宅市场持续监测指标台账"
ws["A1"].font = TITLE_FONT
ws["A1"].fill = PatternFill("solid", fgColor=XL_DARK)
ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[1].height = 32
ws["A2"], ws["B2"] = "项目", "说明"
style_header(ws, 2, 2)
for i, (k, v) in enumerate(notes, start=3):
    ws.cell(row=i, column=1, value=k)
    ws.cell(row=i, column=2, value=v)
style_body(ws, 3, 2 + len(notes), 2, wrap_cols=(2,))
for r in range(3, 3 + len(notes)):
    ws.cell(row=r, column=1).font = Font(name="Microsoft YaHei", size=10, bold=True, color=XL_DARK)
    ws.cell(row=r, column=1).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws.row_dimensions[r].height = 46
set_widths(ws, [18, 118])
ws.freeze_panes = "A3"

wb.save(OUT)
print("OK", OUT)
print("Sheets:", wb.sheetnames)
print("Registry rows:", len(registry))
