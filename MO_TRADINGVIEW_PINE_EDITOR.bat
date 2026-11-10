@echo off
chcp 65001 > nul
echo ===============================================================================
echo [AGY INVEST] NẠP MÃ NGUỒN PINE SCRIPT V6 VÀO CLIPBOARD & MỞ TRADINGVIEW
echo ===============================================================================
python -c "
import tkinter as tk
with open('knowledge-base/AGY_Fsen_Elliott_Scanner.pine', 'r', encoding='utf-8') as f:
    text = f.read()
r = tk.Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(text)
r.update()
print(f'[SUCCESS] Đã nạp thành công {len(text)} ký tự Pine Script vào Clipboard!')
"
start "" https://www.tradingview.com/chart/
echo [HUONG DAN] Mo tab Pine Editor tren TradingView, an Ctrl+A roi Ctrl+V -> Luu lai!
pause
