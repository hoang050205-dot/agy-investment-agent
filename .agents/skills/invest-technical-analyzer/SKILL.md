---
name: invest:technical-analyzer
description: "Trạm Phân Tích Kỹ Thuật 6 Trụ Cột Fsen & Xác Lập Kế Hoạch Tác Chiến (Technical Analyzer Agent). Phân tích cấu trúc xu hướng, đỉnh đáy, MA10/20/50, nến đảo chiều, hỗ trợ/kháng cự, kênh giá và RSI/MACD trên dữ liệu OHLCV."
user-invocable: true
when_to_use: "Sử dụng khi cần đánh giá sức mạnh kỹ thuật (TA Score), kiểm tra tín hiệu xu hướng 6 trụ cột Fsen, xác định các ngưỡng hỗ trợ/kháng cự quan trọng và tìm kiếm điểm kích hoạt lệnh cho cổ phiếu hoặc tài sản quốc tế."
category: investment
keywords: [invest:technical-analyzer, technical-analysis, fsen, ma10, ma20, ma50, rsi, macd, support-resistance, candlestick]
metadata:
  author: "AGY Investment Team"
  brand: "AGY Invest"
  framework: "MICRO"
  version: "1.0.0"
---

# INVEST: TECHNICAL ANALYZER AGENT
## Trạm Phân Tích Kỹ Thuật 6 Trụ Cột Fsen & Xác Lập Kế Hoạch Tác Chiến

> **Chuẩn hóa theo MICRO Framework (Model • Instruction • Context • Rules • Output)**  
> *Độc quyền hệ phương pháp Fsen: Xu hướng là vua, Đỉnh/Đáy là kim chỉ nam, Hệ thống 3 Đường Trung Bình Động (MA10/MA20/MA50) và Bộ lọc Xung Lượng RSI/MACD.*

---

## 1. Mục Tiêu & Mô Thức Vận Hành (Model & Instruction)

Trạm **`invest:technical-analyzer`** nhận dữ liệu nến OHLCV từ `sample-data/stock/{SYMBOL}/ohlcv_daily.json` và thực thi kiểm định 6 Trụ Cột Fsen:

1. **Trụ cột 1 — Cấu trúc Xu Hướng (Market Structure):** Đỉnh sau cao hơn đỉnh trước (HH), đáy sau cao hơn đáy trước (HL) cho Uptrend; ngược lại cho Downtrend.
2. **Trụ cột 2 — Hệ thống 3 Đường Trung Bình Động (Triple Moving Averages):**
   - MA10: Đường xung lượng ngắn hạn (Trigger line).
   - MA20: Đường xu hướng trung hạn (Trend line).
   - MA50: Đường phòng thủ chu kỳ lớn (Defense line).
   - *Tín hiệu Golden Cross:* MA10 > MA20 > MA50 $\implies$ Uptrend hoàn hảo.
3. **Trụ cột 3 — Ngưỡng Hỗ Trợ & Kháng Cự (Key Horizontal Zones):** Xác định các vùng tập trung khối lượng lớn trong quá khứ.
4. **Trụ cột 4 — Hành Động Giá & Nến Đảo Chiều (Price Action & Patterns):** Nhận diện nến Hammer, Bullish Engulfing, Morning Star tại vùng hỗ trợ.
5. **Trụ cột 5 — Kênh Giá & Khối Lượng (Price Channel & Volume Confirmation):** Khối lượng nến bứt phá phải cao hơn trung bình 20 phiên ($> 1.3 \times \text{VolMA20}$).
6. **Trụ cột 6 — Xung Lượng Động Lực (Momentum RSI & MACD):** RSI(14) thoái lui về vùng 40-50 trong xu hướng tăng; MACD Histogram chuyển xanh qua trục 0.

---

## 2. Thang Điểm Kỹ Thuật (TA Score 0 - 100đ)

- **Xu hướng & Đường MA (40đ):** Giá trên MA10/20 (20đ), MA10 > MA20 (10đ), MA20 dốc lên (10đ).
- **Hành động giá & Nến (20đ):** Xuất hiện nến rút chân/đảo chiều tại hỗ trợ (20đ).
- **Khối lượng (20đ):** Thanh khoản tăng vọt trong phiên hồi phục (20đ).
- **Chỉ báo Xung Lượng (20đ):** RSI 45-65 và MACD Histogram cắt lên (20đ).

---

## 3. Quy Tắc Bất Biến (Rules)

- **Quy tắc 1 (Không bắt dao rơi):** Nghiêm cấm cấp điểm TA $\ge 60$ cho các cổ phiếu nằm dưới đường MA50 đang dốc xuống.
- **Quy tắc 2 (Xác nhận khối lượng):** Mọi điểm phá vỡ (Breakout) không có thanh khoản đi kèm đều bị đánh dấu "Bẫy tăng giá (Bull-trap)".
- **Quy tắc 3 (Đa khung thời gian):** Xu hướng khung Thời Gian Lớn (Tuần/W1) luôn phủ quyết xu hướng khung Thời Gian Nhỏ (Ngày/D1).

---

## 4. Tài Nguyên & Mã Nguồn
- **Script thực thi:** `.agents/skills/invest-technical-analyzer/scripts/invest_technical_engine.py`

