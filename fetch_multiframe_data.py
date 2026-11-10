"""
Fetch Multi-Timeframe OHLCV Data for:
- Vietnam Stock (FPT): M, W, D, 1H
- Global / Crypto (BTCUSD): W, D, 4H, 1H
"""

import os
import sys
import json
import time
import urllib.request
import pandas as pd
from datetime import datetime

try:
    from vnstock import Market
    VNSTOCK_AVAILABLE = True
except Exception:
    VNSTOCK_AVAILABLE = False


def fetch_binance_klines(symbol="BTCUSDT", interval="1d", limit=150):
    """Lấy dữ liệu nến từ Binance public API"""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        rows = []
        for item in data:
            # [open_time, open, high, low, close, volume, close_time, ...]
            dt = datetime.fromtimestamp(item[0] / 1000).strftime('%Y-%m-%d %H:%M')
            rows.append({
                "time": dt,
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5])
            })
        return rows
    except Exception as e:
        print(f"Error fetching Binance {symbol} {interval}: {e}")
        return []


def fetch_vndirect_dchart(symbol="FPT", resolution="D", limit=150):
    """Lấy dữ liệu nến từ VNDirect Dchart API"""
    # resolution: D, W, M, 60
    to_time = int(time.time())
    # 150 nến ngược về trước
    if resolution == "M":
        from_time = to_time - 150 * 30 * 86400
    elif resolution == "W":
        from_time = to_time - 150 * 7 * 86400
    elif resolution == "D":
        from_time = to_time - 250 * 86400
    elif resolution == "60":
        from_time = to_time - 90 * 86400
    else:
        from_time = to_time - 150 * 86400

    url = f"https://dchart-api.vndirect.com.vn/dchart/history?resolution={resolution}&symbol={symbol}&from={from_time}&to={to_time}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        if data.get('s') != 'ok':
            return []
        rows = []
        times = data.get('t', [])
        opens = data.get('o', [])
        highs = data.get('h', [])
        lows = data.get('l', [])
        closes = data.get('c', [])
        volumes = data.get('v', [])
        for i in range(len(times)):
            dt = datetime.fromtimestamp(times[i]).strftime('%Y-%m-%d %H:%M')
            rows.append({
                "time": dt,
                "open": float(opens[i]),
                "high": float(highs[i]),
                "low": float(lows[i]),
                "close": float(closes[i]),
                "volume": float(volumes[i])
            })
        return rows[-limit:]
    except Exception as e:
        print(f"Error fetching VNDirect {symbol} {resolution}: {e}")
        return []


def fetch_all_timeframes(symbol: str, out_dir: str = "sample-data/stock"):
    symbol = symbol.upper()
    target_dir = os.path.join(out_dir, symbol)
    os.makedirs(target_dir, exist_ok=True)
    tf_data = {}

    if "BTC" in symbol:
        # Asset Crypto / Global
        print(f"[*] Thu thập dữ liệu đa khung cho {symbol} (W, D, 4H, 1H)...")
        tf_data["W"] = fetch_binance_klines("BTCUSDT", "1w", limit=100)
        tf_data["D"] = fetch_binance_klines("BTCUSDT", "1d", limit=120)
        tf_data["4H"] = fetch_binance_klines("BTCUSDT", "4h", limit=100)
        tf_data["1H"] = fetch_binance_klines("BTCUSDT", "1h", limit=100)
    else:
        # Asset Vietnam Equity (M, W, D, 1H)
        print(f"[*] Thu thập dữ liệu đa khung chuẩn Việt Nam cho {symbol} (M, W, D, 1H)...")
        # 1. Khung 1H trực tiếp từ VNDirect
        tf_data["1H"] = fetch_vndirect_dchart(symbol, "60", limit=120)

        # 2. Khung D (lấy 500 phiên để resample chuẩn W và M)
        daily_candles = fetch_vndirect_dchart(symbol, "D", limit=500)
        if not daily_candles and VNSTOCK_AVAILABLE:
            try:
                df_vns = Market().equity(symbol).ohlcv()
                if not df_vns.empty:
                    df_vns['time'] = df_vns['time'].astype(str)
                    daily_candles = df_vns.tail(500).to_dict(orient="records")
            except Exception:
                pass

        tf_data["D"] = daily_candles[-120:] if daily_candles else []

        # 3. Resample sang W và M từ Daily candles
        if daily_candles:
            df_d = pd.DataFrame(daily_candles)
            df_d['time'] = pd.to_datetime(df_d['time'])
            df_d.set_index('time', inplace=True)
            df_w = df_d.resample('W').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna().reset_index()
            df_m = df_d.resample('ME').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna().reset_index()

            df_w['time'] = df_w['time'].dt.strftime('%Y-%m-%d')
            df_m['time'] = df_m['time'].dt.strftime('%Y-%m')

            tf_data["W"] = df_w.tail(80).to_dict(orient="records")
            tf_data["M"] = df_m.tail(36).to_dict(orient="records")
        else:
            tf_data["W"] = []
            tf_data["M"] = []

    for tf, candles in tf_data.items():
        tf_path = os.path.join(target_dir, f"ohlcv_{tf}.json")
        with open(tf_path, "w", encoding="utf-8") as f:
            json.dump(candles, f, ensure_ascii=False, indent=2)
        print(f"  [+] {symbol} [{tf}]: {len(candles)} nến -> {tf_path}")

    return tf_data


if __name__ == "__main__":
    fetch_all_timeframes("BTCUSD")
    fetch_all_timeframes("FPT")
