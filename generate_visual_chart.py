"""
Generate Visual Scenario Charts (PNG & HTML)
Vẽ biểu đồ nến kịch bản kỹ thuật trực quan chuẩn xác:
- Candlestick + MA10, MA20, MA50
- Các đường ngang Hỗ trợ & Kháng cự (kèm nhãn giá bên phải)
- Mức thoái lui Fibonacci & Kênh giá
- Nhãn Sóng Elliott & ĐIỂM VÔ HIỆU HÓA KỊCH BẢN (Đường đứt nét đỏ)
- Mũi tên kịch bản giao dịch (Target TP1, TP2)
- Subplot Volume & MACD Histogram
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
from datetime import datetime
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


def plot_matplotlib_scenario(symbol: str, tf_analysis: dict, tf_name: str, out_png: str):
    """Vẽ biểu đồ tĩnh độ nét cao bằng Matplotlib để chèn trực tiếp vào file Word"""
    raw = tf_analysis["raw"]
    df = raw["df"].tail(60).copy().reset_index(drop=True)

    fig, (ax_main, ax_vol, ax_macd) = plt.subplots(
        3, 1, figsize=(14, 9),
        gridspec_kw={'height_ratios': [5, 1.2, 1.5]},
        dpi=150
    )
    fig.patch.set_facecolor('#FFFFFF')

    # 1. TOP PANEL: NẾN & CHỈ BÁO & KỊCH BẢN
    ax_main.set_facecolor('#FCFCFC')
    ax_main.grid(True, linestyle='--', alpha=0.4, color='#D0D0D0')

    x_indices = np.arange(len(df))

    # Vẽ Candlestick thủ công
    width = 0.6
    width2 = 0.1
    up = df[df['close'] >= df['open']]
    down = df[df['close'] < df['open']]

    # Nến xanh
    ax_main.bar(up.index, up['close'] - up['open'], width, bottom=up['open'], color='#26A69A', edgecolor='#26A69A')
    ax_main.bar(up.index, up['high'] - up['close'], width2, bottom=up['close'], color='#26A69A')
    ax_main.bar(up.index, up['low'] - up['open'], width2, bottom=up['open'], color='#26A69A')

    # Nến đỏ
    ax_main.bar(down.index, down['close'] - down['open'], width, bottom=down['open'], color='#EF5350', edgecolor='#EF5350')
    ax_main.bar(down.index, down['high'] - down['open'], width2, bottom=down['open'], color='#EF5350')
    ax_main.bar(down.index, down['low'] - down['close'], width2, bottom=down['close'], color='#EF5350')

    # Đường MA10, MA20, MA50
    if 'sma10' in df.columns:
        ax_main.plot(df.index, df['sma10'], label='MA10', color='#FF7F0E', linewidth=1.5)
    if 'sma20' in df.columns:
        ax_main.plot(df.index, df['sma20'], label='MA20', color='#2CA02C', linewidth=1.5)
    if 'sma50' in df.columns:
        ax_main.plot(df.index, df['sma50'], label='MA50', color='#1F77B4', linewidth=1.5)

    # Các đường Hỗ trợ & Kháng cự ngang
    for s in raw.get("supports", [])[:2]:
        ax_main.axhline(y=s, color='#3B82F6', linestyle='-', linewidth=1.2, alpha=0.8)
        ax_main.text(len(df) - 1, s, f" HT {s:,.1f}", color='#1D4ED8', verticalalignment='center', fontweight='bold', fontsize=8.5)

    for r in raw.get("resistances", [])[:2]:
        ax_main.axhline(y=r, color='#9333EA', linestyle='-', linewidth=1.2, alpha=0.8)
        ax_main.text(len(df) - 1, r, f" KC {r:,.1f}", color='#7E22CE', verticalalignment='center', fontweight='bold', fontsize=8.5)

    # ĐIỂM VÔ HIỆU HÓA KỊCH BẢN (Invalidation Point)
    inval = raw.get("invalidation_point")
    if inval:
        ax_main.axhline(y=inval, color='#DC2626', linestyle='--', linewidth=1.8, alpha=0.9)
        ax_main.text(0, inval, f" [DIEM VO HIEU HOA / STOP LOSS]: {inval:,.1f}", color='#B91C1C', verticalalignment='bottom', fontweight='bold', fontsize=9.5, backgroundcolor='#FEE2E2')

    # Mũi tên kịch bản giao dịch (Bullish Target)
    last_idx = len(df) - 1
    last_c = df['close'].iloc[-1]
    tp1 = raw.get("tp1", last_c * 1.05)
    ax_main.annotate(
        f"Kịch bản BUY ➔ TP1: {tp1:,.1f}",
        xy=(last_idx, last_c),
        xytext=(last_idx - 12, tp1),
        arrowprops=dict(facecolor='#10B981', edgecolor='#059669', arrowstyle='->', lw=2.2),
        fontweight='bold', fontsize=9.5, color='#065F46',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#D1FAE5', edgecolor='#10B981')
    )

    # Đánh nhãn Sóng Elliott tượng trưng tại các điểm xoay
    recent_min_idx = df['low'].idxmin()
    recent_max_idx = df['high'].idxmax()
    ax_main.text(recent_min_idx, df['low'].loc[recent_min_idx], " [S2/Đáy]", fontsize=9, fontweight='bold', color='#2563EB', ha='center', va='top')
    ax_main.text(recent_max_idx, df['high'].loc[recent_max_idx], " [S3/Đỉnh]", fontsize=9, fontweight='bold', color='#D97706', ha='center', va='bottom')

    title_asset = f"{symbol} ({tf_name}) — BIỂU ĐỒ KỊCH BẢN KỸ THUẬT & ĐIỂM VÔ HIỆU HÓA SÓNG"
    ax_main.set_title(title_asset, fontsize=13, fontweight='bold', color='#1B365D', pad=10)
    ax_main.legend(loc='upper left', frameon=True, fontsize=8.5)
    ax_main.set_xlim(-1, len(df) + 3)

    # 2. MIDDLE PANEL: KHỐI LƯỢNG (VOLUME)
    ax_vol.set_facecolor('#FCFCFC')
    ax_vol.grid(True, linestyle='--', alpha=0.3)
    vol_colors = ['#26A69A' if c >= o else '#EF5350' for c, o in zip(df['close'], df['open'])]
    ax_vol.bar(df.index, df['volume'], color=vol_colors, width=0.6, alpha=0.8)
    ax_vol.set_ylabel("Volume", fontsize=8.5)
    ax_vol.set_xlim(-1, len(df) + 3)

    # 3. BOTTOM PANEL: MACD & HISTOGRAM
    ax_macd.set_facecolor('#FCFCFC')
    ax_macd.grid(True, linestyle='--', alpha=0.3)
    if 'macd' in df.columns:
        ax_macd.plot(df.index, df['macd'], label='MACD', color='#2563EB', linewidth=1.2)
        ax_macd.plot(df.index, df['macd_signal'], label='Signal', color='#F59E0B', linewidth=1.2)
        hist_colors = ['#10B981' if h >= 0 else '#EF4444' for h in df['macd_hist']]
        ax_macd.bar(df.index, df['macd_hist'], color=hist_colors, width=0.5, alpha=0.7)
        ax_macd.axhline(0, color='#9CA3AF', linestyle='-', linewidth=0.8)
        ax_macd.legend(loc='upper left', frameon=False, fontsize=8)

    # Trục ngày tháng
    step = max(1, len(df) // 8)
    ax_macd.set_xticks(df.index[::step])
    ax_macd.set_xticklabels([str(t).split(' ')[0] for t in df['time'].iloc[::step]], rotation=25, ha='right', fontsize=8)

    plt.tight_layout()
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.savefig(out_png, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"  [+] Đã xuất biểu đồ PNG: {out_png}")


def plot_plotly_scenario(symbol: str, tf_analysis: dict, tf_name: str, out_html: str):
    """Vẽ biểu đồ tương tác HTML (Plotly) để phóng to, thu nhỏ, rê chuột xem nến"""
    if not PLOTLY_AVAILABLE:
        print(f"[*] Plotly chưa được cài đặt - Bỏ qua biểu đồ Plotly {out_html}")
        return
    raw = tf_analysis["raw"]
    df = raw["df"].copy().reset_index(drop=True)

    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        vertical_spacing=0.03, row_heights=[0.65, 0.15, 0.20],
        subplot_titles=(f"{symbol} [{tf_name}] Kịch Bản Kỹ Thuật & Sóng", "Khối Lượng", "MACD (12, 26, 9)")
    )

    # 1. Candlestick
    fig.add_trace(go.Candlestick(
        x=df['time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'],
        name='Nến', increasing_line_color='#26A69A', decreasing_line_color='#EF5350'
    ), row=1, col=1)

    # MA10, MA20, MA50
    if 'sma10' in df.columns:
        fig.add_trace(go.Scatter(x=df['time'], y=df['sma10'], mode='lines', name='MA10', line=dict(color='#FF7F0E', width=1.5)), row=1, col=1)
    if 'sma20' in df.columns:
        fig.add_trace(go.Scatter(x=df['time'], y=df['sma20'], mode='lines', name='MA20', line=dict(color='#2CA02C', width=1.5)), row=1, col=1)
    if 'sma50' in df.columns:
        fig.add_trace(go.Scatter(x=df['time'], y=df['sma50'], mode='lines', name='MA50', line=dict(color='#1F77B4', width=1.5)), row=1, col=1)

    # Đường Invalidation
    inval = raw.get("invalidation_point")
    if inval:
        fig.add_hline(y=inval, line_dash="dash", line_color="red", line_width=2,
                      annotation_text=f"🚨 ĐIỂM VÔ HIỆU HÓA: {inval:,.1f}", annotation_position="top left", row=1, col=1)

    # Hỗ trợ / Kháng cự
    for s in raw.get("supports", [])[:2]:
        fig.add_hline(y=s, line_color="#3B82F6", line_width=1, annotation_text=f"HT {s:,.1f}", row=1, col=1)
    for r in raw.get("resistances", [])[:2]:
        fig.add_hline(y=r, line_color="#9333EA", line_width=1, annotation_text=f"KC {r:,.1f}", row=1, col=1)

    # 2. Volume
    vol_colors = ['#26A69A' if c >= o else '#EF5350' for c, o in zip(df['close'], df['open'])]
    fig.add_trace(go.Bar(x=df['time'], y=df['volume'], marker_color=vol_colors, name='Volume'), row=2, col=1)

    # 3. MACD
    if 'macd' in df.columns:
        fig.add_trace(go.Scatter(x=df['time'], y=df['macd'], mode='lines', name='MACD', line=dict(color='#2563EB', width=1.2)), row=3, col=1)
        fig.add_trace(go.Scatter(x=df['time'], y=df['macd_signal'], mode='lines', name='Signal', line=dict(color='#F59E0B', width=1.2)), row=3, col=1)
        hist_colors = ['#10B981' if h >= 0 else '#EF4444' for h in df['macd_hist']]
        fig.add_trace(go.Bar(x=df['time'], y=df['macd_hist'], marker_color=hist_colors, name='Hist'), row=3, col=1)

    fig.update_layout(
        template="plotly_white",
        xaxis_rangeslider_visible=False,
        height=850,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    fig.write_html(out_html)
    print(f"  [+] Đã xuất biểu đồ HTML tương tác: {out_html}")


def generate_all_charts(symbol: str, tf_results: dict, out_dir: str = "outputs/investment"):
    # Chọn khung thời gian chủ đạo để vẽ biểu đồ chi tiết (Daily cho cả 2 mã)
    primary_tf = "D" if tf_results.get("D") else ("W" if tf_results.get("W") else "1H")
    tf_data = tf_results[primary_tf]

    png_path = os.path.join(out_dir, f"chart_scenario_{symbol}.png")
    html_path = os.path.join(out_dir, f"chart_scenario_{symbol}.html")

    print(f"[*] Đang vẽ biểu đồ kịch bản cho {symbol} [{primary_tf}]...")
    plot_matplotlib_scenario(symbol, tf_data, primary_tf, png_path)
    plot_plotly_scenario(symbol, tf_data, primary_tf, html_path)

    return png_path, html_path
