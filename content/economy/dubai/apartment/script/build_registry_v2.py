# -*- coding: utf-8 -*-
"""迪拜公寓住宅市场监测台账 v2.0 年度重置脚本（在 v1.0 基础上增量修订）

用法：python script/build_registry_v2.py [--force]

防覆盖保护：输出文件已存在时默认跳过；加 --force 才允许重写（重写前请确认
xlsx 无手工增量修订，否则会被本脚本基于 v1 快照的生成结果回滚）。
输入：data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_2026-11.xlsx（仓库相对）
输出：data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_2027-01.xlsx
"""
import sys
from copy import copy
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[5]  # 仓库根（content/<theme>/<region>/<category>/script/）
DATA_DIR = ROOT / "data" / "processed" / "economy" / "dubai" / "apartment"
SRC = str(DATA_DIR / "dubai_apartment_indicator_registry_2026-11.xlsx")
DST = str(DATA_DIR / "dubai_apartment_indicator_registry_2027-01.xlsx")

if Path(DST).exists() and "--force" not in sys.argv:
    print("SKIP", DST, "已存在（防覆盖保护；确认无手工增量后可用 --force 重写）")
    sys.exit(0)
if not Path(SRC).exists():
    print("ERROR 输入源不存在：", SRC, "（须先存在 v1.0 基线台账）")
    sys.exit(1)

FONT = "Microsoft YaHei"
NAVY = "16324F"
BLUE = "2F5597"
PALE = "F2F6FC"
LINE = "BFBFBF"

H_FONT = Font(name=FONT, size=10, bold=True, color="FFFFFF")
B_FONT = Font(name=FONT, size=9.5, color="1A1A1A")
TITLE_FONT = Font(name=FONT, size=14, bold=True, color="FFFFFF")
SUB_FONT = Font(name=FONT, size=9, color="404040")
thin = Side(style="thin", color=LINE)
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

STATUS_STYLE = {
    "硬红·完全": ("FFC7CE", "9C0006"),
    "硬红·方向": ("FFC7CE", "9C0006"),
    "预警红": ("FCE4D6", "C55A11"),
    "黄": ("FFEB9C", "9C6500"),
    "绿": ("C6EFCE", "006100"),
    "灰": ("EDEDED", "808080"),
    "未核验": ("FFC7CE", "9C0006"),
    "参考": ("EDEDED", "808080"),
    "数据底座": ("D9E2F3", "2F5597"),
    "已核验": ("C6EFCE", "006100"),
}


def clone_style(src, dst):
    dst.font = copy(src.font)
    dst.fill = copy(src.fill)
    dst.border = copy(src.border)
    dst.alignment = copy(src.alignment)
    dst.number_format = src.number_format
    dst.protection = copy(src.protection)


def style_new_header(ws, row, cols):
    for c in cols:
        cell = ws.cell(row=row, column=c)
        cell.font = H_FONT
        cell.fill = PatternFill("solid", fgColor=BLUE)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = 34


def style_new_body(ws, row, cols, wrap=True):
    for c in cols:
        cell = ws.cell(row=row, column=c)
        cell.font = B_FONT
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=wrap)
        cell.border = BORDER
        if row % 2 == 0:
            cell.fill = PatternFill("solid", fgColor=PALE)


def paint_status(cell):
    val = str(cell.value or "")
    for key, (bg, fg) in STATUS_STYLE.items():
        if val.startswith(key):
            cell.fill = PatternFill("solid", fgColor=bg)
            cell.font = Font(name=FONT, size=9, bold=True, color=fg)
            return


wb = load_workbook(SRC)
wb.properties.title = "迪拜公寓住宅市场持续监测指标台账 v2.0（2027 年度基线）"
wb.properties.subject = "Dubai Apartment Market Continuous Monitoring - Annual Reset 2026"
wb.properties.creator = "WorkBuddy Research"
wb.properties.description = "v2.0：2026 年度复盘重置；新增预警红线体系、年度基线2027、来源巡检列；指标 69→71。"

# ---------------------------------------------------------------- 看板
ws = wb["看板"]
ws["A1"] = "迪拜公寓住宅市场持续监测 · 年度复盘看板 v2.0（2027 年度基线）"
ws["A2"] = ("基线日期 2026-11-11（北京时间）｜年度复盘日 2026-11-11｜来源：英文网站；经济指标一律官方英文一手｜"
            "新增「硬红 / 预警红 / 黄 / 绿 / 灰」五态｜所有输出为中文")

ws["A4"], ws["A5"], ws["A6"] = "公寓登记中位价（YTD）", "AED 1,714/sqft", "2026-01-01 至 11-10 · 较 2025 年 −1.1% · DXBinteract（DLD 登记）"
ws["C4"], ws["C5"], ws["C6"] = "Q3 住宅成交量", "≈34,500 笔", "2026Q3 · Savills · 同比 −38% · 金额 AED 70.8bn（−46%）"
ws["E4"], ws["E5"], ws["E6"] = "公寓毛收益率（三口径）", "6.0 / 6.2 / 6.6%", "2026Q3 · DRED / Peak / CM · 净（仅扣物业费）中位 5.4%"
ws["G4"], ws["G5"], ws["G6"] = "9M 已交付", "40,400 套", "C&W Core · 2026-10-29 · 另 CM 38,000 / ValuStrat 33,000"

ws["A7"], ws["A8"], ws["A9"] = "CBUAE 基准利率", "3.900%", "2026-10-28 维持 · 官方一手"
ws["C7"], ws["C8"], ws["C9"] = "3 个月 EIBOR", "4.364820%", "2026-11-10 定盘 · 距硬红 13.5bp · 已越预警红"
ws["E7"], ws["E8"], ws["E9"] = "Fed 目标区间", "3.75%–4.00%", "2026-10-28 · 10–2 票，2 票主张加息"
ws["G7"], ws["G8"], ws["G9"] = "UAE 2025 FDI 流入", "US$48,243m", "UNCTAD WIR 2026 · 同比 +5.7%"

