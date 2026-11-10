---
name: invest:stock-screener
description: "Trạm Sàng Lọc Cổ Phiếu Toàn Thị Trường (Stock Screener Agent) theo chuẩn Fsen & Định Giá Nội Bộ. Phân tích đa tầng 4 lớp (FA 30%, Định Giá 30%, TA 25%, Sóng 15%), cung cấp 5 bộ lọc Presets (Siêu Cổ Phiếu Giá Trị, Bùng Nổ Đà Tăng, Bắt Đáy Quá Bán, Cổ Tức Bền Vững, Watchlist Nén Sóng) và xếp hạng Combined Score toàn diện."
user-invocable: true
when_to_use: "Sử dụng khi cần sàng lọc toàn thị trường để tìm top 5-10 cổ phiếu xuất sắc nhất, chấm điểm Combined Score đa tầng, hoặc lọc theo 5 Presets chiến lược."
category: investment
keywords: [invest:stock-screener, stock-screener, combined-score, value-investing, momentum-breakout, oversold-bounce, dividend]
metadata:
  author: "AGY Investment Team"
  brand: "AGY Invest"
  framework: "MICRO"
  version: "1.1.0"
---

# `invest:stock-screener` — BỘ LỌC CỔ PHIẾU ĐA TẦNG FSEN & ĐỊNH GIÁ NỘI BỘ

## 1. MỤC TIÊU & NGUYÊN TẮC HOẠT ĐỘNG
Trạm `invest:stock-screener` là bộ lọc định lượng và cơ bản kết hợp, quét qua toàn bộ rổ cổ phiếu mục tiêu (VN30, Midcap hoặc danh mục theo dõi) để tìm ra các cơ hội đầu tư có xác suất thắng cao nhất dựa trên nguyên tắc:
> **"Chỉ giải ngân vào doanh nghiệp có Lợi thế cạnh tranh (Moat), Định giá dưới giá trị thực (> 25% biên an toàn), và Biểu đồ kỹ thuật đã sẵn sàng vào Sóng đẩy."**

---

## 2. CÔNG THỨC CHẤM ĐIỂM TỔNG HỢP (COMBINED SCORE)

$$\text{Combined Score (100đ)} = (\text{FA Score} \times 30\%) + (\text{Valuation Score} \times 30\%) + (\text{TA Score} \times 25\%) + (\text{Wave Score} \times 15\%)$$

### Trọng số và tiêu chí chi tiết:
1. **FA Score (Tối đa 100 điểm — Trọng số 30%):**
   * Hệ thống 3 đèn cảnh báo tài chính:
     * $D/E < 1.0$ & $Current\ Ratio > 1.2$: +25đ
     * $ROE \ge 15\%$ & Biên lợi nhuận gộp $\ge 30\%$: +25đ
     * Dòng tiền thuần $FCF > 0$ & $CFO \ge LNST$: +25đ
   * Đánh giá Economic Moat (Lợi thế cạnh tranh lâu bền):
     * Sở hữu $\ge 2$ lợi thế cạnh tranh cốt lõi (Thương hiệu, Chi phí chuyển đổi, Quy mô, Rào cản ngành): +25đ

2. **Valuation Score (Tối đa 100 điểm — Trọng số 30%):**
   * Chạy song song 2 mô hình: DCF 10 năm ($g_{ước tính} = 0.5 \times g_{quá khứ}$, chiết khấu thực 10%) và Định giá Tài sản ròng bóc tách nợ chiếm dụng.
   * Biên an toàn $MOS = \frac{Giá\ trị\ thực - Thị\ giá}{Thị\ giá}$:
     * $MOS \ge 35\%$: 100 điểm
     * $25\% \le MOS < 35\%$: 85 điểm (Đạt chuẩn giải ngân)
     * $15\% \le MOS < 25\%$: 60 điểm (Quan sát)
     * $MOS < 15\%$: 20 điểm
     * $MOS < 0\%$ (Định giá đắt hơn thị giá): 0 điểm

3. **TA Score (Tối đa 100 điểm — Trọng số 25%):**
   * Khung 6 Trụ cột Fsen:
     * Giá nằm trên MA10 và MA20 trên khung Ngày/Tuần: +25đ
     * MACD Histogram dương và dốc lên (hoặc phân kỳ dương): +25đ
     * RSI(14) nằm trong vùng sung mãn 45 - 65: +25đ
     * Giá giữ vững trong nửa trên kênh xu hướng hoặc bứt phá cản: +25đ

4. **Wave Score (Tối đa 100 điểm — Trọng số 15%):**
   * Đếm sóng Elliott Fsen:
     * Chân Sóng 1 hoặc hoàn tất Sóng 2 (kiểm định Fibo 0.5 - 0.618): 100đ
     * Bắt đầu Sóng 3 bùng nổ (xung lực MACD mạnh nhất): 95đ
     * Hoàn tất Sóng điều chỉnh C cạn kiệt khối lượng (nến rút chân): 90đ
     * Sóng 4 phức tạp tích lũy đáy không vi phạm đỉnh Sóng 1: 75đ
     * Sóng 5 phân kỳ âm hoặc Sóng C đang rơi: 0đ (Loại bỏ)

---

## 3. 5 BỘ LỌC PRESETS CHIẾN THUẬT

1. **Preset 1: Siêu Cổ Phiếu Giá Trị (Deep Value Compounders):**
   * Điều kiện: $MOS \ge 25\%$, $Moat \ge 2$, $ROE \ge 15\%$, Sóng 2 hoặc Sóng C kết thúc.
   * Thích hợp: Nhà đầu tư giá trị, tích sản trung - dài hạn.

2. **Preset 2: Bùng Nổ Đà Tăng (Momentum Breakout):**
   * Điều kiện: EPS tăng trưởng $> 15\%$, Volume đột biến $> 1.5 \times MA20$, Giá vượt đỉnh cản, Bắt đầu Sóng 3.
   * Thích hợp: Nhà đầu tư theo đà tăng trưởng, lướt sóng trung hạn.

3. **Preset 3: Bắt Đáy Quá Bán (Oversold Bounce):**
   * Điều kiện: $FCF > 0$, RSI(14) $< 35$, Chạm đáy kênh dưới hoặc hỗ trợ Fibo 0.618, Xuất hiện nến Hammer/Doji rút chân.
   * Thích hợp: Bắt điểm đảo chiều với tỷ lệ Risk/Reward cao ($\ge 1 : 3.5$).

4. **Preset 4: Cổ Tức Bền Vững (Dividend Aristocrats):**
   * Điều kiện: Tỷ suất cổ tức (Dividend Yield) $> 6\%$, Nợ $D/E < 0.5$, Biên an toàn $> 20\%$.
   * Thích hợp: Dòng tiền phòng thủ, an toàn vốn.

5. **Preset 5: Theo Dõi Kích Hoạt (Watchlist Trigger):**
   * Điều kiện: Cổ phiếu nén chặt trong mô hình tam giác (Contracting Triangle) hoặc đi ngang vùng đáy Sóng 4.

---

## 4. OUTPUT BÀN GIAO
* Bảng xếp hạng Top 5 – 10 Cổ phiếu đạt điểm Combined Score cao nhất.
* Thẻ tóm tắt chỉ số FA, Biên an toàn DCF/Tài sản ròng, và Tín hiệu Sóng.
* Chuyển giao dữ liệu sang Trạm `invest:signal-agent` để tạo Signal Card chi tiết.

