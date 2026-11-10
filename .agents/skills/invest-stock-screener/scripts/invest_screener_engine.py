"""
Invest Screener Engine — Bộ Máy Sàng Lọc Toàn Thị Trường Fsen & Định Giá
Công thức Combined Score:
  Combined Score = (FA Score * 30%) + (Valuation Score * 30%) + (TA Score * 25%) + (Wave Score * 15%)
Phân loại theo 5 Bộ Lọc Presets:
  1. Siêu Cổ Phiếu Giá Trị (Value Investing)
  2. Bùng Nổ Đà Tăng (Momentum Breakout)
  3. Bắt Đáy Quá Bán (Oversold Bounce)
  4. Cổ Tức Bền Vững (High Dividend)
  5. Theo Dõi Kích Hoạt (Watchlist Trigger)
"""

import os
import sys
import json
import pandas as pd
import numpy as np

# Danh sách cổ phiếu / tài sản kiểm nghiệm
UNIVERSE = [
    {
        "symbol": "FPT",
        "name": "Công ty Cổ phần FPT",
        "market": "VN_EQUITY",
        "current_price": 50.80, # nghìn đồng
        "intrinsic_value": 72.50, # DCF 10 năm
        "net_asset_value": 68.00, # Tài sản ròng
        "pe": 16.5,
        "roe": 26.8,
        "de": 0.45,
        "current_ratio": 1.42,
        "gross_margin": 38.5,
        "fcf_positive": True,
        "moats": ["Chi phí chuyển đổi cao", "Thương hiệu công nghệ #1", "Quy mô nhân lực 30k+ kỹ sư"],
        "ta_trend": "Uptrend dài hạn, nến tuần tạo đáy cân bằng",
        "rsi": 42.5,
        "macd_hist_slope": "Dốc lên (Phân kỳ dương)",
        "wave_status": "Hoàn tất Sóng điều chỉnh C tại 49.55k, bắt đầu Sóng 1 đẩy",
        "fibo_zone": "Kiểm định hỗ trợ Fibo 0.500 (50.2k)"
    },
    {
        "symbol": "SIP",
        "name": "CTCP Đầu tư Sài Gòn VRG",
        "market": "VN_EQUITY",
        "current_price": 61.30, # nghìn đồng
        "intrinsic_value": 81.28, # DCF 10 năm theo tài liệu nội bộ
        "net_asset_value": 78.50, # Tài sản ròng bóc tách nợ chiếm dụng
        "pe": 12.8,
        "roe": 22.4,
        "de": 0.38,
        "current_ratio": 1.65,
        "gross_margin": 42.0,
        "fcf_positive": True,
        "moats": ["Quỹ đất KCN 3,200 ha TP.HCM/Tây Ninh", "Độc quyền phân phối điện nước nội khu", "Khách hàng FDI lớn"],
        "ta_trend": "Tích lũy nền giá trên MA50 tuần",
        "rsi": 48.0,
        "macd_hist_slope": "Cắt lên trên Zero",
        "wave_status": "Kết thúc Sóng 2 điều chỉnh phẳng (Flat), chuẩn bị vào Sóng 3 mở rộng",
        "fibo_zone": "Hội tụ Fibo Retracement 0.618"
    },
    {
        "symbol": "HPG",
        "name": "CTCP Tập đoàn Hòa Phát",
        "market": "VN_EQUITY",
        "current_price": 27.20,
        "intrinsic_value": 34.50,
        "net_asset_value": 31.00,
        "pe": 14.2,
        "roe": 14.5,
        "de": 0.58,
        "current_ratio": 1.35,
        "gross_margin": 18.2,
        "fcf_positive": True,
        "moats": ["Lợi thế chi phí thấp lò cao BOF", "Thị phần thép xây dựng 38% #1 VN", "Dự án Dung Quất 2"],
        "ta_trend": "Sideway đi ngang biên độ 26-29",
        "rsi": 45.0,
        "macd_hist_slope": "Đi ngang quanh 0",
        "wave_status": "Sóng 4 tích lũy mô hình tam giác thu hẹp",
        "fibo_zone": "Fibo 0.382"
    },
    {
        "symbol": "VNM",
        "name": "CTCP Sữa Việt Nam",
        "market": "VN_EQUITY",
        "current_price": 66.50,
        "intrinsic_value": 78.00,
        "net_asset_value": 72.00,
        "pe": 15.8,
        "roe": 28.5,
        "de": 0.28,
        "current_ratio": 2.10,
        "gross_margin": 41.5,
        "fcf_positive": True,
        "moats": ["Thương hiệu sữa quốc dân", "Mạng lưới phân phối 250k điểm bán", "Cổ tức tiền mặt đều đặn 7-8%/năm"],
        "ta_trend": "Đáy dài hạn, dòng tiền phòng thủ",
        "rsi": 38.0,
        "macd_hist_slope": "Phân kỳ dương 3 đoạn",
        "wave_status": "Hoàn thành Sóng C lớn khung tháng",
        "fibo_zone": "Chạm hỗ trợ kênh dưới"
    },
    {
        "symbol": "MWG",
        "name": "CTCP Đầu tư Thế Giới Di Động",
        "market": "VN_EQUITY",
        "current_price": 63.80,
        "intrinsic_value": 74.00,
        "net_asset_value": 65.00,
        "pe": 24.5,
        "roe": 18.2,
        "de": 0.65,
        "current_ratio": 1.25,
        "gross_margin": 24.0,
        "fcf_positive": True,
        "moats": ["Chuỗi bán lẻ Bách Hóa Xanh đạt điểm hòa vốn", "Thị phần bán lẻ điện máy 50%"],
        "ta_trend": "Uptrend trung hạn, bứt phá đỉnh ngắn hạn",
        "rsi": 58.0,
        "macd_hist_slope": "Dương và mở rộng",
        "wave_status": "Đang chạy Sóng 3 đẩy trung hạn",
        "fibo_zone": "Vượt đỉnh Fibo 0.618"
    },
    {
        "symbol": "BTCUSD",
        "name": "Bitcoin / U.S. Dollar",
        "market": "GLOBAL_CRYPTO",
        "current_price": 75870.0,
        "intrinsic_value": 65000.0, # Định giá chi phí khai thác trung bình + biên lợi nhuận thợ đào
        "net_asset_value": 60000.0,
        "pe": 0,
        "roe": 0,
        "de": 0,
        "current_ratio": 0,
        "gross_margin": 0,
        "fcf_positive": True,
        "moats": ["Tiền mã hóa phi tập trung số 1", "Hiệu ứng mạng lưới toàn cầu", "Nguồn cung cố định 21M"],
        "ta_trend": "Downtrend sau khi gãy MA20 Tuần, hồi kỹ thuật",
        "rsi": 38.0,
        "macd_hist_slope": "Phân kỳ âm khung tuần",
        "wave_status": "Sóng (A) 57.8k, Sóng (B) 87.4k; Hiện tại đang trong Sóng (C) đổ đèo",
        "fibo_zone": "Kiểm định Fibo Extension 1.000 ($48.5k) và 1.272 ($37.9k)"
    }
]