ws["A10"] = "先行信号矩阵（v2.0 五态判读）"
matrix = [
    ("CBUAE 基准利率 / 3M EIBOR", "3.900% / 4.3648%", "高位·越预警线", "预警红（K01）", "利率→按揭月供→购买力→成交量→价格", "2–4 季", "融资成本高位，距硬红 13.5bp；确认窗未完成", "官方一手"),
    ("Fed 政策倾向", "3.75–4.00%，2 票主张加息", "偏鹰", "硬红·方向（K02）", "Fed→IORB→CBUAE→EIBOR→按揭", "2–4 季", "声明确认；纪要 11-18 待双确认", "官方一手"),
    ("建筑许可 / 许可面积", "10,776 套许可 / +48% 面积", "扩张", "预警红（K03）", "许可→开工→2–4 年交付→租金与价格", "8–16 季", "仅 2026Q1 一季，无法确认「连续 2 季」", "官方一手"),
    ("新推盘量", "9M ≈50,000 套 / −64% 同比", "收缩", "绿灯（K05）", "推盘→3–4 年后交付 / 当期可售库存", "当期+长周期", "开发商主动刹车，缓冲 2029+ 供给", "行业机构"),
    ("FDI 流入", "US$48,243m（2025）/ +5.7%", "增长", "绿灯（K11）", "FDI→企业设立→外籍就业→家庭形成→需求", "2–6 季", "支撑长期自住与租赁需求", "官方一手"),
    ("人口 / 家庭形成", "4.580m（2025 末）/ +7.5%", "增长", "绿灯（K12）", "人口→家庭数→租赁需求→租金→价格", "1–4 季", "需求分母仍在扩张", "官方一手"),
    ("降租续约占比", "21.4%（Q3）vs 4.8%（Q1）", "恶化", "硬红·方向（K06）", "交付→空置竞争→议价权→租金→收益率", "0–2 季", "定价权快速流失；Q2 缺失，原始 PDF 未取得", "行业机构（媒体转述）"),
    ("就业 / 失业率", "2026 调查 10 月启动，结果未发布", "数据缺口", "灰灯（K13）", "就业→净迁入→家庭形成→租金", "1–3 季", "最大监测盲区，暂不可量化", "官方（无数值）"),
]
for i, row in enumerate(matrix, start=12):
    for j, val in enumerate(row, start=1):
        ws.cell(row=i, column=j, value=val)
    paint_status(ws.cell(row=i, column=4))

ws["A21"] = ("综合判断：周期由「高位放缓 → 结构性再平衡」修正为「高位钝化 → 供给延迟型再平衡」。"
             "v2.0 五态：硬红 4（1 完全 + 3 方向）/ 预警红 4 / 黄 2 / 绿 4 / 灰 1；"
             "核心 8 项矩阵为 2 硬红 + 2 预警红 + 3 绿 + 1 灰。风险方向未变，确认进度不足。")

# 预警红线总览（新增区块）
ws.merge_cells("A23:H23")
c = ws["A23"]
c.value = "预警红线体系（v2.0 新增）｜硬红 = 已确认/方向确认；预警红 = 已越线但确认未完成；灰 = 数据缺口"
c.font = TITLE_FONT
c.fill = PatternFill("solid", fgColor=NAVY)
c.alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[23].height = 26

headers = ["状态", "数量", "规则编号", "定义", "动作", "", "", ""]
for j, h in enumerate(headers, start=1):
    ws.cell(row=24, column=j, value=h)
style_new_header(ws, 24, range(1, 9))

tiers = [
    ("硬红·完全", 1, "K15", "越过硬红线且完成全部确认", "立即重算情景"),
    ("硬红·方向", 3, "K02、K04、K06", "越过硬红线且 ≥2 来源方向一致，完全确认未完成", "重算区间并标注确认缺口"),
    ("预警红", 4, "K01、K03、K07、K08", "已越预警红线，硬红确认未完成", "季度专项 + 补数据，不重算长期情景"),
    ("黄", 2, "K10、K14", "观察区间，方向未定或分化", "提高监测频率"),
    ("绿", 4, "K05、K09、K11、K12", "支持区间", "维持基线"),
    ("灰", 1, "K13", "官方数据缺口", "不进入信号合成"),
]
for i, row in enumerate(tiers, start=25):
    ws.cell(row=i, column=1, value=row[0])
    ws.cell(row=i, column=2, value=row[1])
    ws.cell(row=i, column=3, value=row[2])
    ws.cell(row=i, column=4, value=row[3])
    ws.cell(row=i, column=5, value=row[4])
    for j in range(1, 9):
        cell = ws.cell(row=i, column=j)
        cell.font = B_FONT
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cell.border = BORDER
    paint_status(ws.cell(row=i, column=1))

for col, w in {"A": 30, "B": 26, "C": 26, "D": 22, "E": 42, "F": 12, "G": 44, "H": 18}.items():
    ws.column_dimensions[col].width = w

# ---------------------------------------------------------------- 指标台账
ws = wb["指标台账"]
ws.unmerge_cells("A1:S1")
ws.merge_cells("A1:V1")
ws["A1"] = "指标台账｜四维体系（价格·供需·租赁·宏观先行）+ 政策｜v2.0 年度基线 2026-11-11（适用 2027 周期）"

new_headers = {
    "T": "对应信号规则",
    "U": "预警红线状态（v2.0）",
    "V": "v2.0 备注 / 校准",
}
for col, val in new_headers.items():
    cell = ws[f"{col}2"]
    cell.value = val
    clone_style(ws["S2"], cell)
ws.row_dimensions[2].height = 34

rows = {}
for r in range(3, ws.max_row + 1):
    v = ws.cell(row=r, column=1).value
    if v:
        rows[str(v).strip()] = r

