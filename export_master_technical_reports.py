"""
Export Master Technical Analysis Reports (Word .docx, Excel .xlsx, Markdown .md)
- Tích hợp 100% Sóng Elliott Fsen & MACD chuẩn xác:
  + BTCUSD (W, D, 4H, 1H): Đáy Sóng (A) 57.8k ở trước, Đỉnh Sóng (B) 87.4k ở trước, Hiện tại nến 75.8k trong Sóng (C) đổ đèo.
  + FPT (M, W, D, 1H): Hoàn tất chu kỳ điều chỉnh A-B-C tại 49.55k, bắt đầu chu kỳ 5 sóng đẩy mới hướng về 68k và 82k.
  + XAUUSD (W, D, 1H): Đáy chu kỳ A-B-C tại 3,879.3$, bắt đầu 5 sóng đẩy mới hướng về 4,850$ và 5,580$.
- Chèn trực tiếp ảnh biểu đồ Pro độ nét cao vào file Word.
- Bố cục Bảng 6 Trụ Cột Đa Khung chuẩn Fsen tông màu Corporate sang trọng.
"""

import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

out_dir = "outputs/investment"
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------
# XML STYLING HELPERS FOR WORD
# -------------------------------------------------------------
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
    new_run_text = parse_xml(f'<w:t {nsdecls("w")}>{text}</w:t>')
    new_run.append(new_run_text)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


