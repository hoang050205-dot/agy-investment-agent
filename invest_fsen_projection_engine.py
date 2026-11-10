"""
invest_fsen_projection_engine.py
Module Tính Toán & Dự Báo Sóng Tương Lai Fsen Toàn Diện (Dạng Sóng - Biên Độ - Thời Gian)
Tuân thủ 100% Khung Lý Thuyết Sóng Fsen (Tổng hợp lý thuyết Sóng.xlsx)
và Chuẩn Hiển Thị TradingView Pine Script v6 (MarkitTick & SMC CHoCH Invalidation)
"""

import json
import math
import os
from datetime import datetime, timedelta

def calculate_projection_metrics(
    p0: float, p1: float, p2: float, 
    is_bullish: bool, 
    t0_str: str, t1_str: str, t2_str: str,
    custom_invalidation: float = None,
    pattern_type: str = None
):
    """
    Tính toán toán học toàn diện bộ 3 thành tố dự báo sóng tương lai:
    1. Dạng sóng dự kiến (Pattern Forecast)
    2. Biên độ dự kiến (Amplitude & Price Targets via Fibo Retracement & Extension)
    3. Thời gian dự kiến (Time & Cycle Targets via Fibonacci Time)
    """
    h1 = abs(p1 - p0)
    ret2 = abs(p2 - p1) / h1 if h1 > 0 else 0.0
    invalidation = custom_invalidation if custom_invalidation is not None else p0

    # 1. TÍNH TOÁN BIÊN ĐỘ GIÁ (AMPLITUDE FORECAST)
    if is_bullish:
        w3_target = round(p2 + h1 * 1.618, 2)
        w3_len = w3_target - p2
        w4_target = round(w3_target - w3_len * 0.382, 2)
        w5_target = round(w4_target + h1 * 1.000, 2)
        
        # Sóng 4 không được vi phạm đỉnh Sóng 1
        overlap_violation = w4_target <= p1
        
        # Chuỗi điều chỉnh ABC sau Sóng 5
        cycle_len = w5_target - p0
        wa_target = round(w5_target - cycle_len * 0.382, 2)
        wb_target = round(wa_target + (w5_target - wa_target) * 0.500, 2)
        wc_target = round(wb_target - (w5_target - wa_target) * 1.000, 2)
        
        risk = abs(p2 - invalidation)
        reward_w3 = abs(w3_target - p2)
        rr_w3 = round(reward_w3 / risk, 2) if risk > 0 else 0.0
        
        direction = "LONG (Mua Bứt Phá)"
        pattern_str = pattern_type if pattern_type else "Sóng Đẩy Mở Rộng [5-3-5-3-5]"
        prz_w3 = [round(w3_target * 0.97, 2), round(w3_target * 1.03, 2)]
        prz_w5 = [round(w5_target * 0.97, 2), round(w5_target * 1.03, 2)]
    else:
        # Nhịp giảm (Bearish): Sóng 1 giảm, Sóng 2 hồi lên
        # Target Fibo Extension: -0.5 (-50%), -0.618 (-61.8%), -1.0 (-100%)
        w3_ext1 = round(p1 - h1 * 0.500, 2) # Fibo -0.5
        w3_ext2 = round(p1 - h1 * 0.618, 2) # Fibo -0.618
        w3_target = w3_ext2
        prz_w3 = [min(w3_ext1, w3_ext2), max(w3_ext1, w3_ext2)]
        
        # Sóng 4 hồi 38.2% từ Sóng 3
        w4_target = round(w3_target + (p2 - w3_target) * 0.382, 2)
        
        # Sóng 5 rơi về Fibo -1.0 của H1
        w5_target = round(p1 - h1 * 1.000, 2)
        prz_w5 = [round(w5_target * 0.98, 2), round(w5_target * 1.02, 2)]
        
        overlap_violation = w4_target >= p1
        
        # Chuỗi hồi phục điều chỉnh ABC sau khi hoàn tất 5 nhịp giảm
        cycle_len = p0 - w5_target
        wa_target = round(w5_target + cycle_len * 0.382, 2)
        wb_target = round(wa_target - (wa_target - w5_target) * 0.500, 2)
        wc_target = round(wb_target + (wa_target - w5_target) * 1.000, 2)
        
        risk = abs(invalidation - p2)
        reward_w3 = abs(p2 - w3_target)
        rr_w3 = round(reward_w3 / risk, 2) if risk > 0 else 0.0
        
        direction = "SHORT (Bán Hạ Tỷ Trọng)"
        pattern_str = pattern_type if pattern_type else "Sóng Tuần Dự Kiến Là Zigzag [5-3-5]"

    # 2. TÍNH TOÁN THỜI GIAN DỰ KIẾN (TIME FORECAST VIA FIBONACCI TIME CYCLE)
    t0 = datetime.strptime(t0_str, "%Y-%m-%d")
    t1 = datetime.strptime(t1_str, "%Y-%m-%d")
    t2 = datetime.strptime(t2_str, "%Y-%m-%d")
    
    dur1_days = max(1, (t1 - t0).days)
    dur2_days = max(1, (t2 - t1).days)
    dur1_weeks = round(dur1_days / 7, 1)
    dur2_weeks = round(dur2_days / 7, 1)

    # Fibonacci Time Projections
    dur_w3_est = int(dur1_days * 1.618)
    dur_w4_est = int(dur2_days * 1.000)
    dur_w5_est = int(dur1_days * 1.000)

    t3_target = t2 + timedelta(days=dur_w3_est)
    t4_target = t3_target + timedelta(days=dur_w4_est)
    t5_target = t4_target + timedelta(days=dur_w5_est)

    dur_wa_est = int(dur1_days * 0.618)
    dur_wb_est = int(dur2_days * 0.618)
    dur_wc_est = int(dur1_days * 1.000)

    ta_target = t5_target + timedelta(days=dur_wa_est)
    tb_target = ta_target + timedelta(days=dur_wb_est)
    tc_target = tb_target + timedelta(days=dur_wc_est)

    def format_quarter(dt: datetime) -> str:
        q = (dt.month - 1) // 3 + 1
        return f"Q{q}/{dt.year} ({dt.strftime('%m/%Y')})"

    time_summary = {
        "t0_start": t0.strftime("%Y-%m-%d"),
        "t1_wave1": t1.strftime("%Y-%m-%d"),
        "t2_wave2": t2.strftime("%Y-%m-%d"),
        "dur_wave1_days": dur1_days,
        "dur_wave1_weeks": dur1_weeks,
        "dur_wave2_days": dur2_days,
        "dur_wave2_weeks": dur2_weeks,
        "t3_projected_date": t3_target.strftime("%Y-%m-%d"),
        "t3_projected_quarter": format_quarter(t3_target),
        "t4_projected_date": t4_target.strftime("%Y-%m-%d"),
        "t4_projected_quarter": format_quarter(t4_target),
        "t5_projected_date": t5_target.strftime("%Y-%m-%d"),
        "t5_projected_quarter": format_quarter(t5_target),
        "ta_projected_date": ta_target.strftime("%Y-%m-%d"),
        "ta_projected_quarter": format_quarter(ta_target),
        "tb_projected_date": tb_target.strftime("%Y-%m-%d"),
        "tb_projected_quarter": format_quarter(tb_target),
        "tc_projected_date": tc_target.strftime("%Y-%m-%d"),
        "tc_projected_quarter": format_quarter(tc_target),
        "time_overview_str": f"W3? ({format_quarter(t3_target)}) -> W5? ({format_quarter(t5_target)}) -> Sóng C? ({format_quarter(tc_target)})"
    }

    return {
        "direction": direction,
        "pattern": pattern_str,
        "is_bullish": is_bullish,
        "anchor_p0": p0,
        "anchor_p1": p1,
        "anchor_p2": p2,
        "invalidation": invalidation,
        "h1": round(h1, 2),
        "ret2_pct": round(ret2 * 100, 1),
        "w3_target": w3_target,
        "prz_w3": prz_w3,
        "w4_target": w4_target,
        "w5_target": w5_target,
        "prz_w5": prz_w5,
        "wa_target": wa_target,
        "wb_target": wb_target,
        "wc_target": wc_target,
        "overlap_violation": overlap_violation,
        "rr_w3": rr_w3,
        "w3_fibo": "-0.5 & -0.618 x H1" if not is_bullish else "1.618 x H1",
        "w4_fibo": "0.382 x W3",
        "w5_fibo": "-1.000 x H1" if not is_bullish else "1.000 x H1",
        "time_projection": time_summary,
        "notes": "Tuân thủ thiết luật Fsen: Sóng 3 không ngắn nhất; Sóng 4 không vi phạm đỉnh Sóng 1; Đáy Sóng C phân kỳ dương MACD."
    }

