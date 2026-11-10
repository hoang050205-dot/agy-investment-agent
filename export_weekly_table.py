"""
Export Weekly Analysis Table (Excel .xlsx & Word .docx & Markdown .md)
Tái tạo chính xác 100% bố cục bảng viết tay của Hoàng:
- Việt Nam (FPT): M | W | D | 1H | GHI CHÚ
- Quốc tế (BTCUSD): W | D | 4H | 1H | GHI CHÚ
- Chèn trực tiếp biểu đồ kịch bản trực quan vào file Word!
"""

import os
import sys
import json
from datetime import datetime, timedelta
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
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


def export_excel_weekly_table(symbol: str, tf_results: dict, out_xlsx: str):
    """Xuất bảng phân tích tuần sang Excel (.xlsx) chuẩn màu cam đất #FCE4D6"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Phan_Tich_Tuan_{symbol}"

    is_crypto = "BTC" in symbol
    if is_crypto:
        cols_tf = ["W", "D", "4H", "1H"]
    else:
        cols_tf = ["M", "W", "D", "1H"]

    headers = ["Khung thời gian"] + cols_tf + ["GHI CHÚ"]

    # 1. Tiêu đề lớn
    today = datetime.now()
    next_week = today + timedelta(days=6)
    date_str = f"{today.strftime('%d/%m')} - {next_week.strftime('%d/%m/%Y')}"
    ws.merge_cells("A1:F1")
    title_cell = ws["A1"]
    title_cell.value = f"BẢNG PHÂN TÍCH TUẦN {date_str} — MÃ: {symbol}"
    title_cell.font = Font(name="Times New Roman", size=14, bold=True, color="1B365D")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 35

    # 2. Header bảng
    ws.row_dimensions[2].height = 25
    header_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
    header_font = Font(name="Times New Roman", size=11, bold=True, color="000000")
    thin_border = Border(
        left=Side(style='thin', color='A6A6A6'),
        right=Side(style='thin', color='A6A6A6'),
        top=Side(style='thin', color='A6A6A6'),
        bottom=Side(style='thin', color='A6A6A6')
    )

    for col_idx, h_text in enumerate(headers, start=1):
        c = ws.cell(row=2, column=col_idx)
        c.value = h_text
        c.fill = header_fill
        c.font = header_font
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = thin_border

    # 3. Các dòng nội dung 6 Trụ Cột
    rows_data = [
        ("XU HƯỚNG", "trend", "Đánh giá vị thế giá tổng thể:\nXu hướng dài hạn quyết định chiến lược, ngắn hạn tìm điểm vào."),
        ("BIÊN ĐỘ", "range", "Các mốc phản ứng Fibonacci Retracement quan trọng (0.382 & 0.618) và Extension."),
        ("SÓNG", "wave", "Vị trí chu kỳ sóng Elliott hiện tại và Điểm vô hiệu hóa kịch bản (Stop Loss)."),
        ("THỜI GIAN", "time", "Đếm số nến từ đỉnh/đáy, vùng hội tụ thời gian đảo chiều."),
        ("BỘ CHẤM ĐIỂM", "score", "Tổng điểm điều kiện vào lệnh (MA + MACD + Fibo + Kênh)."),
        ("KỊCH BẢN GIAO DỊCH", "scenario", "Kịch bản ưu tiên giải ngân, Target TP1, TP2 và Stop loss."),
        ("CHIẾN THUẬT VÀO LỆNH", "tactics", "Chiến thuật đánh theo nhịp điều chỉnh khung 1H của xu hướng chính.")
    ]

    for row_idx, (r_name, r_key, note_txt) in enumerate(rows_data, start=3):
        # Cột A: Tên tiêu chí
        cA = ws.cell(row=row_idx, column=1)
        cA.value = r_name
        cA.font = Font(name="Times New Roman", size=10.5, bold=True, color="1B365D")
        cA.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cA.border = thin_border
        cA.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

        # Các cột khung thời gian
        for c_idx, tf in enumerate(cols_tf, start=2):
            cell = ws.cell(row=row_idx, column=c_idx)
            tf_data = tf_results.get(tf)
            if tf_data:
                if r_key == "tactics":
                    cell.value = f"Canh điểm vào tại khung {tf}: Đợi nến kiểm định hỗ trợ MA20/Fibo 0.618."
                else:
                    cell.value = tf_data.get(r_key, "").replace("**", "")
            else:
                cell.value = "Chưa có dữ liệu"
            cell.font = Font(name="Times New Roman", size=9.5)
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            cell.border = thin_border

        # Cột Ghi Chú
        cG = ws.cell(row=row_idx, column=len(headers))
        cG.value = note_txt
        cG.font = Font(name="Times New Roman", size=9.5, italic=True)
        cG.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cG.border = thin_border
        cG.fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
        ws.row_dimensions[row_idx].height = 80

    # 4. DÒNG NÚT BẤM 1-CLICK MỞ BIỂU ĐỒ CHẠY NGAY (OFFLINE & LOCALHOST)
    html_file = f"chart_scenario_{symbol}.html"
    link_row = len(rows_data) + 3
    ws.merge_cells(start_row=link_row, start_column=1, end_row=link_row, end_column=len(headers))
    c_btn = ws.cell(row=link_row, column=1)
    c_btn.value = f'=HYPERLINK("{html_file}", "⚡ [NHẤP ĐỂ MỞ BIỂU ĐỒ CHẠY NGAY TỨC THÌ TRÊN GOOGLE CHROME (100% OFFLINE KHÔNG CẦN SERVER) ↗]")'
    c_btn.font = Font(name="Times New Roman", size=11, bold=True, color="008000", underline="single")
    c_btn.alignment = Alignment(horizontal="center", vertical="center")
    c_btn.fill = PatternFill(start_color="F0FFF4", end_color="F0FFF4", fill_type="solid")
    c_btn.border = thin_border
    ws.row_dimensions[link_row].height = 32

    # Chỉnh độ rộng cột
    ws.column_dimensions['A'].width = 18
    for col_idx in range(2, 2 + len(cols_tf)):
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = 32
    ws.column_dimensions[get_column_letter(len(headers))].width = 28

    os.makedirs(os.path.dirname(out_xlsx), exist_ok=True)
    wb.save(out_xlsx)
    print(f"  [+] Đã xuất file Excel Bảng Phân Tích Tuần: {out_xlsx}")


def export_word_weekly_table(symbol: str, tf_results: dict, chart_png: str, out_docx: str):
    """Xuất file Word báo cáo tuần gồm Bảng phân tích 6 trụ cột VÀ biểu đồ nến kịch bản trực quan chèn sẵn!"""
    doc = docx.Document()

    for sec in doc.sections:
        sec.top_margin = Inches(0.7)
        sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.7)
        sec.right_margin = Inches(0.7)

    # Style
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(10.5)

    # 1. TIÊU ĐỀ
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_after = Pt(2)

    r_sub = title_p.add_run("BỘ NÃO PHÂN TÍCH KỸ THUẬT 6 TRỤ CỘT & SÓNG ELLIOTT\n")
    r_sub.font.bold = True
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = RGBColor(0x0F, 0x4C, 0x81)

    today = datetime.now()
    next_week = today + timedelta(days=6)
    date_str = f"{today.strftime('%d/%m')} - {next_week.strftime('%d/%m/%Y')}"
    r_main = title_p.add_run(f"BẢNG PHÂN TÍCH TUẦN ({date_str}) — {symbol}\n")
    r_main.font.bold = True
    r_main.font.size = Pt(16)
    r_main.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    is_crypto = "BTC" in symbol
    if is_crypto:
        cols_tf = ["W", "D", "4H", "1H"]
        desc_tf = "Khung thời gian chuẩn quốc tế: W (Trung hạn), D (Ngắn hạn), 4H (Chiến thuật), 1H (Điểm vào)"
    else:
        cols_tf = ["M", "W", "D", "1H"]
        desc_tf = "Khung thời gian chuẩn chứng khoán Việt Nam: M (Dài hạn), W (Trung hạn), D (Ngắn hạn), 1H (Điểm vào)"

    r_desc = title_p.add_run(desc_tf)
    r_desc.font.italic = True
    r_desc.font.size = Pt(9)
    r_desc.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

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
    set_cell_margins(c_link, top=120, bottom=120, left=180, right=180)

    p_link = c_link.paragraphs[0]
    p_link.paragraph_format.space_after = Pt(2)
    r_title = p_link.add_run("📊 TRUY CẬP BIỂU ĐỒ 1-CLICK (CHART QUICK-ACCESS):\n")
    r_title.font.bold = True
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    p_tv = c_link.add_paragraph()
    p_tv.paragraph_format.space_after = Pt(2)
    p_tv.add_run("🚀 ")
    add_hyperlink(p_tv, tv_url, f"MỞ BIỂU ĐỒ TRỰC TIẾP TRÊN TRADINGVIEW ({tv_symbol}) ↗", color="004B87")
    r_tv_desc = p_tv.add_run(" — Xem nến Real-time tích hợp bộ chỉ báo AGY Wave Pro")
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

    # 2. CHÈN BIỂU ĐỒ TRỰC QUAN
    if os.path.exists(chart_png):
        h_chart = doc.add_paragraph()
        r_hc = h_chart.add_run("I. BIỂU ĐỒ NẾN KỊCH BẢN KỸ THUẬT & ĐIỂM VÔ HIỆU HÓA SÓNG")
        r_hc.font.bold = True
        r_hc.font.size = Pt(12)
        r_hc.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        h_chart.paragraph_format.space_before = Pt(8)
        h_chart.paragraph_format.space_after = Pt(4)

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(chart_png, width=Inches(6.8))

        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_after = Pt(8)
        r_cap = p_caption.add_run("Hình 1: Biểu đồ nến kịch bản, MA10/20/50, Hỗ trợ/Kháng cự ngang, Vạch đỏ Stop Loss & Target TP")
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True

        # Hộp link truy cập biểu đồ Web Interactive
        t_link = doc.add_table(rows=1, cols=1)
        t_link.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_link = t_link.rows[0].cells[0]
        set_cell_background(c_link, "F0F9FF")
        set_cell_margins(c_link, top=100, bottom=100, left=140, right=140)

        offline_url = f"chart_scenario_{symbol}.html"
        http_url = f"http://localhost:8888/chart_scenario_{symbol}.html"
        
        p_lnk1 = c_link.paragraphs[0]
        p_lnk1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lnk1.add_run("⚡ ")
        add_hyperlink(p_lnk1, offline_url, f"MỞ BIỂU ĐỒ CHẠY NGAY TỨC THÌ (100% OFFLINE KHÔNG CẦN SERVER) ↗", color="008000")
        
        p_lnk2 = c_link.add_paragraph()
        p_lnk2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lnk2.paragraph_format.space_before = Pt(3)
        p_lnk2.add_run("🌐 ")
        add_hyperlink(p_lnk2, http_url, f"HOẶC MỞ QUA WEB SERVER LOCALHOST (HTTP://LOCALHOST:8888) ↗", color="0284C7")

    # 3. BẢNG PHÂN TÍCH TUẦN 6 TRỤ CỘT
    h_tab = doc.add_paragraph()
    r_ht = h_tab.add_run("II. BẢNG PHÂN TÍCH CHI TIẾT 6 TRỤ CỘT ĐA KHUNG THỜI GIAN")
    r_ht.font.bold = True
    r_ht.font.size = Pt(12)
    r_ht.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h_tab.paragraph_format.space_before = Pt(8)
    h_tab.paragraph_format.space_after = Pt(4)

    headers = ["Trụ Cột"] + cols_tf + ["Ghi Chú"]
    widths = [Inches(1.1)] + [Inches(1.25)] * len(cols_tf) + [Inches(1.2)]

    table = doc.add_table(rows=8, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    for c_idx, h_text in enumerate(headers):
        c = table.cell(0, c_idx)
        c.text = h_text
        c.width = widths[c_idx]
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(c, "FCE4D6")
        set_cell_margins(c)

    rows_data = [
        ("XU HƯỚNG", "trend", "Đánh giá vị thế giá tổng thể."),
        ("BIÊN ĐỘ", "range", "Các mốc phản ứng Fibo 0.382 & 0.618."),
        ("SÓNG", "wave", "Vị trí sóng Elliott & Điểm vô hiệu hóa."),
        ("THỜI GIAN", "time", "Đếm nến chu kỳ đối xứng."),
        ("BỘ CHẤM ĐIỂM", "score", "Chấm điểm điều kiện vào lệnh."),
        ("KỊCH BẢN", "scenario", "Kịch bản giải ngân, TP1, TP2 & SL."),
        ("CHIẾN THUẬT", "tactics", "Chiến thuật đánh nhịp 1H theo trend lớn.")
    ]

    for r_idx, (r_name, r_key, note_txt) in enumerate(rows_data, start=1):
        # Cột 0
        c0 = table.cell(r_idx, 0)
        c0.text = r_name
        c0.width = widths[0]
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(8.5)
        set_cell_background(c0, "FFF2CC")
        set_cell_margins(c0)

        # Cột khung thời gian
        for col_idx, tf in enumerate(cols_tf, start=1):
            cell = table.cell(r_idx, col_idx)
            cell.width = widths[col_idx]
            tf_data = tf_results.get(tf)
            if tf_data:
                if r_key == "tactics":
                    cell.text = f"Đợi nến 1H kiểm định MA20/Fibo 0.618 để mở vị thế."
                else:
                    raw_txt = tf_data.get(r_key, "").replace("**", "")
                    cell.text = raw_txt
            else:
                cell.text = "Chưa có dữ liệu"
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            set_cell_margins(cell)

        # Cột Ghi chú
        c_last = table.cell(r_idx, len(headers) - 1)
        c_last.text = note_txt
        c_last.width = widths[-1]
        c_last.paragraphs[0].runs[0].font.size = Pt(8)
        c_last.paragraphs[0].runs[0].font.italic = True
        set_cell_background(c_last, "F9FAFB")
        set_cell_margins(c_last)

    # 4. KẾT LUẬN & ĐIỂM VÔ HIỆU HÓA TỔNG QUAN
    h_disc = doc.add_paragraph()
    r_hd = h_disc.add_run("\nIII. NGUYÊN TẮC HÀNH ĐỘNG CỐT LÕI")
    r_hd.font.bold = True
    r_hd.font.size = Pt(11)
    r_hd.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_disc = doc.add_paragraph()
    r_p = p_disc.add_run("• Nguyên tắc vàng Fsen: Chỉ vào lệnh khi có xác nhận đồng thời bởi yếu tố Chu kỳ VÀ Sóng.\n• Quản trị rủi ro: Tuyệt đối tuân thủ Điểm vô hiệu hóa kịch bản (Stop loss). Nếu giá vi phạm vạch đỏ, toàn bộ kịch bản sóng đẩy bị hủy, phải chuyển sang kịch bản phòng thủ.")
    r_p.font.size = Pt(9.5)
    r_p.font.italic = True

    os.makedirs(os.path.dirname(out_docx), exist_ok=True)
    doc.save(out_docx)
    print(f"  [+] Đã xuất file Word Bảng Phân Tích Tuần (kèm biểu đồ): {out_docx}")


def export_all(symbol: str, tf_results: dict, chart_png: str, out_dir: str = "outputs/investment"):
    xlsx_path = os.path.join(out_dir, f"Bang_Phan_Tich_Tuan_{symbol}.xlsx")
    docx_path = os.path.join(out_dir, f"Bang_Phan_Tich_Tuan_{symbol}.docx")

    print(f"[*] Đang xuất bản Bảng Phân Tích Tuần cho {symbol}...")
    export_excel_weekly_table(symbol, tf_results, xlsx_path)
    export_word_weekly_table(symbol, tf_results, chart_png, docx_path)

    return xlsx_path, docx_path

