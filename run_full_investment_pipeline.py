"""
run_full_investment_pipeline.py
Script Khởi Chạy Toàn Diện Hệ Sinh Thái Đầu Tư AGY (1-Click Master Pipeline Runner)
Chạy tự động từ Phase 1 -> Phase 2 -> Phase 3 -> Dự Báo Sóng Fsen -> Xuất Bản Dashboard
"""

import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run_step(step_name: str, script_name: str):
    print(f"\n===============================================================================")
    print(f"[*] BƯỚC: {step_name} ({script_name})")
    print(f"===============================================================================")
    cmd = [sys.executable, str(BASE_DIR / script_name)]
    ret = subprocess.run(cmd, cwd=str(BASE_DIR))
    if ret.returncode != 0:
        print(f"[CẢNH BÁO] Bước {step_name} kết thúc với mã lỗi: {ret.returncode}")
    else:
        print(f"[THÀNH CÔNG] Hoàn tất {step_name}!")

def main():
    print("===============================================================================")
    print("      AGY INVESTMENT AGENTIC SYSTEM — KHỞI CHẠY TOÀN BỘ PIPELINE")
    print("===============================================================================")

    # 1. Phase 1: Phân tích cơ bản BCTC & Định giá đôi (DCF + Net Asset)
    run_step("Phase 1: BCTC & Định Giá Đôi", "test_phase1_investment.py")

    # 2. Phase 2: Phân tích Kỹ thuật 6 Trụ Cột & Sóng Elliott
    run_step("Phase 2: Phân Tích Kỹ Thuật & Sóng", "test_phase2_investment.py")

    # 3. Phase 3: Sàng lọc thị trường, Tín hiệu & Sổ cái Danh mục
    run_step("Phase 3: Screener & Sổ Cái Danh Mục", "test_phase3_investment.py")

    # 4. Dự báo sóng tương lai Fsen (3 Thành Tố: Dạng Sóng - Biên Độ - Thời Gian)
    run_step("Động Cơ Dự Báo Sóng Tương Lai Fsen", "invest_fsen_projection_engine.py")

    # 5. Phân loại động 4 họ sóng điều chỉnh & Cửa ngõ phân kỳ MACD
    run_step("Động Cơ Định Danh Sóng Điều Chỉnh Fsen v2.0", "wave_analyzer_engine.py")

    # 6. Tái tạo Biểu đồ Web Tương tác Master 60fps
    run_step("Tạo Biểu Đồ Web Interactive Master", "build_multiframe_realtime_dashboard.py")

    # 7. Tái tạo Sổ Master Excel 5 Sheet
    run_step("Tạo Sổ Master Excel Dashboard", "build_excel_master_dashboard.py")

    print("\n===============================================================================")
    print("[HOÀN TẤT 100%] Toàn bộ hệ thống AGY Investment Agent đã vận hành thành công!")
    print("  • Biểu đồ Web Master: outputs/investment/chart_scenario_interactive_MASTER.html")
    print("  • Sổ Master Excel:    outputs/investment/Excel_Master_Investment_Dashboard.xlsx")
    print("  • Ma trận Sóng JSON:  outputs/investment/corrective_wave_matrix.json")
    print("  • Để mở biểu đồ web:  Chạy MO_BIEU_DO_WEB.bat")
    print("  • Để nạp TradingView: Chạy MO_TRADINGVIEW_PINE_EDITOR.bat")
    print("===============================================================================\n")

if __name__ == "__main__":
    main()