# =============================================================
# DATA SPECIFICATION FOR 3 ASSETS
# =============================================================
REPORTS_CONFIG = {
    "BTCUSD": {
        "title": "BÁO CÁO PHÂN TÍCH KỸ THUẬT & KỊCH BẢN GIAO DỊCH BITCOIN (BTCUSD)",
        "market_type": "Quốc tế / Crypto",
        "timeframes": ["W", "D", "4H", "1H"],
        "tf_desc": "W (Trung hạn) | D (Ngắn hạn) | 4H (Chiến thuật) | 1H (Điểm vào lệnh)",
        "chart_png": os.path.abspath("outputs/investment/chart_scenario_BTCUSD_pro.png"),
        "summary": "Bitcoin đang vận động trong pha điều chỉnh lớn của Sóng (C). Sau khi hoàn tất Sóng (A) tại $57,800 và Sóng (B) hồi phục tại $87,396, thị trường đã gãy đường kênh tăng và nến tuần hiện tại ($75,870) đang ở đáy sóng con C-1. Chiến lược chủ đạo: Canh Bán nhịp hồi kỹ thuật sóng con C-2 tại vùng $80,000 - $81,500 với mục tiêu chốt lời TP1: $48,500 và TP2: $37,949. Điểm vô hiệu hóa (Stop Loss) tuyệt đối tại $88,500 (vượt đỉnh Sóng B).",
        "pillars": {
            "W": {
                "trend": "Xu hướng Giảm (Downtrend) trung hạn sau khi gãy MA10/MA20 Tuần. Hỗ trợ đáy cũ: $57,800; Cản động: $81,000 - $82,500.",
                "range": "Fibo Retracement chu kỳ rơi: 0.382 ($95.1k), 0.500 ($86.4k), 0.618 ($78.5k). Fibo Extension mục tiêu: 1.000 ($48.5k), 1.272 ($37,949).",
                "wave": "Sóng (A) xong tại $57.8k; Sóng (B) xong tại $87.4k. Hiện tại nến $75.8k là đáy sóng con C-1. Chuẩn bị cho nhịp hồi C-2 trước khi đổ đèo C-3, C-4, C-5.",
                "time": "Đã đi 5 tuần kể từ đỉnh Sóng (B) $87.4k. Chu kỳ phản ứng Fibonacci Time Zone tại tuần thứ 8-9 (cuối tháng 11/2026).",
                "score": "5/6 Điểm Bán Thuận Xu Hướng: Giá dưới MA20, MACD phân kỳ âm khung tuần, Volume bán áp đảo.",
                "scenario": "Canh Bán hồi C-2 tại $80k-$81.5k. TP1: $48,500, TP2: $37,949. Điểm vô hiệu hóa: $88,500 (Vượt đỉnh Sóng B).",
                "tactics": "Chờ nến rút chân chạm kháng cự $80k-$81.5k xuất hiện Bearish Pinbar trên khung 4H/1D để mở vị thế Short."
            },
            "D": {
                "trend": "Downtrend rõ rệt. Giá kiểm định lại đáy $74,888, đường MA10 dốc xuống cắt dưới MA20 Daily.",
                "range": "Biên độ dao động ngày: $74,800 - $81,200. Kháng cự ngắn hạn: $80,500.",
                "wave": "Đang hoàn tất nhịp xả của sóng con C-1, bắt đầu hình thành vùng giằng co tích lũy trước nhịp hồi C-2.",
                "time": "Nến thứ 14 từ đỉnh $87.4k, biên độ nén hẹp dần.",
                "score": "4/6 Điểm: RSI ngày ở mức 38 (vùng cận quá bán), lực bán suy giảm nhẹ.",
                "scenario": "Chờ nhịp hồi kỹ thuật chạm MA20 Daily quanh $80,500 để kích hoạt lệnh Bán.",
                "tactics": "Không Bán đuổi tại hỗ trợ $75k; chỉ mở vị thế Bán khi có nhịp hồi kiểm định cản."
            },
            "4H": {
                "trend": "Sideway Down. Giá đi ngang tích lũy quanh $75,500 - $76,800 sau nhịp xả mạnh.",
                "range": "Hỗ trợ 4H: $74,888; Kháng cự 4H: $77,500 và $79,800.",
                "wave": "Sóng phụ ngắn hạn: Hình thành mô hình nêm giảm (Falling Wedge) hoặc tam giác tích lũy đáy C-1.",
                "time": "Nến 4H thứ 18, khả năng bứt phá hồi kỹ thuật trong 24-48 giờ tới.",
                "score": "RSI 4H phân kỳ dương nhẹ ở mức 34, báo hiệu sắp có nhịp phục hồi kỹ thuật C-2.",
                "scenario": "Scalping lướt sóng hồi ngắn lên $80k, hoặc kiên nhẫn chờ bán tại $80.5k-$81k.",
                "tactics": "Đặt cảnh báo giá tại $80,000; quản trị vốn với tỷ lệ R/R = 1 : 3.85."
            },
            "1H": {
                "trend": "Sideway giằng co biên độ hẹp quanh $75,600 - $76,200.",
                "range": "Hỗ trợ: $75,200; Kháng cự: $76,800.",
                "wave": "Các nhịp sóng nhỏ dao động tích lũy lực cầu bắt đáy ngắn hạn.",
                "time": "Nến 1H đang bám dải dưới Bollinger Bands.",
                "score": "Chờ tín hiệu MA10 cắt lên MA20 1H để xác nhận bắt đầu sóng hồi C-2.",
                "scenario": "Theo dõi điểm đảo chiều vi mô để tối ưu hóa giá vào lệnh Bán tại vùng cản trên.",
                "tactics": "Tuân thủ nghiêm ngặt điểm dừng lỗ Stop Loss $88,500."
            }
        }
    },
        "VND": {
        "title": "BÁO CÁO PHÂN TÍCH KỸ THUẬT & KỊCH BẢN GIAO DỊCH CỔ PHIẾU VNDIRECT (HOSE: VND)",
        "market_type": "Việt Nam / Dịch vụ Tài chính - Chứng khoán",
        "timeframes": ["M", "W", "D", "1H"],
        "tf_desc": "M (Dài hạn) | W (Trung hạn) | D (Ngắn hạn) | 1H (Điểm vào lệnh)",
        "chart_png": os.path.abspath("outputs/investment/chart_scenario_VND_pro.png"),
        "summary": "Cổ phiếu VND đã hoàn tất trọn vẹn chu kỳ điều chỉnh Zigzag A-B-C kéo dài từ đỉnh lịch sử 26.58k về vùng đáy kép 12.60k - 12.75k. Nến tuần hiện tại bứt phá mạnh mẽ lên 14.95k (+12.4%) với khối lượng kỷ lục 102.7 triệu cổ phiếu, MA10 cắt lên MA20 tuần, MACD phân kỳ dương 2 đoạn xác nhận khởi động chân Sóng đẩy (1) mới. P/B 1.05x tiệm cận đáy lịch sử là bệ đỡ an toàn. Chiến lược: Canh Mua tích lũy tại vùng 14.20k - 14.80k, mục tiêu chốt lời TP1: 17.50k (+17.1%) và TP2: 21.00k (+40.5%). Điểm vô hiệu hóa (Stop Loss) tại 13.70k (thủng đáy nền tích lũy tuần).",
        "pillars": {
            "M": {
                "trend": "Tích lũy đáy chu kỳ lớn sau nhịp giảm A-B-C. Giá giữ vững trên vùng hỗ trợ dài hạn 13.0k - 14.0k.",
                "range": "Fibo Retracement chu kỳ: 0.382 (17.5k), 0.500 (19.6k), 0.618 (21.7k). Đỉnh cũ: 26.58k.",
                "wave": "Hoàn tất Sóng điều chỉnh C lớn tại 12.60k. Chuẩn bị bước vào chu kỳ 5 sóng đẩy tăng trưởng mới.",
                "time": "Tháng thứ 14 điều chỉnh, bước vào vùng hội tụ thời gian đảo chiều chu kỳ cuối năm 2026.",
                "score": "6/6 Điểm Tích Sản: Định giá P/B 1.05x hấp dẫn nhất 5 năm, hưởng lợi lớn từ chu kỳ nâng hạng TTCK.",
                "scenario": "Tích sản dài hạn vùng 13.0k - 14.8k. TP1 dài hạn: 21.0k, TP2: 26.5k.",
                "tactics": "Giải ngân chia 3 bước: 30% vùng nền, 40% khi xác nhận trend, 30% khi retest thành công."
            },
            "W": {
                "trend": "Bứt phá đảo chiều (Trend Reversal). Giá đóng nến tuần vượt dứt khoát MA10, MA20 tuần tại 14.95k.",
                "range": "Hỗ trợ cứng: 13.70k; Kháng cự gần: 16.50k (MA50 tuần); Kháng cự mạnh: 17.50k và 21.00k.",
                "wave": "Sóng (A) về 13.90k, Sóng (B) hồi 19.10k, Sóng (C) cạn kiệt tạo đáy kép tại 12.60k. Bắt đầu Sóng đẩy 1.",
                "time": "26 tuần điều chỉnh kể từ đỉnh Sóng B, chu kỳ bán tháo hoàn toàn kết thúc.",
                "score": "5/6 Điểm Mua Chu Kỳ: Nến Marubozu xanh nổ vol 102.7M CP kỷ lục, MACD cắt lên đường 0.",
                "scenario": "Canh Mua vùng 14.20k - 14.80k. TP1: 17.50k (+17.1%), TP2: 21.00k (+40.5%). Stop Loss: 13.70k.",
                "tactics": "Nắm giữ trung hạn từ 3 đến 6 tháng, tỷ lệ R/R = 1 : 3.80."
            },
            "D": {
                "trend": "Uptrend ngắn hạn mạnh mẽ. Đường giá tạo mô hình 2 Đáy (Double Bottom) bứt phá qua viền cổ 14.2k.",
                "range": "Vùng tích lũy: 13.0k - 14.0k. Cản ngắn hạn: 15.1k - 15.5k.",
                "wave": "Đang trong nhịp Sóng 1 đẩy ngắn hạn, chuỗi 3 nến xanh liên tiếp với volume gia tăng mạnh.",
                "time": "Phiên thứ 3 sau điểm nổ Breakout đảo chiều khỏi kênh giảm.",
                "score": "5/6 Điểm: MACD phân kỳ dương 2 đoạn rõ nét, RSI Daily vượt mốc 60.",
                "scenario": "Chờ nhịp pullback lành mạnh kiểm định lại vùng 14.2k - 14.6k để gia tăng vị thế.",
                "tactics": "Mua gom trong các nhịp điều chỉnh rung lắc trong phiên giao dịch."
            },
            "1H": {
                "trend": "Strong Bullish Intraday. Giá nằm hoàn toàn trên MA10 và MA20 khung 1H.",
                "range": "Hỗ trợ 1H: 14.65k; Kháng cự 1H: 15.10k.",
                "wave": "Sóng đẩy ngắn hạn khung 1H bứt phá dứt khoát.",
                "time": "Dòng tiền lớn mua chủ động xuyên suốt phiên chiều.",
                "score": "Đủ điều kiện giải ngân vị thế ngắn hạn.",
                "scenario": "Canh Mua quanh 14.60k - 14.80k khi nến 1H test lại MA20, Stop Loss đặt tại 14.40k.",
                "tactics": "Giải ngân theo nhịp trùng xuống của thị trường chung."
            }
        }
    },
    "FPT": {
        "title": "BÁO CÁO PHÂN TÍCH KỸ THUẬT & KỊCH BẢN GIAO DỊCH CỔ PHIẾU FPT (HOSE: FPT)",
        "market_type": "Việt Nam / Cổ phiếu Bluechip",
        "timeframes": ["M", "W", "D", "1H"],
        "tf_desc": "M (Dài hạn) | W (Trung hạn) | D (Ngắn hạn) | 1H (Điểm vào lệnh)",
        "chart_png": os.path.abspath("outputs/investment/chart_scenario_FPT_pro.png"),
        "summary": "Cổ phiếu FPT đã hoàn tất trọn vẹn chu kỳ điều chỉnh Zigzag A-B-C kéo dài từ đỉnh lịch sử 97.48k về vùng hỗ trợ cứng 49.55k. Nến tuần hiện tại (50.80k) xuất hiện nến rút chân búa (Hammer) với khối lượng cạn kiệt, xác nhận thiết lập đáy chu kỳ và khởi động Sóng 1 của chu kỳ 5 sóng đẩy mới. Chiến lược chủ đạo: Canh Mua tích lũy tại vùng 50.0k - 51.5k, mục tiêu chốt lời TP1: 68.0k (Sóng 3 mở rộng) và TP2: 82.0k (Sóng 5). Điểm vô hiệu hóa (Stop Loss) tại 48.5k (thủng đáy Sóng C).",
        "pillars": {
            "M": {
                "trend": "Uptrend thế kỷ 15 năm. Giá điều chỉnh về chạm hỗ trợ MA20 Tháng (vùng 48k-50k), duy trì cấu trúc tăng dài hạn.",
                "range": "Fibo Retracement dài hạn: 0.500 (50.2k), 0.618 (44.5k). Đỉnh lịch sử: 97.48k.",
                "wave": "Chu kỳ siêu sóng III lớn: Sóng điều chỉnh IV đã chạm vùng hỗ trợ cân bằng, sẵn sàng bước vào Siêu sóng V bứt phá đỉnh mới.",
                "time": "Tháng thứ 10 của chu kỳ điều chỉnh, bước vào vùng hội tụ chu kỳ Fibonacci Time (Tháng 11-12/2026).",
                "score": "6/6 Điểm Tích Sản: Doanh nghiệp đầu ngành công nghệ, định giá P/E về vùng hấp dẫn lịch sử.",
                "scenario": "Tích sản dài hạn quanh 48k - 52k. TP dài hạn: 97.5k và 120k.",
                "tactics": "Giải ngân từng phần 30% - 30% - 40% theo khung thời gian tháng."
            },
            "W": {
                "trend": "Chuyển từ Downtrend điều chỉnh sang hình thành Đáy đảo chiều. Giá đóng nến tuần giữ vững trên mốc 50k.",
                "range": "Hỗ trợ cứng: 49.55k; Kháng cự gần: 58.0k (MA50); Kháng cự mạnh: 68.0k.",
                "wave": "Sóng (A) về 62.77k, Sóng (B) hồi 70.64k, Sóng (C) cạn kiệt tại 49.55k. Bắt đầu Sóng 1 đẩy mới.",
                "time": "22 tuần điều chỉnh kể từ đỉnh Sóng B, chu kỳ bán tháo đã hoàn tất.",
                "score": "5/6 Điểm Mua Chu Kỳ: Nến Hammer rút chân tuần, RSI tuần phục hồi từ vùng 35.",
                "scenario": "Canh Mua vùng 50.0k - 51.5k. TP1: 68.0k, TP2: 82.0k. Stop Loss: 48.5k.",
                "tactics": "Nắm giữ trung hạn từ 3 đến 6 tháng, tỷ lệ R/R = 1 : 4.20."
            },
            "D": {
                "trend": "Tạo đáy cân bằng (Base Building). Đường giá tạo mô hình Đáy Đôi (Double Bottom) tại 49.55k - 50.0k.",
                "range": "Vùng tích lũy: 50.0k - 52.5k. Cản ngắn hạn MA20 Daily: 53.5k.",
                "wave": "Đang ở chân Sóng 1 của chu kỳ mới, nến xanh chiếm ưu thế trong 3 phiên gần nhất.",
                "time": "Phiên thứ 5 tích lũy đi ngang sau nhịp test đáy 49.55k.",
                "score": "5/6 Điểm: MACD Histogram phân kỳ dương 2 đoạn, lực cầu bắt đáy gia tăng.",
                "scenario": "Mua gia tăng tỷ trọng khi FPT đóng nến vượt dứt khoát 52.5k kèm volume > 5 triệu cổ phiếu.",
                "tactics": "Mua gom trong các phiên rung lắc điều chỉnh đầu phiên sáng."
            },
            "1H": {
                "trend": "Short-term Uptrend. Giá vượt lên trên đường MA20 1H tại 50.6k.",
                "range": "Hỗ trợ 1H: 50.5k; Kháng cự 1H: 51.8k.",
                "wave": "Sóng đẩy ngắn hạn khung 1H bứt phá kênh tích lũy.",
                "time": "Khối lượng gia tăng đột biến vào phiên chiều (sau 14h00).",
                "score": "Đủ điều kiện kích hoạt lệnh Mua thăm dò.",
                "scenario": "Canh Mua quanh 50.6k - 51.0k, Stop Loss đặt chặt chẽ dưới 49.5k.",
                "tactics": "Chia nhỏ lệnh giải ngân theo nhịp võng của chỉ số VN-Index."
            }
        }
    },
    "XAUUSD": {
        "title": "BÁO CÁO PHÂN TÍCH KỸ THUẬT & KỊCH BẢN GIAO DỊCH VÀNG THẾ GIỚI (XAUUSD)",
        "market_type": "Quốc tế / Hàng hóa kim loại quý",
        "timeframes": ["W", "D", "1H"],
        "tf_desc": "W (Trung hạn) | D (Ngắn hạn) | 1H (Điểm vào lệnh)",
        "chart_png": os.path.abspath("outputs/investment/chart_scenario_XAUUSD_pro.png"),
        "summary": "Vàng thế giới (XAUUSD) đã hoàn tất toàn bộ chu kỳ sóng điều chỉnh lớn A-B-C từ đỉnh kỷ lục $5,586.20 về chạm đáy hoàn thành tại $3,879.30 (đầu tháng 11/2026). Nến hiện tại ($4,074.90) đã đảo chiều bứt phá mạnh, xác nhận bắt đầu chu kỳ 5 sóng đẩy mới. Chiến lược chủ đạo: Canh Mua giải ngân tại vùng test hỗ trợ $3,980 - $4,050, hướng tới mục tiêu TP1: $4,850 và TP2: $5,580 (đỉnh cũ). Điểm vô hiệu hóa (Stop Loss) tại $3,850 (thủng đáy $3,879).",
        "pillars": {
            "W": {
                "trend": "Đảo chiều tăng từ đáy chu kỳ. Nến tuần xanh tăng vọt hơn $195 từ đáy $3,879 lên $4,074.90.",
                "range": "Hỗ trợ đáy: $3,879.30; Kháng cự: $4,450 và $4,850; Đỉnh cũ: $5,586.20.",
                "wave": "Sóng (A) về $4,100, Sóng (B) hồi $4,783, Sóng (C) cạn kiệt tại $3,879. Bắt đầu Sóng 1 đẩy mới.",
                "time": "Hoàn tất chu kỳ điều chỉnh 38 tuần sau đỉnh $5,586.",
                "score": "5/6 Điểm Mua: MACD Histogram tạo phân kỳ dương, lực mua bắt đáy áp đảo.",
                "scenario": "Canh Mua trung hạn $3,980 - $4,050. TP1: $4,850, TP2: $5,580. Stop Loss: $3,850.",
                "tactics": "Nắm giữ vị thế Buy Swing theo xu hướng lớn, bảo toàn vị thế khi giá vượt $4,300."
            },
            "D": {
                "trend": "Uptrend ngắn hạn. Nến ngày bứt phá khỏi vùng nén $3,880-$3,920, đóng cửa trên MA10 Daily.",
                "range": "Vùng hỗ trợ: $4,000 - $4,030; Cản MA20 Daily: $4,150.",
                "wave": "Sóng 1 con bứt phá mạnh, đang tìm điểm cân bằng tích lũy.",
                "time": "Phiên thứ 4 liên tiếp đóng nến xanh thân dài.",
                "score": "5/6 Điểm: MACD phân kỳ dương 3 đoạn, RSI ngày hồi lên mức 52.",
                "scenario": "Chờ nhịp điều chỉnh lành mạnh về quanh $4,020-$4,050 để giải ngân.",
                "tactics": "Không mua đuổi khi RSI tiến sát 65; canh nến điều chỉnh giảm volume."
            },
            "1H": {
                "trend": "Uptrend mạnh, giá bám dải trên Bollinger Bands.",
                "range": "Hỗ trợ: $4,050; Kháng cự: $4,095.",
                "wave": "Sóng đẩy 1H mở rộng 5 sóng nhỏ.",
                "time": "Các nhịp nén ngắn hạn trước khi mở rộng phiên Mỹ.",
                "score": "Tín hiệu Mua lướt sóng rõ rệt.",
                "scenario": "Canh Buy Limit quanh $4,045-$4,055, SL: $4,025, TP: $4,090.",
                "tactics": "Quản trị lệnh chặt chẽ theo phiên giao dịch London / New York."
            }
        }
    }
}