# 实质更新
updates = {
    "P03": {"M": "1,659（8,671 笔）", "O": "2026-11-10（页面更新）"},
    "R01": {"M": "65,000（2026-10）；同质化 0.0%（230 组）", "N": "2026-10", "O": "2026-11-03",
            "I": "https://peaktrust.ae/insights/rent-yield-monitor/2026-10"},
    "M16": {"M": "2025 69；2026F 96；2027F 84；4Q26F 105；9 月现货 114", "O": "2026-10-06"},
    "S01": {"M": "9M 2026 累计 40,400（C&W）；CM 38,000；ValuStrat 33,000（至 9 月末）", "O": "2026-10-29"},
    "P06": {"S": "官方主站与方法论未取得，仅见英文经纪商转载；v2.0 降级为参考序列，不进入信号合成"},
    "S10": {"S": "数值仅见英文媒体转述 DDSE；官方英文页面未取得；v2.0 保留但降权，不进入信号合成"},
    "S12": {"C": "许可建筑面积（并入 S11）", "S": "v2.0 并入 S11，作为同一次发布的子项，不单独计权"},
    "S11": {"S": "v2.0 起含许可面积子项（原 S12）：≈390 万 m²、+48% YoY；Q2/Q3 2026 未检索到同类发布"},
    "M02": {"M": "4.364820%（11-06 4.20677；11-09 4.321380）"},
    "M05": {"M": "3.75–4.00（维持，10-2 票；Cook、Hammack 主张 +25bp）"},
}
for rid, cols in updates.items():
    if rid not in rows:
        continue
    r = rows[rid]
    for col, val in cols.items():
        ws[f"{col}{r}"] = val

signal_map = {
    "P01": ("K07（辅助）", "参考", "均价受结构影响，不作 K07 主序列"),
    "P02": ("K07", "预警红", "同质化 −1.7% QoQ；同比确认需 3 月"),
    "P03": ("K07", "预警红", "−5.5% YoY 仅 1 期，未满足连续 3 月"),
    "P04": ("K07", "预警红", "9 月发布页缺席，K07 连续性不足"),
    "P05": ("K07", "预警红", "估值型指数，与成交口径并列"),
    "P06": ("—", "参考", "v2.0 降级，不进入信号合成"),
    "P07": ("K08", "预警红", "−38% 仅 1 季，Q2 同口径缺失"),
    "P08": ("K09（辅助）", "黄", "期房占比高但现房金额在升"),
    "P09": ("K09", "绿", "现房 +18.5% QoQ，流动性向现房集中"),
    "P10": ("K09（辅助）", "黄", "豪宅成交连续回落，但非核心规则"),
    "P11": ("K07（高端）", "绿", "+4.0% YoY 与 ValuStrat prime −3.4% 冲突，并列"),
    "S01": ("K04", "硬红·方向", "三口径并列；兑现率单源"),
    "S02": ("K04（辅助）", "黄", "计划口径，非实际"),
    "S03": ("K04", "硬红·方向", "2027 计划区间化 60,000–162,500"),
    "S04": ("K04", "硬红·方向", "4 个月内修订 +21.4%，高频修订"),
    "S05": ("K04（辅助）", "硬红·方向", "仅作长期上限，不作短期预测"),
    "S06": ("K04", "硬红·方向", "41.3% 低于 FY2025 的 48.9%；主报告 403"),
    "S07": ("K05", "绿", "−64%，开发端主动刹车"),
    "S08": ("K12（辅助）", "黄", "第三方估算，非官方存量"),
    "S09": ("K12", "绿", "+7.5%；2026-09 约 4.8m 未核验"),
    "S10": ("K12（辅助）", "黄", "保留但降权；未核验"),
    "S11": ("K03", "预警红", "+12% 份数；仅 Q1 一季"),
    "S12": ("K03", "预警红", "并入 S11；+48% 面积，仅 Q1 一季"),
    "S13": ("K03（辅助）", "预警红", "竣工证书 3,154；仅 Q1 发布"),
    "S14": ("—", "灰", "无官方序列，不入信号合成"),
    "S15": ("数据底座", "数据底座", "自建存量/户型口径"),
    "S16": ("数据底座", "数据底座", "一手校验第三方成交"),
    "R01": ("K06（辅助）", "黄", "同质化 0.0%，总量跌来自结构"),
    "R02": ("K06（辅助）", "黄", "续约 59,000；页面日期矛盾"),
    "R03": ("K06（辅助）", "黄", "平均租金 +5.5%，增速放缓"),
    "R04": ("K06（辅助）", "黄", "各来源统计域不同，不可串序列"),
    "R05": ("K06（辅助）", "黄", "新签 77,700 / 续约 94,300"),
    "R06": ("K06", "硬红·方向", "21.4% > 20%；Q2 缺失、媒体转述"),
    "R07": ("K06（辅助）", "黄", "持平 38.7%"),
    "R08": ("K06（辅助）", "黄", "40.0%，处阈值临界"),
    "R09": ("K06（辅助）", "黄", "−15.3%；续约仅 −1%"),
    "R10": ("K10", "黄", "6.0–6.6% 高于 5.5%，低收益区已破线"),
    "R11": ("K10（辅助）", "黄", "净 5.4% 中位；毛净差 0.8–1.3pp"),
    "R12": ("K10（辅助）", "黄", "各来源口径不同，仅横向分级"),
    "R13": ("K06（辅助）", "黄", "挂牌端跌幅大于登记端，存在情绪超调"),
    "R14": ("K06（辅助）", "黄", "单盘询盘 −23%"),
    "R15": ("政策", "黄", "规则记录；无可下载序列"),
    "R16": ("数据底座", "数据底座", "v2.0 强制：自主复算 R06–R08"),
    "R17": ("数据底座", "数据底座", "官方销售价格指数锚"),
    "M01": ("K01", "预警红", "3.900%；9 月加息生效日未官方核验"),
    "M02": ("K01", "预警红", "4.364820%，已越预警红 4.35%"),
    "M03": ("K01（辅助）", "预警红", "1Y 4.603340%；11-02 异常值"),
    "M04": ("—", "绿", "钉住 3.6725，未变"),
    "M05": ("K02", "硬红·方向", "10–2 票；2 票主张加息"),
    "M06": ("K02", "硬红·方向", "纪要 11-18；12-08/09 含 SEP"),
    "M07": ("三级", "绿", "2026-08；+2.6% m/m"),
    "M08": ("三级", "绿", "2026-08；+0.7% m/m"),
    "M09": ("三级", "绿", "M1/M2/M3 2026-08"),
    "M10": ("三级", "绿", "QER 2026-09"),
    "M11": ("K13", "灰", "调查 2026-10-13 启动，结果未发布"),
    "M12": ("K11", "绿", "+5.7%（2025）"),
    "M13": ("K11（辅助）", "绿", "存量/绿地项目；部分核验"),
    "M14": ("K15", "硬红·完全", "CBUAE 1.8% vs IMF 2.5%，并列"),
    "M15": ("K15", "硬红·完全", "CBUAE 5.6% vs IMF 3.1%，差 2.5pp"),
    "M16": ("三级", "黄", "4Q26F 105；触发 >15% 复核"),
    "M17": ("K14", "黄", "1–8 月 6.97m；9/10 月缺席"),
    "M18": ("K14", "黄", "66%；仅高于预警线 1pp"),
    "M19": ("K15（辅助）", "黄", "仅标题数据 AED473bn，细项未核验"),
    "G01": ("政策", "未核验", "未取得官方英文页；禁止引用中介数值"),
    "G02": ("政策", "未核验", "未取得 CBUAE 官方通告"),
    "G03": ("政策", "未核验", "未取得 DLD 官方费率页"),
    "G04": ("政策", "未核验", "不引用法条编号作为事实"),
    "G05": ("政策", "已核验", "DLD 官方 FAQ 明示 90 天"),
}

