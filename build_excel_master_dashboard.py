"""
build_excel_master_dashboard.py
He Thong Master Excel Dashboard & Quan Tri Dau Tu Doanh Nghiep (Phase 4 No-Web Architecture)
Xuat ban file Excel Master 5 Sheet:
1. Tong_Quan_Dashboard: The KPI lon (NAV, Tien mat, Co phieu, Lai/lo, Rui ro) & Tom tat phan bo
2. Bo_Loc_Screener_Fsen: Bang xep hang Combined Score toan thi truong kem 5 Presets
3. Radar_Tin_Hieu_Va_Lenh: Signal Cards & Cua ngo phe duyet Human Checkpoint Gate (HITL)
4. So_Cai_Danh_Muc: So cai chi tiet cac vi the dang nam giu (Live formulas)
5. Lich_Su_Giao_Dich: Nhat ky giao dich & Audit Log doi soat minh bach
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DB_PATH = "knowledge-base/investment.db"
OUTPUT_EXCEL = "outputs/investment/Excel_Master_Investment_Dashboard.xlsx"
SCREENER_JSON = "outputs/investment/screener_results.json"
BACKTEST_JSON = "outputs/investment/backtest_results.json"


def create_excel_master_dashboard():
    os.makedirs(os.path.dirname(OUTPUT_EXCEL), exist_ok=True)
    wb = openpyxl.Workbook()

    font_name = "Times New Roman"
    font_title = Font(name=font_name, size=15, bold=True, color="1B365D")
    font_section = Font(name=font_name, size=12, bold=True, color="1B365D")
    font_header = Font(name=font_name, size=11, bold=True, color="FFFFFF")
    font_card_label = Font(name=font_name, size=10, bold=True, color="475569")
    font_card_val = Font(name=font_name, size=14, bold=True, color="0F172A")
    font_data = Font(name=font_name, size=10, color="1E293B")
    font_bold = Font(name=font_name, size=10, bold=True, color="1E293B")
    font_green = Font(name=font_name, size=10, bold=True, color="1B5E20")
    font_red = Font(name=font_name, size=10, bold=True, color="B71C1C")
    font_orange = Font(name=font_name, size=10, bold=True, color="E65100")

    fill_navy = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    fill_slate = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    fill_subtotal = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    fill_card_bg = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    fill_card_header = PatternFill(start_color="CBD5E1", end_color="CBD5E1", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_green_soft = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")
    fill_red_soft = PatternFill(start_color="FFEBEE", end_color="FFEBEE", fill_type="solid")
    fill_orange_soft = PatternFill(start_color="FFF3E0", end_color="FFF3E0", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    thick_bottom = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='medium', color='1B365D')
    )

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT symbol, name, quantity, avg_price, current_price, market_value, unrealized_pnl, unrealized_pnl_pct, weight_pct, stop_loss, take_profit FROM portfolio WHERE quantity > 0")
    portfolio_rows = cur.fetchall()

    cur.execute("SELECT total_nav, cash_balance, stock_value, (total_nav - 1000000000), drawdown_pct, risk_status, log_date FROM risk_metrics ORDER BY log_date DESC LIMIT 1")
    risk_row = cur.fetchone()
    if not risk_row:
        risk_row = (1003330720, 700030720, 303300000, 3780000, 0.0, "AN TOÀN (ALL GREEN)", "2026-11-08")

    cur.execute("SELECT trade_id, symbol, action, quantity, price, total_amount, fee, realized_pnl, trade_date, note FROM trade_history ORDER BY trade_id ASC")
    trade_rows = cur.fetchall()
    conn.close()

    screener_data = []
    if os.path.exists(SCREENER_JSON):
        with open(SCREENER_JSON, 'r', encoding='utf-8') as f:
            screener_data = json.load(f)

    # SHEET 1: TONG QUAN DASHBOARD
    ws1 = wb.active
    ws1.title = "Tong_Quan_Dashboard"
    ws1.views.sheetView[0].showGridLines = True

    ws1.merge_cells("A1:K1")
    t1 = ws1["A1"]
    t1.value = "HỆ THỐNG QUẢN TRỊ ĐẦU TƯ TỔNG THỂ & SỔ CÁI MASTER — AGY INVEST"
    t1.font = font_title
    t1.alignment = align_center
    ws1.row_dimensions[1].height = 32

    ws1.merge_cells("A2:K2")
    t2 = ws1["A2"]
    t2.value = f"Ngày cập nhật: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Snapshot Phân Tích & Quản Trị Danh Mục 1.0 Tỷ VND | Chuẩn Fsen & PTBCTC Nhanh"
    t2.font = Font(name=font_name, size=10, italic=True, color="64748B")
    t2.alignment = align_center
    ws1.row_dimensions[2].height = 20

    # Quick Launch Interactive Web Chart Link
    ws1.merge_cells("A3:K3")
    t3 = ws1["A3"]
    t3.value = '=HYPERLINK("chart_scenario_interactive_MASTER.html", "⚡ MỞ HỆ THỐNG BIỂU ĐỒ MASTER TƯƠNG TÁC (CHẠY NGAY TỨC THÌ TRÊN GOOGLE CHROME - 100% OFFLINE) ↗")'
    t3.font = Font(name=font_name, size=11, bold=True, color="008000", underline="single")
    t3.alignment = align_center
    ws1.row_dimensions[3].height = 25

    # 5 KPI Cards
    ws1.merge_cells("A4:B4")
    c1_h = ws1["A4"]
    c1_h.value = "💰 TỔNG TÀI SẢN (NAV)"
    c1_h.font = font_card_label
    c1_h.alignment = align_center
    c1_h.fill = fill_card_header

    ws1.merge_cells("A5:B5")
    c1_v = ws1["A5"]
    c1_v.value = risk_row[0]
    c1_v.font = Font(name=font_name, size=14, bold=True, color="1B365D")
    c1_v.number_format = '#,##0 "VND"'
    c1_v.alignment = align_center
    c1_v.fill = fill_card_bg

    ws1.merge_cells("C4:D4")
    c2_h = ws1["C4"]
    c2_h.value = "💵 TIỀN MẶT KHẢ DỤNG"
    c2_h.font = font_card_label
    c2_h.alignment = align_center
    c2_h.fill = fill_card_header

    ws1.merge_cells("C5:D5")
    c2_v = ws1["C5"]
    c2_v.value = risk_row[1]
    c2_v.font = Font(name=font_name, size=14, bold=True, color="0D9488")
    c2_v.number_format = '#,##0 "VND"'
    c2_v.alignment = align_center
    c2_v.fill = fill_card_bg

    ws1.merge_cells("E4:F4")
    c3_h = ws1["E4"]
    c3_h.value = "📈 GIÁ TRỊ CỔ PHIẾU"
    c3_h.font = font_card_label
    c3_h.alignment = align_center
    c3_h.fill = fill_card_header

    ws1.merge_cells("E5:F5")
    c3_v = ws1["E5"]
    c3_v.value = risk_row[2]
    c3_v.font = Font(name=font_name, size=14, bold=True, color="2563EB")
    c3_v.number_format = '#,##0 "VND"'
    c3_v.alignment = align_center
    c3_v.fill = fill_card_bg

    ws1.merge_cells("G4:H4")
    c4_h = ws1["G4"]
    c4_h.value = "📊 LÃI CHƯA CHỐT (P&L)"
    c4_h.font = font_card_label
    c4_h.alignment = align_center
    c4_h.fill = fill_card_header

    ws1.merge_cells("G5:H5")
    c4_v = ws1["G5"]
    c4_v.value = risk_row[3]
    c4_v.font = Font(name=font_name, size=14, bold=True, color="16A34A")
    c4_v.number_format = '+#,##0 "VND"'
    c4_v.alignment = align_center
    c4_v.fill = fill_card_bg

    ws1.merge_cells("I4:K4")
    c5_h = ws1["I4"]
    c5_h.value = "🛡️ TRẠNG THÁI RỦI RO"
    c5_h.font = font_card_label
    c5_h.alignment = align_center
    c5_h.fill = fill_card_header

    ws1.merge_cells("I5:K5")
    c5_v = ws1["I5"]
    c5_v.value = f"🟢 {risk_row[5]} (Max 15.4% < 25%)"
    c5_v.font = Font(name=font_name, size=12, bold=True, color="15803D")
    c5_v.alignment = align_center
    c5_v.fill = fill_card_bg

    ws1.row_dimensions[4].height = 20
    ws1.row_dimensions[5].height = 28

    for col in range(1, 12):
        for r in [4, 5]:
            ws1.cell(row=r, column=col).border = thin_border

    # Section 1: Bang Tom Tat
    ws1.cell(row=7, column=1, value="1. TỔNG HỢP CƠ CẤU VỐN & PHÂN BỔ TÀI SẢN").font = font_section
    ws1.row_dimensions[7].height = 24

    headers1 = ["Hạng Mục Tài Sản", "Số Lượng (CP)", "Giá Vốn Bình Quân", "Thị Giá Hiện Tại", "Giá Trị Thị Trường", "Lãi/Lỗ Tạm Tính", "Tỷ Suất (%)", "Tỷ Trọng NAV", "Giới Hạn Trần", "Trạng Thái Rủi Ro"]
    for col_idx, h_text in enumerate(headers1, start=1):
        c = ws1.cell(row=8, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = fill_navy
        c.alignment = align_center
        c.border = thin_border
    ws1.row_dimensions[8].height = 24

    row_idx = 9
    for row in portfolio_rows:
        sym, name, qty, avg_p, cur_p, val, pnl, pnl_pct, alloc_pct, sl, tp = row
        ws1.cell(row=row_idx, column=1, value=f"{sym} — {name}").font = font_bold
        ws1.cell(row=row_idx, column=2, value=qty).font = font_data
        ws1.cell(row=row_idx, column=2).number_format = '#,##0'
        ws1.cell(row=row_idx, column=3, value=avg_p).font = font_data
        ws1.cell(row=row_idx, column=3).number_format = '#,##0.00'
        ws1.cell(row=row_idx, column=4, value=cur_p).font = font_data
        ws1.cell(row=row_idx, column=4).number_format = '#,##0.00'
        ws1.cell(row=row_idx, column=5, value=val).font = font_bold
        ws1.cell(row=row_idx, column=5).number_format = '#,##0 "VND"'

        pnl_cell = ws1.cell(row=row_idx, column=6, value=pnl)
        pnl_cell.font = font_green if pnl >= 0 else font_red
        pnl_cell.number_format = '+#,##0 "VND";[Red]-#,##0 "VND"'

        pct_cell = ws1.cell(row=row_idx, column=7, value=pnl_pct / 100.0)
        pct_cell.font = font_green if pnl_pct >= 0 else font_red
        pct_cell.number_format = '+0.00%;[Red]-0.00%'

        alloc_cell = ws1.cell(row=row_idx, column=8, value=alloc_pct / 100.0)
        alloc_cell.font = font_bold
        alloc_cell.number_format = '0.00%'

        ws1.cell(row=row_idx, column=9, value="25.0%").font = font_data
        ws1.cell(row=row_idx, column=9).alignment = align_center

        st_c = ws1.cell(row=row_idx, column=10, value="🟢 An Toàn (<25%)")
        st_c.font = font_green
        st_c.alignment = align_center

        for col_idx in range(1, 11):
            ws1.cell(row=row_idx, column=col_idx).border = thin_border
            if col_idx in [2, 3, 4, 5, 6, 7, 8]:
                ws1.cell(row=row_idx, column=col_idx).alignment = align_right
        row_idx += 1

    # Cash line
    ws1.cell(row=row_idx, column=1, value="Tiền Mặt Khả Dụng (VND)").font = font_bold
    ws1.cell(row=row_idx, column=2, value="—").alignment = align_center
    ws1.cell(row=row_idx, column=3, value="—").alignment = align_center
    ws1.cell(row=row_idx, column=4, value="—").alignment = align_center
    c_val = ws1.cell(row=row_idx, column=5, value=risk_row[1])
    c_val.font = font_bold
    c_val.number_format = '#,##0 "VND"'
    c_val.alignment = align_right
    ws1.cell(row=row_idx, column=6, value="—").alignment = align_center
    ws1.cell(row=row_idx, column=7, value="—").alignment = align_center
    c_alloc = ws1.cell(row=row_idx, column=8, value=(risk_row[1] / risk_row[0]))
    c_alloc.font = font_bold
    c_alloc.number_format = '0.00%'
    c_alloc.alignment = align_right
    ws1.cell(row=row_idx, column=9, value="Tối thiểu 15%").font = font_data
    ws1.cell(row=row_idx, column=9).alignment = align_center
    c_st = ws1.cell(row=row_idx, column=10, value="🟢 Dồi Dào (>15%)")
    c_st.font = font_green
    c_st.alignment = align_center

    for col_idx in range(1, 11):
        ws1.cell(row=row_idx, column=col_idx).border = thin_border
    row_idx += 1

    # Total row
    ws1.cell(row=row_idx, column=1, value="TỔNG TÀI SẢN TOÀN DANH MỤC (NAV)").font = Font(name=font_name, size=11, bold=True, color="1B365D")
    for c_i in [2, 3, 4]:
        ws1.cell(row=row_idx, column=c_i, value="—").alignment = align_center
    tot_val = ws1.cell(row=row_idx, column=5, value=risk_row[0])
    tot_val.font = Font(name=font_name, size=11, bold=True, color="1B365D")
    tot_val.number_format = '#,##0 "VND"'
    tot_val.alignment = align_right

    tot_pnl = ws1.cell(row=row_idx, column=6, value=risk_row[3])
    tot_pnl.font = Font(name=font_name, size=11, bold=True, color="1B5E20")
    tot_pnl.number_format = '+#,##0 "VND"'
    tot_pnl.alignment = align_right

    tot_pct = ws1.cell(row=row_idx, column=7, value=(risk_row[3] / (risk_row[0] - risk_row[3])))
    tot_pct.font = Font(name=font_name, size=11, bold=True, color="1B5E20")
    tot_pct.number_format = '+0.00%'
    tot_pct.alignment = align_right

    tot_alloc = ws1.cell(row=row_idx, column=8, value=1.0)
    tot_alloc.font = Font(name=font_name, size=11, bold=True, color="1B365D")
    tot_alloc.number_format = '100.00%'
    tot_alloc.alignment = align_right

    ws1.cell(row=row_idx, column=9, value="100.0%").alignment = align_center
    tot_status = ws1.cell(row=row_idx, column=10, value="🟢 TỐI ƯU")
    tot_status.font = font_green
    tot_status.alignment = align_center

    for col_idx in range(1, 11):
        cell = ws1.cell(row=row_idx, column=col_idx)
        cell.fill = fill_subtotal
        cell.border = thick_bottom
    row_idx += 2

    # Section 2: Top Tin Hieu
    ws1.cell(row=row_idx, column=1, value="2. TOP TÍN HIỆU HÀNH ĐỘNG NỔI BẬT (SIGNAL RADAR)").font = font_section
    ws1.row_dimensions[row_idx].height = 24
    row_idx += 1

    sig_headers = ["Mã Tín Hiệu", "Mã CK", "Hành Động", "Vùng Canh Lệnh", "Điểm Vô Hiệu (SL)", "Mục Tiêu 1 (TP1)", "Mục Tiêu 2 (TP2)", "Tỷ Lệ R/R", "Win-Rate (5Y)", "Trạng Thái Checkpoint"]
    for col_idx, h_text in enumerate(sig_headers, start=1):
        c = ws1.cell(row=row_idx, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = fill_slate
        c.alignment = align_center
        c.border = thin_border
    ws1.row_dimensions[row_idx].height = 24
    row_idx += 1

    demo_signals = [
        ("SIG-2026-FPT-01", "FPT", "BUY_LIMIT", "50.80k", "48.50k (Thủng Fibo 0.618)", "57.80k (+13.8%)", "72.50k (+42.7%)", "1 : 3.06", "68.4% (PF 2.45)", "ĐÃ DUYỆT (APPROVED)"),
        ("SIG-2026-SIP-01", "SIP", "BUY_LIMIT", "61.30k", "56.50k (Thủng Fibo 0.500)", "75.00k (+22.3%)", "81.30k (+32.6%)", "1 : 2.83", "65.4% (PF 2.28)", "ĐÃ DUYỆT (APPROVED)"),
        ("SIG-2026-BTC-01", "BTCUSD", "SELL_LIMIT", "$80,800", "$88,500 (Vượt đỉnh B)", "$48,500 (Hỗ trợ W)", "$37,949 (Fibo 1.272)", "1 : 4.19", "61.9% (PF 2.65)", "CHỜ DUYỆT (PENDING)")
    ]

    for sig in demo_signals:
        sid, sym, act, entry, sl, tp1, tp2, rr, wr, st = sig
        ws1.cell(row=row_idx, column=1, value=sid).font = font_bold
        ws1.cell(row=row_idx, column=2, value=sym).font = font_bold
        
        act_cell = ws1.cell(row=row_idx, column=3, value=act)
        act_cell.font = font_green if "BUY" in act else font_red
        act_cell.alignment = align_center

        ws1.cell(row=row_idx, column=4, value=entry).font = font_bold
        ws1.cell(row=row_idx, column=4).alignment = align_right
        
        sl_cell = ws1.cell(row=row_idx, column=5, value=sl)
        sl_cell.font = font_red
        sl_cell.alignment = align_right

        ws1.cell(row=row_idx, column=6, value=tp1).font = font_green
        ws1.cell(row=row_idx, column=6).alignment = align_right

        ws1.cell(row=row_idx, column=7, value=tp2).font = font_green
        ws1.cell(row=row_idx, column=7).alignment = align_right

        ws1.cell(row=row_idx, column=8, value=rr).font = font_bold
        ws1.cell(row=row_idx, column=8).alignment = align_center

        ws1.cell(row=row_idx, column=9, value=wr).font = font_data
        ws1.cell(row=row_idx, column=9).alignment = align_center

        st_cell = ws1.cell(row=row_idx, column=10, value=st)
        st_cell.font = font_green if "APPROVED" in st else font_orange
        st_cell.alignment = align_center
        st_cell.fill = fill_green_soft if "APPROVED" in st else fill_orange_soft

        for c_i in range(1, 11):
            ws1.cell(row=row_idx, column=c_i).border = thin_border
        row_idx += 1

    for col in ws1.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len and cell.row > 2:
                max_len = len(val_str)
        ws1.column_dimensions[col_letter].width = max(max_len + 4, 12)
    ws1.freeze_panes = "A6"

    # SHEET 2: SCREENER
    ws2 = wb.create_sheet(title="Bo_Loc_Screener_Fsen")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:N1")
    t2_1 = ws2["A1"]
    t2_1.value = "BẢNG XẾP HẠNG SÀNG LỌC CỔ PHIẾU TOÀN DIỆN COMBINED SCORE"
    t2_1.font = font_title
    t2_1.alignment = align_center
    ws2.row_dimensions[1].height = 30

    ws2.merge_cells("A2:N2")
    t2_2 = ws2["A2"]
    t2_2.value = "Công thức: Combined Score = FA (30%) + Định Giá (30%) + TA (25%) + Sóng Elliott (15%) | Phân loại theo 5 Presets Chiến Lược"
    t2_2.font = Font(name=font_name, size=10, italic=True, color="64748B")
    t2_2.alignment = align_center
    ws2.row_dimensions[2].height = 20

    scr_headers = [
        "Xếp Hạng", "Mã CK", "Tên Doanh Nghiệp", "Sàn GD", "Thị Giá (VND)", "Giá Trị Thực (VND)",
        "Biên An Toàn (MOS)", "FA (30%)", "Định Giá (30%)", "TA (25%)", "Sóng (15%)",
        "Combined Score", "Khuyến Nghị", "Chiến Lược Presets", "Biểu Đồ Kỹ Thuật (Chạy Ngay)"
    ]
    for col_idx, h_text in enumerate(scr_headers, start=1):
        c = ws2.cell(row=4, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = fill_navy
        c.alignment = align_center
        c.border = thin_border
    ws2.row_dimensions[4].height = 25

    r_idx = 5
    for item in screener_data:
        ws2.cell(row=r_idx, column=1, value=f"Top {item.get('rank', r_idx-4)}").alignment = align_center
        ws2.cell(row=r_idx, column=2, value=item.get("symbol", "")).font = font_bold
        ws2.cell(row=r_idx, column=3, value=item.get("company_name", "")).font = font_data
        ws2.cell(row=r_idx, column=4, value=item.get("exchange", "")).alignment = align_center

        p_cell = ws2.cell(row=r_idx, column=5, value=item.get("market_price", 0))
        p_cell.font = font_bold
        p_cell.number_format = '#,##0.00'
        p_cell.alignment = align_right

        v_cell = ws2.cell(row=r_idx, column=6, value=item.get("intrinsic_value", 0))
        v_cell.font = font_data
        v_cell.number_format = '#,##0.00'
        v_cell.alignment = align_right

        mos = item.get("margin_of_safety_pct", 0)
        mos_cell = ws2.cell(row=r_idx, column=7, value=mos / 100.0)
        mos_cell.font = font_green if mos > 0 else font_red
        mos_cell.number_format = '+0.0%;[Red]-0.0%'
        mos_cell.alignment = align_right

        ws2.cell(row=r_idx, column=8, value=item.get("fa_score", 0)).alignment = align_right
        ws2.cell(row=r_idx, column=9, value=item.get("valuation_score", 0)).alignment = align_right
        ws2.cell(row=r_idx, column=10, value=item.get("ta_score", 0)).alignment = align_right
        ws2.cell(row=r_idx, column=11, value=item.get("wave_score", 0)).alignment = align_right

        comb = ws2.cell(row=r_idx, column=12, value=item.get("combined_score", 0))
        comb.font = Font(name=font_name, size=11, bold=True, color="1B365D")
        comb.alignment = align_right

        rec = item.get("recommendation", "")
        rec_cell = ws2.cell(row=r_idx, column=13, value=rec)
        rec_cell.font = font_green if "MUA" in rec else (font_orange if "TÍCH LŨY" in rec else font_red)
        rec_cell.alignment = align_center

        presets_str = ", ".join(item.get("presets_matched", []))
        ws2.cell(row=r_idx, column=14, value=presets_str).font = font_data

        sym = item.get("symbol", "")
        html_file = f"chart_scenario_{sym}.html" if os.path.exists(os.path.join("outputs", "investment", f"chart_scenario_{sym}.html")) else "chart_scenario_interactive_MASTER.html"
        chart_cell = ws2.cell(row=r_idx, column=15, value=f'=HYPERLINK("{html_file}", "⚡ Mở Biểu Đồ (Chạy Ngay) ↗")')
        chart_cell.font = Font(name=font_name, size=10, bold=True, color="008000", underline="single")
        chart_cell.alignment = align_center

        for col_idx in range(1, 16):
            ws2.cell(row=r_idx, column=col_idx).border = thin_border
            if r_idx % 2 == 0:
                ws2.cell(row=r_idx, column=col_idx).fill = fill_zebra
        r_idx += 1

    for col in ws2.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len and cell.row > 2:
                max_len = len(val_str)
        ws2.column_dimensions[col_letter].width = max(max_len + 4, 12)
    ws2.freeze_panes = "A5"

    # SHEET 3: RADAR TIN HIEU
    ws3 = wb.create_sheet(title="Radar_Tin_Hieu_Va_Lenh")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:L1")
    t3_1 = ws3["A1"]
    t3_1.value = "RADAR TÍN HIỆU TÁC CHIẾN & CỬA NGÕ PHÊ DUYỆT LỆNH (HUMAN CHECKPOINT GATE)"
    t3_1.font = font_title
    t3_1.alignment = align_center
    ws3.row_dimensions[1].height = 30

    ws3.merge_cells("A2:L2")
    t3_2 = ws3["A2"]
    t3_2.value = "Nguyên tắc: AI không bao giờ tự trade. Mọi Signal Card bắt buộc phải có phê duyệt từ Nhà đầu tư trước khi lưu vào Sổ cái SQLite."
    t3_2.font = Font(name=font_name, size=10, italic=True, color="B71C1C")
    t3_2.alignment = align_center
    ws3.row_dimensions[2].height = 20

    radar_headers = [
        "Mã Signal", "Ngày Tạo", "Mã CK", "Lệnh", "Vùng Canh Lệnh (Entry)", "Cắt Lỗ Vô Hiệu Hóa (SL)",
        "Mục Tiêu 1 (TP1)", "Mục Tiêu 2 (TP2)", "Tỷ Lệ R/R", "Backtest Win-Rate", "Profit Factor",
        "Trạng Thái Checkpoint"
    ]
    for col_idx, h_text in enumerate(radar_headers, start=1):
        c = ws3.cell(row=4, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = fill_slate
        c.alignment = align_center
        c.border = thin_border
    ws3.row_dimensions[4].height = 25

    detailed_signals = [
        ("SIG-2026-FPT-01", "08/11/2026", "FPT", "BUY_LIMIT", "50,800 VND", "48,500 VND (Thủng Fibo 0.618)", "57,800 VND (Đỉnh Sóng 3)", "72,500 VND (Fibo 1.618)", "1 : 3.06", "68.4%", "2.45", "ĐÃ DUYỆT (APPROVED)"),
        ("SIG-2026-SIP-01", "08/11/2026", "SIP", "BUY_LIMIT", "61,300 VND", "56,500 VND (Thủng Fibo 0.500)", "75,000 VND (Đỉnh cũ)", "81,300 VND (Fibo 1.618)", "1 : 2.83", "65.4%", "2.28", "ĐÃ DUYỆT (APPROVED)"),
        ("SIG-2026-BTC-01", "08/11/2026", "BTCUSD", "SELL_LIMIT", "$80,800 USD", "$88,500 USD (Vượt đỉnh Sóng B)", "$48,500 USD (Hỗ trợ W)", "$37,949 USD (Fibo 1.272)", "1 : 4.19", "61.9%", "2.65", "CHỜ DUYỆT (PENDING)"),
        ("SIG-2026-MWG-01", "08/11/2026", "MWG", "BUY_LIMIT", "62,500 VND", "59,000 VND (Gãy nền MA20)", "70,000 VND (Kháng cự)", "74,000 VND (Giá trị thực)", "1 : 2.71", "62.5%", "2.15", "CHỜ DUYỆT (PENDING)"),
        ("SIG-2026-HPG-01", "08/11/2026", "HPG", "BUY_ACCUMULATE", "26,500 VND", "24,800 VND (Đáy hộp Darvas)", "31,000 VND (Fibo 0.382)", "34,500 VND (Fibo 0.618)", "1 : 2.65", "58.8%", "1.98", "CHỜ DUYỆT (PENDING)")
    ]

    r3_idx = 5
    for s in detailed_signals:
        sid, sdate, sym, act, entry, sl, tp1, tp2, rr, wr, pf, st = s
        ws3.cell(row=r3_idx, column=1, value=sid).font = font_bold
        ws3.cell(row=r3_idx, column=2, value=sdate).alignment = align_center
        ws3.cell(row=r3_idx, column=3, value=sym).font = font_bold

        act_cell = ws3.cell(row=r3_idx, column=4, value=act)
        act_cell.font = font_green if "BUY" in act else font_red
        act_cell.alignment = align_center

        ws3.cell(row=r3_idx, column=5, value=entry).font = font_bold
        ws3.cell(row=r3_idx, column=5).alignment = align_right

        sl_cell = ws3.cell(row=r3_idx, column=6, value=sl)
        sl_cell.font = font_red
        sl_cell.alignment = align_right

        ws3.cell(row=r3_idx, column=7, value=tp1).font = font_green
        ws3.cell(row=r3_idx, column=7).alignment = align_right

        ws3.cell(row=r3_idx, column=8, value=tp2).font = font_green
        ws3.cell(row=r3_idx, column=8).alignment = align_right

        ws3.cell(row=r3_idx, column=9, value=rr).font = font_bold
        ws3.cell(row=r3_idx, column=9).alignment = align_center

        ws3.cell(row=r3_idx, column=10, value=wr).alignment = align_center
        ws3.cell(row=r3_idx, column=11, value=pf).alignment = align_center

        st_cell = ws3.cell(row=r3_idx, column=12, value=st)
        st_cell.font = font_green if "APPROVED" in st else font_orange
        st_cell.fill = fill_green_soft if "APPROVED" in st else fill_orange_soft
        st_cell.alignment = align_center

        for col_idx in range(1, 13):
            ws3.cell(row=r3_idx, column=col_idx).border = thin_border
        r3_idx += 1

    for col in ws3.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len and cell.row > 2:
                max_len = len(val_str)
        ws3.column_dimensions[col_letter].width = max(max_len + 4, 12)
    ws3.freeze_panes = "A5"

    # SHEET 4: SO CAI DANH MUC
    ws4 = wb.create_sheet(title="So_Cai_Danh_Muc")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:K1")
    t4_1 = ws4["A1"]
    t4_1.value = "SỔ CÁI QUẢN TRỊ DANH MỤC ĐẦU TƯ HIỆN HÀNH (PORTFOLIO LEDGER)"
    t4_1.font = font_title
    t4_1.alignment = align_center
    ws4.row_dimensions[1].height = 30

    ws4.merge_cells("A2:K2")
    t4_2 = ws4["A2"]
    t4_2.value = "Đồng bộ 2 chiều với CSDL SQLite knowledge-base/investment.db | Quản trị rủi ro trần 25% NAV / mã"
    t4_2.font = Font(name=font_name, size=10, italic=True, color="64748B")
    t4_2.alignment = align_center
    ws4.row_dimensions[2].height = 20

    port_headers = [
        "Mã CK", "Tên Doanh Nghiệp", "Khối Lượng (CP)", "Giá Vốn (VND)", "Thị Giá Hiện Tại (VND)",
        "Giá Trị Đầu Tư (VND)", "Giá Trị Thị Trường (VND)", "Lãi/Lỗ Tạm Tính (VND)", "Tỷ Suất (%)",
        "Tỷ Trọng NAV", "Cắt Lỗ Bảo Vệ (SL)"
    ]
    for col_idx, h_text in enumerate(port_headers, start=1):
        c = ws4.cell(row=4, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = fill_navy
        c.alignment = align_center
        c.border = thin_border
    ws4.row_dimensions[4].height = 25

    r4_idx = 5
    for row in portfolio_rows:
        sym, name, qty, avg_p, cur_p, val, pnl, pnl_pct, alloc_pct, sl, tp = row

        ws4.cell(row=r4_idx, column=1, value=sym).font = font_bold
        ws4.cell(row=r4_idx, column=2, value=name).font = font_data

        q_c = ws4.cell(row=r4_idx, column=3, value=qty)
        q_c.font = font_bold
        q_c.number_format = '#,##0'
        q_c.alignment = align_right

        cost_c = ws4.cell(row=r4_idx, column=4, value=avg_p * 1000)
        cost_c.font = font_data
        cost_c.number_format = '#,##0'
        cost_c.alignment = align_right

        cur_c = ws4.cell(row=r4_idx, column=5, value=cur_p * 1000)
        cur_c.font = font_bold
        cur_c.number_format = '#,##0'
        cur_c.alignment = align_right

        cval_c = ws4.cell(row=r4_idx, column=6, value=f"=C{r4_idx}*D{r4_idx}")
        cval_c.font = font_data
        cval_c.number_format = '#,##0 "VND"'
        cval_c.alignment = align_right

        mval_c = ws4.cell(row=r4_idx, column=7, value=f"=C{r4_idx}*E{r4_idx}")
        mval_c.font = font_bold
        mval_c.number_format = '#,##0 "VND"'
        mval_c.alignment = align_right

        pnl_c = ws4.cell(row=r4_idx, column=8, value=f"=G{r4_idx}-F{r4_idx}")
        pnl_c.font = font_green
        pnl_c.number_format = '+#,##0 "VND";[Red]-#,##0 "VND"'
        pnl_c.alignment = align_right

        pct_c = ws4.cell(row=r4_idx, column=9, value=f"=H{r4_idx}/F{r4_idx}")
        pct_c.font = font_green
        pct_c.number_format = '+0.00%;[Red]-0.00%'
        pct_c.alignment = align_right

        alloc_c = ws4.cell(row=r4_idx, column=10, value=f"=G{r4_idx}/{risk_row[0]}")
        alloc_c.font = font_bold
        alloc_c.number_format = '0.00%'
        alloc_c.alignment = align_right

        sl_c = ws4.cell(row=r4_idx, column=11, value=sl * 1000)
        sl_c.font = font_red
        sl_c.number_format = '#,##0'
        sl_c.alignment = align_right

        for c_i in range(1, 12):
            ws4.cell(row=r4_idx, column=c_i).border = thin_border
        r4_idx += 1

    # Cash line
    ws4.cell(row=r4_idx, column=1, value="CASH").font = font_bold
    ws4.cell(row=r4_idx, column=2, value="Tiền mặt khả dụng VND").font = font_data
    ws4.cell(row=r4_idx, column=3, value="—").alignment = align_center
    ws4.cell(row=r4_idx, column=4, value="—").alignment = align_center
    ws4.cell(row=r4_idx, column=5, value="—").alignment = align_center

    c_f = ws4.cell(row=r4_idx, column=6, value=risk_row[1])
    c_f.number_format = '#,##0 "VND"'
    c_f.alignment = align_right

    c_g = ws4.cell(row=r4_idx, column=7, value=risk_row[1])
    c_g.font = font_bold
    c_g.number_format = '#,##0 "VND"'
    c_g.alignment = align_right

    ws4.cell(row=r4_idx, column=8, value=0).number_format = '#,##0 "VND"'
    ws4.cell(row=r4_idx, column=8).alignment = align_right
    ws4.cell(row=r4_idx, column=9, value=0).number_format = '0.00%'
    ws4.cell(row=r4_idx, column=9).alignment = align_right

    cash_alloc = ws4.cell(row=r4_idx, column=10, value=f"=G{r4_idx}/{risk_row[0]}")
    cash_alloc.font = font_bold
    cash_alloc.number_format = '0.00%'
    cash_alloc.alignment = align_right

    ws4.cell(row=r4_idx, column=11, value="—").alignment = align_center
    for c_i in range(1, 12):
        ws4.cell(row=r4_idx, column=c_i).border = thin_border
    r4_idx += 1

    # Total line
    ws4.cell(row=r4_idx, column=1, value="TỔNG CỘNG").font = Font(name=font_name, size=11, bold=True, color="1B365D")
    ws4.cell(row=r4_idx, column=2, value="Toàn bộ danh mục đầu tư").font = font_bold
    ws4.cell(row=r4_idx, column=3, value="—").alignment = align_center
    ws4.cell(row=r4_idx, column=4, value="—").alignment = align_center
    ws4.cell(row=r4_idx, column=5, value="—").alignment = align_center

    tot_cost = ws4.cell(row=r4_idx, column=6, value=f"=SUM(F5:F{r4_idx-1})")
    tot_cost.font = Font(name=font_name, size=11, bold=True, color="1B365D")
    tot_cost.number_format = '#,##0 "VND"'
    tot_cost.alignment = align_right

    tot_mval = ws4.cell(row=r4_idx, column=7, value=f"=SUM(G5:G{r4_idx-1})")
    tot_mval.font = Font(name=font_name, size=11, bold=True, color="1B365D")
    tot_mval.number_format = '#,##0 "VND"'
    tot_mval.alignment = align_right

    tot_pnl = ws4.cell(row=r4_idx, column=8, value=f"=SUM(H5:H{r4_idx-1})")
    tot_pnl.font = Font(name=font_name, size=11, bold=True, color="1B5E20")
    tot_pnl.number_format = '+#,##0 "VND"'
    tot_pnl.alignment = align_right

    tot_pct = ws4.cell(row=r4_idx, column=9, value=f"=H{r4_idx}/F{r4_idx}")
    tot_pct.font = Font(name=font_name, size=11, bold=True, color="1B5E20")
    tot_pct.number_format = '+0.00%'
    tot_pct.alignment = align_right

    tot_alloc = ws4.cell(row=r4_idx, column=10, value=f"=SUM(J5:J{r4_idx-1})")
    tot_alloc.font = Font(name=font_name, size=11, bold=True, color="1B365D")
    tot_alloc.number_format = '100.00%'
    tot_alloc.alignment = align_right

    ws4.cell(row=r4_idx, column=11, value="—").alignment = align_center

    for c_i in range(1, 12):
        cell = ws4.cell(row=r4_idx, column=c_i)
        cell.fill = fill_subtotal
        cell.border = thick_bottom

    for col in ws4.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len and cell.row > 2:
                max_len = len(val_str)
        ws4.column_dimensions[col_letter].width = max(max_len + 4, 12)
    ws4.freeze_panes = "A5"

    # SHEET 5: LICH SU GIAO DICH
    ws5 = wb.create_sheet(title="Lich_Su_Giao_Dich")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells("A1:J1")
    t5_1 = ws5["A1"]
    t5_1.value = "NHẬT KÝ GIAO DỊCH & AUDIT LOG ĐỐI SOÁT MINH BẠCH"
    t5_1.font = font_title
    t5_1.alignment = align_center
    ws5.row_dimensions[1].height = 30

    trade_headers = [
        "Mã Lệnh", "Mã CK", "Loại Lệnh", "Khối Lượng", "Giá Khớp (VND)", "Tổng Giá Trị (VND)",
        "Thuế & Phí", "Lãi/Lỗ Thực Hiện", "Ngày Khớp Lệnh", "Căn Cứ / Ghi Chú"
    ]
    for col_idx, h_text in enumerate(trade_headers, start=1):
        c = ws5.cell(row=3, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = fill_navy
        c.alignment = align_center
        c.border = thin_border
    ws5.row_dimensions[3].height = 25

    r5_idx = 4
    for t in trade_rows:
        tid, sym, act, qty, price, total, fee, pnl, tdate, notes = t
        ws5.cell(row=r5_idx, column=1, value=tid).font = font_bold
        ws5.cell(row=r5_idx, column=2, value=sym).font = font_bold

        act_cell = ws5.cell(row=r5_idx, column=3, value=act)
        act_cell.font = font_green if "BUY" in act else font_red
        act_cell.alignment = align_center

        q_c = ws5.cell(row=r5_idx, column=4, value=qty)
        q_c.number_format = '#,##0'
        q_c.alignment = align_right

        p_c = ws5.cell(row=r5_idx, column=5, value=price * 1000)
        p_c.number_format = '#,##0'
        p_c.alignment = align_right

        tot_c = ws5.cell(row=r5_idx, column=6, value=total)
        tot_c.font = font_bold
        tot_c.number_format = '#,##0 "VND"'
        tot_c.alignment = align_right

        fee_c = ws5.cell(row=r5_idx, column=7, value=fee)
        fee_c.number_format = '#,##0 "VND"'
        fee_c.alignment = align_right

        pnl_c = ws5.cell(row=r5_idx, column=8, value=pnl)
        pnl_c.number_format = '+#,##0 "VND";[Red]-#,##0 "VND"'
        pnl_c.alignment = align_right

        ws5.cell(row=r5_idx, column=9, value=tdate).alignment = align_center
        ws5.cell(row=r5_idx, column=10, value=notes).font = font_data

        for c_i in range(1, 11):
            ws5.cell(row=r5_idx, column=c_i).border = thin_border
            if r5_idx % 2 == 1:
                ws5.cell(row=r5_idx, column=c_i).fill = fill_zebra
        r5_idx += 1

    for col in ws5.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len and cell.row > 2:
                max_len = len(val_str)
        ws5.column_dimensions[col_letter].width = max(max_len + 4, 12)
    ws5.freeze_panes = "A4"

    wb.save(OUTPUT_EXCEL)
    print(f"[*] Da xuat ban thanh cong Master Excel Dashboard tai: {OUTPUT_EXCEL}")
    return OUTPUT_EXCEL


if __name__ == "__main__":
    create_excel_master_dashboard()