# =============================================================
# EXCEL GENERATOR (MA TRẬN 6 TRỤ CỘT ĐA KHUNG)
# =============================================================
def generate_excel_report(sym, cfg):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Phan_Tich_Ky_Thuat_{sym}"

    cols_tf = cfg["timeframes"]
    headers = ["Trụ Cột Fsen"] + cols_tf + ["Ý Nghĩa & Ghi Chú Chiến Thuật"]

    today = datetime.now()
    next_week = today + timedelta(days=6)
    date_str = f"{today.strftime('%d/%m')} - {next_week.strftime('%d/%m/%Y')}"

    # Tiêu đề
    ws.merge_cells(f"A1:{get_column_letter(len(headers))}1")
    t_cell = ws["A1"]
    t_cell.value = f"BẢNG PHÂN TÍCH KỸ THUẬT 6 TRỤ CỘT & SÓNG ELLIOTT — {sym} ({date_str})"
    t_cell.font = Font(name="Times New Roman", size=13, bold=True, color="1B365D")
    t_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 32

    # Header hàng 2
    ws.row_dimensions[2].height = 25
    h_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
    h_font = Font(name="Times New Roman", size=10.5, bold=True, color="000000")
    thin_border = Border(
        left=Side(style='thin', color='A6A6A6'), right=Side(style='thin', color='A6A6A6'),
        top=Side(style='thin', color='A6A6A6'), bottom=Side(style='thin', color='A6A6A6')
    )

    for c_idx, h_text in enumerate(headers, start=1):
        c = ws.cell(row=2, column=c_idx)
        c.value = h_text
        c.fill = h_fill
        c.font = h_font
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = thin_border

    rows_def = [
        ("XU HƯỚNG", "trend", "Đánh giá cấu trúc giá, vị thế so với 4MA (10, 20, 50, 200) và các mốc cản then chốt."),
        ("BIÊN ĐỘ & FIBO", "range", "Các mốc tỷ lệ vàng Fibonacci Retracement (0.382, 0.500, 0.618) và Extension đo mục tiêu giá."),
        ("SÓNG ELLIOTT", "wave", "Vị trí sóng đẩy/sóng chỉnh, đối soát MACD và Điểm Vô Hiệu Hóa kịch bản (Stop Loss) bất biến."),
        ("THỜI GIAN", "time", "Đếm số nến chu kỳ, vùng hội tụ thời gian Fibonacci Time Zone đảo chiều xu hướng."),
        ("BỘ CHẤM ĐIỂM", "score", "Định lượng xác suất thắng dựa trên 6 tiêu chí kỹ thuật đồng thuận."),
        ("KỊCH BẢN TÁC CHIẾN", "scenario", "Kế hoạch hành động cụ thể: Vùng Canh Lệnh, Mục Tiêu Chốt Lời TP1, TP2 và Điểm Cắt Lỗ."),
        ("CHIẾN THUẬT VÀO LỆNH", "tactics", "Chiến thuật bắt nhịp điều chỉnh ngắn hạn thuận theo xu hướng lớn, tỷ lệ Risk/Reward.")
    ]

    for r_idx, (r_name, r_key, note) in enumerate(rows_def, start=3):
        # Cột A
        cA = ws.cell(row=r_idx, column=1)
        cA.value = r_name
        cA.font = Font(name="Times New Roman", size=10, bold=True, color="1B365D")
        cA.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cA.border = thin_border
        cA.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

        # Cột các khung thời gian
        for col_i, tf in enumerate(cols_tf, start=2):
            cell = ws.cell(row=r_idx, column=col_i)
            tf_info = cfg["pillars"].get(tf, {})
            val = tf_info.get(r_key, "Chưa có dữ liệu")
            cell.value = val
            cell.font = Font(name="Times New Roman", size=9)
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            cell.border = thin_border

        # Cột Ghi chú
        cG = ws.cell(row=r_idx, column=len(headers))
        cG.value = note
        cG.font = Font(name="Times New Roman", size=9, italic=True)
        cG.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cG.border = thin_border
        cG.fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

        ws.row_dimensions[r_idx].height = 75

    ws.column_dimensions['A'].width = 18
    for col_i in range(2, 2 + len(cols_tf)):
        ws.column_dimensions[get_column_letter(col_i)].width = 34
    ws.column_dimensions[get_column_letter(len(headers))].width = 28

    xlsx_path = os.path.join(out_dir, f"Bang_Phan_Tich_Tuan_{sym}.xlsx")
    wb.save(xlsx_path)
    print(f"[+] Saved Excel: {xlsx_path}")
    return xlsx_path