for rid, (sig, status, note) in signal_map.items():
    if rid not in rows:
        continue
    r = rows[rid]
    for col, val in (("T", sig), ("U", status), ("V", note)):
        cell = ws[f"{col}{r}"]
        if cell.value is None:
            clone_style(ws[f"S{r}"], cell)
        cell.value = val
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    paint_status(ws[f"U{r}"])

# 新增指标 P13 / R18 / M20
new_rows = [
    ("P13", "价格", "期房-现房成交中位价差", "Off-plan vs ready median price spread", "同步", 0,
     "PropertyIndex.ae（DLD 登记）", "行业机构", "https://www.propertyindex.ae/dubai-real-estate-prices",
     "月度", "次月上旬", "%", "32.6%（1,760 vs 1,327）", "2026-10", "2026-11-10", "月",
     "价差半年收敛 >8pp = 期房溢价退潮", "已核验", "派生：期房中位 ÷ 现房中位 − 1；非官方指数",
     "K09（辅助）", "黄", "v2.0 新增；用于区分期房溢价与现房折价"),
    ("R18", "租赁", "Ejari 自主复算降租续约占比（派生）", "Self-computed share of renewals with lower rent (Ejari)",
     "领先", "0–6", "DLD / Dubai Pulse（R16 派生）", "官方一手（派生）",
     "https://www.dubaipulse.gov.ae/data/dld-registration/dld_rent_contracts-open",
     "月度（自建）", "周", "%", "未执行（v2.0 强制任务）", "2026-11", "—", "月",
     "同 R06：>20% 硬红；>15% 预警红", "待执行", "需下载全量 Ejari；2026-04 起无卧室数，按面积段配对",
     "K06", "灰", "v2.0 新增；目标替代 R06–R08 的媒体转述"),
    ("M20", "宏观先行", "Fed SEP 点阵图中位数", "FOMC SEP median dot", "领先", "6–12",
     "U.S. Federal Reserve", "官方一手", "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm",
     "季度（含 SEP 会议）", "决议当日", "%", "未取得（12-08/09 会议含 SEP）", "2026Q4", "—", "季",
     "中位数上移 ≥25bp = K02 强化", "未取得", "点阵图为委员匿名预测，非政策承诺",
     "K02", "灰", "v2.0 新增；用于 K02 路径判读"),
]
start = ws.max_row + 1
for i, row in enumerate(new_rows, start=start):
    for j, val in enumerate(row, start=1):
        cell = ws.cell(row=i, column=j, value=val)
        cell.font = B_FONT
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cell.border = BORDER
    paint_status(ws.cell(row=i, column=21))

# 删除 S12 行（已并入 S11），保持 71 项有效指标
if "S12" in rows:
    ws.delete_rows(rows["S12"], 1)

ws.auto_filter.ref = f"A2:V{ws.max_row}"
ws.freeze_panes = "C3"
for col, w in {"T": 14, "U": 16, "V": 34}.items():
    ws.column_dimensions[col].width = w

# ---------------------------------------------------------------- 信号规则
ws = wb["信号规则"]
ws.unmerge_cells("A1:I1")
ws.merge_cells("A1:O1")
ws["A1"] = "信号灯阈值与确认标准（v2.0：五态 + 三级红线组 + 预警红线）"

extra = {
    "J": "红线等级",
    "K": "预警红线（v2.0 新增）",
    "L": "当前读数（2026-11-10）",
    "M": "距硬红线",
    "N": "2026 可观测触发",
    "O": "v2.0 校准动作",
}
for col, val in extra.items():
    cell = ws[f"{col}2"]
    cell.value = val
    clone_style(ws["I2"], cell)

