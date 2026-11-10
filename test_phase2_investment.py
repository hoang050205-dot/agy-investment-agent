"""
Test Phase 2 Investment Pipeline — Phân Tích Kỹ Thuật 6 Trụ Cột, Sóng Elliott & Biểu Đồ Trực Quan
Chạy thử nghiệm thực tế trên 2 mã:
1. BTCUSD (Quốc tế/Crypto: W, D, 4H, 1H)
2. FPT (Việt Nam: M, W, D, 1H)
"""

import os
import sys
import json
from fetch_multiframe_data import fetch_all_timeframes
from invest_technical_engine import analyze_multiframe
from generate_visual_chart import generate_all_charts
from export_weekly_table import export_all

def run_phase2_test():
    symbols = ["BTCUSD", "FPT"]
    out_dir = "outputs/investment"
    os.makedirs(out_dir, exist_ok=True)

    results_summary = {}

    for sym in symbols:
        print(f"\n{'='*65}")
        print(f"🚀 BẮT ĐẦU CHẠY PIPELINE PHASE 2 CHO MÃ: {sym}")
        print(f"{'='*65}")

        # 1. Fetch multi-timeframe data
        print(f"[1/4] Thu thập dữ liệu nến đa khung thời gian cho {sym}...")
        tf_data = fetch_all_timeframes(sym)

        # 2. Technical analysis 6 pillars & wave count
        print(f"[2/4] Phân tích 6 Trụ Cột Fsen & Sóng Elliott cho {sym}...")
        tf_analysis = analyze_multiframe(sym)

        # 3. Generate Visual Charts (PNG & HTML)
        print(f"[3/4] Tạo biểu đồ nến kịch bản, kênh giá, hỗ trợ kháng cự & điểm vô hiệu hóa...")
        chart_png, chart_html = generate_all_charts(sym, tf_analysis, out_dir=out_dir)

        # 4. Export Bảng Phân Tích Tuần (Excel & Word)
        print(f"[4/4] Xuất bản BẢNG PHÂN TÍCH TUẦN (Excel & Word có chèn ảnh)...")
        xlsx_file, docx_file = export_all(sym, tf_analysis, chart_png, out_dir=out_dir)

        # Trích xuất điểm mấu chốt để báo cáo
        primary_tf = "D" if tf_analysis.get("D") else "W"
        raw = tf_analysis[primary_tf]["raw"]
        results_summary[sym] = {
            "price": tf_analysis[primary_tf]["current_price"],
            "trend": tf_analysis[primary_tf]["trend"].split('\n')[0].replace('• Hướng: ', '').replace('*', ''),
            "score": tf_analysis[primary_tf]["score"].split('\n')[0].replace('• Tổng điểm: ', '').replace('*', ''),
            "invalidation": raw.get("invalidation_point"),
            "tp1": raw.get("tp1"),
            "chart_png": chart_png,
            "chart_html": chart_html,
            "xlsx_file": xlsx_file,
            "docx_file": docx_file
        }
        print(f"[SUCCESS] Hoàn tất toàn bộ sản phẩm cho mã {sym}!")

    print(f"\n{'='*65}")
    print(f"✨ KẾT QUẢ NGHIỆM THU PHASE 2:")
    print(f"{'='*65}")
    for sym, res in results_summary.items():
        print(f"📌 {sym}:")
        print(f"   • Thị giá: {res['price']:,.2f}")
        print(f"   • Xu hướng chủ đạo: {res['trend']}")
        print(f"   • Điểm kỹ thuật Fsen: {res['score']}")
        print(f"   • 🚨 ĐIỂM VÔ HIỆU HÓA (STOP LOSS): {res['invalidation']:,.2f}")
        print(f"   • 🎯 MỤC TIÊU TAKE PROFIT 1: {res['tp1']:,.2f}")
        print(f"   • File Excel: {res['xlsx_file']}")
        print(f"   • File Word (Kèm Biểu Đồ): {res['docx_file']}")
        print(f"   • File HTML tương tác: {res['chart_html']}\n")

if __name__ == "__main__":
    run_phase2_test()

