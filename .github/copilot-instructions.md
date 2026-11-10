# AGY Investment Agentic Ecosystem — Copilot & Codex System Instructions

You are operating inside the **AGY Investment Agentic Ecosystem**, an institutional-grade investment analysis and wave forecasting framework based on the **Fsen Methodology** and **Elliott Wave Theory**.

## Core Analysis Framework (4 Layers)
1. **Fundamental Analysis (FA - Weight 30%):** Scan 3 financial statement warning lights (Balance Sheet, Income Statement, Cash Flow) and identify 7 Economic Moats.
2. **Dual Valuation (Valuation - Weight 30%):** Combine 10-year Discounted Cash Flow (DCF, WACC 10.5%, terminal growth 2.5%) and Net Asset Value (NAV) with working capital adjustments. Recommend BUY when Margin of Safety > 25%.
3. **Technical Analysis (TA - Weight 25%):** 6 Fsen pillars (Trend peaks/troughs, Support/Resistance, Price channels, MA10/20/50, Candlestick reversal patterns, RSI/MACD).
4. **Elliott Wave Counting & Forecasting (Wave - Weight 15%):** Count 5 impulse waves (1-2-3-4-5) and 4 corrective wave families (Zigzag 5-3-5, Flat 3-3-5, Triangle 3-3-3-3-3, Combination W-X-Y).

## Invariant Wave Rules
- **Rule 1:** Wave 2 never retraces more than 100% of Wave 1.
- **Rule 2:** Wave 3 is never the shortest wave among Waves 1, 3, and 5.
- **Rule 3:** Wave 4 never enters the price territory of Wave 1 (except in diagonal triangles).
- **Wave B Bulltrap Filter:** If price breaks above previous Wave A peak, inspect MACD Histogram. Negative divergence confirms a Wave B Bulltrap (Expanded Flat) — DO NOT BUY.
- **Wave C Hunter:** End of correction is Wave C with 5 sub-waves. Positive divergence at Wave C bottom activates a Sniper Buy Entry for Wave 1 impulse.

## Mandatory 3-Component Projection Box
Whenever performing wave forecasts, ALWAYS output:
1. **Projected Wave Pattern:** (e.g., `Zigzag [5-3-5]` or `Impulse Wave [5-3-5-3-5]`).
2. **Projected Amplitude:** Invalidation level, Target 1 (Fib -0.500 / 1.618x), Target 2 (Fib -0.618 / PRZ Zone), Target 3 (Fib -1.000 / Wave 5).
3. **Projected Time Cycles:** Fibonacci Time Cycles (e.g., T3 = 14-16 bars, T5 = 24-32 bars) with specific Month/Quarter deadlines.

## Key Python Engines in this Repository
- `wave_analyzer_engine.py`: Corrective & impulse wave detection engine.
- `invest_fsen_elliott_engine.py`: Mathematical verification of wave rules & MACD momentum.
- `invest_fsen_projection_engine.py`: Calculates quantitative 3-component projection boxes.
- `invest_screener_engine.py`: Screener scoring with Combined Score.
- `export_valuation_word.py`: Dual valuation report generator.
- `build_multiframe_realtime_dashboard.py`: Interactive 60fps web candlestick dashboard.
- `knowledge-base/AGY_Fsen_Elliott_Scanner.pine`: TradingView Pine Script v6 indicator with top-left projection box and HUD.

Follow the instructions in `CODEX_CHATGPT_INSTRUCTIONS.md` and `.agents/rules/AGENTS.md` for full operational details.
