"""
Invest Data Fetcher — Trạm thu thập & chuẩn hóa dữ liệu tài chính chứng khoán VN
Kết hợp vnstock 5.x + TradingView Screener + Bộ nhớ đệm cục bộ
"""

import os
import sys
import json
import argparse
from datetime import datetime
import pandas as pd

try:
    from vnstock import Market, Reference
    VNSTOCK_AVAILABLE = True
except Exception:
    VNSTOCK_AVAILABLE = False

try:
    from tradingview_screener import Query, col
    TV_AVAILABLE = True
except Exception:
    TV_AVAILABLE = False


def fetch_profile_and_ratios(symbol: str) -> dict:
    """Lấy thông tin cơ bản và chỉ số tài chính của doanh nghiệp"""
    symbol = symbol.upper()
    data = {
        "symbol": symbol,
        "fetch_time": datetime.now().isoformat(),
        "name": "",
        "industry": "",
        "listing_date": "",
        "shares_outstanding": 0,
        "market_cap": 0,
        "current_price": 0,
        "pe": None,
        "pb": None,
        "roe": None,
        "roa": None,
        "gross_margin": None,
        "operating_margin": None,
        "net_margin": None,
        "debt_to_equity": None,
        "current_ratio": None,
        "free_cash_flow": None,
        "total_assets": None,
        "total_debt": None,
        "total_liabilities": None,
        "net_income": None
    }

    # 1. Thử lấy từ vnstock Reference
    if VNSTOCK_AVAILABLE:
        try:
            ref_info = Reference().company(symbol).info()
            if not ref_info.empty:
                r = ref_info.iloc[0]
                data["name"] = str(r.get("name", ""))
                data["industry"] = str(r.get("industry", ""))
                data["listing_date"] = str(r.get("listing_date", ""))
                issued = r.get("issued_share")
                if pd.notna(issued):
                    data["shares_outstanding"] = float(issued)
        except Exception as e:
            pass

    # 2. Thử lấy chỉ số từ TradingView Screener (Vietnam market)
    if TV_AVAILABLE:
        try:
            fields = [
                'name', 'description', 'close', 'total_shares_outstanding',
                'market_cap_basic', 'price_earnings_ttm', 'price_book_ratio',
                'return_on_equity', 'return_on_assets', 'gross_margin',
                'operating_margin', 'net_margin', 'debt_to_equity',
                'current_ratio', 'free_cash_flow', 'total_assets',
                'total_debt', 'total_liabilities_fy', 'net_income'
            ]
            q = Query().set_markets('vietnam').select(*fields).where(col('name') == symbol)
            total, df = q.get_scanner_data()
            if not df.empty:
                row = df.iloc[0]
                if not data["name"]:
                    data["name"] = str(row.get("description", ""))
                price = row.get("close")
                if pd.notna(price):
                    data["current_price"] = float(price)
                shares = row.get("total_shares_outstanding")
                if pd.notna(shares) and data["shares_outstanding"] == 0:
                    data["shares_outstanding"] = float(shares)
                mcap = row.get("market_cap_basic")
                if pd.notna(mcap):
                    data["market_cap"] = float(mcap)

                # Các chỉ số tài chính
                for k_tv, k_data in [
                    ('price_earnings_ttm', 'pe'),
                    ('price_book_ratio', 'pb'),
                    ('return_on_equity', 'roe'),
                    ('return_on_assets', 'roa'),
                    ('gross_margin', 'gross_margin'),
                    ('operating_margin', 'operating_margin'),
                    ('net_margin', 'net_margin'),
                    ('debt_to_equity', 'debt_to_equity'),
                    ('current_ratio', 'current_ratio'),
                    ('free_cash_flow', 'free_cash_flow'),
                    ('total_assets', 'total_assets'),
                    ('total_debt', 'total_debt'),
                    ('total_liabilities_fy', 'total_liabilities'),
                    ('net_income', 'net_income')
                ]:
                    val = row.get(k_tv)
                    if pd.notna(val):
                        data[k_data] = float(val)
        except Exception as e:
            pass

    return data


def fetch_ohlcv_data(symbol: str, count: int = 200) -> list:
    """Lấy dữ liệu nến OHLCV từ vnstock"""
    symbol = symbol.upper()
    if VNSTOCK_AVAILABLE:
        try:
            df = Market().equity(symbol).ohlcv()
            if not df.empty:
                df = df.tail(count)
                # Chuyển đổi định dạng chuẩn
                df['time'] = df['time'].astype(str)
                return df.to_dict(orient="records")
        except Exception as e:
            pass
    return []


def main():
    parser = argparse.ArgumentParser(description="Fetch stock data for VN stocks")
    parser.add_argument("--symbol", type=str, required=True, help="Stock symbol (e.g. SIP, FPT)")
    parser.add_argument("--outdir", type=str, default="sample-data/stock", help="Output directory")
    args = parser.parse_args()

    symbol = args.symbol.upper()
    target_dir = os.path.join(args.outdir, symbol)
    os.makedirs(target_dir, exist_ok=True)

    print(f"[*] Đang thu thập dữ liệu mã: {symbol}...")
    profile = fetch_profile_and_ratios(symbol)
    profile_path = os.path.join(target_dir, "profile.json")
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"  [+] Đã lưu thông tin cơ bản: {profile_path}")

    ohlcv = fetch_ohlcv_data(symbol)
    ohlcv_path = os.path.join(target_dir, "ohlcv_daily.json")
    with open(ohlcv_path, "w", encoding="utf-8") as f:
        json.dump(ohlcv, f, ensure_ascii=False, indent=2)
    print(f"  [+] Đã lưu dữ liệu nến ngày ({len(ohlcv)} phiên): {ohlcv_path}")

    print(f"[OK] Hoàn tất thu thập dữ liệu cho {symbol}!")


if __name__ == "__main__":
    main()