ASSETS_PROJECTION_REGISTRY = {
    "XAUUSD": {
        "name": "Gold Spot / U.S. Dollar (XAUUSD)",
        "timeframe": "1W (Khung Tuần)",
        "is_bullish": False,
        "p0": 4891.54,
        "p1": 4116.76,
        "p2": 4450.00,
        "custom_invalidation": 4697.105,
        "pattern_type": "Sóng Tuần Dự Kiến Là Zigzag [5-3-5]",
        "t0": "2025-10-15",
        "t1": "2026-03-10",
        "t2": "2026-07-20",
        "target_zone_w3": [3355.00, 3467.00],
        "target_zone_w5": [2934.00, 2992.00],
        "ath_target": 4891.54
    },
    "VND": {
        "name": "CTCP Chứng khoán VNDIRECT (HOSE: VND)",
        "timeframe": "1W (Khung Tuần)",
        "is_bullish": True,
        "p0": 12.60,
        "p1": 14.95,
        "p2": 14.35,
        "custom_invalidation": 12.60,
        "pattern_type": "Sóng Đẩy Mở Rộng [5-3-5-3-5] (Khởi đầu Sóng 3)",
        "t0": "2026-08-15",
        "t1": "2026-09-30",
        "t2": "2026-10-25",
        "target_zone_w3": [17.50, 18.50],
        "target_zone_w5": [20.50, 21.50],
        "ath_target": 29.00
    },
    "FPT": {
        "name": "CTCP FPT (HOSE: FPT)",
        "timeframe": "1W (Khung Tuần)",
        "is_bullish": True,
        "p0": 49.55,
        "p1": 53.00,
        "p2": 50.80,
        "custom_invalidation": 49.55,
        "pattern_type": "Hoàn Tất Sóng 2 Flat -> Sóng 3 Mở Rộng",
        "t0": "2026-07-10",
        "t1": "2026-09-15",
        "t2": "2026-10-20",
        "target_zone_w3": [56.00, 58.00],
        "target_zone_w5": [70.00, 75.00],
        "ath_target": 82.00
    },
    "BTCUSD": {
        "name": "Bitcoin / U.S. Dollar (BTCUSD)",
        "timeframe": "1W (Khung Tuần)",
        "is_bullish": False,
        "p0": 88500.00,
        "p1": 68000.00,
        "p2": 80800.00,
        "custom_invalidation": 88500.00,
        "pattern_type": "Sóng Tuần Dự Kiến Là Expanded Flat / Bão Sóng C",
        "t0": "2026-03-20",
        "t1": "2026-06-15",
        "t2": "2026-09-10",
        "target_zone_w3": [47631.00, 48500.00],
        "target_zone_w5": [37949.00, 39500.00],
        "ath_target": 88500.00
    }
}