rule_rows = {str(ws.cell(row=r, column=1).value).strip(): r for r in range(3, ws.max_row + 1)}
rules = {
    "K01": ("一级", ">4.35% 或 3 月累计上行 >40bp", "4.364820%", "13.5bp（已越预警线 1.5bp）", "1 期（单日定盘）", "预警红；月均连续 2 期 ≥4.50% 升级硬红"),
    "K02": ("一级", "≥1 票主张加息", "2 票主张 +25bp", "已触发", "1 期（声明）", "硬红·方向；纪要 11-18 双确认"),
    "K03": ("二级", ">20% 单季", "+48%（2026Q1）", "超 18pp（仅 1 季）", "1 期", "预警红；第 2 季 >30% 升级硬红"),
    "K04": ("一级", "<50%", "41.3%（2026H1）", "低于 3.7pp", "1 期", "硬红·方向；补同口径双源"),
    "K05": ("三级", ">+10% 单季", "−64%（9M）", "远低于", "1 期", "绿灯；维持"),
    "K06": ("一级", ">15%", "21.4%（2026Q3）", "高出 1.4pp", "2 期（Q1/Q3）", "硬红·方向；补 Q2 与原始 PDF"),
    "K07": ("二级", "<−3% 连续 2 月", "−5.5% YoY（PIX 10 月）", "超 0.5pp（仅 1 期）", "1 期", "预警红；3 月 + 2 指数后升级"),
    "K08": ("一级", "<−20%", "−38% YoY（Q3）", "超 8pp（仅 1 季）", "1 期", "预警红；连续 2 季后升级"),
    "K09": ("三级", "单季下滑", "现房 +18.5% QoQ", "未触发", "1 期", "绿灯；按金额复核"),
    "K10": ("二级", "<6.0%", "6.0–6.6% 中位", "中位高于 0.5–1.1pp", "1 期", "黄灯；低收益区已破 5.5%"),
    "K11": ("二级", "<+2%", "+5.7%（2025）", "高于 5.7pp", "年度 1 期", "绿灯；2027-06/07 观察"),
    "K12": ("二级", "<5%", "+7.5%（2025 末）", "高于 4.5pp", "年度 1 期", "绿灯；家庭户数未核验"),
    "K13": ("三级", "结果发布后 30 日未入库", "未发布", "无法计算", "0 期", "灰灯；发布后立即入库"),
    "K14": ("三级", "<65%", "66%（2026-08）", "高于 6pp", "1 期", "黄灯；仅高于预警线 1pp"),
    "K15": ("二级", ">1.5pp", "GDP 5.6% vs 3.1%", "超 0.5pp", "1 期", "硬红·完全；并列呈现"),
}
for rid, vals in rules.items():
    r = rule_rows.get(rid)
    if not r:
        continue
    for col, val in zip(["J", "K", "L", "M", "N", "O"], vals):
        cell = ws[f"{col}{r}"]
        cell.value = val
        if cell.value:
            cell.font = B_FONT
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            cell.border = BORDER
    if r % 2 == 0:
        for col in ["J", "K", "L", "M", "N", "O"]:
            ws[f"{col}{r}"].fill = PatternFill("solid", fgColor=PALE)

ws.auto_filter.ref = f"A2:O{ws.max_row}"
for col, w in {"J": 9, "K": 30, "L": 24, "M": 22, "N": 16, "O": 34}.items():
    ws.column_dimensions[col].width = w

# ---------------------------------------------------------------- 官方来源清单
ws = wb["官方来源清单"]
ws.unmerge_cells("A1:I1")
ws.merge_cells("A1:L1")
ws["A1"] = "官方英文权威来源清单（经济指标唯一采信层）｜v2.0 含年度巡检状态"
for col, val in {"J": "最近巡检", "K": "巡检状态", "L": "频率变化 / 处置"}.items():
    cell = ws[f"{col}2"]
    cell.value = val
    clone_style(ws["I2"], cell)

audit = {
    1: ("2026-11-10", "有效", "Base Rate 3.900% / AEDUSD 3.6725 直连"),
    2: ("2026-11-10", "有效", "全期限可读；短端历史文件 404，不补值"),
    3: ("2026-11-09", "有效", "钉住 3.6725 未变"),
    4: ("2026-10-06", "聚合页有效", "最新 2026-08；直连 PDF 曾 404，改聚合页"),
    5: ("未单独核验", "待核验", "与统计公报同期；下期补"),
    6: ("2026-09-30", "有效", "QER 2026-09；Q3 QER 未发布"),
    7: ("2026-11-11", "有效", "10 月纪要 11-18；12-08/09 含 SEP"),
    8: ("2026-03-25", "有效但停更", "Q2/Q3 无同类发布；季度→不定期"),
    9: ("2026-09-13", "停更约 2 月", "9/10 月缺席；K14 无法判连续 3 月"),
    10: ("2026-07-30", "有效", "年度基准 4.580m；下一期 2027-07"),
    11: ("2026-09", "受限", "仅见 2022 年度表；住房主题页未核验"),
    12: ("未单独核验", "待核验", "经 Dubai Pulse 提供；需查数据集元数据"),
    13: ("2026-11-10", "有效", "数据集元数据入口"),
    14: ("2026-11-10", "有效", "CC BY 4.0；v2.0 要求自主复算 R06–R08"),
    15: ("2026-11-10", "有效", "2004 年起逐笔；一手校验成交"),
    16: ("2026-11-10", "有效", "自建存量/户型口径"),
    17: ("2026-11-10", "有效但无序列", "季度销售指数可读；无租金指数下载"),
    18: ("2026-11-10", "规则可读", "官方称年度更新；无下载序列"),
    19: ("2026-07", "直连受限", "PDF 返回验证页；经索引文本核验"),
    20: ("2026-10", "有效", "2026F GDP 3.1% / CPI 2.5%"),
    21: ("2026-10-06", "版本延迟", "11 月版未更新，不采用"),
    22: ("2026-10-06", "通讯社", "仅作官方新闻稿英文转载"),
    23: ("未取得", "未核验", "官方 CPI/GDP/劳动力序列 URL 未取得"),
}
for r in range(3, ws.max_row + 1):
    idx = ws.cell(row=r, column=1).value
    if idx in audit:
        vals = audit[idx]
        for col, val in zip(["J", "K", "L"], vals):
            cell = ws[f"{col}{r}"]
            cell.value = val
            cell.font = B_FONT
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            cell.border = BORDER
        paint_status(ws[f"K{r}"])

ws.auto_filter.ref = f"A2:L{ws.max_row}"
for col, w in {"J": 14, "K": 16, "L": 46}.items():
    ws.column_dimensions[col].width = w

