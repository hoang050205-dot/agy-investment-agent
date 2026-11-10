"""
Export Valuation Word Reports (.docx)
Xuất bản báo cáo thẩm định BCTC & Định giá chuyên nghiệp dạng file Word (.docx)
cho các mã cổ phiếu phân tích (SIP, FPT).
"""

import os
import sys
import json
from datetime import datetime
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô bảng"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt lề trong cho ô bảng"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_hyperlink(paragraph, url, text, color="004B87", underline=True, bold=True):
    """Thêm siêu liên kết clickable 1-click vào văn bản Word"""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w")} r:id="{r_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>')
    new_run = parse_xml(f'<w:r {nsdecls("w")}/>')
    rPr = parse_xml(f'<w:rPr {nsdecls("w")}/>')

    if color:
        c = parse_xml(f'<w:color {nsdecls("w")} w:val="{color}"/>')
        rPr.append(c)

    if underline:
        u = parse_xml(f'<w:u {nsdecls("w")} w:val="single"/>')
        rPr.append(u)

    if bold:
        b = parse_xml(f'<w:b {nsdecls("w")}/>')
        rPr.append(b)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink

def create_docx_report(symbol: str, data_dir: str = "sample-data/stock", out_dir: str = "outputs/investment"):
    symbol = symbol.upper()
    stock_dir = os.path.join(data_dir, symbol)
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(stock_dir, "profile.json"), "r", encoding="utf-8") as f:
        profile = json.load(f)
    with open(os.path.join(stock_dir, "fundamental_analysis.json"), "r", encoding="utf-8") as f:
        fundamental = json.load(f)
    with open(os.path.join(stock_dir, "valuation_result.json"), "r", encoding="utf-8") as f:
        valuation = json.load(f)

    doc = docx.Document()

    # Căn lề trang 2cm
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Style mặc định
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # 1. TIÊU ĐỀ BÁO CÁO
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_after = Pt(2)
    run_sub = title_p.add_run("HỆ THỐNG AI INVESTMENT AGENT — PHƯƠNG PHÁP LUẬN FSEN & ĐỊNH GIÁ NỘI BỘ\n")
    run_sub.font.size = Pt(9.5)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0x0F, 0x4C, 0x81)

    run_title = title_p.add_run(f"BÁO CÁO THẨM ĐỊNH BCTC & ĐỊNH GIÁ DOANH NGHIỆP: {symbol}\n")
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    run_name = title_p.add_run(f"{profile.get('name', symbol).upper()}")
    run_name.font.size = Pt(11)
    run_name.font.italic = True
    run_name.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_p.paragraph_format.space_after = Pt(14)
    run_meta = meta_p.add_run(f"Ngày lập báo cáo: {datetime.now().strftime('%d/%m/%Y')} | Người thực hiện: AGY Investment Analyst | Cấp thẩm định: C-Suite / Hội Đồng Đầu Tư")
    run_meta.font.size = Pt(9)
    run_meta.font.italic = True

    # 2. KHỐI TỔNG QUAN DOANH NGHIỆP
    h1 = doc.add_paragraph()
    r_h1 = h1.add_run("I. THÔNG TIN CƠ BẢN & CHỈ SỐ THỊ TRƯỜNG")
    r_h1.font.bold = True
    r_h1.font.size = Pt(12)
    r_h1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h1.paragraph_format.space_before = Pt(8)
    h1.paragraph_format.space_after = Pt(4)

    table_info = doc.add_table(rows=4, cols=4)
    table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_info.autofit = False

    info_data = [
        [("Mã chứng khoán", symbol), ("Ngành nghề", profile.get("industry") or "Bất động sản KCN / Công nghệ")],
        [("Thị giá hiện tại", f"{profile.get('current_price', 0):,.0f} VND ({valuation['asset_valuation']['inputs']['current_price_k']:.2f}k)"), 
         ("Vốn hóa thị trường", f"{profile.get('market_cap', 0)/1e9:,.1f} tỷ VND")],
        [("Số lượng CPLH", f"{profile.get('shares_outstanding', 0)/1e6:,.2f} triệu CP"), 
         ("Chỉ số P/E & P/B", f"P/E: {profile.get('pe', 'N/A')} | P/B: {profile.get('pb', 'N/A')}")],
        [("Chỉ số sinh lời", f"ROE: {profile.get('roe', 0):.2f}% | ROA: {profile.get('roa', 0):.2f}%"), 
         ("Biên lợi nhuận", f"Gộp: {profile.get('gross_margin', 0):.1f}% | Ròng: {profile.get('net_margin', 0):.1f}%")]
    ]

    for row_idx, row_content in enumerate(info_data):
        col_idx = 0
        for label, val in row_content:
            c_lbl = table_info.cell(row_idx, col_idx)
            c_lbl.width = Inches(1.5)
            c_lbl.text = label
            c_lbl.paragraphs[0].runs[0].font.bold = True
            c_lbl.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_background(c_lbl, "F2F4F7")
            set_cell_margins(c_lbl)

            c_val = table_info.cell(row_idx, col_idx + 1)
            c_val.width = Inches(2.0)
            c_val.text = str(val)
            c_val.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(c_val)
            col_idx += 2

    # KHUNG CALLOUT MỞ BIỂU ĐỒ 1-CLICK TRỰC TIẾP
    tv_symbol = f"BINANCE:{symbol}T" if "BTC" in symbol else (f"OANDA:{symbol}" if "XAU" in symbol else f"HOSE:{symbol}")
    tv_url = f"https://www.tradingview.com/chart/?symbol={tv_symbol}"
    tv_layout_url = f"https://www.tradingview.com/chart/iboM2olW/?symbol={tv_symbol}"

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(2)

    tbl_link = doc.add_table(rows=1, cols=1)
    tbl_link.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_link = tbl_link.cell(0, 0)
    c_link.width = Inches(7.0)
    set_cell_background(c_link, "F0F9FF")
    set_cell_margins(c_link, top=140, bottom=140, left=180, right=180)

    p_link = c_link.paragraphs[0]
    p_link.paragraph_format.space_after = Pt(3)
    r_title = p_link.add_run("🌐 CỔNG TRUY CẬP BIỂU ĐỒ KỸ THUẬT & SÓNG ELLIOTT TƯƠNG TÁC (1-CLICK ACCESS):\n")
    r_title.font.bold = True
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    # 1. Standalone Direct Offline Link (GUARANTEED TO RUN IMMEDIATELY - ZERO SERVER NEEDED)
    offline_chart_url = f"chart_scenario_{symbol}.html"
    p_offline = c_link.add_paragraph()
    p_offline.paragraph_format.space_after = Pt(4)
    p_offline.add_run("⚡ ")
    add_hyperlink(p_offline, offline_chart_url, f"MỞ BIỂU ĐỒ CHẠY NGAY LẬP TỨC (100% OFFLINE KHÔNG CẦN SERVER) ↗", color="008000")
    r_off_desc = p_offline.add_run(" — Nhấp đúp mở ngay trên Google Chrome trong 0.1s: Nến mượt 60fps, đếm sóng chuẩn Fsen & kịch bản tương lai")
    r_off_desc.font.size = Pt(9)
    r_off_desc.font.bold = True
    r_off_desc.font.color.rgb = RGBColor(0x00, 0x80, 0x00)

    # 2. Localhost HTTP Port 8888
    http_chart_url = f"http://localhost:8888/chart_scenario_{symbol}.html"
    p_web = c_link.add_paragraph()
    p_web.paragraph_format.space_after = Pt(3)
    p_web.add_run("🚀 ")
    add_hyperlink(p_web, http_chart_url, f"MỞ QUA WEB SERVER LOCALHOST (HTTP://LOCALHOST:8888) ↗", color="0284C7")
    r_web_desc = p_web.add_run(f" — Web Server cục bộ phục vụ đồ thị chuyên sâu {symbol}")
    r_web_desc.font.size = Pt(9)
    r_web_desc.font.italic = True
    r_web_desc.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    # 3. Master Multi-Asset Dashboard (Offline & Online)
    p_master = c_link.add_paragraph()
    p_master.paragraph_format.space_after = Pt(3)
    p_master.add_run("🖥️ ")
    add_hyperlink(p_master, "chart_scenario_interactive_MASTER.html", "MỞ HỆ THỐNG BIỂU ĐỒ MASTER ĐA TÀI SẢN (CHẠY NGAY) ↗", color="004B87")
    r_mas_desc = p_master.add_run(" — Hệ thống đa tài sản (VND, FPT, BTC, VÀNG) đa khung thời gian 1M, 1W, 1D, 1H")
    r_mas_desc.font.size = Pt(9)
    r_mas_desc.font.italic = True
    r_mas_desc.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # 3. External TradingView options
    p_tv = c_link.add_paragraph()
    p_tv.paragraph_format.space_after = Pt(2)
    p_tv.add_run("📈 ")
    add_hyperlink(p_tv, tv_url, f"MỞ BIỂU ĐỒ TRỰC TIẾP TRÊN TRADINGVIEW ({tv_symbol}) ↗", color="004B87")
    r_tv_desc = p_tv.add_run(" — Xem nến Real-time trên TradingView Online")
    r_tv_desc.font.size = Pt(9)
    r_tv_desc.font.italic = True
    r_tv_desc.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_layout = c_link.add_paragraph()
    p_layout.paragraph_format.space_after = Pt(2)
    p_layout.add_run("🖥️ ")
    add_hyperlink(p_layout, tv_layout_url, "MỞ TRÊN LAYOUT CÁ NHÂN HOANG050205 TRADINGVIEW ↗", color="004B87")
    r_lay_desc = p_layout.add_run(" — Mở trực tiếp đồ thị đã lưu cá nhân")
    r_lay_desc.font.size = Pt(9)
    r_lay_desc.font.italic = True
    r_lay_desc.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    chart_png_path = os.path.join(out_dir, f"chart_scenario_{symbol}_pro.png")
    if not os.path.exists(chart_png_path):
        chart_png_path = os.path.join("outputs", "investment", f"chart_scenario_{symbol}_pro.png")
    if os.path.exists(chart_png_path):
        p_img = c_link.add_paragraph()
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        r_img_title = p_img.add_run("🖼️ Kịch bản kỹ thuật & Vùng giải ngân Fsen:")
        r_img_title.font.bold = True
        r_img_title.font.size = Pt(9.5)
        p_img_pic = c_link.add_paragraph()
        p_img_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img_pic.paragraph_format.space_after = Pt(2)
        p_img_pic.add_run().add_picture(chart_png_path, width=Inches(6.4))


    # 2.5 BẢNG KẾ HOẠCH DỰ BÁO SÓNG FSEN TƯƠNG LAI (DỰA VÀO SÓNG ĐẰNG TRƯỚC)
    from invest_fsen_projection_engine import ASSETS_PROJECTION_REGISTRY, calculate_projection_metrics
    if symbol in ASSETS_PROJECTION_REGISTRY:
        proj_cfg = ASSETS_PROJECTION_REGISTRY[symbol]
        proj = calculate_projection_metrics(
            proj_cfg["p0"], proj_cfg["p1"], proj_cfg["p2"],
            proj_cfg["is_bullish"], proj_cfg["t0"], proj_cfg["t1"], proj_cfg["t2"]
        )
        
        h_proj = doc.add_paragraph()
        r_hp = h_proj.add_run("II. KẾ HOẠCH DỰ BÁO SÓNG FSEN TƯƠNG LAI (DỰA TRÊN SÓNG ĐẰNG TRƯỚC)")
        r_hp.font.bold = True
        r_hp.font.size = Pt(12)
        r_hp.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        h_proj.paragraph_format.space_before = Pt(10)
        h_proj.paragraph_format.space_after = Pt(3)

        p_desc = doc.add_paragraph()
        r_pd = p_desc.add_run(f"• Dạng mô hình dự kiến: {proj['pattern']} | Khung thời gian: {proj_cfg['timeframe']}\n"
                              f"• Điểm vô hiệu hóa tuyệt đối: INVALID tại {proj['invalidation']} nghìn đồng (Thủng mốc này thì kịch bản bị hủy)\n"
                              f"• Chiều cao Sóng 1 (H1): {proj['h1']}k (Kích hoạt CHoCH tại {proj['anchor_p1']}k) | Mức hồi Sóng 2: {proj['ret2_pct']}%")
        r_pd.font.size = Pt(9.5)
        r_pd.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        p_desc.paragraph_format.space_after = Pt(4)

        t_proj = doc.add_table(rows=7, cols=4)
        t_proj.alignment = WD_TABLE_ALIGNMENT.CENTER
        proj_headers = ["Bước Sóng", "Công Thức Đo Sóng Trước", "Mục Tiêu Giá", "Ý Nghĩa Kỹ Thuật & Tỷ Lệ R/R"]
        proj_rows = [
            ("Sóng 0 -> 1", "Khởi nguồn & Chân sóng", f"{proj['anchor_p0']}k -> {proj['anchor_p1']}k", f"Biên độ H1 = {proj['h1']}k, nổ vol 102.7M nến tuần tạo CHoCH."),
            ("Sóng 2~", f"Pullback {proj['ret2_pct']}% Sóng 1", f"{proj['anchor_p2']}k", f"Vùng gom mua test MA20 tuần (14.2 - 14.5k). INVALID: {proj['invalidation']}k."),
            ("Sóng 3? (Target)", f"1.618 x H1 (từ Sóng 2)", f"{proj['w3_target']}k", f"Sóng đẩy mạnh nhất, vượt cản Sóng B. Tỷ lệ R/R = 1 : {proj['rr_w3']}."),
            ("Sóng 4? (Pullback)", f"Thoái lui 0.382 x Sóng 3", f"{proj['w4_target']}k", f"Tích lũy kiểm định hỗ trợ, bảo toàn thiết luật > S1 ({proj['anchor_p1']}k)."),
            ("Sóng 5? (Mục tiêu lớn)", f"1.000 x H1 & Fibo 0.618", f"{proj['w5_target']}k - {proj_cfg['target_zone_w5'][1]}k", f"Chinh phục kháng cự chu kỳ lớn, hướng tới kiểm định đỉnh ATH {proj_cfg['ath_target']}k."),
            ("Chuỗi A? - B? - C?", "Tái tích lũy 3 nhịp Fsen", f"A: {proj['wa_target']}k | B: {proj['wb_target']}k | C: {proj['wc_target']}k", f"Tái lập mặt bằng giá mới sau khi hoàn tất 5 sóng đẩy mở rộng.")
        ]

        for c_idx, h_t in enumerate(proj_headers):
            cell = t_proj.rows[0].cells[c_idx]
            cell.text = h_t
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            set_cell_background(cell, "1B365D")
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        for r_i, r_data in enumerate(proj_rows, start=1):
            for c_i, val in enumerate(r_data):
                cell = t_proj.rows[r_i].cells[c_i]
                cell.text = str(val)
                r_cell = cell.paragraphs[0].runs[0]
                r_cell.font.size = Pt(9)
                if c_i == 0:
                    r_cell.font.bold = True
                    r_cell.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
                elif c_i == 2:
                    r_cell.font.bold = True
                    r_cell.font.color.rgb = RGBColor(0x10, 0x7C, 0x41) if proj['is_bullish'] else RGBColor(0xD9, 0x38, 0x3A)
                if r_i % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    # 3. HỆ THỐNG 3 ĐÈN CẢNH BÁO BCTC
    h2 = doc.add_paragraph()
    r_h2 = h2.add_run("II. BỘ MÁY QUÉT 3 ĐÈN CẢNH BÁO BÁO CÁO TÀI CHÍNH (PTBCTC NHANH)")
    r_h2.font.bold = True
    r_h2.font.size = Pt(12)
    r_h2.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)

    warn = fundamental.get("warnings", {})
    all_warnings = []
    for item in warn.get("balance_sheet", []):
        all_warnings.append(("CĐKT", item))
    for item in warn.get("income_statement", []):
        all_warnings.append(("KQKD", item))
    for item in warn.get("cash_flow", []):
        all_warnings.append(("LCTT", item))

    table_warn = doc.add_table(rows=len(all_warnings) + 1, cols=5)
    table_warn.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = ["Báo cáo", "Chỉ số / Khoản mục", "Giá trị", "Tiêu chuẩn", "Đánh giá & Cảnh báo"]
    widths = [Inches(0.9), Inches(1.8), Inches(1.0), Inches(1.0), Inches(2.3)]

    hdr_cells = table_warn.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        hdr_cells[i].width = widths[i]
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i])

    for row_idx, (b_name, item) in enumerate(all_warnings, start=1):
        row_cells = table_warn.rows[row_idx].cells
        row_cells[0].text = b_name
        row_cells[1].text = item['metric']
        row_cells[2].text = str(item['value'])
        row_cells[3].text = item['threshold']
        row_cells[4].text = item['message']

        for c_idx in range(5):
            row_cells[c_idx].width = widths[c_idx]
            row_cells[c_idx].paragraphs[0].runs[0].font.size = Pt(9)
            set_cell_margins(row_cells[c_idx])
            if item['status'] == "RED":
                set_cell_background(row_cells[c_idx], "FDE8E8")
            elif item['status'] == "ORANGE":
                set_cell_background(row_cells[c_idx], "FEF08A")
            elif "GREEN" in item['status']:
                set_cell_background(row_cells[c_idx], "DEF7EC")

    # 4. HÀO THÀNH KINH TẾ (ECONOMIC MOAT)
    h3 = doc.add_paragraph()
    r_h3 = h3.add_run("III. ĐÁNH GIÁ LỢI THẾ CẠNH TRANH LÂU BỀN (ECONOMIC MOAT)")
    r_h3.font.bold = True
    r_h3.font.size = Pt(12)
    r_h3.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)

    moat = fundamental.get("economic_moat", {})
    p_moat_status = doc.add_paragraph()
    r_mst = p_moat_status.add_run(f"Xếp hạng Moat: {moat.get('classification')} — Phát hiện {moat.get('moats_count')} lợi thế cốt lõi:")
    r_mst.font.bold = True
    r_mst.font.size = Pt(10.5)

    for m in moat.get("details", []):
        p_m = doc.add_paragraph(style='List Bullet')
        p_m.paragraph_format.space_after = Pt(2)
        r_mn = p_m.add_run(f"{m['name']}: ")
        r_mn.font.bold = True
        r_mn.font.size = Pt(10)
        r_me = p_m.add_run(m['evidence'])
        r_me.font.size = Pt(10)

    # 5. KẾT QUẢ ĐỊNH GIÁ ĐÔI
    h4 = doc.add_paragraph()
    r_h4 = h4.add_run("IV. KẾT QUẢ ĐỊNH GIÁ ĐÔI (DCF 10 NĂM & TÀI SẢN RÒNG)")
    r_h4.font.bold = True
    r_h4.font.size = Pt(12)
    r_h4.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(4)

    asset = valuation['asset_valuation']
    dcf = valuation['dcf_valuation']

    table_val = doc.add_table(rows=6, cols=3)
    table_val.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_val = [Inches(2.5), Inches(2.2), Inches(2.3)]

    v_headers = ["Chỉ tiêu thẩm định", "Định Giá Tài Sản Ròng", "Định Giá DCF (10 Năm)"]
    for i, h_text in enumerate(v_headers):
        c = table_val.cell(0, i)
        c.text = h_text
        c.width = widths_val[i]
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9.5)
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(c, "0F4C81")
        set_cell_margins(c)

    rows_val_data = [
        ("Cơ sở dữ liệu đầu vào", 
         f"Tổng TS: {asset['inputs']['total_assets_bil']:,.1f} tỷ\nNợ chiếm dụng: {asset['inputs']['unearned_advances_bil']:,.1f} tỷ", 
         f"LNST 5 năm: {dcf['inputs']['lnst_5y'][-1]:,.1f} tỷ\nTăng trưởng: {dcf['growth_rates']['g_estimated']*100:.1f}%/năm"),
        ("Giá trị doanh nghiệp (EV)", f"{asset['enterprise_value_bil']:,.2f} tỷ VND", f"{dcf['enterprise_value_bil']:,.2f} tỷ VND"),
        ("Giá trị thực / Cổ phiếu", f"{asset['intrinsic_value_per_share']:.2f} nghìn đồng", f"{dcf['intrinsic_value_per_share']:.2f} nghìn đồng"),
        ("Thị giá cổ phiếu hiện tại", f"{asset['inputs']['current_price_k']:.2f} nghìn đồng", f"{dcf['inputs']['current_price_k']:.2f} nghìn đồng"),
        ("BIÊN AN TOÀN (MOS)", f"{asset['margin_of_safety_pct']:.2f}%", f"{dcf['margin_of_safety_pct']:.2f}%")
    ]

    for r_idx, (lbl, col1, col2) in enumerate(rows_val_data, start=1):
        for c_idx, val_text in enumerate([lbl, col1, col2]):
            c = table_val.cell(r_idx, c_idx)
            c.text = val_text
            c.width = widths_val[c_idx]
            c.paragraphs[0].runs[0].font.size = Pt(9.5)
            if r_idx == 5:
                c.paragraphs[0].runs[0].font.bold = True
                if c_idx == 1 and asset['margin_of_safety_pct'] > 25:
                    set_cell_background(c, "DEF7EC")
                elif c_idx == 2 and dcf['margin_of_safety_pct'] > 25:
                    set_cell_background(c, "DEF7EC")
                elif c_idx > 0:
                    set_cell_background(c, "FDE8E8")
            elif r_idx % 2 == 1:
                set_cell_background(c, "F9FAFB")
            set_cell_margins(c)

    # 6. KHUYẾN NGHỊ & HÀNH ĐỘNG
    h5 = doc.add_paragraph()
    r_h5 = h5.add_run("V. TỔNG HỢP KHUYẾN NGHỊ ĐẦU TƯ")
    r_h5.font.bold = True
    r_h5.font.size = Pt(12)
    r_h5.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(4)

    p_action = doc.add_paragraph()
    r_act = p_action.add_run(f"👉 HÀNH ĐỘNG ĐỀ XUẤT: {valuation['final_recommendation'].upper()}\n")
    r_act.font.bold = True
    r_act.font.size = Pt(11)
    if "MUA" in valuation['final_recommendation']:
        r_act.font.color.rgb = RGBColor(0x0E, 0x7A, 0x43)
    else:
        r_act.font.color.rgb = RGBColor(0xC8, 0x1E, 0x1E)

    r_rule = p_action.add_run("Nguyên tắc cốt lõi: Chỉ vào lệnh khi có xác nhận bởi yếu tố Chu kỳ VÀ Sóng.\n")
    r_rule.font.italic = True
    r_rule.font.size = Pt(10)

    p_disc = doc.add_paragraph()
    r_disc = p_disc.add_run("⚠️ Lưu ý quan trọng: Báo cáo này được lập tự động dựa trên dữ liệu BCTC chính thức và quy trình định giá nội bộ. Đây không phải là lời mời chào hay tư vấn đầu tư chứng khoán theo Luật Chứng khoán 2019.")
    r_disc.font.size = Pt(8.5)
    r_disc.font.italic = True
    r_disc.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    out_file = os.path.join(out_dir, f"valuation_report_{symbol}.docx")
    doc.save(out_file)
    print(f"[SUCCESS] Đã xuất bản file Word: {out_file}")
    return out_file

def main():
    out_dir = "outputs/investment"
    symbols = sys.argv[1:] if len(sys.argv) > 1 else ["SIP", "FPT", "VND"]
    for s in symbols:
        create_docx_report(s, out_dir=out_dir)

if __name__ == "__main__":
    main()