def score_single_asset(item):
    """Tính toán 4 điểm thành phần và Combined Score cho 1 tài sản"""
    # 1. FA Score (0 - 100đ, Trọng số 30%)
    if item["market"] == "VN_EQUITY":
        fa_pts = 0
        if item["de"] < 1.0 and item["current_ratio"] > 1.2: fa_pts += 25
        if item["roe"] >= 15.0 and item["gross_margin"] >= 30.0: fa_pts += 25
        if item["fcf_positive"]: fa_pts += 25
        if len(item["moats"]) >= 2: fa_pts += 25
        fa_score = fa_pts
    else:
        # Crypto / Commodity đánh giá theo Moat mạng lưới và chu kỳ
        fa_score = 75.0 if len(item["moats"]) >= 2 else 50.0

    # 2. Valuation Score (0 - 100đ, Trọng số 30%)
    curr_p = item["current_price"]
    val_p = item["intrinsic_value"]
    if curr_p > 0:
        mos = (val_p - curr_p) / curr_p
    else:
        mos = 0

    if mos >= 0.35:
        val_score = 100.0
    elif mos >= 0.25:
        val_score = 85.0
    elif mos >= 0.15:
        val_score = 65.0
    elif mos >= 0.05:
        val_score = 40.0
    else:
        val_score = 15.0

    # 3. TA Score (0 - 100đ, Trọng số 25%)
    ta_pts = 0
    if "Uptrend" in item["ta_trend"] or "Tạo đáy" in item["ta_trend"] or "Tích lũy" in item["ta_trend"]:
        ta_pts += 25
    if 40 <= item["rsi"] <= 65:
        ta_pts += 25
    elif item["rsi"] < 40: # Quá bán
        ta_pts += 20
    if "Dương" in item["macd_hist_slope"] or "cắt lên" in item["macd_hist_slope"].lower() or "dốc lên" in item["macd_hist_slope"].lower():
        ta_pts += 25
    if "Fibo" in item["fibo_zone"]:
        ta_pts += 25
    ta_score = min(100.0, float(ta_pts))

    # 4. Wave Score (0 - 100đ, Trọng số 15%)
    w_text = item["wave_status"].lower()
    if "sóng 1" in w_text or "kết thúc sóng 2" in w_text:
        wave_score = 100.0
    elif "sóng 3" in w_text:
        wave_score = 95.0
    elif "hoàn tất sóng" in w_text or "sóng c" in w_text:
        if "đang trong sóng (c) đổ đèo" in w_text:
            wave_score = 40.0 # Bán thuận xu hướng, không mua
        else:
            wave_score = 90.0 # Bắt đáy đảo chiều
    elif "sóng 4" in w_text:
        wave_score = 75.0
    else:
        wave_score = 50.0

    # Combined Score
    combined = (fa_score * 0.30) + (val_score * 0.30) + (ta_score * 0.25) + (wave_score * 0.15)

    # Phân loại Preset
    matched_presets = []
    if mos >= 0.25 and len(item["moats"]) >= 2:
        matched_presets.append("Siêu Cổ Phiếu Giá Trị")
    if "sóng 3" in w_text or "bứt phá" in item["ta_trend"].lower():
        matched_presets.append("Bùng Nổ Đà Tăng")
    if item["rsi"] < 42 and ("đáy" in item["ta_trend"].lower() or "hoàn tất" in w_text):
        matched_presets.append("Bắt Đáy Quá Bán")
    if item["symbol"] in ["VNM", "SIP"]:
        matched_presets.append("Cổ Tức Bền Vững")
    if "sóng 4" in w_text or "tích lũy" in item["ta_trend"].lower():
        matched_presets.append("Theo Dõi Kích Hoạt (Watchlist)")

    return {
        "symbol": item["symbol"],
        "name": item["name"],
        "market": item["market"],
        "current_price": curr_p,
        "intrinsic_value": val_p,
        "margin_of_safety_pct": round(mos * 100, 2),
        "fa_score": round(fa_score, 1),
        "val_score": round(val_score, 1),
        "ta_score": round(ta_score, 1),
        "wave_score": round(wave_score, 1),
        "combined_score": round(combined, 1),
        "presets": matched_presets,
        "wave_status": item["wave_status"],
        "recommendation": "MUA MẠNH (BUY)" if combined >= 80 else ("TÍCH LŨY (ACCUMULATE)" if combined >= 70 else "THEO DÕI (WATCHLIST)")
    }


def run_screener():
    print("[*] Đang chạy Bộ Máy Sàng Lọc Toàn Thị Trường Fsen (Universe: 6 tài sản)...")
    results = [score_single_asset(item) for item in UNIVERSE]
    df_res = pd.DataFrame(results).sort_values(by="combined_score", ascending=False).reset_index(drop=True)
    df_res["rank"] = df_res.index + 1
    
    print("\n=== BẢNG XẾP HẠNG TOP CỔ PHIẾU COMBINED SCORE ===")
    for _, r in df_res.iterrows():
        print(f"Top {r['rank']} | {r['symbol']:<7} | Combined: {r['combined_score']:>5.1f}đ | FA: {r['fa_score']:>4.0f} | Val: {r['val_score']:>4.0f} | TA: {r['ta_score']:>4.0f} | Wave: {r['wave_score']:>4.0f} | MOS: {r['margin_of_safety_pct']:>5.1f}% | {r['recommendation']}")

    # Lưu kết quả
    out_json = "outputs/investment/screener_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(df_res.to_dict(orient="records"), f, ensure_ascii=False, indent=2)
    print(f"\n[+] Đã lưu kết quả sàng lọc: {out_json}")
    return df_res


if __name__ == "__main__":
    run_screener()

