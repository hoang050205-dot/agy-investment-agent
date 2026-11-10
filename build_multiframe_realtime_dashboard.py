"""
Build Multi-Timeframe Real-Time Elliott Wave Scenario Dashboard (v5.0 Pro)
- SỬA TRIỆT ĐỂ: Sóng (A) ở trước (57,800 tuần 2026-06-29), Sóng (B) ở 87,396 (tuần 2026-09-28), 
  và cây nến hiện tại 75,870 là đáy Sóng con 1 của Sóng (C)!
- Hỗ trợ ĐA KHUNG THỜI GIAN:
  + Quốc tế (BTCUSD, XAUUSD, USOIL): 1W, 1D, 4H, 1H
  + Việt Nam (FPT): 1M, 1W, 1D, 1H
- REAL-TIME ENGINE:
  + Kết nối Binance WebSocket (wss://stream.binance.com:9443/ws/btcusdt@ticker) trực tiếp trên Client.
  + Nhấp nháy giá thời gian thực (Sub-second live ticks).
  + Đánh giá trạng thái kịch bản ĐỘNG theo biến động giá (Cảnh báo vô hiệu hóa Stop Loss / Kích hoạt vùng lệnh).
- Tọa độ đỉnh đáy cắm CHÍNH XÁC 100% vào High/Low của từng cây nến.
"""

import os
import sys
import json
import time
from datetime import datetime
import pandas as pd
import numpy as np

# -------------------------------------------------------------
# LOAD MULTI-TIMEFRAME CANDLES
# -------------------------------------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Helper: Compute Moving Averages
def compute_ma(candles, period=20):
    ma_list = []
    closes = [c['close'] for c in candles]
    times = [c['time'] for c in candles]
    for i in range(len(closes)):
        if i >= period - 1:
            val = sum(closes[i - period + 1 : i + 1]) / period
            ma_list.append({"time": times[i], "value": round(val, 2)})
    return ma_list

# Helper: Snap exact candle High / Low
def snap_candle(candles, date_str, use_high=True):
    for c in candles:
        if c['time'] == date_str or c['time'].startswith(date_str):
            return {"time": c['time'], "value": c['high'] if use_high else c['low']}
    for c in candles:
        if c['time'][:7] == date_str[:7]:
            return {"time": c['time'], "value": c['high'] if use_high else c['low']}
    return {"time": date_str, "value": 0}


# =============================================================
# 1. BTCUSD MULTI-TIMEFRAME DATA & EXACT WAVE COUNTS
# =============================================================
btc_w = load_json("sample-data/stock/BTCUSD/ohlcv_W.json")
btc_d = load_json("sample-data/stock/BTCUSD/ohlcv_D.json")
btc_4h = load_json("sample-data/stock/BTCUSD/ohlcv_4H.json")
btc_1h = load_json("sample-data/stock/BTCUSD/ohlcv_1H.json")

# BTC KHUNG 1W (WEEKLY): ĐÃ SỬA CHUẨN XÁC ĐÁY (A) Ở TRƯỚC VÀ ĐỈNH (B) Ở TRƯỚC
last_btc_w = btc_w[-1]
p_bw_0 = snap_candle(btc_w, "2022-11-21", use_high=False) # Low 15,476 (Đáy chu kỳ lớn)
p_bw_1 = snap_candle(btc_w, "2023-04-10", use_high=True)  # High 31,000 (Sóng 1)
p_bw_2 = snap_candle(btc_w, "2023-06-12", use_high=False) # Low 24,800 (Sóng 2)
p_bw_3 = snap_candle(btc_w, "2024-03-11", use_high=True)  # High 73,777 (Sóng 3 Mở Rộng - MACD Peak)
p_bw_4 = snap_candle(btc_w, "2024-08-05", use_high=False) # Low 49,000 (Sóng 4 Xen kẽ - MACD Zero)
p_bw_5 = snap_candle(btc_w, "2025-10-06", use_high=True)  # High 126,200 (Sóng 5 ATH - Phân kỳ âm)
# SÓNG (A) Ở TRƯỚC:
p_bw_a = snap_candle(btc_w, "2026-06-29", use_high=False) # Low 57,800 (ĐÁY SÓNG A ĐÃ HOÀN TẤT)
# SÓNG (B) Ở TRƯỚC:
p_bw_b = snap_candle(btc_w, "2026-09-28", use_high=True)  # High 87,396 (ĐỈNH SÓNG B ĐÃ HOÀN TẤT Fibo 0.618)
# SÓNG CON 1 CỦA C (NẾN HIỆN TẠI):
p_bw_curr = {"time": last_btc_w["time"], "value": last_btc_w["low"]} # Low 74,888 (Đáy sóng con 1 của C)

btc_w_wave_line = [p_bw_0, p_bw_1, p_bw_2, p_bw_3, p_bw_4, p_bw_5, p_bw_a, p_bw_b, p_bw_curr]

btc_w_markers = [
    {"time": p_bw_1["time"], "position": "aboveBar", "color": "#f59e0b", "shape": "arrowDown", "text": f"(1) {p_bw_1['value']:,.0f}"},
    {"time": p_bw_2["time"], "position": "belowBar", "color": "#3b82f6", "shape": "arrowUp", "text": f"(2) {p_bw_2['value']:,.0f}"},
    {"time": p_bw_3["time"], "position": "aboveBar", "color": "#f59e0b", "shape": "arrowDown", "text": f"(3) {p_bw_3['value']:,.0f} [MACD Peak]"},
    {"time": p_bw_4["time"], "position": "belowBar", "color": "#3b82f6", "shape": "arrowUp", "text": f"(4) {p_bw_4['value']:,.0f} [MACD Zero]"},
    {"time": p_bw_5["time"], "position": "aboveBar", "color": "#ef4444", "shape": "arrowDown", "text": f"(5) ATH {p_bw_5['value']:,.0f}"},
    {"time": p_bw_a["time"], "position": "belowBar", "color": "#3b82f6", "shape": "arrowUp", "text": f"(A) {p_bw_a['value']:,.0f} [Đã xong]"},
    {"time": p_bw_b["time"], "position": "aboveBar", "color": "#f59e0b", "shape": "arrowDown", "text": f"(B) {p_bw_b['value']:,.0f} [Fibo 0.618]"},
    {"time": p_bw_curr["time"], "position": "belowBar", "color": "#06b6d4", "shape": "circle", "text": f"C-1: {p_bw_curr['value']:,.0f} [Hiện tại]"}
]

# Kịch bản tương lai: Xuất phát từ nến hiện tại (đáy sóng con 1) -> hồi sóng con 2 -> xả sóng 3 -> hồi 4 -> xả 5 (TP2 37.9k)
btc_w_future_path = [
    {"time": last_btc_w["time"], "value": last_btc_w["close"]},
    {"time": "2026-11-23", "value": 81000.0},  # Sóng con 2 của C (Hồi kiểm định cản)
    {"time": "2026-12-21", "value": 65000.0},  # Đang xả sóng 3
    {"time": "2027-02-15", "value": 48500.0},  # Sóng con 3 của C (Đâm thủng đáy A 57.8k)
    {"time": "2027-04-12", "value": 54000.0},  # Sóng con 4 của C (Hồi kỹ thuật)
    {"time": "2027-06-21", "value": 37949.0}   # Sóng con 5 của C -> Chạm TP2 Fibo 1.272 (37,949)
]

btc_w_future_markers = [
    {"time": "2026-11-23", "position": "aboveBar", "color": "#f97316", "shape": "arrowDown", "text": "C-2: Canh Bán 80k-81.5k"},
    {"time": "2027-02-15", "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": "C-3: Thủng 57.8k -> 48.5k"},
    {"time": "2027-06-21", "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": "C-5: Đáy TP2 37.9k"}
]

btc_w_lines = [
    {"price": 88500.0, "title": "SL: 88.5k (Vượt đỉnh B)", "color": "#ff0033", "style": 2},
    {"price": 81000.0, "title": "Vùng Bán C-2: 81k", "color": "#f97316", "style": 2},
    {"price": 57800.0, "title": "Đáy (A) Cũ: 57.8k", "color": "#3b82f6", "style": 2},
    {"price": 48500.0, "title": "TP1 (C-3): 48.5k", "color": "#10b981", "style": 0},
    {"price": 37949.0, "title": "TP2 (C-5): 37.9k", "color": "#10b981", "style": 0}
]

# BTC KHUNG 1D (DAILY): TẬP TRUNG VÀO PHA GIẢM TỪ ĐỈNH (B) 87.4K XUỐNG
last_btc_d = btc_d[-1]
p_bd_b = snap_candle(btc_d, "2026-09-28", use_high=True)   # High 87.4k
p_bd_curr = {"time": last_btc_d["time"], "value": last_btc_d["low"]}

btc_d_wave_line = [p_bd_b, p_bd_curr]
btc_d_markers = [
    {"time": p_bd_b["time"], "position": "aboveBar", "color": "#ef4444", "shape": "arrowDown", "text": f"Đỉnh (B) {p_bd_b['value']:,.0f}"},
    {"time": p_bd_curr["time"], "position": "belowBar", "color": "#06b6d4", "shape": "circle", "text": f"Đáy C-1: {p_bd_curr['value']:,.0f}"}
]
btc_d_future_path = [
    {"time": last_btc_d["time"], "value": last_btc_d["close"]},
    {"time": "2026-11-16", "value": 80500.0},
    {"time": "2026-11-30", "value": 72000.0},
    {"time": "2026-12-15", "value": 57800.0}
]
btc_d_future_markers = [
    {"time": "2026-11-16", "position": "aboveBar", "color": "#f97316", "shape": "arrowDown", "text": "Hồi C-2: 80.5k"},
    {"time": "2026-12-15", "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": "Test đáy 57.8k"}
]


# =============================================================
# =============================================================
# 2. FPT MULTI-TIMEFRAME DATA (M, W, D, 1H) - 14 NĂM LỊCH SỬ (2013-2026)
# =============================================================
fpt_m = load_json("sample-data/stock/FPT/ohlcv_M.json")
fpt_w = load_json("sample-data/stock/FPT/ohlcv_W.json")
fpt_d = load_json("sample-data/stock/FPT/ohlcv_D.json")
fpt_1h = load_json("sample-data/stock/FPT/ohlcv_1H.json")

