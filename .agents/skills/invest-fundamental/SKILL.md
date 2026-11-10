---
name: invest:fundamental-analyzer
description: "Trạm phân tích báo cáo tài chính 5 năm liền kề: Quét 3 hệ thống đèn cảnh báo (Bảng CĐKT, KQKD, LCTT) và nhận diện 7 lợi thế cạnh tranh lâu bền (Economic Moat) theo tài liệu nội bộ PTBCTC NHANH."
user-invocable: true
metadata:
  framework: MICRO
  category: investment
  version: 1.0.0
---

# Invest: Fundamental Analyzer — Phân Tích Báo Cáo Tài Chính 5 Năm & Economic Moat

## 1. Mục Tiêu (Objective)
Đánh giá toàn diện sức khỏe tài chính doanh nghiệp dựa trên số liệu BCTC 5 năm liền kề, phát hiện rủi ro cơ cấu vốn, thanh khoản, chất lượng lợi nhuận và nhận diện hào thành kinh tế (Economic Moat).

## 2. Hệ Thống 3 Đèn Cảnh Báo
1. **Bảng Cân Đối Kế Toán:**
   - $D/E > 1.0$: 🔴 Đỏ | $ROE > 15\%$: 🟢 Xanh đậm | $Current\ Ratio < 1.0$: 🔴 Đỏ
2. **Báo Cáo Kết Quả Kinh Doanh:**
   - Biên gộp $< 35\%$: 🟠 Cam | Biên hoạt động $< 15\%$: 🟠 Cam | Biên ròng $< 10\%$: 🔴 Đỏ
   - Chi phí BH + QLDN $< 30\%$: 🟢 Đạt
3. **Báo Cáo Lưu Chuyển Tiền Tệ:**
   - $FCF = CFO - CAPEX < 0$: 🔴 Đỏ (Dòng tiền tự do âm)
   - $CFO < LNST$: 🟡 Vàng (Lợi nhuận chưa thu được tiền mặt)
   - $FCF / Doanh\ thu > 10\%$: 🟢 Đạt chuẩn dòng tiền mạnh

## 3. Nhận Diện 7 Economic Moat
- Thương hiệu mạnh, Hiệu ứng mạng lưới, Chi phí chuyển đổi cao, Lợi thế chi phí, Độc quyền / Bằng sáng chế, Rào cản gia nhập ngành, Dễ mở rộng quy mô.
- Doanh nghiệp có $\ge 2-3$ lợi thế trở lên ➔ Economic Moat mạnh.

## 4. Cách Sử Dụng
```powershell
& "$HOME\.venv\Scripts\python.exe" .agents/skills/invest-fundamental/scripts/analyze_fundamental.py --symbol SIP
```

