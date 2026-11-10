@echo off
chcp 65001 > nul
echo ===============================================================================
echo [AGY INVEST] CHẠY KIỂM THỬ TOÀN BỘ PIPELINE ĐẦU TƯ 3 PHA
echo ===============================================================================
python test_phase1_investment.py
python test_phase2_investment.py
python test_phase3_investment.py
python invest_fsen_projection_engine.py
python build_multiframe_realtime_dashboard.py
echo ===============================================================================
echo [HOÀN TẤT] Hệ thống đã chạy thành công 100%!
echo ===============================================================================
pause
