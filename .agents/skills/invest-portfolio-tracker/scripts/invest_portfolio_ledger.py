"""
Invest Portfolio Tracker & SQLite Ledger Engine
- CSDL cục bộ: knowledge-base/investment.db
- Bảng: portfolio, trade_history, risk_metrics
- Ghi nhận lịch sử lệnh được duyệt từ Human Checkpoint Gate
- Kiểm soát rủi ro: Giới hạn 25% NAV/mã, Max Drawdown < 7%, Tiền mặt tối thiểu 15%
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta

DB_DIR = "knowledge-base"
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "investment.db")


def init_database():
    """Khởi tạo cấu trúc 3 bảng dữ liệu cho Portfolio Ledger"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Bảng portfolio (Danh mục hiện hành)
    c.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        symbol TEXT PRIMARY KEY,
        name TEXT,
        market TEXT,
        quantity REAL,
        avg_price REAL,
        current_price REAL,
        market_value REAL,
        unrealized_pnl REAL,
        unrealized_pnl_pct REAL,
        weight_pct REAL,
        stop_loss REAL,
        take_profit REAL,
        updated_at TEXT
    );
    """)

    # 2. Bảng trade_history (Nhật ký giao dịch đã phê duyệt)
    c.execute("""
    CREATE TABLE IF NOT EXISTS trade_history (
        trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        action TEXT,
        quantity REAL,
        price REAL,
        fee REAL,
        total_amount REAL,
        realized_pnl REAL,
        trade_date TEXT,
        signal_id TEXT,
        approved_by TEXT,
        note TEXT
    );
    """)

    # 3. Bảng risk_metrics (Theo dõi NAV & Giới hạn rủi ro)
    c.execute("""
    CREATE TABLE IF NOT EXISTS risk_metrics (
        log_date TEXT PRIMARY KEY,
        total_nav REAL,
        cash_balance REAL,
        stock_value REAL,
        cash_weight_pct REAL,
        peak_nav REAL,
        drawdown_pct REAL,
        risk_status TEXT,
        notes TEXT
    );
    """)

    conn.commit()
    conn.close()
    print(f"[+] Initialized SQLite Database at: {DB_PATH}")


def seed_demo_portfolio():
    """Khởi tạo danh mục thực tế mẫu (Vốn 1.0 tỷ VND) với các lệnh duyệt từ Phase 2/3"""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Reset data
    c.execute("DELETE FROM portfolio;")
    c.execute("DELETE FROM trade_history;")
    c.execute("DELETE FROM risk_metrics;")

    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Lệnh duyệt Mua FPT (3,000 CP @ 50.80)
    c.execute("""
    INSERT INTO trade_history (symbol, action, quantity, price, fee, total_amount, realized_pnl, trade_date, signal_id, approved_by, note)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("FPT", "BUY", 3000, 50.80, 228.6, 152628.6, 0.0, today_str, "SIG-202611-FPT-01", "HUMAN_CHECKPOINT", "Phê duyệt bắt đáy Sóng C hoàn tất quanh 50k"))

    # 2. Lệnh duyệt Mua SIP (2,400 CP @ 61.30)
    c.execute("""
    INSERT INTO trade_history (symbol, action, quantity, price, fee, total_amount, realized_pnl, trade_date, signal_id, approved_by, note)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("SIP", "BUY", 2400, 61.30, 220.68, 147340.68, 0.0, today_str, "SIG-202611-SIP-02", "HUMAN_CHECKPOINT", "Phê duyệt mua Sóng 3 mở rộng, biên an toàn DCF 32.6%"))

    # 3. Cập nhật Bảng portfolio
    # Giả định giá thị trường hiện tại: FPT = 51.5k, SIP = 62.0k
    holdings = [
        ("FPT", "Công ty Cổ phần FPT", "VN_EQUITY", 3000, 50.80, 51.50, 48.50, 68.00),
        ("SIP", "CTCP Đầu tư Sài Gòn VRG", "VN_EQUITY", 2400, 61.30, 62.00, 56.50, 78.00)
    ]

    total_stock_val = 0
    for sym, name, mkt, qty, avg_p, cur_p, sl, tp in holdings:
        mkt_val = qty * cur_p * 1000 # đổi sang đồng
        cost_val = qty * avg_p * 1000
        unrealized = mkt_val - cost_val
        unrealized_pct = (unrealized / cost_val) * 100
        total_stock_val += mkt_val

        c.execute("""
        INSERT INTO portfolio (symbol, name, market, quantity, avg_price, current_price, market_value, unrealized_pnl, unrealized_pnl_pct, weight_pct, stop_loss, take_profit, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sym, name, mkt, qty, avg_p, cur_p, mkt_val, unrealized, round(unrealized_pct, 2), 0.0, sl, tp, today_str))

    # Tổng NAV = Tiền mặt + Giá trị cổ phiếu
    INITIAL_CASH = 1000000000.0 # 1 Tỷ VND
    spent_cash = (3000 * 50.80 * 1000 + 228.6 * 1000) + (2400 * 61.30 * 1000 + 220.68 * 1000) # ~ 300 triệu
    rem_cash = INITIAL_CASH - spent_cash
    total_nav = rem_cash + total_stock_val

    # Cập nhật weight_pct cho từng mã
    c.execute("UPDATE portfolio SET weight_pct = ROUND((market_value / ?) * 100, 2)", (total_nav,))

    # 4. Ghi nhận Bảng risk_metrics
    cash_weight = (rem_cash / total_nav) * 100
    c.execute("""
    INSERT INTO risk_metrics (log_date, total_nav, cash_balance, stock_value, cash_weight_pct, peak_nav, drawdown_pct, risk_status, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (today_str[:10], total_nav, rem_cash, total_stock_val, round(cash_weight, 2), total_nav, 0.0, "AN TOÀN (ALL GREEN)", "Danh mục giải ngân đợt 1 đạt chuẩn Fsen, tỷ trọng tiền mặt 69.7% dồi dào"))

    conn.commit()
    conn.close()
    print("[+] Seeded Demo Portfolio into SQLite successfully!")


def get_portfolio_summary():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM portfolio")
    items = [dict(row) for row in c.fetchall()]

    c.execute("SELECT * FROM risk_metrics ORDER BY log_date DESC LIMIT 1")
    risk_row = c.fetchone()
    risk = dict(risk_row) if risk_row else {}

    c.execute("SELECT * FROM trade_history ORDER BY trade_id DESC")
    trades = [dict(row) for row in c.fetchall()]

    conn.close()
    return items, risk, trades


if __name__ == "__main__":
    seed_demo_portfolio()
    items, risk, trades = get_portfolio_summary()
    print(f"\n=== SỔ CÁI DANH MỤC ĐẦU TƯ (NAV: {risk.get('total_nav', 0):,.0f} VND) ===")
    print(f"Tiền mặt: {risk.get('cash_balance', 0):,.0f} VND ({risk.get('cash_weight_pct', 0)}%) | Cổ phiếu: {risk.get('stock_value', 0):,.0f} VND")
    print(f"Trạng thái kiểm soát rủi ro: {risk.get('risk_status')}")
    print("\n--- Danh Mục Đang Nắm Giữ ---")
    for it in items:
        print(f"• {it['symbol']:<5} | SL: {it['quantity']:>5,.0f} | Giá vốn: {it['avg_price']:>6.2f}k | Giá TT: {it['current_price']:>6.2f}k | Lãi chưa chốt: +{it['unrealized_pnl']:>10,.0f} VND (+{it['unrealized_pnl_pct']}%) | Tỷ trọng: {it['weight_pct']}% NAV")