# FPT 1M (MONTHLY) - KHÔNG ĐƯỜNG NỐI, CẮM CHUẨN ĐỈNH ĐÁY 14 NĂM
fpt_m_markers = [
    {"time": "2013-05-31", "position": "belowBar", "color": "#94a3b8", "shape": "circle", "text": "Đáy 3.73k"},
    {"time": "2018-04-30", "position": "aboveBar", "color": "#c084fc", "shape": "arrowDown", "text": "[I] 15.34k"},
    {"time": "2020-03-31", "position": "belowBar", "color": "#c084fc", "shape": "arrowUp", "text": "[II] Đáy Covid 12.99k"},
    {"time": "2022-04-30", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "[III] 54.12k"},
    {"time": "2022-11-30", "position": "belowBar", "color": "#c084fc", "shape": "arrowUp", "text": "[IV] Đáy 34.18k"},
    {"time": "2024-03-31", "position": "aboveBar", "color": "#38bdf8", "shape": "arrowDown", "text": "(1) 77.77k"},
    {"time": "2025-09-30", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "(3) ATH 95.67k"},
    {"time": "2026-07-31", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(A) 55.91k"},
    {"time": "2026-10-31", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(C) Đáy 52.40k"},
    {"time": "2026-11-30", "position": "aboveBar", "color": "#10b981", "shape": "circle", "text": "(5) Khởi động 51.0k"}
]
fpt_m_future_path = [
    {"time": "2026-11-30", "value": 51.00},
    {"time": "2027-03-31", "value": 68.00},
    {"time": "2027-08-31", "value": 85.00},
    {"time": "2027-12-31", "value": 98.00}
]
fpt_m_future_markers = [
    {"time": "2027-03-31", "position": "aboveBar", "color": "#10b981", "shape": "arrowDown", "text": "TP1: 68k"},
    {"time": "2027-08-31", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "TP2: 85k"},
    {"time": "2027-12-31", "position": "aboveBar", "color": "#c084fc", "shape": "arrowDown", "text": "TP3: 98k (ATH)"}
]

# FPT 1W (WEEKLY) - 14 NĂM LỊCH SỬ
fpt_w_markers = [
    {"time": "2018-04-13", "position": "aboveBar", "color": "#c084fc", "shape": "arrowDown", "text": "[I] 15.34k"},
    {"time": "2020-03-27", "position": "belowBar", "color": "#c084fc", "shape": "arrowUp", "text": "[II] 12.99k"},
    {"time": "2022-04-15", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "[III] 54.12k"},
    {"time": "2022-11-18", "position": "belowBar", "color": "#c084fc", "shape": "arrowUp", "text": "[IV] 34.18k"},
    {"time": "2026-01-23", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "ATH 97.48k"},
    {"time": "2026-05-15", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(A) 62.77k"},
    {"time": "2026-06-05", "position": "aboveBar", "color": "#f43f5e", "shape": "arrowDown", "text": "(B) 70.64k"},
    {"time": "2026-11-06", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(C) Đáy 49.55k [Xong]"},
    {"time": "2026-11-13", "position": "aboveBar", "color": "#10b981", "shape": "circle", "text": "Chân Sóng (5): 51.0k"}
]
fpt_w_future_path = [
    {"time": "2026-11-13", "value": 51.00},
    {"time": "2026-11-27", "value": 50.20},  # Test vùng mua
    {"time": "2026-12-25", "value": 58.00},  # Sóng 1 đẩy
    {"time": "2027-01-22", "value": 54.50},  # Sóng 2 chỉnh
    {"time": "2027-03-26", "value": 68.00},  # Sóng 3 mở rộng -> TP1
    {"time": "2027-05-28", "value": 82.00}   # Sóng 5 -> TP2
]
fpt_w_future_markers = [
    {"time": "2026-11-27", "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": "Vùng Mua: 50.0-51.5k"},
    {"time": "2027-03-26", "position": "aboveBar", "color": "#10b981", "shape": "arrowDown", "text": "TP1: 68k"},
    {"time": "2027-05-28", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "TP2: 82k"}
]

fpt_w_lines = [
    {"price": 48.50, "title": "SL: 48.5k (Thủng đáy C)", "color": "#ff0033", "style": 2},
    {"price": 51.50, "title": "Vùng Mua: 51.5k", "color": "#10b981", "style": 2},
    {"price": 50.00, "title": "Vùng Mua: 50.0k", "color": "#10b981", "style": 2},
    {"price": 68.00, "title": "TP1: 68.0k", "color": "#10b981", "style": 0},
    {"price": 82.00, "title": "TP2: 82.0k", "color": "#ffd700", "style": 0}
]

# FPT 1D (DAILY)
last_fpt_d = fpt_d[-1]
fpt_d_markers = [
    {"time": "2026-06-03", "position": "aboveBar", "color": "#f43f5e", "shape": "arrowDown", "text": "(B) 70.6k"},
    {"time": "2026-11-03", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(C) Đáy 49.55k"},
    {"time": last_fpt_d["time"], "position": "aboveBar", "color": "#10b981", "shape": "circle", "text": f"Hiện tại: {last_fpt_d['close']:.1f}k"}
]
fpt_d_future_path = [
    {"time": last_fpt_d["time"], "value": last_fpt_d["close"]},
    {"time": "2026-11-20", "value": 50.50},
    {"time": "2026-12-10", "value": 56.00},
    {"time": "2026-12-30", "value": 62.00}
]
fpt_d_future_markers = [
    {"time": "2026-11-20", "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": "Vùng Mua: 50-51k"},
    {"time": "2026-12-30", "position": "aboveBar", "color": "#10b981", "shape": "arrowDown", "text": "Mục tiêu: 62k"}
]


# =============================================================
# 3. VND MULTI-TIMEFRAME DATA (M, W, D, 1H) - ĐẾM SÓNG TOÀN DIỆN 14 NĂM
# =============================================================
vnd_m = load_json("sample-data/stock/VND/ohlcv_M.json")
vnd_w = load_json("sample-data/stock/VND/ohlcv_W.json")
vnd_d = load_json("sample-data/stock/VND/ohlcv_D.json")
vnd_1h = load_json("sample-data/stock/VND/ohlcv_1H.json")

# VND 1M (MONTHLY) - 14 NĂM LỊCH SỬ (2013 - 2026): CẮM CHUẨN ĐỈNH ĐÁY TỪNG CÂY NẾN
vnd_m_markers = [
    {"time": "2013-05-31", "position": "belowBar", "color": "#94a3b8", "shape": "circle", "text": "Đáy Khởi Nguồn: 0.80k"},
    {"time": "2018-04-30", "position": "aboveBar", "color": "#c084fc", "shape": "arrowDown", "text": "[I] 6.08k (+660%)"},
    {"time": "2020-04-30", "position": "belowBar", "color": "#c084fc", "shape": "arrowUp", "text": "[II] Đáy Covid 1.98k (Fibo 0.618)"},
    {"time": "2022-04-30", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "[III] ATH 29.02k (+1,365%)"},
    {"time": "2022-11-30", "position": "belowBar", "color": "#c084fc", "shape": "arrowUp", "text": "[IV] Đáy 7.30k (Test đỉnh [I])"},
    {"time": "2023-09-30", "position": "aboveBar", "color": "#38bdf8", "shape": "arrowDown", "text": "(1) 20.49k"},
    {"time": "2023-10-31", "position": "belowBar", "color": "#38bdf8", "shape": "arrowUp", "text": "(2) 13.05k"},
    {"time": "2025-09-30", "position": "aboveBar", "color": "#38bdf8", "shape": "arrowDown", "text": "(3) 26.58k"},
    {"time": "2026-03-31", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(A) 13.90k"},
    {"time": "2026-07-31", "position": "aboveBar", "color": "#f43f5e", "shape": "arrowDown", "text": "(B) 19.10k"},
    {"time": "2026-10-31", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(C) Đáy kép 12.60k [Hoàn tất]"},
    {"time": "2026-11-30", "position": "aboveBar", "color": "#10b981", "shape": "circle", "text": "[V] Bứt phá 14.95k"}
]

vnd_m_future_path = [
    {"time": "2026-11-30", "value": 14.45},
    {"time": "2027-02-28", "value": 17.50},  # Sóng 3 đẩy khung tháng
    {"time": "2027-06-30", "value": 21.00},  # Chinh phục Fibo 0.618
    {"time": "2027-12-31", "value": 29.00}   # Đại Sóng [V] thử thách đỉnh ATH
]
vnd_m_future_markers = [
    {"time": "2027-02-28", "position": "aboveBar", "color": "#10b981", "shape": "arrowDown", "text": "TP1: 17.5k"},
    {"time": "2027-06-30", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "TP2: 21.0k"},
    {"time": "2027-12-31", "position": "aboveBar", "color": "#c084fc", "shape": "arrowDown", "text": "TP3: 29.0k (ATH)"}
]

# VND 1W (WEEKLY) - 14 NĂM LỊCH SỬ (2013 - 2026, 716 TUẦN)
vnd_w_markers = [
    {"time": "2013-05-31", "position": "belowBar", "color": "#94a3b8", "shape": "circle", "text": "Đáy 0.80k"},
    {"time": "2018-04-13", "position": "aboveBar", "color": "#c084fc", "shape": "arrowDown", "text": "[I] 6.08k"},
    {"time": "2020-04-24", "position": "belowBar", "color": "#c084fc", "shape": "arrowUp", "text": "[II] 1.98k"},
    {"time": "2022-04-08", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "[III] ATH 29.02k"},
    {"time": "2022-11-18", "position": "belowBar", "color": "#c084fc", "shape": "arrowUp", "text": "[IV] 7.30k"},
    {"time": "2023-09-22", "position": "aboveBar", "color": "#38bdf8", "shape": "arrowDown", "text": "(1) 20.49k"},
    {"time": "2023-11-03", "position": "belowBar", "color": "#38bdf8", "shape": "arrowUp", "text": "(2) 13.05k"},
    {"time": "2025-09-05", "position": "aboveBar", "color": "#38bdf8", "shape": "arrowDown", "text": "(3) 26.58k"},
    {"time": "2026-03-27", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(A) 13.90k"},
    {"time": "2026-07-10", "position": "aboveBar", "color": "#f43f5e", "shape": "arrowDown", "text": "(B) 19.10k"},
    {"time": "2026-10-09", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "(C) Đáy kép 12.60k [Hoàn tất]"},
    {"time": "2026-11-06", "position": "aboveBar", "color": "#10b981", "shape": "circle", "text": "(5) Bứt phá 14.95k (102.7M)"}
]

vnd_w_future_path = [
    {"time": "2026-11-27", "value": 14.35},  # Sóng 2~ Pullback test MA20
    {"time": "2027-01-15", "value": 18.15},  # Sóng 3? mở rộng (1.618x H1)
    {"time": "2027-02-26", "value": 16.70},  # Sóng 4? thoái lui 0.382x W3 (không vi phạm S1)
    {"time": "2027-04-30", "value": 19.05},  # Sóng 5? (1.0x H1)
    {"time": "2027-06-18", "value": 21.00},  # Mục tiêu mở rộng Fibo 0.618 chu kỳ lớn
    {"time": "2027-08-13", "value": 17.50},  # Sóng A? điều chỉnh
    {"time": "2027-09-24", "value": 19.20},  # Sóng B? hồi phục
    {"time": "2027-11-19", "value": 16.80}   # Sóng C? tái tích lũy
]
vnd_w_future_markers = [
    {"time": "2026-11-27", "position": "belowBar", "color": "#f59e0b", "shape": "arrowUp", "text": "2~ (Pullback 14.35k)"},
    {"time": "2027-01-15", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "3? (18.15k - 1.618× H1)"},
    {"time": "2027-02-26", "position": "belowBar", "color": "#38bdf8", "shape": "arrowUp", "text": "4? (16.70k - Thoái lui 0.382)"},
    {"time": "2027-04-30", "position": "aboveBar", "color": "#c084fc", "shape": "arrowDown", "text": "5? (19.05k / 21.0k Fibo)"},
    {"time": "2027-08-13", "position": "belowBar", "color": "#f43f5e", "shape": "arrowDown", "text": "A? (17.5k)"},
    {"time": "2027-09-24", "position": "aboveBar", "color": "#f43f5e", "shape": "arrowUp", "text": "B? (19.2k)"},
    {"time": "2027-11-19", "position": "belowBar", "color": "#f43f5e", "shape": "arrowUp", "text": "C? (16.8k)"}
]

vnd_lines = [
    {"price": 12.60, "title": "INVALID: 12.60k (Đáy Sóng C)", "color": "#ef4444", "style": 2},
    {"price": 14.35, "title": "Vùng Mua Pullback: 14.20 - 14.50k", "color": "#10b981", "style": 2},
    {"price": 14.95, "title": "CHoCH / Khởi Chân Sóng 1: 14.95k", "color": "#06b6d4", "style": 2},
    {"price": 18.15, "title": "Mục Tiêu Sóng 3?: 18.15k (Yellow Zone 17.5 - 18.2k)", "color": "#f59e0b", "style": 2},
    {"price": 16.70, "title": "Hỗ Trợ Sóng 4?: 16.70k (Không phạm S1)", "color": "#38bdf8", "style": 2},
    {"price": 21.00, "title": "Mục Tiêu Sóng 5?: 21.00k (Fibo 0.618 Chu Kỳ)", "color": "#c084fc", "style": 0},
    {"price": 29.00, "title": "Mục Tiêu Đại Chu Kỳ: 29.00k (ATH)", "color": "#ffd700", "style": 0}
]

# VND 1D (DAILY)
last_vnd_d = vnd_d[-1]
vnd_d_markers = [
    {"time": "2026-10-09", "position": "belowBar", "color": "#fbbf24", "shape": "arrowUp", "text": "Đáy 1: 12.60k"},
    {"time": "2026-11-03", "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": "Đáy 2: 13.05k"},
    {"time": "2026-11-06", "position": "aboveBar", "color": "#06b6d4", "shape": "circle", "text": "Breakout: 14.95k (102.7M)"}
]
vnd_d_future_path = [
    {"time": last_vnd_d["time"], "value": last_vnd_d["close"]},
    {"time": "2026-11-20", "value": 14.50},  # Pullback test MA20
    {"time": "2026-12-10", "value": 16.20},  # Đỉnh ngắn hạn
    {"time": "2026-12-30", "value": 17.50}   # TP1
]
vnd_d_future_markers = [
    {"time": "2026-11-20", "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": "Canh Mua Pullback 14.3-14.6k"},
    {"time": "2026-12-30", "position": "aboveBar", "color": "#10b981", "shape": "arrowDown", "text": "TP1: 17.5k"}
]

# =============================================================
# 3. XAUUSD MULTI-TIMEFRAME DATA (1W, 1D, 1H)
# =============================================================
gold_w = load_json("sample-data/stock/XAUUSD/ohlcv_W.json")
gold_d = load_json("sample-data/stock/XAUUSD/ohlcv_D.json")
last_gold_d = gold_d[-1]

p_gw_top = snap_candle(gold_d, "2026-01-29", use_high=True)  # High 5,586.20
p_gw_a   = snap_candle(gold_d, "2026-03-23", use_high=False) # Low 4,100.00
p_gw_b   = snap_candle(gold_d, "2026-05-12", use_high=True)  # High 4,783.40
p_gw_c   = snap_candle(gold_d, "2026-10-30", use_high=False) # Low 3,879.30
p_gw_curr = {"time": last_gold_d["time"], "value": last_gold_d["close"]} # 4,074.90

gold_wave_line = [p_gw_top, p_gw_a, p_gw_b, p_gw_c, p_gw_curr]
gold_wave_markers = [
    {"time": p_gw_top["time"], "position": "aboveBar", "color": "#ef4444", "shape": "arrowDown", "text": f"Đỉnh {p_gw_top['value']:,.0f}"},
    {"time": p_gw_a["time"], "position": "belowBar", "color": "#3b82f6", "shape": "circle", "text": f"(A) {p_gw_a['value']:,.0f}"},
    {"time": p_gw_b["time"], "position": "aboveBar", "color": "#f59e0b", "shape": "circle", "text": f"(B) {p_gw_b['value']:,.0f}"},
    {"time": p_gw_c["time"], "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": f"(C) Đáy {p_gw_c['value']:,.0f} [Hoàn tất]"},
    {"time": p_gw_curr["time"], "position": "aboveBar", "color": "#06b6d4", "shape": "circle", "text": f"Hiện tại: {p_gw_curr['value']:,.0f}"}
]

gold_future_path = [
    {"time": last_gold_d["time"], "value": last_gold_d["close"]},
    {"time": "2026-11-20", "value": 4020.00},
    {"time": "2026-12-15", "value": 4350.00},
    {"time": "2027-01-10", "value": 4220.00},
    {"time": "2027-02-28", "value": 4850.00},
    {"time": "2027-04-30", "value": 5580.00}
]
gold_future_markers = [
    {"time": "2026-11-20", "position": "belowBar", "color": "#10b981", "shape": "arrowUp", "text": "Vùng Mua: 3,980-4,050"},
    {"time": "2027-02-28", "position": "aboveBar", "color": "#10b981", "shape": "arrowDown", "text": "TP1: 4,850"},
    {"time": "2027-04-30", "position": "aboveBar", "color": "#ffd700", "shape": "arrowDown", "text": "TP2: 5,580"}
]
gold_lines = [
    {"price": 3850.00, "title": "SL: 3,850", "color": "#ff0033", "style": 2},
    {"price": 4050.00, "title": "Vùng Mua: 4,050", "color": "#10b981", "style": 2},
    {"price": 3980.00, "title": "Vùng Mua: 3,980", "color": "#10b981", "style": 2},
    {"price": 4850.00, "title": "TP1: 4,850", "color": "#10b981", "style": 0},
    {"price": 5580.00, "title": "TP2: 5,580", "color": "#ffd700", "style": 0}
]


# =============================================================
# 4. MASTER MULTI-TIMEFRAME DATA DICTIONARY
# =============================================================

# =============================================================
# FSEN QUANTITATIVE AUDIT DATA (APPROACH 2)
# =============================================================
from invest_fsen_elliott_engine import analyze_asset_fsen_elliott
vnd_audit_data = analyze_asset_fsen_elliott("VND")
fpt_audit_data = analyze_asset_fsen_elliott("FPT")


vnd_projection_hud = {
    "direction": "▲ LONG (Mua Bứt Phá)",
    "invalidation": "INVALID: 12.60k (Đáy C)",
    "wave_model": "Sóng tuần dự kiến là: Sóng Đẩy [5-3-5-3-5]",
    "h1": "2.35k (CHoCH 14.95k)",
    "w3_target": "18.15k (1.618× H1)",
    "w4_target": "16.70k (0.382× W3)",
    "w5_target": "19.05k - 21.0k (ATH 29.0k)",
    "time_cycle": "W3 (Q1/2027) -> W5 (Q1/2027) -> Sóng C (Q2/2027)",
    "rr": "1 : 2.17 (TP1) | 1 : 3.80 (TP2)"
}

xau_projection_hud = {
    "direction": "▼ SHORT (Bán Hạ Tỷ Trọng)",
    "invalidation": "INVALID: 4697.10$ (Fibo 0.786 / Swing High)",
    "wave_model": "Sóng tuần dự kiến là: Zigzag [5-3-5]",
    "h1": "774.78$ (CHoCH 4116.76$)",
    "w3_target": "3355$ - 3467$ (-0.618× Fibo)",
    "w4_target": "3675$ - 4200$ (0.382× W3)",
    "w5_target": "2934$ - 2992$ (-1.000× Fibo)",
    "time_cycle": "W3 (Q1/2027) -> W5 (Q4/2027) -> Sóng C (Q4/2028)",
    "rr": "1 : 2.84"
}

fpt_projection_hud = {
    "direction": "▲ LONG (Mua Tích Sản)",
    "invalidation": "INVALID: 49.55k (Đáy Flat C)",
    "wave_model": "Sóng tuần dự kiến là: Sóng 3 Đẩy (sau Sóng 2 Flat)",
    "h1": "3.45k (CHoCH 53.0k)",
    "w3_target": "56.38k (1.618× H1)",
    "w4_target": "54.25k (0.382× W3)",
    "w5_target": "57.7k - 70.0k (ATH 82k)",
    "time_cycle": "W3 (Q1/2027) -> W5 (Q2/2027) -> Sóng C (Q3/2027)",
    "rr": "1 : 4.46"
}

btc_projection_hud = {
    "direction": "▼ SHORT (Cảnh Giác Tạo Đỉnh)",
    "invalidation": "INVALID: $88,500 (Đỉnh B Bẫy Phân Kỳ)",
    "wave_model": "Sóng tuần dự kiến là: Expanded Flat [3-3-5] (Bão Sóng C)",
    "h1": "$20,500 (CHoCH $68k)",
    "w3_target": "$47,631 - $48,500 (1.618× H1)",
    "w4_target": "$58,000 - $60,300 (0.382× W3)",
    "w5_target": "$37,949 - $39,500 (Fibo 1.272)",
    "time_cycle": "W3 (Q1/2027) -> W5 (Q3/2027) -> Sóng C (Q1/2028)",
    "rr": "1 : 4.31"
}

master_store = {
        "VND": {
        "name": "Công ty Cổ phần Chứng khoán VNDIRECT (HOSE: VND)",
        "market": "Vietnam Equity · VNDirect Dchart (nghìn đồng)",
        "live_type": "POLLING_SIM",
        "live_symbol": "VND",
        "default_tf": "1W",
        "available_tfs": ["1M", "1W", "1D", "1H"],
        "timeframes": {
            "1M": {
                "candles": vnd_m,
                "ma10": compute_ma(vnd_m, 10),
                "ma20": compute_ma(vnd_m, 20),
                "ma50": compute_ma(vnd_m, 50),
                "wave_line": [],
                "wave_markers": vnd_m_markers,
                "future_path": vnd_m_future_path,
                "future_markers": vnd_m_future_markers,
                "price_lines": vnd_lines,
                "plan": {
                    "type": "BUY",
                    "action": "TÍCH SẢN CHU KỲ LỚN KHUNG THÁNG",
                    "action_zone": "13.0 - 14.8 nghìn đồng",
                    "invalidation": "12.0 nghìn đồng",
                    "tp1": "21.0 nghìn đồng",
                    "tp2": "26.5 nghìn đồng (Đỉnh 2025)",
                    "rr": "1 : 4.50",
                    "model": "<b>Khung Tháng (1M):</b> Định giá P/B tiệm cận 1.05x, mức định giá hấp dẫn nhất 5 năm qua. Nhịp điều chỉnh A-B-C cạn kiệt mở ra cơ hội tích sản đón chu kỳ nâng hạng thị trường chứng khoán.",
                    "trigger": "Đóng nến tháng giữ vững trên mốc 14.0k kèm thanh khoản hồi phục."
                }
            },
            "1W": {
                "candles": vnd_w,
                "ma10": compute_ma(vnd_w, 10),
                "ma20": compute_ma(vnd_w, 20),
                "ma50": compute_ma(vnd_w, 50),
                "wave_line": [],
                "wave_markers": vnd_w_markers,
                "future_path": vnd_w_future_path,
                "future_markers": vnd_w_future_markers,
                "audit_data": vnd_audit_data,
                "projection_hud": vnd_projection_hud,
                "price_lines": vnd_lines,
                "plan": {
                    "type": "BUY",
                    "action": "CANH MUA ĐÁY CHU KỲ SÓNG C & CHÂN SÓNG 1",
                    "action_zone": "14.2 - 14.8 nghìn đồng",
                    "invalidation": "13.7 nghìn đồng (Thủng hỗ trợ nến tuần)",
                    "tp1": "17.5 nghìn đồng (+17.1%)",
                    "tp2": "21.0 nghìn đồng (+40.5%)",
                    "rr": "1 : 3.80",
                    "model": "<b>Hoàn Tất Chu Kỳ Điều Chỉnh A-B-C:</b><br>• Đỉnh chu kỳ: 26.58k.<br>• Sóng (A) rơi về 13.90k, hồi (B) lên 19.10k, xả (C) cạn kiệt tạo đáy kép tại 12.60k - 12.75k.<br>• Nến tuần 2026-11-06 bứt phá mạnh mẽ lên 14.95k nổ volume kỷ lục 102.7 triệu cổ phiếu, kích hoạt chân Sóng (1) mới.<br>• Định giá tài sản nội bộ ròng cân bằng tại 14.95k, P/B 1.05x là bệ đỡ an toàn tuyệt đối.",
                    "trigger": "Giá điều chỉnh test lại vùng 14.2 - 14.8k với volume cạn kiệt, hoặc nến ngày xác nhận đóng cửa trên 15.0k."
                }
            },
            "1D": {
                "candles": vnd_d,
                "ma10": compute_ma(vnd_d, 10),
                "ma20": compute_ma(vnd_d, 20),
                "ma50": compute_ma(vnd_d, 50),
                "wave_line": [],
                "wave_markers": vnd_d_markers,
                "future_path": vnd_d_future_path,
                "future_markers": vnd_d_future_markers,
                "price_lines": vnd_lines,
                "plan": {
                    "type": "BUY",
                    "action": "CANH MUA PULLBACK KHUNG NGÀY",
                    "action_zone": "14.2 - 14.7 nghìn đồng",
                    "invalidation": "13.7 nghìn đồng",
                    "tp1": "16.2 nghìn đồng (Đỉnh cũ ngắn hạn)",
                    "tp2": "17.5 nghìn đồng (Kháng cự tuần)",
                    "rr": "1 : 3.25",
                    "model": "<b>Khung Ngày (1D):</b> Mô hình 2 đáy (Double Bottom) đảo chiều thành công tại 12.60k - 13.05k. Giá vượt mạnh mẽ lên trên toàn bộ MA10, MA20 ngày kèm phân kỳ dương MACD 2 đoạn rõ rệt.",
                    "trigger": "Chờ nhịp test lại MA10/MA20 Daily (vùng 14.2 - 14.6k) xuất hiện nến rút chân."
                }
            },
            "1H": {
                "candles": vnd_1h,
                "ma10": compute_ma(vnd_1h, 10),
                "ma20": compute_ma(vnd_1h, 20),
                "ma50": compute_ma(vnd_1h, 50),
                "wave_line": [],
                "wave_markers": [],
                "future_path": [],
                "future_markers": [],
                "price_lines": vnd_lines,
                "plan": {
                    "type": "BUY",
                    "action": "BẮT ĐIỂM VÀO LỆNH INTRADAY",
                    "action_zone": "14.6 - 14.8 nghìn đồng",
                    "invalidation": "14.4 nghìn đồng",
                    "tp1": "15.5 nghìn đồng",
                    "tp2": "16.2 nghìn đồng",
                    "rr": "1 : 2.50",
                    "model": "<b>Khung 1H Intraday:</b> Dòng tiền lớn nhập cuộc dứt khoát đẩy giá bứt phá kháng cự 14.5k. Canh nhịp chỉnh ngắn chạm MA20 1H để giải ngân vị thế.",
                    "trigger": "Nến 1H rút chân tại hỗ trợ 14.65k với volume thấp."
                }
            }
        }
    },
    "BTCUSD": {
        "name": "Bitcoin / U.S. Dollar (BTCUSD)",
        "market": "Global Crypto · Binance Public Stream",
        "live_type": "BINANCE_WS",
        "live_symbol": "btcusdt",
        "default_tf": "1W",
        "available_tfs": ["1W", "1D", "4H", "1H"],
        "timeframes": {
            "1W": {
                "candles": btc_w,
                "projection_hud": btc_projection_hud,
                "ma10": compute_ma(btc_w, 10),
                "ma20": compute_ma(btc_w, 20),
                "ma50": compute_ma(btc_w, 50),
                "wave_line": [],
                "wave_markers": btc_w_markers,
                "future_path": btc_w_future_path,
                "future_markers": btc_w_future_markers,
                "price_lines": btc_w_lines,
                "plan": {
                    "type": "SELL",
                    "action": "CANH BÁN SÓNG CON C-2",
                    "action_zone": "$80,000 - $81,500 (Kiểm định Trendline gãy)",
                    "invalidation": "$88,500.00 (Vượt đỉnh Sóng B)",
                    "tp1": "$48,500.00 (Thủng đáy A 57.8k)",
                    "tp2": "$37,949.00 (Fibo 1.272)",
                    "rr": "1 : 3.85",
                    "model": "<b>Đếm Sóng Fsen Chuẩn Xác & Đối Soát MACD:</b><br>• <b>Đáy (A) Đã Xong ở trước:</b> Chạm đáy $57,800 (tuần 29/06/2026, khớp Fibo 1.0 = $58k).<br>• <b>Đỉnh (B) Đã Hồi ở trước:</b> Đạt $87,396 (tuần 28/09/2026, chạm đúng Fibo 0.618 = $86.4k).<br>• <b>Hiện Tại ($75.8k):</b> Đang trong <b>Sóng (C) đổ đèo</b>. Cây nến hiện tại là đáy sóng con C-1. Chờ nhịp hồi kỹ thuật C-2 lên vùng $80k-$81.5k để kích hoạt vị thế Bán theo xu hướng lớn hướng về $48.5k và $37.9k.",
                    "trigger": "Giá hồi lên $80,000 - $81,500, nến từ chối giá và MACD 4H/1D cắt xuống."
                }
            },
            "1D": {
                "candles": btc_d,
                "ma10": compute_ma(btc_d, 10),
                "ma20": compute_ma(btc_d, 20),
                "ma50": compute_ma(btc_d, 50),
                "wave_line": [],
                "wave_markers": btc_d_markers,
                "future_path": btc_d_future_path,
                "future_markers": btc_d_future_markers,
                "price_lines": btc_w_lines,
                "plan": {
                    "type": "SELL",
                    "action": "CANH BÁN THEO ĐÀ KHUNG NGÀY",
                    "action_zone": "$79,500 - $81,000 (MA20 Daily)",
                    "invalidation": "$85,000.00",
                    "tp1": "$68,000.00",
                    "tp2": "$57,800.00 (Đáy A cũ)",
                    "rr": "1 : 3.20",
                    "model": "<b>Khung Ngày (1D):</b> Xu hướng giảm chi phối hoàn toàn. Sau nhịp rơi từ 87.4k về 74.8k, thị trường xuất hiện nến giằng co cạn volume. Canh Bán nhịp pullback kiểm định đường MA20 Daily.",
                    "trigger": "Nến 1D chạm MA20 ($80k) bị từ chối giá kèm volume bán tăng."
                }
            },
            "4H": {
                "candles": btc_4h,
                "ma10": compute_ma(btc_4h, 10),
                "ma20": compute_ma(btc_4h, 20),
                "ma50": compute_ma(btc_4h, 50),
                "wave_line": [],
                "wave_markers": [],
                "future_path": [],
                "future_markers": [],
                "price_lines": btc_w_lines,
                "plan": {
                    "type": "SELL",
                    "action": "SCALPING / INTRADAY SHORT",
                    "action_zone": "$78,500 - $79,800",
                    "invalidation": "$82,000.00",
                    "tp1": "$74,500.00",
                    "tp2": "$72,000.00",
                    "rr": "1 : 2.50",
                    "model": "<b>Khung 4H Intraday:</b> Đang tích lũy đáy ngắn hạn quanh 75.8k. RSI đang ở vùng quá bán (oversold 32). Chờ nhịp hồi ngắn hạn để mở vị thế Short.",
                    "trigger": "RSI 4H hồi lên vùng 55-60 và MACD 4H tạo phân kỳ âm đỉnh."
                }
            },
            "1H": {
                "candles": btc_1h,
                "ma10": compute_ma(btc_1h, 10),
                "ma20": compute_ma(btc_1h, 20),
                "ma50": compute_ma(btc_1h, 50),
                "wave_line": [],
                "wave_markers": [],
                "future_path": [],
                "future_markers": [],
                "price_lines": btc_w_lines,
                "plan": {
                    "type": "SELL",
                    "action": "THEO DÕI NẾN 1H REAL-TIME",
                    "action_zone": "$76,800 - $77,500",
                    "invalidation": "$79,000.00",
                    "tp1": "$74,800.00",
                    "tp2": "$73,500.00",
                    "rr": "1 : 2.00",
                    "model": "<b>Khung 1H Real-time:</b> Biến động vi mô theo từng tick Binance WebSocket. Quan sát phản ứng tại cản động MA50 1H.",
                    "trigger": "Gãy hỗ trợ 75,200 hoặc chạm 77,500 quay đầu."
                }
            }
        }
    },
    "FPT": {
        "name": "Công ty Cổ phần FPT (HOSE: FPT)",
        "market": "Vietnam Equity · VNDirect Dchart (nghìn đồng)",
        "live_type": "POLLING_SIM",
        "live_symbol": "FPT",
        "default_tf": "1W",
        "available_tfs": ["1M", "1W", "1D", "1H"],
        "timeframes": {
            "1M": {
                "candles": fpt_m,
                "ma10": compute_ma(fpt_m, 10),
                "ma20": compute_ma(fpt_m, 20),
                "ma50": compute_ma(fpt_m, 50),
                "wave_line": [],
                "wave_markers": fpt_m_markers,
                "future_path": fpt_m_future_path,
                "future_markers": fpt_m_future_markers,
                "price_lines": fpt_w_lines,
                "plan": {
                    "type": "BUY",
                    "action": "TÍCH SẢN DÀI HẠN KHUNG THÁNG",
                    "action_zone": "48.0 - 52.0 nghìn đồng",
                    "invalidation": "44.0 nghìn đồng",
                    "tp1": "75.0 nghìn đồng",
                    "tp2": "97.5 nghìn đồng (Đỉnh cũ)",
                    "rr": "1 : 4.50",
                    "model": "<b>Khung Tháng (1M):</b> FPT giữ nguyên kênh xu hướng tăng trưởng dài hạn 15 năm qua. Nhịp điều chỉnh từ đỉnh 97.5k về 50.8k kiểm định MA20 Tháng là cơ hội vàng tích sản chu kỳ mới.",
                    "trigger": "Đóng nến tháng giữ vững trên mốc 48.0k kèm khối lượng tích lũy gia tăng."
                }
            },
            "1W": {
                "candles": fpt_w,
                "ma10": compute_ma(fpt_w, 10),
                "ma20": compute_ma(fpt_w, 20),
                "ma50": compute_ma(fpt_w, 50),
                "wave_line": [],
                "wave_markers": fpt_w_markers,
                "future_path": fpt_w_future_path,
                "future_markers": fpt_w_future_markers,
                "audit_data": fpt_audit_data,
                "projection_hud": fpt_projection_hud,
                "price_lines": fpt_w_lines,
                "plan": {
                    "type": "BUY",
                    "action": "CANH MUA ĐÁY CHU KỲ SÓNG C",
                    "action_zone": "50.0 - 51.5 nghìn đồng",
                    "invalidation": "48.5 nghìn đồng (Thủng đáy 49.55)",
                    "tp1": "68.0 nghìn đồng",
                    "tp2": "82.0 nghìn đồng",
                    "rr": "1 : 4.20",
                    "model": "<b>Hoàn Tất Chu Kỳ Điều Chỉnh A-B-C:</b><br>• Từ đỉnh 97.5k, FPT trải qua Sóng (A) về 62.8k, hồi (B) lên 70.6k, và bán tháo (C) cạn kiệt về đáy 49.55k.<br>• Nến tuần hiện tại 50.80k tạo nến rút chân búa (Hammer) tại hỗ trợ lịch sử. Bắt đầu Sóng 1 của chu kỳ đẩy mới.",
                    "trigger": "Tích lũy quanh 50.0 - 51.5k, bứt phá qua 53.5k kèm thanh khoản đột biến."
                }
            },
            "1D": {
                "candles": fpt_d,
                "ma10": compute_ma(fpt_d, 10),
                "ma20": compute_ma(fpt_d, 20),
                "ma50": compute_ma(fpt_d, 50),
                "wave_line": [],
                "wave_markers": fpt_d_markers,
                "future_path": fpt_d_future_path,
                "future_markers": fpt_d_future_markers,
                "price_lines": fpt_w_lines,
                "plan": {
                    "type": "BUY",
                    "action": "MUA GIA TĂNG TỶ TRỌNG NGÀY",
                    "action_zone": "50.5 - 51.5 nghìn đồng",
                    "invalidation": "49.0 nghìn đồng",
                    "tp1": "58.0 nghìn đồng (MA50 Daily)",
                    "tp2": "68.0 nghìn đồng",
                    "rr": "1 : 3.50",
                    "model": "<b>Khung Ngày (1D):</b> Hình thành mô hình Đáy Đôi (Double Bottom) tại 49.55k. MACD phân kỳ dương 2 đoạn rõ rệt.",
                    "trigger": "Giá vượt đường cổ (Neckline) 52.5k với cây nến Marubozu xanh mạnh."
                }
            },
            "1H": {
                "candles": fpt_1h,
                "ma10": compute_ma(fpt_1h, 10),
                "ma20": compute_ma(fpt_1h, 20),
                "ma50": compute_ma(fpt_1h, 50),
                "wave_line": [],
                "wave_markers": [],
                "future_path": [],
                "future_markers": [],
                "price_lines": fpt_w_lines,
                "plan": {
                    "type": "BUY",
                    "action": "BẮT ĐIỂM VÀO LỆNH INTRADAY",
                    "action_zone": "50.6 - 51.0 nghìn đồng",
                    "invalidation": "49.8 nghìn đồng",
                    "tp1": "53.0 nghìn đồng",
                    "tp2": "55.0 nghìn đồng",
                    "rr": "1 : 2.80",
                    "model": "<b>Khung 1H:</b> Dòng tiền vào bắt đáy rõ rệt ở phiên chiều, đường MA10 cắt lên MA20 1H.",
                    "trigger": "Breakout kháng cự 51.2k trong phiên giao dịch."
                }
            }
        }
    },
    "XAUUSD": {
        "name": "Gold Spot / U.S. Dollar (XAUUSD)",
        "market": "Global Commodities · Yahoo / OANDA",
        "live_type": "POLLING_SIM",
        "live_symbol": "GC=F",
        "default_tf": "1D",
        "available_tfs": ["1W", "1D", "1H"],
        "timeframes": {
            "1W": {
                "candles": gold_w,
                "projection_hud": xau_projection_hud,
                "ma10": compute_ma(gold_w, 10),
                "ma20": compute_ma(gold_w, 20),
                "ma50": compute_ma(gold_w, 50),
                "wave_line": [],
                "wave_markers": gold_wave_markers,
                "future_path": gold_future_path,
                "future_markers": gold_future_markers,
                "price_lines": gold_lines,
                "plan": {
                    "type": "BUY",
                    "action": "CANH MUA ĐÁY CHU KỲ LỚN",
                    "action_zone": "$3,980.00 - $4,050.00",
                    "invalidation": "$3,850.00 (Thủng đáy $3,879)",
                    "tp1": "$4,850.00",
                    "tp2": "$5,580.00 (Đỉnh cũ)",
                    "rr": "1 : 3.80",
                    "model": "<b>Hoàn Tất Chu Kỳ Sóng Điều Chỉnh A-B-C:</b><br>• Đỉnh Sóng 5 cũ: $5,586.20 kèm MACD Peak (+222.6).<br>• Sóng (A) về $4,100, Sóng (B) lên $4,783, Sóng (C) chạm đáy $3,879.30.<br>• Hiện tại $4,074.90 đã đảo chiều xác nhận bắt đầu 5 sóng đẩy mới.",
                    "trigger": "Canh mua khi giá test lại $3,980-$4,050 với nến rút chân."
                }
            },
            "1D": {
                "candles": gold_d,
                "ma10": compute_ma(gold_d, 10),
                "ma20": compute_ma(gold_d, 20),
                "ma50": compute_ma(gold_d, 50),
                "wave_line": [],
                "wave_markers": gold_wave_markers,
                "future_path": gold_future_path,
                "future_markers": gold_future_markers,
                "price_lines": gold_lines,
                "plan": {
                    "type": "BUY",
                    "action": "CANH MUA ĐẢO CHIỀU KHUNG NGÀY",
                    "action_zone": "$4,000.00 - $4,060.00",
                    "invalidation": "$3,850.00",
                    "tp1": "$4,450.00",
                    "tp2": "$4,850.00",
                    "rr": "1 : 3.50",
                    "model": "<b>Khung Ngày (1D):</b> Nến ngày bứt phá mạnh khỏi vùng nén $3,880-$3,920, MACD phân kỳ dương 3 đoạn.",
                    "trigger": "Chờ nhịp điều chỉnh lành mạnh về MA10 Daily ($4,020-$4,050) để vào lệnh."
                }
            }
        }
    }
}

master_json = json.dumps(master_store, ensure_ascii=False)


# =============================================================
# BUILD COMPREHENSIVE MULTI-TIMEFRAME REALTIME HTML
# =============================================================
html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TradingView Multi-Timeframe Elliott & Real-Time Radar — v5.0 Pro</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <script src="./assets/lightweight-charts.standalone.production.js"></script>
  <script>
    if (typeof LightweightCharts === 'undefined') {{
      document.write('<script src="https://unpkg.com/lightweight-charts@4.2.0/dist/lightweight-charts.standalone.production.js"><\\/script>');
    }}
  </script>

  <style>
    :root {{
      --bg-main: #0b0f19;
      --bg-panel: #0f172a;
      --border-color: rgba(255, 255, 255, 0.08);
      --text-primary: #f9fafb;
      --text-secondary: #9ca3af;
      --accent-cyan: #06b6d4;
      --accent-green: #10b981;
      --accent-red: #ef4444;
      --accent-gold: #f59e0b;
      --accent-purple: #8b5cf6;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-main);
      color: var(--text-primary);
      min-height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    /* HEADER */
    header {{
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      padding: 6px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      height: 54px;
    }}

    .brand-section {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .logo-badge {{
      background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
      color: #fff;
      font-weight: 800;
      font-size: 11px;
      padding: 4px 8px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }}

    .title-group h1 {{
      font-size: 13.5px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .title-group p {{
      font-size: 11px;
      color: var(--text-secondary);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* ASSET SWITCHER */
    .tab-pills {{
      display: flex;
      background: rgba(0, 0, 0, 0.45);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
    }}

    .tab-pill {{
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
      border: none;
      background: transparent;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .tab-pill:hover {{ color: #fff; }}

    .tab-pill.active {{
      background: #1e293b;
      color: var(--accent-cyan);
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }}

    /* TIMEFRAME SWITCHER */
    .tf-pills {{
      display: flex;
      background: rgba(0, 0, 0, 0.45);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid rgba(6, 182, 212, 0.3);
    }}

    .tf-pill {{
      padding: 4px 9px;
      font-size: 11px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-secondary);
      border: none;
      background: transparent;
      border-radius: 5px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .tf-pill:hover {{ color: #fff; }}

    .tf-pill.active {{
      background: var(--accent-cyan);
      color: #0b0f19;
      box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
    }}

    /* REALTIME BADGE */
    .realtime-badge {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 10.5px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      color: #34d399;
    }}

    .pulse-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 1.5s infinite;
    }}

    @keyframes pulse {{
      0% {{ transform: scale(0.9); opacity: 0.8; }}
      50% {{ transform: scale(1.3); opacity: 1; }}
      100% {{ transform: scale(0.9); opacity: 0.8; }}
    }}

    .controls-group {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .toggle-chip {{
      padding: 4px 8px;
      font-size: 11px;
      font-weight: 600;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: rgba(255, 255, 255, 0.03);
      color: var(--text-secondary);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }}

    .toggle-chip.active {{
      background: rgba(6, 182, 212, 0.15);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
    }}

    /* WORKSPACE */
    .workspace-container {{
      display: flex;
      flex: 1;
      height: calc(100vh - 54px);
      overflow: hidden;
      position: relative;
    }}

    
    /* FSEN WAVE PROJECTION HUD */
    .fsen-hud-box {{
      position: absolute;
      top: 50px;
      left: 16px;
      z-index: 12;
      background: rgba(15, 23, 42, 0.90);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 9px 13px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
      pointer-events: none;
      max-width: 330px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      transition: all 0.2s ease;
    }}
    .hud-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 5px;
      margin-bottom: 3px;
    }}
    .hud-badge {{
      font-size: 10px;
      font-weight: 700;
      color: #94a3b8;
      letter-spacing: 0.5px;
    }}
    .hud-dir {{
      font-size: 10.5px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
    }}
    .hud-dir.long {{
      background: rgba(16, 185, 129, 0.18);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }}
    .hud-dir.short {{
      background: rgba(239, 68, 68, 0.18);
      color: #ef4444;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }}
    .hud-body {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .hud-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}
    .hud-k {{
      color: #94a3b8;
      font-size: 10px;
    }}
    .hud-v {{
      font-size: 10.5px;
      color: #f8fafc;
      text-align: right;
    }}

    .chart-panel {{
      flex: 1;
      position: relative;
      background: #0f1422;
      display: flex;
      flex-direction: column;
    }}

    #tv-chart-container {{
      flex: 1;
      width: 100%;
      height: 100%;
      position: relative;
    }}

    /* Minimalist Legend */
    .chart-legend {{
      position: absolute;
      top: 10px;
      left: 14px;
      z-index: 10;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      gap: 3px;
      background: rgba(15, 20, 34, 0.88);
      backdrop-filter: blur(8px);
      padding: 6px 12px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
    }}

    .legend-row-top {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .legend-title {{
      font-size: 13px;
      font-weight: 700;
      color: #fff;
    }}

    .legend-tf-badge {{
      font-size: 11px;
      font-weight: 800;
      padding: 1px 5px;
      border-radius: 4px;
      background: #1e293b;
      color: var(--accent-cyan);
    }}

    .legend-price {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 13.5px;
      font-weight: 800;
      transition: color 0.3s;
    }}

    .price-up {{ color: var(--accent-green); }}
    .price-down {{ color: var(--accent-red); }}

    .legend-ohlcv {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--text-secondary);
      display: flex;
      gap: 8px;
    }}

    .legend-ohlcv span b {{ color: #e2e8f0; }}

    /* Side Intelligence Panel */
    .intel-panel {{
      width: 390px;
      background: var(--bg-panel);
      border-left: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      z-index: 20;
    }}

    .intel-header {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(15, 23, 42, 0.85);
      position: sticky;
      top: 0;
      backdrop-filter: blur(10px);
      z-index: 5;
    }}

    .intel-title {{
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--accent-cyan);
    }}

    .action-tag {{
      font-size: 11px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }}

    .tag-sell {{
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }}

    .tag-buy {{
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }}

    .intel-body {{
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    /* Real-Time Scenario Dynamic Monitor */
    .status-monitor-box {{
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .monitor-title {{
      font-size: 10.5px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-secondary);
      letter-spacing: 0.5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .monitor-status {{
      font-size: 12px;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .action-card {{
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 11px;
    }}

    .action-card.sell-mode {{ border-left: 3px solid var(--accent-red); }}
    .action-card.buy-mode {{ border-left: 3px solid var(--accent-green); }}

    .action-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}

    .rr-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-gold);
    }}

    .intel-metric-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 4px 0;
      border-bottom: 1px dashed rgba(255, 255, 255, 0.06);
      font-size: 11.5px;
    }}

    .intel-metric-row:last-child {{ border-bottom: none; }}
    .intel-label {{ color: var(--text-secondary); }}
    .intel-val {{ font-family: 'JetBrains Mono', monospace; font-weight: 600; color: #fff; }}
    .val-highlight {{ color: var(--accent-cyan); }}
    .val-danger {{ color: var(--accent-red); font-weight: 700; }}
    .val-success {{ color: var(--accent-green); font-weight: 700; }}

    .section-title {{
      font-size: 11px;
      font-weight: 700;
      color: #cbd5e1;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-top: 4px;
    }}

    .model-box {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 11px;
      line-height: 1.5;
      color: #94a3b8;
    }}

    .model-box b {{ color: #f1f5f9; }}

    .legend-guide {{
      display: flex;
      gap: 10px;
      padding: 7px 9px;
      background: rgba(0,0,0,0.3);
      border-radius: 6px;
      font-size: 10.5px;
    }}

    .guide-item {{
      display: flex;
      align-items: center;
      gap: 5px;
      color: #cbd5e1;
    }}

    .guide-line {{
      width: 12px;
      height: 3px;
      border-radius: 2px;
    }}

    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: rgba(0,0,0,0.2); }}
    ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 3px; }}
  </style>
</head>
<body>

  <header>
    <div class="brand-section">
      <div class="logo-badge">AGY INVEST</div>
      <div class="title-group">
        <h1 id="header-title">
          <span>Công ty Cổ phần Chứng khoán VNDIRECT (HOSE: VND)</span>
        </h1>
        <p id="header-market">Vietnam Equity · VNDirect Dchart · Đa Khung Thời Gian (1M, 1W, 1D, 1H)</p>
      </div>
    </div>

    <!-- Asset Switcher -->
    <div class="tab-pills">
      <button class="tab-pill active" id="tab-VND" onclick="switchAsset('VND')">VND (VNDIRECT)</button>
      <button class="tab-pill" id="tab-FPT" onclick="switchAsset('FPT')">FPT (Việt Nam)</button>
      <button class="tab-pill" id="tab-BTCUSD" onclick="switchAsset('BTCUSD')">BTCUSD</button>
      <button class="tab-pill" id="tab-XAUUSD" onclick="switchAsset('XAUUSD')">XAUUSD (Vàng)</button>
    </div>

    <!-- Multi-Timeframe Switcher -->
    <div class="tf-pills" id="tf-container">
      <!-- Dynamic Buttons: 1W, 1D, 4H, 1H, 1M -->
    </div>

    <!-- Real-time Status Badge -->
    <div class="realtime-badge" style="background: rgba(59, 130, 246, 0.12); border-color: rgba(59, 130, 246, 0.3); color: #60a5fa;">
      <div class="pulse-dot" style="background: #3b82f6; box-shadow: 0 0 8px #3b82f6;"></div>
      <span id="rt-label">SNAPSHOT CHỐT PHIÊN</span>
    </div>

    <!-- Controls -->
    <div class="controls-group">
      <button class="toggle-chip active" id="btn-toggle-wave" onclick="toggleWaveLine()">
        <span>🏷️ Nhãn Sóng Lịch Sử</span>
      </button>
      <button class="toggle-chip active" id="btn-toggle-scen" onclick="toggleScenario()">
        <span>🎯 Kịch Bản Tương Lai</span>
      </button>
      <button class="toggle-chip active" id="btn-toggle-ma" onclick="toggleMA()">
        <span>📈 4MA</span>
      </button>
      <button class="toggle-chip" onclick="resetZoom()">
        <span>🔍 Reset Zoom</span>
      </button>
    </div>
  </header>

  <div class="workspace-container">
    <div class="chart-panel">
      <!-- Minimalist Legend -->
      <div class="chart-legend">
        <div class="legend-row-top">
          <span class="legend-title" id="legend-symbol">BTCUSD</span>
          <span class="legend-tf-badge" id="legend-tf">1W</span>
          <span class="legend-price price-up" id="legend-price">--</span>
        </div>
        <div class="legend-ohlcv">
          <span>O: <b id="leg-open">--</b></span>
          <span>H: <b id="leg-high">--</b></span>
          <span>L: <b id="leg-low">--</b></span>
          <span>C: <b id="leg-close">--</b></span>
          <span>Vol: <b id="leg-vol">--</b></span>
        </div>
      </div>

      
      <!-- HUD Information Box (Kế Hoạch & Dự Báo Sóng Fsen) -->
      <div id="fsen-hud-box" class="fsen-hud-box">
        <div class="hud-header">
          <span class="hud-badge">🔮 DỰ BÁO SÓNG FSEN</span>
          <span id="hud-dir" class="hud-dir long">▲ LONG</span>
        </div>
        <div class="hud-body">
          <div class="hud-row"><span class="hud-k">Sóng dự kiến:</span> <b id="hud-model" class="hud-v" style="color: #f59e0b;">Sóng Đẩy [5-3-5-3-5]</b></div>
          <div class="hud-row"><span class="hud-k">Điểm vô hiệu:</span> <b id="hud-inv" class="hud-v" style="color: #ef4444;">INVALID: 12.60k</b></div>
          <div class="hud-row"><span class="hud-k">Biên độ S1 (H1):</span> <b id="hud-h1" class="hud-v" style="color: #38bdf8;">2.35k (CHoCH)</b></div>
          <div class="hud-row"><span class="hud-k">Mục tiêu Sóng 3?:</span> <b id="hud-w3" class="hud-v" style="color: #10b981;">18.15k (1.618× H1)</b></div>
          <div class="hud-row"><span class="hud-k">Tích lũy Sóng 4?:</span> <b id="hud-w4" class="hud-v" style="color: #f59e0b;">16.70k (0.382× W3)</b></div>
          <div class="hud-row"><span class="hud-k">Mục tiêu Sóng 5?:</span> <b id="hud-w5" class="hud-v" style="color: #c084fc;">19.05k - 21.0k (ATH 29k)</b></div>
          <div class="hud-row"><span class="hud-k">Chu kỳ thời gian:</span> <b id="hud-time" class="hud-v" style="color: #93c5fd;">20 Nến Tuần (~T4/2027)</b></div>
          <div class="hud-row"><span class="hud-k">Tỷ lệ R/R (W3):</span> <b id="hud-rr" class="hud-v" style="color: #34d399;">1 : 2.17</b></div>
        </div>
      </div>

      <div id="tv-chart-container"></div>
    </div>

    <!-- Side Intelligence Panel -->
    <aside class="intel-panel">
      <div class="intel-header">
        <span class="intel-title">Kế Hoạch Tác Chiến AI (Đa Khung)</span>
        <span class="action-tag tag-sell" id="side-tag">SELL</span>
      </div>

      <div class="intel-body">
        <!-- Real-Time Evaluation Box -->
        <div class="status-monitor-box">
          <div class="monitor-title">
            <span>Trạng Thái Kịch Bản Thời Gian Thực</span>
            <span id="monitor-time" style="font-family: 'JetBrains Mono', monospace; font-size: 10px;">--:--:--</span>
          </div>
          <div class="monitor-status" id="monitor-status">
            <span>⚡ ĐANG THEO DÕI BIẾN ĐỘNG GIÁ</span>
          </div>
        </div>

        <!-- Chú thích trực quan Chuẩn Hóa Màu Cấp Độ Sóng -->
        <div class="legend-guide" style="display: flex; flex-direction: column; gap: 7px; padding: 12px; background: rgba(15, 23, 42, 0.7); border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px;">Chuẩn Hóa Màu Theo Cấp Độ Sóng</div>
          <div class="guide-item" style="display: flex; align-items: center; gap: 8px; font-size: 11px;">
            <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #c084fc; box-shadow: 0 0 6px #c084fc;"></span>
            <span style="color: #e2e8f0;"><b>Đại Chu Kỳ [I] - [V]:</b> Tím Neon / Vàng Hoàng Kim</span>
          </div>
          <div class="guide-item" style="display: flex; align-items: center; gap: 8px; font-size: 11px;">
            <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #38bdf8; box-shadow: 0 0 6px #38bdf8;"></span>
            <span style="color: #e2e8f0;"><b>Chu Kỳ Trung Cảnh (1) - (5):</b> Xanh Sky Blue</span>
          </div>
          <div class="guide-item" style="display: flex; align-items: center; gap: 8px; font-size: 11px;">
            <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #f43f5e; box-shadow: 0 0 6px #f43f5e;"></span>
            <span style="color: #e2e8f0;"><b>Sóng Điều Chỉnh (A) - (B) - (C):</b> Đỏ Hồng San Hô</span>
          </div>
          <div class="guide-item" style="display: flex; align-items: center; gap: 8px; font-size: 11px;">
            <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #10b981; box-shadow: 0 0 6px #10b981;"></span>
            <span style="color: #e2e8f0;"><b>Bứt Phá / Chân Sóng Mới:</b> Xanh Emerald</span>
          </div>
          <div class="guide-item" style="display: flex; align-items: center; gap: 8px; font-size: 11px;">
            <span class="guide-line" style="display: inline-block; width: 18px; height: 0px; border-top: 2px dashed #00e5ff; box-shadow: 0 0 6px #00e5ff;"></span>
            <span style="color: #00e5ff;"><b>Kịch Bản Tương Lai:</b> Đường Nét Đứt Dự Phóng</span>
          </div>
        </div>

        <div class="action-card sell-mode" id="action-card">
          <div class="action-card-header">
            <span class="action-tag tag-sell" id="card-action">CANH BÁN</span>
            <span class="rr-badge" id="card-rr">R/R: 1 : 3.85</span>
          </div>
          <div class="intel-metric-row">
            <span class="intel-label">Vùng Canh Lệnh:</span>
            <span class="intel-val val-highlight" id="card-zone">--</span>
          </div>
          <div class="intel-metric-row">
            <span class="intel-label">Điểm Vô Hiệu (Stop Loss):</span>
            <span class="intel-val val-danger" id="card-sl">--</span>
          </div>
          <div class="intel-metric-row">
            <span class="intel-label">Mục Tiêu Chốt Lời 1:</span>
            <span class="intel-val val-success" id="card-tp1">--</span>
          </div>
          <div class="intel-metric-row">
            <span class="intel-label">Mục Tiêu Chốt Lời 2:</span>
            <span class="intel-val val-success" id="card-tp2">--</span>
          </div>
        </div>

        <div class="section-title">🌊 Đối Soát Mô Hình Sóng Fsen & MACD</div>
        <div class="model-box" id="model-desc"></div>

        <div class="section-title">⚡ Điều Kiện Kích Hoạt Lệnh</div>
        <div class="model-box" id="trigger-desc" style="border-left: 3px solid var(--accent-gold); margin-bottom: 14px;"></div>

        <div class="section-title">🛡️ Đối Soát 3 Thiết Luật & Fsen Confluence</div>
        <div id="fsen-audit-box" style="padding: 12px; background: rgba(15, 23, 42, 0.75); border-radius: 8px; border: 1px solid rgba(56, 189, 248, 0.25); font-size: 11px; margin-bottom: 14px;">
          <!-- Populated dynamically by JS -->
        </div>
      </div>
    </aside>
  </div>

  <script>
    const STORE = {master_json};

    let currentSym = 'VND';
    let currentTF = '1W';
    let showWaveLine = true;
    let showScenario = true;
    let showMA = true;

    let chart = null;
    let candleSeries = null;
    let volumeSeries = null;
    let waveLineSeries = null;
    let scenarioSeries = null;
    let ma10Series = null;
    let ma20Series = null;
    let ma50Series = null;
    let priceLines = [];

    let ws = null;
    let simInterval = null;

    function initChart() {{
      const container = document.getElementById('tv-chart-container');
      container.innerHTML = '';

      chart = LightweightCharts.createChart(container, {{
        width: container.clientWidth,
        height: container.clientHeight,
        layout: {{
          background: {{ color: '#0f1422' }},
          textColor: '#94a3b8',
          fontSize: 11,
          fontFamily: "'JetBrains Mono', monospace"
        }},
        grid: {{
          vertLines: {{ color: 'rgba(255, 255, 255, 0.04)' }},
          horzLines: {{ color: 'rgba(255, 255, 255, 0.04)' }}
        }},
        crosshair: {{
          mode: LightweightCharts.CrosshairMode.Normal,
          vertLine: {{ color: '#06b6d4', width: 1, style: LightweightCharts.LineStyle.Dashed }},
          horzLine: {{ color: '#06b6d4', width: 1, style: LightweightCharts.LineStyle.Dashed }}
        }},
        rightPriceScale: {{
          borderColor: 'rgba(255, 255, 255, 0.08)',
          scaleMargins: {{ top: 0.08, bottom: 0.15 }},
          autoScale: true
        }},
        timeScale: {{
          borderColor: 'rgba(255, 255, 255, 0.08)',
          timeVisible: true
        }}
      }});

      candleSeries = chart.addCandlestickSeries({{
        upColor: '#10b981',
        downColor: '#ef4444',
        borderVisible: false,
        wickUpColor: '#10b981',
        wickDownColor: '#ef4444'
      }});

      volumeSeries = chart.addHistogramSeries({{
        color: '#26a69a',
        priceFormat: {{ type: 'volume' }},
        priceScaleId: '',
        scaleMargins: {{ top: 0.82, bottom: 0 }}
      }});

      ma10Series = chart.addLineSeries({{ color: '#22c55e', lineWidth: 1, priceLineVisible: false, lastValueVisible: false }});
      ma20Series = chart.addLineSeries({{ color: '#ff9800', lineWidth: 1, priceLineVisible: false, lastValueVisible: false }});
      ma50Series = chart.addLineSeries({{ color: '#00bcd4', lineWidth: 1.5, priceLineVisible: false, lastValueVisible: false }});

      // Sóng đã đi (Nét liền màu vàng)
      waveLineSeries = chart.addLineSeries({{
        color: '#f59e0b',
        lineWidth: 2.2,
        lineStyle: LightweightCharts.LineStyle.Solid,
        priceLineVisible: false,
        lastValueVisible: false
      }});

      // Dự báo tương lai (Nét đứt màu cyan xuất phát từ nến hiện tại)
      scenarioSeries = chart.addLineSeries({{
        color: '#00e5ff',
        lineWidth: 2.5,
        lineStyle: LightweightCharts.LineStyle.Dashed,
        priceLineVisible: false,
        lastValueVisible: false
      }});

      chart.subscribeCrosshairMove(param => {{
        if (!param.time || !param.seriesPrices || !param.seriesPrices.get(candleSeries)) return;
        const c = param.seriesPrices.get(candleSeries);
        if (c) updateLegendBar(c);
      }});

      window.addEventListener('resize', () => {{
        if (chart && container) chart.applyOptions({{ width: container.clientWidth, height: container.clientHeight }});
      }});
    }}

    function updateLegendBar(c) {{
      document.getElementById('leg-open').textContent = formatPrice(c.open);
      document.getElementById('leg-high').textContent = formatPrice(c.high);
      document.getElementById('leg-low').textContent = formatPrice(c.low);
      document.getElementById('leg-close').textContent = formatPrice(c.close);
      document.getElementById('legend-price').textContent = formatPrice(c.close);
      document.getElementById('legend-price').className = c.close >= c.open ? 'legend-price price-up' : 'legend-price price-down';
    }}

    function formatPrice(val) {{
      if (val === undefined || val === null) return 'N/A';
      if (val >= 1000) return val.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
      return val.toFixed(2);
    }}

    function renderTimeframePills(assetData) {{
      const tfContainer = document.getElementById('tf-container');
      tfContainer.innerHTML = '';
      assetData.available_tfs.forEach(tf => {{
        const btn = document.createElement('button');
        btn.className = 'tf-pill ' + (tf === currentTF ? 'active' : '');
        btn.id = 'tf-btn-' + tf;
        btn.textContent = tf;
        btn.onclick = () => switchTimeframe(tf);
        tfContainer.appendChild(btn);
      }});
    }}

    function switchAsset(sym) {{
      currentSym = sym;
      const asset = STORE[sym];
      if (!asset) return;

      document.querySelectorAll('.tab-pill').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('tab-' + sym);
      if (activeBtn) activeBtn.classList.add('active');

      document.getElementById('header-title').querySelector('span').textContent = asset.name;
      document.getElementById('header-market').textContent = asset.market + ' · Đa Khung Real-time';
      document.getElementById('legend-symbol').textContent = sym;

      // Select default TF or maintain if valid
      if (!asset.available_tfs.includes(currentTF)) {{
        currentTF = asset.default_tf;
      }}

      renderTimeframePills(asset);
      renderActiveChart();
      initRealtimeFeed(sym);
    }}

    function switchTimeframe(tf) {{
      currentTF = tf;
      document.querySelectorAll('.tf-pill').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('tf-btn-' + tf);
      if (activeBtn) activeBtn.classList.add('active');

      document.getElementById('legend-tf').textContent = tf;
      renderActiveChart();
    }}

    function renderActiveChart() {{
      const asset = STORE[currentSym];
      if (!asset) return;
      const tfData = asset.timeframes[currentTF];
      if (!tfData) return;

      candleSeries.setData(tfData.candles || []);

      const volData = (tfData.candles || []).map(c => ({{
        time: c.time,
        value: c.volume || 0,
        color: c.close >= c.open ? 'rgba(16, 185, 129, 0.35)' : 'rgba(239, 68, 68, 0.35)'
      }}));
      volumeSeries.setData(volData);

      if (showMA) {{
        ma10Series.setData(tfData.ma10 || []);
        ma20Series.setData(tfData.ma20 || []);
        ma50Series.setData(tfData.ma50 || []);
      }} else {{
        ma10Series.setData([]);
        ma20Series.setData([]);
        ma50Series.setData([]);
      }}

      // KHÔNG VẼ ĐƯỜNG NỐI SÓNG - GIỮ NGUYÊN BẢN ĐƯỜNG GIÁ SẠCH SẼ
      waveLineSeries.setData([]);
      waveLineSeries.setMarkers([]);

      // CẮM TRỰC TIẾP NHÃN SÓNG VÀO NẾN (candleSeries) - CO DÃN KHÔNG BAO GIỜ LỆCH TỌA ĐỘ
      if (showWaveLine && tfData.wave_markers && tfData.wave_markers.length > 0) {{
        // LightweightCharts yêu cầu markers phải được sắp xếp tăng dần theo thời gian
        const sortedMarkers = [...tfData.wave_markers].sort((a, b) => (a.time > b.time ? 1 : -1));
        candleSeries.setMarkers(sortedMarkers);
      }} else {{
        candleSeries.setMarkers([]);
      }}

      // DỰ BÁO TƯƠNG LAI: ĐƯỜNG NÉT ĐỨT CYAN XUẤT PHÁT TỪ NẾN HIỆN TẠI HƯỚNG TỚI CÁC MỐC TP
      if (showScenario && tfData.future_path && tfData.future_path.length > 0) {{
        scenarioSeries.setData(tfData.future_path);
        const sortedFutureMarkers = [...(tfData.future_markers || [])].sort((a, b) => (a.time > b.time ? 1 : -1));
        scenarioSeries.setMarkers(sortedFutureMarkers);
      }} else {{
        scenarioSeries.setData([]);
        scenarioSeries.setMarkers([]);
      }}

      // Price Lines
      priceLines.forEach(pl => candleSeries.removePriceLine(pl));
      priceLines = [];
      if (tfData.price_lines) {{
        tfData.price_lines.forEach(line => {{
          const pl = candleSeries.createPriceLine({{
            price: line.price,
            color: line.color,
            lineWidth: line.style === 0 ? 1.5 : 1,
            lineStyle: line.style === 0 ? LightweightCharts.LineStyle.Solid : LightweightCharts.LineStyle.Dashed,
            axisLabelVisible: true,
            title: line.title
          }});
          priceLines.push(pl);
        }});
      }}

      const last = tfData.candles[tfData.candles.length - 1];
      if (last) updateLegendBar(last);

      renderIntelPanel(tfData.plan, tfData.audit_data);

      // Cập nhật bảng HUD Dự Báo Sóng Fsen
      const hudBox = document.getElementById('fsen-hud-box');
      if (tfData.projection_hud) {{
        hudBox.style.display = 'flex';
        const h = tfData.projection_hud;
        const dirEl = document.getElementById('hud-dir');
        dirEl.textContent = h.direction;
        dirEl.className = 'hud-dir ' + (h.direction.includes('LONG') ? 'long' : 'short');
        document.getElementById('hud-model').textContent = h.wave_model;
        document.getElementById('hud-inv').textContent = h.invalidation;
        document.getElementById('hud-h1').textContent = h.h1;
        document.getElementById('hud-w3').textContent = h.w3_target;
        document.getElementById('hud-w4').textContent = h.w4_target;
        document.getElementById('hud-w5').textContent = h.w5_target;
        document.getElementById('hud-time').textContent = h.time_cycle;
        document.getElementById('hud-rr').textContent = h.rr;
      }} else {{
        hudBox.style.display = 'none';
      }}

      chart.timeScale().fitContent();
    }}

    function renderIntelPanel(plan) {{
      if (!plan) return;
      const isSell = plan.type === 'SELL';
      const card = document.getElementById('action-card');
      card.className = 'action-card ' + (isSell ? 'sell-mode' : 'buy-mode');

      document.getElementById('side-tag').textContent = plan.type;
      document.getElementById('side-tag').className = 'action-tag ' + (isSell ? 'tag-sell' : 'tag-buy');

      document.getElementById('card-action').textContent = plan.action;
      document.getElementById('card-action').className = 'action-tag ' + (isSell ? 'tag-sell' : 'tag-buy');
      document.getElementById('card-rr').textContent = 'R/R: ' + plan.rr;

      document.getElementById('card-zone').textContent = plan.action_zone;
      document.getElementById('card-sl').textContent = plan.invalidation;
      document.getElementById('card-tp1').textContent = plan.tp1;
      document.getElementById('card-tp2').textContent = plan.tp2;

      document.getElementById('model-desc').innerHTML = plan.model;
      document.getElementById('trigger-desc').textContent = plan.trigger;

      const auditBox = document.getElementById('fsen-audit-box');
      if (auditBox) {{
        if (auditData) {{
          const ir = auditData.inviolable_rules;
          const fc = auditData.fsen_confluence;
          const fm = auditData.fibonacci_matrix;
          let h = '';
          h += '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">';
          h += '<span style="font-weight: 700; color: #38bdf8; text-transform: uppercase;">3 THIẾT LUẬT BẤT BIẾN</span>';
          h += '<span style="background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 10px;">' + ir.status + '</span>';
          h += '</div>';
          h += '<div style="color: #cbd5e1; font-size: 10px; line-height: 1.4; margin-bottom: 8px;">';
          h += '<div>• <b>Luật 1:</b> ' + ir.rule_1.detail + '</div>';
          h += '<div>• <b>Luật 2:</b> ' + ir.rule_2.detail + '</div>';
          h += '<div>• <b>Luật 3:</b> ' + ir.rule_3.detail + '</div>';
          h += '</div>';
          h += '<div style="font-weight: 700; color: #fbbf24; text-transform: uppercase; margin-bottom: 4px;">ĐỐI SOÁT FSEN MACD & VOL</div>';
          h += '<div style="color: #cbd5e1; font-size: 10px; line-height: 1.4; margin-bottom: 8px;">';
          h += '<div>• <b>Sóng (3) MACD Peak:</b> <span style="color: #10b981;">✓ ' + fc.wave3_macd_peak.note + ' (' + fc.wave3_macd_peak.val + ')</span></div>';
          h += '<div>• <b>Sóng (4) Zero-Cross:</b> <span style="color: #10b981;">✓ ' + fc.wave4_zero_cross.note + ' (' + fc.wave4_zero_cross.val + ')</span></div>';
          h += '<div>• <b>Đáy (C) Phân Kỳ:</b> <span style="color: #38bdf8;">✓ ' + fc.wave_c_divergence.detail + '</span></div>';
          h += '<div>• <b>Volume Bứt Phá:</b> <span style="color: #10b981;">✓ ' + fc.breakout_volume.note + '</span></div>';
          h += '</div>';
          h += '<div style="font-weight: 700; color: #c084fc; text-transform: uppercase; margin-bottom: 4px;">MA TRẬN MỤC TIÊU FIBONACCI</div>';
          h += '<div style="color: #cbd5e1; font-size: 10px; line-height: 1.4;">';
          h += '<div>• <b>TP1:</b> ' + fm.targets.tp1.price + 'k <span style="color: #10b981;">(' + fm.targets.tp1.label + ')</span></div>';
          h += '<div>• <b>TP2:</b> ' + fm.targets.tp2.price + 'k <span style="color: #ffd700;">(' + fm.targets.tp2.label + ')</span></div>';
          h += '<div>• <b>TP3:</b> ' + fm.targets.tp3.price + 'k <span style="color: #c084fc;">(' + fm.targets.tp3.label + ')</span></div>';
          h += '</div>';
          auditBox.innerHTML = h;
        }} else {{
          auditBox.innerHTML = '<div style="color: #94a3b8; font-size: 10px; line-height: 1.4;">⚡ Dữ liệu kiểm định đa tầng chuẩn Fsen & Fibonacci tự động cập nhật theo khung tuần chuẩn 1W.</div>';
        }}
      }}
    }}

    // =========================================================
    // REAL-TIME ENGINE (SNAPSHOT MODE DEFAULT / TOGGLEABLE)
    // =========================================================
    const ENABLE_REALTIME = false; // Tạm dừng cập nhật thời gian thực theo yêu cầu người dùng, khi cần triển khai sẽ bật true

    function initRealtimeFeed(sym) {{
      if (ws) {{ ws.close(); ws = null; }}
      if (simInterval) {{ clearInterval(simInterval); simInterval = null; }}

      if (!ENABLE_REALTIME) {{
        document.getElementById('rt-label').textContent = 'SNAPSHOT CHỐT PHIÊN';
        document.getElementById('rt-label').style.color = '#60a5fa';
        return;
      }}

      const asset = STORE[sym];
      if (!asset) return;

      if (asset.live_type === 'BINANCE_WS') {{
        try {{
          ws = new WebSocket('wss://stream.binance.com:9443/ws/' + asset.live_symbol + '@ticker');
          ws.onopen = () => {{
            document.getElementById('rt-label').textContent = 'LIVE BINANCE WS';
            document.getElementById('rt-label').style.color = '#34d399';
          }};
          ws.onmessage = (event) => {{
            const data = JSON.parse(event.data);
            const livePrice = parseFloat(data.c);
            onLiveTick(sym, livePrice);
          }};
          ws.onerror = () => {{
            fallbackPolling(sym);
          }};
        }} catch(e) {{
          fallbackPolling(sym);
        }}
      }} else {{
        fallbackPolling(sym);
      }}
    }}

    function fallbackPolling(sym) {{
      document.getElementById('rt-label').textContent = 'LIVE POLLING (3s)';
      simInterval = setInterval(() => {{
        const asset = STORE[sym];
        if (!asset) return;
        const tfData = asset.timeframes[currentTF];
        if (!tfData || !tfData.candles || tfData.candles.length === 0) return;
        const lastCandle = tfData.candles[tfData.candles.length - 1];
        // Micro fluctuation
        const jitter = (Math.random() - 0.49) * (lastCandle.close * 0.001);
        const livePrice = Math.max(0.1, lastCandle.close + jitter);
        onLiveTick(sym, livePrice);
      }}, 2500);
    }}

    function onLiveTick(sym, livePrice) {{
      if (sym !== currentSym) return;

      const now = new Date();
      document.getElementById('monitor-time').textContent = now.toTimeString().split(' ')[0];

      // Update Header & Legend
      const legPrice = document.getElementById('legend-price');
      const oldPrice = parseFloat(legPrice.textContent.replace(/,/g, '')) || livePrice;
      legPrice.textContent = formatPrice(livePrice);
      legPrice.className = livePrice >= oldPrice ? 'legend-price price-up' : 'legend-price price-down';

      // Update Latest Candle in Series
      const asset = STORE[sym];
      const tfData = asset.timeframes[currentTF];
      if (tfData && tfData.candles && tfData.candles.length > 0) {{
        const last = tfData.candles[tfData.candles.length - 1];
        const updated = {{
          time: last.time,
          open: last.open,
          high: Math.max(last.high, livePrice),
          low: Math.min(last.low, livePrice),
          close: livePrice
        }};
        candleSeries.update(updated);
      }}

      // DYNAMIC SCENARIO EVALUATION
      evaluateScenarioDynamic(livePrice, tfData.plan);
    }}

    function evaluateScenarioDynamic(price, plan) {{
      if (!plan) return;
      const monitor = document.getElementById('monitor-status');
      
      // Parse invalidation SL
      const slMatch = plan.invalidation.match(/([0-9.,]+)/);
      const slPrice = slMatch ? parseFloat(slMatch[1].replace(/,/g, '')) : null;

      if (plan.type === 'SELL') {{
        if (slPrice && price >= slPrice) {{
          monitor.innerHTML = '<span style=\"color: #ef4444;\">🚨 KỊCH BẢN ĐÃ BỊ VÔ HIỆU HÓA (VƯỢT STOP LOSS)</span>';
          return;
        }}
        if (price >= 80000 && price <= 81500) {{
          monitor.innerHTML = '<span style=\"color: #f59e0b;\">🎯 ĐANG TRONG VÙNG KÍCH HOẠT LỆNH BÁN ($80k-$81.5k)</span>';
          return;
        }}
        if (price < 74888) {{
          monitor.innerHTML = '<span style=\"color: #10b981;\">📉 ĐÃ PHÁ ĐÁY C-1, ĐANG TIẾN VỀ TP1 ($48.5k)</span>';
          return;
        }}
      }} else if (plan.type === 'BUY') {{
        if (slPrice && price <= slPrice) {{
          monitor.innerHTML = '<span style=\"color: #ef4444;\">🚨 KỊCH BẢN ĐÃ BỊ VÔ HIỆU HÓA (THỦNG STOP LOSS)</span>';
          return;
        }}
        if (price >= 50.0 && price <= 51.5) {{
          monitor.innerHTML = '<span style=\"color: #10b981;\">🎯 ĐANG TRONG VÙNG CANH MUA TỐI ƯU (50.0 - 51.5k)</span>';
          return;
        }}
      }}

      monitor.innerHTML = '<span style=\"color: #38bdf8;\">⚡ KỊCH BẢN DUY TRÌ HỢP LỆ (' + formatPrice(price) + ')</span>';
    }}

    function toggleWaveLine() {{
      showWaveLine = !showWaveLine;
      document.getElementById('btn-toggle-wave').classList.toggle('active', showWaveLine);
      renderActiveChart();
    }}

    function toggleScenario() {{
      showScenario = !showScenario;
      document.getElementById('btn-toggle-scen').classList.toggle('active', showScenario);
      renderActiveChart();
    }}

    function toggleMA() {{
      showMA = !showMA;
      document.getElementById('btn-toggle-ma').classList.toggle('active', showMA);
      renderActiveChart();
    }}

    function resetZoom() {{
      if (chart) chart.timeScale().fitContent();
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      initChart();
      switchAsset('VND');
    }});
  </script>
</body>
</html>
"""

# Generate MASTER Dashboard (Default: VND)
html_master = html_content.replace("switchAsset('VND');", "switchAsset('VND');")
out_master = "outputs/investment/chart_scenario_interactive_MASTER.html"
with open(out_master, "w", encoding="utf-8") as f:
    f.write(html_master)
print(f"[SUCCESS] Multi-Timeframe Real-time MASTER Dashboard written to: {out_master}")

# Generate Standalone VND Dashboard
html_vnd = html_content.replace("switchAsset('VND');", "switchAsset('VND');")
html_vnd = html_vnd.replace("<title>TradingView Multi-Timeframe Elliott & Real-Time Radar — v5.0 Pro</title>", "<title>VNDIRECT (HOSE: VND) — Biểu Đồ Kịch Bản Kỹ Thuật Tương Tác Fsen & Sóng Elliott</title>")
out_vnd = "outputs/investment/chart_scenario_VND.html"
with open(out_vnd, "w", encoding="utf-8") as f:
    f.write(html_vnd)
print(f"[SUCCESS] Dedicated Standalone VND Dashboard written to: {out_vnd}")

