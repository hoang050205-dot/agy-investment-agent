@echo off
chcp 65001 > nul
echo ===============================================================================
echo [AGY INVEST] KHỞI ĐỘNG HỆ THỐNG BIỂU ĐỒ KỊCH BẢN TƯƠNG TÁC
echo ===============================================================================
start "" http://localhost:8888/chart_scenario_interactive_MASTER.html
python server_investment_charts.py
pause