# =============================================================
# WORD GENERATOR (BÁO CÁO PHÂN TÍCH KỸ THUẬT CHUYÊN NGHIỆP)
# =============================================================
def generate_word_report(sym, cfg):
    doc = docx.Document()

    for sec in doc.sections:
        sec.top_margin = Inches(0.65)
        sec.bottom_margin = Inches(0.65)
        sec.left_margin = Inches(0.65)
        sec.right_margin = Inches(0.65)

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(10)

    # 1. TIÊU ĐỀ
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_after = Pt(2)

    r_sub = title_p.add_run("BỘ NÃO PHÂN TÍCH KỸ THUẬT 6 TRỤ CỘT FSEN & SÓNG ELLIOTT\n")
    r_sub.font.bold = True
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = RGBColor(0x0F, 0x4C, 0x81)

    today = datetime.now()
    next_week = today + timedelta(days=6)
    date_str = f"{today.strftime('%d/%m')} - {next_week.strftime('%d/%m/%Y')}"
    r_main = title_p.add_run(f"{cfg['title']}\n")
    r_main.font.bold = True
    r_main.font.size = Pt(15)
    r_main.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    r_desc = title_p.add_run(f"Kỳ phân tích: {date_str} | Thị trường: {cfg['market_type']} | Đa khung: {cfg['tf_desc']}")
    r_desc.font.italic = True
    r_desc.font.size = Pt(8.5)
    r_desc.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # 2. TÓM TẮT ĐIỀU HÀNH & KỊCH BẢN CỐT LÕI
    h_sum = doc.add_paragraph()
    r_hs = h_sum.add_run("I. TÓM TẮT ĐIỀU HÀNH & KẾ HOẠCH TÁC CHIẾN CỐT LÕI")
    r_hs.font.bold = True
    r_hs.font.size = Pt(11.5)
    r_hs.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h_sum.paragraph_format.space_before = Pt(8)
    h_sum.paragraph_format.space_after = Pt(3)

    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_after = Pt(8)
    r_st = p_sum.add_run(cfg["summary"])
    r_st.font.size = Pt(10)

    # 3. BIỂU ĐỒ NẾN KỊCH BẢN CHUẨN XÁC
    if os.path.exists(cfg["chart_png"]):
        h_chart = doc.add_paragraph()
        r_hc = h_chart.add_run("II. BIỂU ĐỒ KỊCH BẢN SÓNG ELLIOTT & ĐIỂM VÔ HIỆU HÓA (STOP LOSS)")
        r_hc.font.bold = True
        r_hc.font.size = Pt(11.5)
        r_hc.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        h_chart.paragraph_format.space_before = Pt(6)
        h_chart.paragraph_format.space_after = Pt(4)

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(cfg["chart_png"], width=Inches(6.8))

        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_after = Pt(10)
        r_cap = p_caption.add_run(f"Hình 1: Biểu đồ nến kịch bản {sym} — Đường Vàng sóng lịch sử cắm khớp râu nến; Đường Cyan nét đứt dự báo từ nến hiện tại; Vạch đỏ Stop Loss.")
        r_cap.font.size = Pt(8)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

        # Hộp liên kết 1-Click mở trên Google Chrome (Port 8888)
        t_link = doc.add_table(rows=1, cols=1)
        t_link.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_link = t_link.rows[0].cells[0]
        set_cell_background(c_link, "F0F9FF")
        set_cell_margins(c_link, top=100, bottom=100, left=140, right=140)

        offline_url = f"chart_scenario_{sym}.html"
        http_url = f"http://localhost:8888/chart_scenario_{sym}.html"
        
        p_lnk1 = c_link.paragraphs[0]
        p_lnk1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lnk1.add_run("⚡ ")
        add_hyperlink(p_lnk1, offline_url, f"MỞ BIỂU ĐỒ CHẠY NGAY TỨC THÌ (100% OFFLINE KHÔNG CẦN SERVER) ↗", color="008000")
        
        p_lnk2 = c_link.add_paragraph()
        p_lnk2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lnk2.paragraph_format.space_before = Pt(3)
        p_lnk2.add_run("🌐 ")
        add_hyperlink(p_lnk2, http_url, f"HOẶC MỞ QUA WEB SERVER LOCALHOST (HTTP://LOCALHOST:8888) ↗", color="0284C7")


    # 3.5 BẢNG DỰ BÁO SÓNG FSEN TƯƠNG LAI (DỰA TRÊN SÓNG ĐẰNG TRƯỚC)
    from invest_fsen_projection_engine import ASSETS_PROJECTION_REGISTRY, calculate_projection_metrics
    if sym in ASSETS_PROJECTION_REGISTRY:
        proj_cfg = ASSETS_PROJECTION_REGISTRY[sym]
        proj = calculate_projection_metrics(
            proj_cfg["p0"], proj_cfg["p1"], proj_cfg["p2"],
            proj_cfg["is_bullish"], proj_cfg["t0"], proj_cfg["t1"], proj_cfg["t2"]
        )
        
        h_proj = doc.add_paragraph()
        r_hp = h_proj.add_run("II. BẢNG KẾ HOẠCH DỰ BÁO SÓNG FSEN TƯƠNG LAI (DỰA VÀO SÓNG ĐẰNG TRƯỚC)")
        r_hp.font.bold = True
        r_hp.font.size = Pt(11.5)
        r_hp.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        h_proj.paragraph_format.space_before = Pt(8)
        h_proj.paragraph_format.space_after = Pt(3)

        p_desc = doc.add_paragraph()
        r_pd = p_desc.add_run(f"• Mô hình dự kiến: {proj['pattern']} | Chiến lược: {proj['direction']}\n"
                              f"• Điểm vô hiệu hóa tuyệt đối: INVALID tại {proj['invalidation']} (Vượt mốc này kịch bản hủy bỏ)\n"
                              f"• Chiều cao Sóng 1 (H1): {proj['h1']} (Điểm bứt phá CHoCH tại {proj['anchor_p1']}) | Sóng 2 hồi: {proj['ret2_pct']}%")
        r_pd.font.size = Pt(9.5)
        r_pd.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        p_desc.paragraph_format.space_after = Pt(4)

        t_proj = doc.add_table(rows=7, cols=4)
        t_proj.alignment = WD_TABLE_ALIGNMENT.CENTER
        proj_headers = ["Bước Sóng", "Công Thức Đo Sóng Trước", "Mục Tiêu Giá", "Ý Nghĩa Kỹ Thuật & Tỷ Lệ R/R"]
        proj_rows = [
            ("Sóng 0 -> 1", "Khởi nguồn & Chân sóng", f"{proj['anchor_p0']} -> {proj['anchor_p1']}", f"Biên độ H1 = {proj['h1']}, xác nhận tín hiệu CHoCH đảo cấu trúc."),
            ("Sóng 2~", f"Hồi quy {proj['ret2_pct']}% của Sóng 1", f"{proj['anchor_p2']}", f"Vùng đệm hỗ trợ/kháng cự nến tuần. Mức INVALID: {proj['invalidation']}."),
            ("Sóng 3? (Target)", f"1.618 x H1 (từ Sóng 2)", f"{proj['w3_target']}", f"Sóng đẩy mạnh nhất chu kỳ, tỷ lệ R/R đạt 1 : {proj['rr_w3']}."),
            ("Sóng 4? (Pullback)", f"Thoái lui 0.382 x Sóng 3", f"{proj['w4_target']}", f"Tích lũy luân phiên, bảo toàn thiết luật không vi phạm đỉnh S1 ({proj['anchor_p1']})."),
            ("Sóng 5? (Bùng nổ)", f"1.000 x H1 (hoặc Fibo chu kỳ)", f"{proj['w5_target']}", f"Đạt đỉnh chu kỳ 5 sóng đẩy trước khi chuyển sang pha điều chỉnh lớn."),
            ("Chuỗi A? - B? - C?", "Hiệu chỉnh 3 nhịp Fsen", f"A: {proj['wa_target']} | B: {proj['wb_target']} | C: {proj['wc_target']}", f"Tái tích lũy xây nền giá mới cho chu kỳ tăng trưởng dài hạn tiếp theo.")
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

    # 4. MA TRẬN 6 TRỤ CỘT ĐA KHUNG
    h_tab = doc.add_paragraph()
    r_ht = h_tab.add_run("III. MA TRẬN PHÂN TÍCH 6 TRỤ CỘT FSEN ĐA KHUNG THỜI GIAN")
    r_ht.font.bold = True
    r_ht.font.size = Pt(11.5)
    r_ht.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h_tab.paragraph_format.space_before = Pt(6)
    h_tab.paragraph_format.space_after = Pt(4)

    cols_tf = cfg["timeframes"]
    headers = ["Trụ Cột"] + cols_tf + ["Ý Nghĩa & Ghi Chú"]
    num_cols = len(headers)

    table = doc.add_table(rows=8, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "1B365D")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            run.font.size = Pt(8.5)

    rows_def = [
        ("XU HƯỚNG", "trend", "Đánh giá cấu trúc xu hướng, vị thế MA10/MA20/MA50 và các mốc cản then chốt."),
        ("BIÊN ĐỘ & FIBO", "range", "Các mốc tỷ lệ vàng Fibo Retracement và Extension đo lường mục tiêu giá."),
        ("SÓNG ELLIOTT", "wave", "Vị trí chu kỳ sóng, đối soát MACD và Điểm Vô Hiệu Hóa (Stop Loss)."),
        ("THỜI GIAN", "time", "Đếm số nến chu kỳ, vùng hội tụ thời gian Fibonacci Time Zone đảo chiều."),
        ("BỘ CHẤM ĐIỂM", "score", "Định lượng xác suất thành công dựa trên sự đồng thuận của các chỉ báo."),
        ("KỊCH BẢN", "scenario", "Kế hoạch hành động cụ thể: Vùng Canh Lệnh, Mục Tiêu Chốt Lời TP1, TP2 và Stop Loss."),
        ("CHIẾN THUẬT", "tactics", "Chiến thuật bắt nhịp điều chỉnh ngắn hạn thuận theo xu hướng lớn, quản trị rủi ro.")
    ]

    for r_idx, (r_name, r_key, note) in enumerate(rows_def, start=1):
        row_cells = table.rows[r_idx].cells
        # Cột A
        row_cells[0].text = r_name
        set_cell_background(row_cells[0], "F2F2F2")
        pA = row_cells[0].paragraphs[0]
        pA.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in pA.runs:
            r.font.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

        # Khung thời gian
        for col_i, tf in enumerate(cols_tf, start=1):
            val = cfg["pillars"].get(tf, {}).get(r_key, "N/A")
            row_cells[col_i].text = val
            p_tf = row_cells[col_i].paragraphs[0]
            p_tf.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p_tf.runs:
                r.font.size = Pt(8)

        # Ghi chú
        row_cells[num_cols - 1].text = note
        set_cell_background(row_cells[num_cols - 1], "FAFAFA")
        pG = row_cells[num_cols - 1].paragraphs[0]
        pG.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in pG.runs:
            r.font.italic = True
            r.font.size = Pt(7.8)

    docx_path = os.path.join(out_dir, f"Bang_Phan_Tich_Tuan_{sym}.docx")
    doc.save(docx_path)
    print(f"[+] Saved Word: {docx_path}")
    return docx_path


# =============================================================
# MASTER RUNNER
# =============================================================
print("[*] Generating Master Technical Analysis Reports (Word & Excel)...")
for sym, cfg in REPORTS_CONFIG.items():
    generate_excel_report(sym, cfg)
    generate_word_report(sym, cfg)

print("\n[SUCCESS] Completed All Master Technical Analysis Reports!")