# ---------------------------------------------------------------- 监测日历
ws = wb["监测日历"]
add_rows = [
    ("季度", "季末+3 周", "预警红线复核：K01/K03/K07/K08 的确认进度与升级判定", "K01/K03/K07/K08",
     "本地台账 + 官方源", "季度分析·红线段", "任一预警红升级 → 触发硬红情景重算"),
    ("年度", "每年 12 月", "预警红线体系校准、五态计数复核与硬红线版本记录", "全部 15 条",
     "本地台账", "reports/YYYY_annual.html + 台账新版", "硬红线数值变更须记录版本，不得事后改写"),
]
start = ws.max_row + 1
for i, row in enumerate(add_rows, start=start):
    for j, val in enumerate(row, start=1):
        cell = ws.cell(row=i, column=j, value=val)
        cell.font = B_FONT
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cell.border = BORDER
    if i % 2 == 0:
        for j in range(1, 8):
            ws.cell(row=i, column=j).fill = PatternFill("solid", fgColor=PALE)

# ---------------------------------------------------------------- 首期基线值（历史）
ws = wb["首期基线值"]
ws["A1"] = "首期基线值（历史锚｜2026-11-10）｜v2.0 起由「年度基线2027」承接"

# ---------------------------------------------------------------- 新增：预警红线
ws = wb.create_sheet("预警红线")
ws.sheet_properties.tabColor = "C55A11"
ws.merge_cells("A1:K1")
c = ws["A1"]
c.value = "预警红线体系 v2.0｜15 条信号规则五态判定（基线 2026-11-11）"
c.font = TITLE_FONT
c.fill = PatternFill("solid", fgColor=NAVY)
c.alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[1].height = 30

headers = ["编号", "监测对象", "红线等级", "绿灯线", "黄灯线", "预警红线（v2.0）", "硬红线",
           "当前读数", "距硬红线", "当前状态", "升级 / 触发动作"]
for j, h in enumerate(headers, start=1):
    ws.cell(row=2, column=j, value=h)
style_new_header(ws, 2, range(1, 12))

red_rows = [
    ("K01", "3M EIBOR", "一级", "<3.50% 或连续 3 月下行", "3.50–4.50% 横盘", ">4.35% 或 3 月累计上行 >40bp", ">4.50% 或 3 月上行 >50bp", "4.364820%", "13.5bp", "预警红", "月均连续 2 期 ≥4.50% → 硬红"),
    ("K02", "Fed 票型 / 点阵图", "一级", "转向降息", "维持不变", "≥1 票主张加息", "加息倾向或 ≥2 票主张加息", "2 票主张 +25bp", "已触发", "硬红·方向", "纪要 11-18 双确认 → 硬红·完全"),
    ("K03", "许可建筑面积同比", "二级", "<0%", "0–20%", ">20% 单季", ">30% 连续 2 季", "+48%（2026Q1）", "超 18pp（仅 1 季）", "预警红", "第 2 季 >30% → 硬红"),
    ("K04", "交付兑现率", "一级", ">65%", "50–65%", "<50%", "<45% 且计划量创高", "41.3%（2026H1）", "低于 3.7pp", "硬红·方向", "补同口径双源 → 硬红·完全"),
    ("K05", "新推盘量同比", "三级", "<−50%", "−50%～0%", ">+10% 单季", ">+20% 连续 2 季", "−64%（9M）", "远低于", "绿灯", "维持"),
    ("K06", "降租续约占比", "一级", "<10%", "10–15%", ">15%", ">20% 或单季 +5pp", "21.4%（2026Q3）", "高出 1.4pp", "硬红·方向", "补 Q2 与原始 PDF → 硬红·完全"),
    ("K07", "公寓中位价同比", "二级", ">+3%", "−3%～+3%", "<−3% 连续 2 月", "<−5% 连续 3 月", "−5.5% YoY（PIX）", "超 0.5pp（仅 1 期）", "预警红", "3 月 + 2 指数 → 硬红"),
    ("K08", "成交量同比", "一级", ">−10%", "−10%～−20%", "<−20%", "<−30% 连续 2 季", "−38% YoY（Q3）", "超 8pp（仅 1 季）", "预警红", "连续 2 季 → 硬红"),
    ("K09", "现房成交金额占比", "三级", "持续上升", "横盘", "单季下滑", "连续 2 季下滑", "现房 +18.5% QoQ", "未触发", "绿灯", "按金额复核"),
    ("K10", "登记口径毛收益率", "二级", ">7.0%", "6.0–7.0%", "<6.0%", "<5.5%", "6.0–6.6%（中位）", "高于 0.5–1.1pp", "黄", "低收益区已破 5.5%"),
    ("K11", "FDI 流入同比", "二级", ">+5%", "0～+5%", "<+2%", "<0%", "+5.7%（2025）", "高于 5.7pp", "绿灯", "2027-06/07 观察"),
    ("K12", "人口 / 家庭增速", "二级", ">5%", "3–5%", "<5%", "<3% 或家庭显著低于人口", "+7.5%（2025 末）", "高于 4.5pp", "绿灯", "家庭户数待核验"),
    ("K13", "就业 / 失业", "三级", "就业净增", "待发布", "结果发布后 30 日未入库", "失业率连续 2 期上行", "未发布", "无法计算", "灰", "发布后立即入库"),
    ("K14", "酒店入住率 / 游客", "三级", ">75% 且同比正增", "65–75%", "<65%", "<60% 连续 3 月", "66%（2026-08）", "高于 6pp", "黄", "仅高于预警线 1pp"),
    ("K15", "官方 GDP/CPI 分歧", "二级", "<1pp", "1–1.5pp", ">1.5pp", ">2pp 或方向相反", "GDP 5.6% vs 3.1%", "超 0.5pp", "硬红·完全", "并列呈现，区间替代点值"),
]
for i, row in enumerate(red_rows, start=3):
    for j, val in enumerate(row, start=1):
        ws.cell(row=i, column=j, value=val)
    style_new_body(ws, i, range(1, 12))
    paint_status(ws.cell(row=i, column=10))

