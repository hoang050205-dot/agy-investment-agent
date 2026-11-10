"""
Invest Fundamental Analyzer — Phân tích Báo cáo Tài chính & Economic Moat
Tuân thủ tài liệu PTBCTC NHANH.docx (Hệ thống 3 đèn cảnh báo + 7 Economic Moats)
"""

import os
import sys
import json
import argparse
from datetime import datetime


def evaluate_warnings(profile: dict) -> dict:
    """Đánh giá hệ thống 3 đèn cảnh báo theo tiêu chuẩn PTBCTC NHANH"""
    warnings = {
        "balance_sheet": [],
        "income_statement": [],
        "cash_flow": [],
        "scores": {"green": 0, "orange": 0, "red": 0}
    }

    # 1. BẢNG CÂN ĐỐI KẾ TOÁN
    de = profile.get("debt_to_equity")
    if de is not None:
        if de > 1.0:
            warnings["balance_sheet"].append({
                "metric": "D/E (Nợ/VCSH)",
                "value": f"{de:.2f}",
                "threshold": "< 1.0",
                "status": "RED",
                "message": "Nợ vay vượt vốn chủ sở hữu, cơ cấu vốn có rủi ro tài chính."
            })
            warnings["scores"]["red"] += 1
        else:
            warnings["balance_sheet"].append({
                "metric": "D/E (Nợ/VCSH)",
                "value": f"{de:.2f}",
                "threshold": "< 1.0",
                "status": "GREEN",
                "message": "Cơ cấu vốn lành mạnh, nợ vay nằm trong ngưỡng an toàn."
            })
            warnings["scores"]["green"] += 1

    roe = profile.get("roe")
    if roe is not None:
        if roe >= 15.0:
            warnings["balance_sheet"].append({
                "metric": "ROE",
                "value": f"{roe:.2f}%",
                "threshold": "> 15%",
                "status": "GREEN_DARK",
                "message": "Hiệu quả sử dụng vốn chủ sở hữu vượt trội (>15%)."
            })
            warnings["scores"]["green"] += 1
        else:
            warnings["balance_sheet"].append({
                "metric": "ROE",
                "value": f"{roe:.2f}%",
                "threshold": "> 15%",
                "status": "YELLOW",
                "message": "ROE dưới mức kỳ vọng 15%."
            })

    cr = profile.get("current_ratio")
    if cr is not None:
        if cr < 1.0:
            warnings["balance_sheet"].append({
                "metric": "Current Ratio (Thanh toán hiện hành)",
                "value": f"{cr:.2f}",
                "threshold": ">= 1.0",
                "status": "RED",
                "message": "Tài sản ngắn hạn nhỏ hơn nợ ngắn hạn, rủi ro thanh khoản cao."
            })
            warnings["scores"]["red"] += 1
        else:
            warnings["balance_sheet"].append({
                "metric": "Current Ratio",
                "value": f"{cr:.2f}",
                "threshold": ">= 1.0",
                "status": "GREEN",
                "message": "Khả năng thanh toán ngắn hạn dồi dào."
            })
            warnings["scores"]["green"] += 1

    # 2. BÁO CÁO KẾT QUẢ KINH DOANH
    gm = profile.get("gross_margin")
    if gm is not None:
        if gm < 35.0:
            warnings["income_statement"].append({
                "metric": "Biên lợi nhuận gộp",
                "value": f"{gm:.2f}%",
                "threshold": ">= 35%",
                "status": "ORANGE",
                "message": "Biên lãi gộp < 35%, cần lưu ý về sức mạnh định giá sản phẩm."
            })
            warnings["scores"]["orange"] += 1
        else:
            warnings["income_statement"].append({
                "metric": "Biên lợi nhuận gộp",
                "value": f"{gm:.2f}%",
                "threshold": ">= 35%",
                "status": "GREEN",
                "message": "Biên lãi gộp mạnh (>35%), dấu hiệu của lợi thế định giá vượt trội."
            })
            warnings["scores"]["green"] += 1

    om = profile.get("operating_margin")
    if om is not None:
        if om < 15.0:
            warnings["income_statement"].append({
                "metric": "Biên lợi nhuận hoạt động",
                "value": f"{om:.2f}%",
                "threshold": ">= 15%",
                "status": "ORANGE",
                "message": "Biên hoạt động < 15%."
            })
            warnings["scores"]["orange"] += 1
        else:
            warnings["income_statement"].append({
                "metric": "Biên lợi nhuận hoạt động",
                "value": f"{om:.2f}%",
                "threshold": ">= 15%",
                "status": "GREEN",
                "message": "Biên hoạt động tốt (>15%)."
            })
            warnings["scores"]["green"] += 1

    nm = profile.get("net_margin")
    if nm is not None:
        if nm < 10.0:
            warnings["income_statement"].append({
                "metric": "Biên lợi nhuận ròng",
                "value": f"{nm:.2f}%",
                "threshold": ">= 10%",
                "status": "RED",
                "message": "Biên ròng mỏng (<10%), dễ bị tổn thương khi chi phí đầu vào biến động."
            })
            warnings["scores"]["red"] += 1
        else:
            warnings["income_statement"].append({
                "metric": "Biên lợi nhuận ròng",
                "value": f"{nm:.2f}%",
                "threshold": ">= 10%",
                "status": "GREEN",
                "message": "Biên ròng đạt chuẩn (>=10%)."
            })
            warnings["scores"]["green"] += 1

    # 3. LƯU CHUYỂN TIỀN TỆ
    fcf = profile.get("free_cash_flow")
    if fcf is not None:
        if fcf < 0:
            warnings["cash_flow"].append({
                "metric": "Dòng tiền tự do (FCF)",
                "value": f"{fcf:,.0f} VND",
                "threshold": "> 0",
                "status": "RED",
                "message": "FCF âm, doanh nghiệp cần huy động nợ hoặc vốn để tài trợ đầu tư."
            })
            warnings["scores"]["red"] += 1
        else:
            warnings["cash_flow"].append({
                "metric": "Dòng tiền tự do (FCF)",
                "value": f"{fcf:,.0f} VND",
                "threshold": "> 0",
                "status": "GREEN",
                "message": "FCF dương dồi dào, khả năng tự tài trợ và trả cổ tức rất cao."
            })
            warnings["scores"]["green"] += 1

    return warnings


