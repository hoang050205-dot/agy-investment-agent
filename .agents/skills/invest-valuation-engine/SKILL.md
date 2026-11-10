---
name: invest:valuation-engine
description: "Trạm định giá cổ phiếu đôi: Định giá chiết khấu dòng tiền (DCF 10 năm) + Định giá Tài sản ròng bóc tách nợ chiếm dụng, đưa ra biên an toàn và khuyến nghị MUA khi chênh lệch > 25%."
user-invocable: true
metadata:
  framework: MICRO
  category: investment
  version: 1.0.0
---

# Invest: Valuation Engine — Bộ Máy Định Giá Cổ Phiếu Đôi (DCF & Tài Sản Ròng)

## 1. Mục Tiêu (Objective)
Tính toán giá trị nội tại thực tế của cổ phiếu dựa trên 2 phương pháp định lượng khoa học, loại bỏ yếu tố cảm xúc và xác định Biên an toàn (Margin of Safety).

## 2. Phương Pháp Luận Định Giá

### A. Định Giá Chiết Khấu Dòng Tiền (DCF 10 Năm)
- Dữ liệu: LNST 5 năm gần nhất ($t-4$ đến $t$).
- Tốc độ tăng trưởng: $g = \frac{1}{4}(g_1 + g_2 + g_3 + g_4)$, $g_{ước tính} = 0.5 \times g$ (tối đa 25%, không vượt $g_4$).
- Dự phóng 10 năm: 5 năm tăng trưởng ($t+1 \dots t+5$) + 5 năm duy trì ($t+6 \dots t+10$).
- Loại trừ lạm phát 7%: $LNST_{thực}(i) = \frac{LNST_{danh nghĩa}(i)}{(1 + 0.07)^i}$.
- Chiết khấu hiện tại 10%: $PV(i) = \frac{LNST_{thực}(i)}{(1 + 0.10)^i}$.
- Giá trị thực / CP = $\frac{\sum_{i=1}^{10} PV(i)}{Số\ CPLH}$.

### B. Định Giá Tài Sản Ròng (Bóc Tách Nợ Chiếm Dụng)
- Nợ chiếm dụng = (Ngắn hạn: mục 3 + 4 + 5 + 10) + (Dài hạn: mục 8 + 11).
- $Nợ\ tính\ lại = Tổng\ nợ - Nợ\ chiếm\ dụng$.
- $Giá\ trị\ DN = Tổng\ tài\ sản - Nợ\ tính\ lại$.
- Giá trị thực / CP = $\frac{Giá\ trị\ DN}{Số\ CPLH}$.

### C. Ngưỡng Hành Động (Action Threshold)
- $Biên\ an\ toàn = \frac{Giá\ trị\ thực - Giá\ hiện\ tại}{Giá\ hiện\ tại}$.
- **Khuyến nghị MUA: Nếu Biên an toàn > 25%** (kết hợp xác nhận yếu tố Chu kỳ và Sóng).
- Nếu Biên an toàn $\le 25\%$: KHÔNG khuyến nghị mua.

## 3. Cách Sử Dụng
```powershell
& "$HOME\.venv\Scripts\python.exe" .agents/skills/invest-valuation-engine/scripts/calculate_valuation.py --symbol SIP
```