widths = [8, 20, 8, 22, 20, 32, 28, 20, 18, 14, 38]
for j, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(j)].width = w
ws.freeze_panes = "C3"
ws.auto_filter.ref = f"A2:K{ws.max_row}"

# ---------------------------------------------------------------- 新增：年度基线2027
ws = wb.create_sheet("年度基线2027")
ws.sheet_properties.tabColor = "2F5597"
ws.merge_cells("A1:J1")
c = ws["A1"]
c.value = "年度基线 2027（v2.0）｜重置日 2026-11-11｜36 项长期锚｜后续各期对比基准"
c.font = TITLE_FONT
c.fill = PatternFill("solid", fgColor=NAVY)
c.alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[1].height = 30

headers = ["指标编号", "指标名称", "v2.0 基线值", "单位", "统计周期", "来源机构", "来源级别", "发布日期", "核验状态", "备注"]
for j, h in enumerate(headers, start=1):
    ws.cell(row=2, column=j, value=h)
style_new_header(ws, 2, range(1, 11))

base_rows = [
    ("P01", "公寓成交均价", "1,817", "AED/sqft", "2026Q3", "Savills", "行业机构", "2026-10-12", "已核验", "−4.8% QoQ"),
    ("P02", "公寓同质化价格变动", "−1.7", "% QoQ", "2026Q3", "Savills", "行业机构", "2026-10-12", "已核验", "真实贬值小于表观"),
    ("P03", "公寓成交中位价", "1,659", "AED/sqft", "2026-10", "PropertyIndex (DLD)", "行业机构", "2026-11-10", "已核验", "8,671 笔；期房 1,760 / 现房 1,327"),
    ("P04", "PIX© 指数", "203.7", "点", "2026-10", "PropertyIndex", "行业机构", "2026-11-02", "部分核验", "−0.9% MoM / −5.5% YoY；9 月发布页缺席"),
    ("P05", "ValuStrat VPI", "168.1 / 218.6", "点", "2026Q3", "ValuStrat", "行业机构", "2026-10", "部分核验", "公寓 / 全市；全市 −4.5% YoY"),
    ("P07", "Q3 住宅成交", "34,500 / 70.8", "笔 / AED bn", "2026Q3", "Savills", "行业机构", "2026-10-12", "已核验", "−38% / −46% YoY"),
    ("P08", "期房成交占比", "72.2", "% 笔数", "2026Q3", "Cavendish Maxwell", "行业机构", "2026-11-02", "部分核验", "媒体转述，需核实原文"),
    ("P09", "现房成交笔数", "9,491", "笔", "2026Q3", "ValuStrat", "行业机构", "2026-10", "部分核验", "现房 +18.5% QoQ；期房 −10.1%"),
    ("P11", "顶级公寓均价", "5,237", "AED/sqft", "2026Q3", "Savills", "行业机构", "2026-10-12", "已核验", "+4.0% YoY，与 ValuStrat prime 冲突"),
    ("S01", "9M 已交付住宅", "40,400", "套", "2026 1–9 月", "C&W Core", "行业机构", "2026-10-29", "已核验", "CM 38,000 / ValuStrat 33,000，不加总"),
    ("S03", "2027 计划交付区间", "60,000–162,500", "套", "2027 计划", "C&W / Cavendish Maxwell", "行业机构", "2026-10-29", "部分核验", "v2.0 区间化，禁用单点"),
    ("S05", "2027–2030 管道", ">525,000", "套", "2027–2030", "Savills", "行业机构", "2026-10-12", "已核验", "计划存量，非交付预测"),
    ("S06", "交付兑现率", "41.3", "%", "2026H1", "Cavendish Maxwell", "行业机构", "2026-08-07", "部分核验", "FY2025 48.9%；KF 2022–24 约 60%"),
    ("S07", "9M 新推盘", "≈50,000", "套", "2026 1–9 月", "Savills", "行业机构", "2026-10-12", "已核验", "−64% YoY；Q3 ≈5,000"),
    ("S08", "住宅存量", "≈977,000", "套", "2026", "ValuStrat", "行业机构", "2026-08-20", "部分核验", "估算值；可用 dld_units 自建"),
    ("S09", "常住人口", "4.580", "百万人", "2025 年末", "DDSE / Digital Dubai", "官方一手", "2026-07-30", "已核验", "+7.5%；日均峰值 6.392m"),
    ("S11", "建筑许可", "10,776", "份", "2026Q1", "Dubai Municipality", "官方一手", "2026-03-25", "已核验", "+12% YoY；v2.0 起含许可面积子项"),
    ("S12", "许可建筑面积", "≈3.9", "百万 m²", "2026Q1", "Dubai Municipality", "官方一手", "2026-03-25", "已核验", "+48%；并入 S11 计权"),
    ("R01", "新签公寓租金中位", "65,000", "AED/年", "2026-10", "Peak Trust (Ejari)", "行业机构", "2026-11-03", "已核验", "同质化 0.0%（230 组）"),
    ("R02", "续约公寓租金中位", "59,000", "AED/年", "2026Q3", "DXBinteract (DLD)", "行业机构", "2026-10-16", "部分核验", "73 AED/sqft/年"),
    ("R03", "平均租金", "77.3", "AED/sqft/年", "2026-09", "Cavendish Maxwell", "行业机构", "2026-11-02", "部分核验", "+5.5% YoY（上年 +11.5%）"),
    ("R06", "降租续约占比", "21.4", "%", "2026Q3", "Cavendish Maxwell", "行业机构", "2026-11-02", "部分核验", "Q1 4.8%；Q2 缺失"),
    ("R09", "同质化新签租约 vs 1 月", "−15.3", "%", "2026-08", "fäm / DLD", "行业机构", "2026-09-23", "已核验", "续约约 −1%"),
    ("R10", "公寓毛收益率", "6.0 / 6.2 / 6.6", "%", "2026Q3 / TTM", "DRED / Peak / CM", "行业机构", "2026-11-09", "部分核验", "三套口径并列"),
    ("R11", "净收益率（仅扣物业费）", "5.4", "% 中位", "2026Q3", "Peak Trust", "行业机构", "2026-10-06", "已核验", "区间 4.1–7.6%"),
    ("M01", "CBUAE 基准利率", "3.900", "%", "2026-10-28", "CBUAE", "官方一手", "2026-10-28", "已核验", "维持"),
    ("M02", "3M EIBOR", "4.364820", "%", "2026-11-10", "CBUAE", "官方一手", "2026-11-10", "已核验", "预警红 4.35 / 硬红 4.50"),
    ("M05", "Fed 目标区间", "3.75–4.00", "%", "2026-10-28", "Federal Reserve", "官方一手", "2026-10-28", "已核验", "10–2 票；2 票主张 +25bp"),
    ("M07", "银行信贷总额", "2,871.4", "AED bn", "2026-08", "CBUAE（通讯社转录）", "官方一手", "2026-10-06", "部分核验", "+2.6% m/m"),
    ("M12", "UAE FDI 流入", "48,243", "US$ m", "2025", "UNCTAD WIR 2026", "官方一手", "2026-07", "已核验", "+5.7%"),
    ("M14", "CPI 通胀", "1.8 / 2.5", "%", "2026F", "CBUAE / IMF", "官方一手", "2026-09-30", "部分核验", "两套官方并列"),
    ("M15", "实际 GDP 增长", "5.6 / 3.1", "%", "2026F", "CBUAE / IMF", "官方一手", "2026-09-30", "部分核验", "分歧 2.5pp，用区间"),
    ("M16", "Brent 原油", "96 / 84", "US$/bbl", "2026F / 2027F", "U.S. EIA", "官方一手", "2026-10-06", "已核验", "4Q26F 105；9 月现货 114"),
    ("M17", "国际过夜游客", "6.97", "百万人", "2026 1–8 月", "Dubai DET", "官方一手", "2026-09-13", "已核验", "9/10 月缺席"),
    ("M18", "酒店入住率", "66", "%", "2026-08", "Dubai DET", "官方一手", "2026-09-13", "已核验", "为 2025-08 的 89%"),
    ("G05", "续约涨租 90 天通知", "90", "天", "现行", "DLD", "官方一手", "官方 FAQ", "已核验", "唯一完成的政策核验项"),
]
for i, row in enumerate(base_rows, start=3):
    for j, val in enumerate(row, start=1):
        ws.cell(row=i, column=j, value=val)
    style_new_body(ws, i, range(1, 11))
    paint_status(ws.cell(row=i, column=9))