def detect_economic_moat(symbol: str, profile: dict) -> dict:
    """Nhận diện 7 lợi thế cạnh tranh lâu bền (Economic Moat)"""
    moats_detected = []
    gm = profile.get("gross_margin", 0) or 0
    roe = profile.get("roe", 0) or 0
    fcf = profile.get("free_cash_flow", 0) or 0
    de = profile.get("debt_to_equity", 2) or 2

    # Quy tắc định lượng
    if gm >= 35.0:
        moats_detected.append({
            "name": "Lợi thế định giá / Độc quyền (Pricing Power)",
            "evidence": f"Biên lãi gộp đạt {gm:.1f}% (vượt chuẩn 35%)."
        })
    if roe >= 20.0:
        moats_detected.append({
            "name": "Hiệu quả vốn vượt trội (Capital Efficiency)",
            "evidence": f"ROE đạt {roe:.1f}% bền vững qua các kỳ."
        })
    if fcf > 1000e9:  # > 1000 tỷ FCF
        moats_detected.append({
            "name": "Cỗ máy in tiền mặt (Cash Generator)",
            "evidence": f"Dòng tiền tự do FCF đạt trên {fcf/1e9:,.0f} tỷ đồng."
        })
    if de < 0.8:
        moats_detected.append({
            "name": "Cơ cấu tài chính pháo đài (Fortress Balance Sheet)",
            "evidence": f"Hệ số nợ D/E ở mức {de:.2f} (thấp hơn nhiều so với chuẩn 1.0)."
        })

    # Đặc thù theo ngành cụ thể
    name = profile.get("name", "") + " " + symbol
    if any(k in name for k in ["SIP", "Khu công nghiệp", "VRG"]):
        moats_detected.append({
            "name": "Rào cản quỹ đất & Doanh thu chưa thực hiện (Real Estate Moat)",
            "evidence": "Quỹ đất KCN sạch quy mô lớn, dòng tiền khách hàng trả trước dài hạn."
        })
    elif any(k in name for k in ["FPT", "Công nghệ", "Phần mềm"]):
        moats_detected.append({
            "name": "Hiệu ứng quy mô & Chi phí chuyển đổi phần mềm (Switching Costs)",
            "evidence": "Hợp đồng IT toàn cầu dài hạn, khách hàng khó thay thế đối tác công nghệ."
        })

    is_strong_moat = len(moats_detected) >= 2
    return {
        "moats_count": len(moats_detected),
        "is_strong_moat": is_strong_moat,
        "classification": "MOAT MẠNH (Hào thành kinh tế sâu)" if is_strong_moat else "MOAT TRUNG BÌNH / HẸP",
        "details": moats_detected
    }


