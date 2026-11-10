"""
Invest Technical Engine — Não bộ phân tích kỹ thuật 6 Trụ Cột Fsen & Sóng Elliott
Hỗ trợ đa khung thời gian:
- Việt Nam (FPT): M, W, D, 1H
- Quốc tế (BTCUSD): W, D, 4H, 1H
"""

import os
import sys
import json
import math
import numpy as np
import pandas as pd


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Tính các chỉ báo SMA, RSI, MACD"""
    df = df.copy()
    close = df['close']

    # SMA 10, 20, 50
    df['sma10'] = close.rolling(window=10).mean()
    df['sma20'] = close.rolling(window=20).mean()
    df['sma50'] = close.rolling(window=50).mean()

    # RSI 14
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df['rsi14'] = 100 - (100 / (1 + rs))
    df['rsi14'] = df['rsi14'].fillna(50.0)

    # MACD (12, 26, 9)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']

    return df


def find_pivots(df: pd.DataFrame, window=5):
    """Tìm các đỉnh đáy swing để vẽ hỗ trợ kháng cự và đếm sóng"""
    highs = df['high'].values
    lows = df['low'].values
    n = len(df)
    pivot_highs = []
    pivot_lows = []

    for i in range(window, n - window):
        if all(highs[i] >= highs[i - k] for k in range(1, window + 1)) and \
           all(highs[i] >= highs[i + k] for k in range(1, window + 1)):
            pivot_highs.append((i, highs[i]))
        if all(lows[i] <= lows[i - k] for k in range(1, window + 1)) and \
           all(lows[i] <= lows[i + k] for k in range(1, window + 1)):
            pivot_lows.append((i, lows[i]))

    return pivot_highs, pivot_lows


def analyze_single_timeframe(df: pd.DataFrame, tf_name: str, asset_type: str = "VN"):
    """Phân tích 6 trụ cột cho một khung thời gian cụ thể"""
    if len(df) < 15:
        return {
            "trend": "Chưa đủ dữ liệu",
            "range": "N/A",
            "wave": "N/A",
            "time": "N/A",
            "score": "N/A",
            "scenario": "N/A"
        }

    df = compute_indicators(df)
    last = df.iloc[-1]
    prev = df.iloc[-2]
    curr_price = last['close']

    # 1. TRỤ 1: XU HƯỚNG
    sma10 = last['sma10']
    sma20 = last['sma20']
    sma50 = last['sma50'] if pd.notna(last['sma50']) else sma20

    is_uptrend = curr_price > sma10 and sma10 > sma20
    is_downtrend = curr_price < sma10 and sma10 < sma20
    trend_direction = "Lên (Uptrend)" if is_uptrend else ("Xuống (Downtrend)" if is_downtrend else "Đi ngang (Sideway)")

    # 2. TRỤ 2: BIÊN ĐỘ, FIBONACCI & HỖ TRỢ / KHÁNG CỰ
    recent_high = df['high'].tail(50).max()
    recent_low = df['low'].tail(50).min()
    price_range = recent_high - recent_low

    fibo_382 = recent_high - 0.382 * price_range
    fibo_500 = recent_high - 0.500 * price_range
    fibo_618 = recent_high - 0.618 * price_range
    fibo_ext_1272 = recent_high + 0.272 * price_range
    fibo_ext_1618 = recent_high + 0.618 * price_range

    p_highs, p_lows = find_pivots(df, window=3)
    supports = sorted([p[1] for p in p_lows if p[1] < curr_price], reverse=True)[:3]
    resistances = sorted([p[1] for p in p_highs if p[1] > curr_price])[:3]

    if not supports:
        supports = [round(fibo_618, 2), round(fibo_500, 2)]
    if not resistances:
        resistances = [round(recent_high, 2), round(fibo_ext_1272, 2)]

    # 3. TRỤ 3: SÓNG ELLIOTT & ĐIỂM VÔ HIỆU HÓA
    # Xác định vị trí sóng ước lượng dựa trên MACD và vị trí Fibo
    if is_uptrend:
        if curr_price > recent_high * 0.98:
            wave_status = "Đang trong nhịp Sóng 3 hoặc Sóng 5 đẩy mở rộng"
            invalidation_point = round(fibo_618, 2)
        elif curr_price > fibo_500:
            wave_status = "Đang trong Sóng 4 điều chỉnh của Sóng 5 đẩy"
            invalidation_point = round(fibo_618, 2)
        else:
            wave_status = "Đang tích lũy đáy Sóng 2, chuẩn bị vào Sóng 3"
            invalidation_point = round(recent_low, 2)
    else:
        wave_status = "Đang điều chỉnh theo cấu trúc Sóng C (hoặc Zigzag W-X-Y)"
        invalidation_point = round(recent_high, 2)

    # 4. TRỤ 4: THỜI GIAN
    # Đếm số nến từ đáy hoặc đỉnh gần nhất
    idx_min = df['low'].tail(50).idxmin()
    candles_from_low = len(df) - 1 - idx_min
    idx_max = df['high'].tail(50).idxmax()
    candles_from_high = len(df) - 1 - idx_max

    # 5. TRỤ 5: BỘ CHẤM ĐIỂM
    score_points = 0
    reasons = []
    if curr_price > sma10:
        score_points += 1
        reasons.append("Giá > MA10 (+1)")
    if sma10 > sma20:
        score_points += 1
        reasons.append("MA10 > MA20 (+1)")
    if last['macd'] > 0:
        score_points += 1
        reasons.append("MACD > 0 (+1)")
    if last['macd_hist'] > prev['macd_hist']:
        score_points += 1
        reasons.append("MACD Histogram dốc lên (+1)")
    if 40 <= last['rsi14'] <= 68:
        score_points += 1
        reasons.append("RSI xung lực tốt (40-68) (+1)")
    if curr_price > fibo_618:
        score_points += 1
        reasons.append("Giá giữ trên Fibo 0.618 (+1)")

    # 6. TRỤ 6: KỊCH BẢN & CHIẾN THUẬT
    entry_zone = f"{fibo_618:,.1f} - {fibo_500:,.1f}"
    tp1 = round(resistances[0], 1) if resistances else round(recent_high, 1)
    tp2 = round(fibo_ext_1618, 1)

    return {
        "timeframe": tf_name,
        "current_price": curr_price,
        "sma10": round(sma10, 2),
        "sma20": round(sma20, 2),
        "sma50": round(sma50, 2),
        "rsi14": round(last['rsi14'], 2),
        "macd": round(last['macd'], 3),
        "macd_hist": round(last['macd_hist'], 3),
        "trend": f"• Hướng: **{trend_direction}**\n• Giá {'nằm trên' if curr_price > sma10 else 'dưới'} MA10, MA20\n• Hỗ trợ: {', '.join([f'{s:,.1f}' for s in supports[:2]])}\n• Kháng cự: {', '.join([f'{r:,.1f}' for r in resistances[:2]])}",
        "range": f"• Fibo Retracement: 0.382 ({fibo_382:,.1f}), 0.5 ({fibo_500:,.1f}), 0.618 ({fibo_618:,.1f})\n• Fibo Extension: 1.272 ({fibo_ext_1272:,.1f}), 1.618 ({fibo_ext_1618:,.1f})\n• Đáy gần nhất: {recent_low:,.1f} | Đỉnh gần nhất: {recent_high:,.1f}",
        "wave": f"• Vị trí: **{wave_status}**\n• 🚨 **ĐIỂM VÔ HIỆU HÓA SÓNG:** Thủng {invalidation_point:,.1f}\n• Cấu trúc: 5 sóng đẩy / ZigZag 5-3-5",
        "time": f"• Đã đi {candles_from_low} nến kể từ đáy ({recent_low:,.1f})\n• Đã đi {candles_from_high} nến kể từ đỉnh ({recent_high:,.1f})\n• Vùng phản ứng chu kỳ: nến thứ 13-17 hoặc 21",
        "score": f"• Tổng điểm: **{score_points}/6 Điểm**\n• Chi tiết: {', '.join(reasons[:3])}\n• Kết luận: {'Đủ điều kiện canh điểm vào' if score_points >= 4 else 'Theo dõi, chưa đủ tín hiệu'}",
        "scenario": f"• Kịch bản đánh lên: Canh giải ngân vùng {entry_zone}\n• Chốt lời: TP1={tp1:,.1f}, TP2={tp2:,.1f}\n• Cắt lỗ: Thủng {invalidation_point:,.1f}",
        "raw": {
            "df": df,
            "supports": supports,
            "resistances": resistances,
            "fibo_levels": {
                "0.382": fibo_382, "0.500": fibo_500, "0.618": fibo_618,
                "1.272": fibo_ext_1272, "1.618": fibo_ext_1618
            },
            "invalidation_point": invalidation_point,
            "recent_high": recent_high,
            "recent_low": recent_low,
            "entry_zone": entry_zone,
            "tp1": tp1,
            "tp2": tp2
        }
    }


def analyze_multiframe(symbol: str, data_dir: str = "sample-data/stock"):
    symbol = symbol.upper()
    stock_dir = os.path.join(data_dir, symbol)

    if "BTC" in symbol:
        timeframes = ["W", "D", "4H", "1H"]
        asset_type = "CRYPTO"
    else:
        timeframes = ["M", "W", "D", "1H"]
        asset_type = "VN"

    results = {}
    for tf in timeframes:
        fpath = os.path.join(stock_dir, f"ohlcv_{tf}.json")
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            results[tf] = analyze_single_timeframe(df, tf, asset_type)
        else:
            results[tf] = None

    return results


if __name__ == "__main__":
    res_btc = analyze_multiframe("BTCUSD")
    print("BTCUSD Daily Trend:", res_btc["D"]["trend"] if res_btc.get("D") else "N/A")
    res_fpt = analyze_multiframe("FPT")
    print("FPT Daily Trend:", res_fpt["D"]["trend"] if res_fpt.get("D") else "N/A")