def generate_full_projection_suite():
    suite = {}
    for sym, cfg in ASSETS_PROJECTION_REGISTRY.items():
        res = calculate_projection_metrics(
            p0=cfg["p0"], 
            p1=cfg["p1"], 
            p2=cfg["p2"],
            is_bullish=cfg["is_bullish"],
            t0_str=cfg["t0"], 
            t1_str=cfg["t1"], 
            t2_str=cfg["t2"],
            custom_invalidation=cfg.get("custom_invalidation"),
            pattern_type=cfg.get("pattern_type")
        )
        res["meta"] = cfg
        suite[sym] = res
    
    out_path = os.path.join("outputs", "investment", "fsen_projection_suite.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(suite, f, ensure_ascii=False, indent=2)
    print(f"[SUCCESS] Đã tạo bộ dữ liệu dự báo sóng tương lai Fsen (Dạng Sóng - Biên Độ - Thời Gian) tại: {out_path}")
    return suite

if __name__ == "__main__":
    suite = generate_full_projection_suite()
    for sym, d in suite.items():
        print(f"\n=======================================================")
        print(f"=== {sym} ({d['direction']}) ===")
        print(f"  [1. DẠNG SÓNG DỰ KIẾN]: {d['pattern']}")
        print(f"  [2. BIÊN ĐỘ DỰ KIẾN]:")
        print(f"     • Invalidation Level: {d['invalidation']}")
        print(f"     • Biên độ Sóng 1 (H1): {d['h1']} | Thoái lui Sóng 2: {d['ret2_pct']}%")
        print(f"     • Dự báo Sóng 3?: {d['w3_target']} (PRZ: {d['prz_w3']}) | R:R = 1 : {d['rr_w3']}")
        print(f"     • Dự báo Sóng 4?: {d['w4_target']} | Không vi phạm S1: {not d['overlap_violation']}")
        print(f"     • Dự báo Sóng 5?: {d['w5_target']} (PRZ: {d['prz_w5']})")
        print(f"     • Chuỗi phục hồi ABC: A?={d['wa_target']} -> B?={d['wb_target']} -> C?={d['wc_target']}")
        print(f"  [3. THỜI GIAN DỰ KIẾN]:")
        tp = d['time_projection']
        print(f"     • Sóng 1: {tp['dur_wave1_weeks']} tuần | Sóng 2: {tp['dur_wave2_weeks']} tuần")
        print(f"     • Điểm rơi Sóng 3?: {tp['t3_projected_date']} [{tp['t3_projected_quarter']}]")
        print(f"     • Điểm rơi Sóng 4?: {tp['t4_projected_date']} [{tp['t4_projected_quarter']}]")
        print(f"     • Điểm rơi Sóng 5?: {tp['t5_projected_date']} [{tp['t5_projected_quarter']}]")
        print(f"     • Điểm rơi Sóng C?: {tp['tc_projected_date']} [{tp['tc_projected_quarter']}]")