def analyze(symbol: str, data_dir: str = "sample-data/stock") -> dict:
    symbol = symbol.upper()
    profile_path = os.path.join(data_dir, symbol, "profile.json")

    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Không tìm thấy dữ liệu profile tại: {profile_path}")

    with open(profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    warnings = evaluate_warnings(profile)
    moat = detect_economic_moat(symbol, profile)

    # Đánh giá tổng quan 5 hạng mục
    summary = {
        "capital_structure": "Lành mạnh" if (profile.get("debt_to_equity") or 0) <= 1.0 else "Cần theo dõi nợ vay",
        "liquidity": "Tốt" if (profile.get("current_ratio") or 0) >= 1.0 else "Rủi ro ngắn hạn",
        "capital_efficiency": "Xuất sắc" if (profile.get("roe") or 0) >= 15.0 else "Trung bình",
        "earnings_quality": "Cao" if (profile.get("net_margin") or 0) >= 10.0 else "Mỏng",
        "cash_flow": "Dồi dào" if (profile.get("free_cash_flow") or 0) > 0 else "Thiếu hụt tiền mặt",
        "overall_health": "KHỎE MẠNH" if warnings["scores"]["red"] == 0 else ("CẦN THEO DÕI" if warnings["scores"]["red"] <= 2 else "YẾU")
    }

    result = {
        "symbol": symbol,
        "company_name": profile.get("name", ""),
        "evaluated_at": datetime.now().isoformat(),
        "summary": summary,
        "warnings": warnings,
        "economic_moat": moat
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Analyze fundamental data & moat")
    parser.add_argument("--symbol", type=str, required=True, help="Stock symbol")
    parser.add_argument("--data-dir", type=str, default="sample-data/stock", help="Data directory")
    args = parser.parse_args()

    res = analyze(args.symbol, args.data_dir)
    symbol = args.symbol.upper()
    out_path = os.path.join(args.data_dir, symbol, "fundamental_analysis.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    print(f"\n=== KẾT QUẢ PHÂN TÍCH BCTC & ECONOMIC MOAT: {symbol} ===")
    print(f"Doanh nghiệp: {res['company_name']}")
    print(f"Sức khỏe tài chính tổng quan: {res['summary']['overall_health']}")
    print(f"Hào thành kinh tế (Moat): {res['economic_moat']['classification']} ({res['economic_moat']['moats_count']} lợi thế)")
    print(f"Điểm đèn cảnh báo: Xanh={res['warnings']['scores']['green']} | Cam={res['warnings']['scores']['orange']} | Đỏ={res['warnings']['scores']['red']}")
    print(f"[+] Báo cáo chi tiết đã lưu: {out_path}\n")


if __name__ == "__main__":
    main()