for j, w in enumerate([10, 26, 18, 13, 14, 24, 12, 13, 11, 42], start=1):
    ws.column_dimensions[get_column_letter(j)].width = w
ws.freeze_panes = "C3"
ws.auto_filter.ref = f"A2:J{ws.max_row}"

# ---------------------------------------------------------------- 使用说明
ws = wb["使用说明"]
for r in range(1, ws.max_row + 1):
    if ws.cell(row=r, column=1).value == "版本记录":
        ws.cell(row=r, column=2).value = (
            "v2.0 / 2026-11-11：年度复盘重置。新增「预警红线」工作表与「年度基线2027」；"
            "信号规则新增五态、三级红线组、15 条预警红线与 4 条确认窗；指标 69→71（+P13/R18/M20，S12 并入 S11）；"
            "来源清单新增巡检列；监测日历 24→26 行。硬红线数值全部不变。"
        )
        ws.insert_rows(r + 1)
        ws.cell(row=r + 1, column=1).value = "历史版本"
        ws.cell(row=r + 1, column=2).value = (
            "v1.0 / 2026-11-10：首期基线，7 个工作表、69 项指标、23 个官方英文来源、24 条监测日历、15 条信号规则、32 项基线值。"
        )
        break

for r in range(1, ws.max_row + 1):
    if ws.cell(row=r, column=1).value == "基线日期":
        ws.cell(row=r, column=2).value = (
            "v2.0 重置日 2026-11-11（北京时间 GMT+8），适用 2027 年度监测周期。"
            "所有「最新值」以 2026-11-10 可取得的最新已发布数据为准；当前周期未发布时使用最近已发布周期并标注数据时点。"
        )
    if ws.cell(row=r, column=1).value == "已知盲区":
        ws.cell(row=r, column=2).value = (
            "① 无官方住宅空置率序列；② 2026 迪拜劳动力调查 10/13 才启动，就业/失业结果未发布；"
            "③ 迪拜无官方竣工登记，各机构交付口径不可加总；④ DLD Smart Rental Index 无可下载时间序列；"
            "⑤ 签证/LTV/过户费等政策阈值未取得官方英文页面；⑥ FCSC 官方 CPI/GDP 序列 URL 未取得；"
            "⑦ 季度报告文件缺失（reports/ 仅有首期基线与 2026-11 月度 v2）；⑧ 预警红线尚未写入三个自动化任务提示词。"
        )
    if ws.cell(row=r, column=1).value == "更新流程":
        ws.cell(row=r, column=2).value = (
            "每月/季/年自动化任务按「监测日历」抓取 → 回填「年度基线2027」的对比列或新增期间行 → "
            "按「信号规则」判定硬红/预警红/黄/绿/灰五态 → 更新「看板」与「预警红线」→ 生成中文 HTML 报告至 reports/ 目录。"
        )

for r in range(3, ws.max_row + 1):
    for c in (1, 2):
        cell = ws.cell(row=r, column=c)
        cell.font = B_FONT
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cell.border = BORDER

# 工作表顺序
order = ["看板", "指标台账", "预警红线", "官方来源清单", "监测日历", "信号规则", "首期基线值", "年度基线2027", "使用说明"]
wb._sheets = [wb[name] for name in order]

wb.save(DST)
print("SAVED", DST)
print("SHEETS", [ws.title for ws in wb.worksheets])
for ws in wb.worksheets:
    print(ws.title, ws.max_row, ws.max_column)
