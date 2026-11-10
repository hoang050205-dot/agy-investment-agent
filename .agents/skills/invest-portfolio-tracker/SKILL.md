---
name: invest:portfolio-tracker
description: "Trạm Quản Trị Danh Mục Đầu Tư & Sổ Cái Giao Dịch SQLite (Portfolio Tracker Agent). Ghi nhận các lệnh đã duyệt từ Human Checkpoint Gate vào CSDL cục bộ (knowledge-base/investment.db), theo dõi biến động NAV thời gian thực, tính toán P&L thực tế & P&L chưa chốt, cảnh báo rủi ro vi phạm tỷ trọng (> 25% NAV/mã) hoặc sụt giảm danh mục (> 7% Max Drawdown)."
user-invocable: true
when_to_use: "Sử dụng khi cần ghi nhận lệnh mới vào sổ cái SQLite, cập nhật thị giá danh mục, tính toán NAV/P&L, kiểm soát giới hạn tỷ trọng tối đa 25% NAV và giám sát rủi ro Max Drawdown."
category: investment
keywords: [invest:portfolio-tracker, portfolio, sqlite, nav, pnl, drawdown, risk-management]
metadata:
  author: "AGY Investment Team"
  brand: "AGY Invest"
  framework: "MICRO"
  version: "1.1.0"
---

# `invest:portfolio-tracker` — SỔ CÁI DANH MỤC ĐẦU TƯ & QUẢN TRỊ RỦI RO SQLITE

## 1. MỤC TIÊU & NHIỆM VỤ
Trạm `invest:portfolio-tracker` đóng vai trò là "Sổ Cái Kế Toán Danh Mục" lưu trữ độc lập, an toàn và minh bạch trên SQLite cục bộ (`knowledge-base/investment.db`).
Hệ thống giúp Nhà đầu tư:
1. Ghi nhận chính xác lịch sử mọi giao dịch đã được phê duyệt qua Human Checkpoint Gate.
2. Theo dõi biến động Tổng Giá Trị Tài Sản Ròng (NAV = Tiền mặt + Giá trị thị trường các cổ phiếu đang nắm giữ).
3. Đo lường tỷ suất sinh lời thực tế (Realized P&L) và lợi nhuận thả nổi (Unrealized P&L).
4. Thiết lập hệ thống cảnh báo sớm (Early Warning System) khi danh mục vi phạm các giới hạn an toàn vốn.

---

## 2. KIẾN TRÚC CƠ SỞ DỮ LIỆU SQLITE (`knowledge-base/investment.db`)

Hệ thống quản lý thông qua 3 bảng dữ liệu chuẩn hóa:

### Bảng 1: `portfolio` (Danh mục đang nắm giữ hiện tại)
* `symbol` (TEXT PRIMARY KEY): Mã cổ phiếu / Tài sản (VD: `FPT`, `SIP`, `BTCUSD`).
* `market` (TEXT): Thị trường (`VN_EQUITY`, `GLOBAL_CRYPTO`, `COMMODITY`).
* `quantity` (REAL): Tổng số lượng đang nắm giữ.
* `avg_price` (REAL): Giá vốn bình quân gia quyền.
* `current_price` (REAL): Giá thị trường cập nhật gần nhất.
* `market_value` (REAL): Giá trị thị trường ($quantity \times current\_price$).
* `unrealized_pnl` (REAL): Lợi nhuận chưa chốt ($market\_value - quantity \times avg\_price$).
* `unrealized_pnl_pct` (REAL): Phần trăm lãi/lỗ chưa chốt.
* `weight_pct` (REAL): Tỷ trọng trong tổng NAV danh mục.
* `stop_loss` (REAL): Mức giá cắt lỗ phòng thủ.
* `take_profit` (REAL): Mức giá mục tiêu chốt lời.
* `updated_at` (TEXT): Thời điểm cập nhật cuối cùng.

### Bảng 2: `trade_history` (Nhật ký giao dịch đã phê duyệt)
* `trade_id` (INTEGER PRIMARY KEY AUTOINCREMENT).
* `symbol` (TEXT): Mã tài sản.
* `action` (TEXT): Chiều giao dịch (`BUY`, `SELL`, `TAKE_PROFIT`, `STOP_LOSS`).
* `quantity` (REAL): Số lượng khớp.
* `price` (REAL): Giá khớp thực tế.
* `fee` (REAL): Thuế & phí giao dịch ước tính.
* `total_amount` (REAL): Tổng giá trị thanh toán ($quantity \times price + fee$).
* `realized_pnl` (REAL): Lãi/Lỗ thực tế chốt được (nếu là lệnh SELL).
* `trade_date` (TEXT): Thời gian khớp lệnh.
* `signal_id` (TEXT): Mã tham chiếu Signal Card ban đầu.
* `approved_by` (TEXT): Người phê duyệt (`HUMAN_CHECKPOINT`).
* `note` (TEXT): Ghi chú chiến thuật vào/ra lệnh.

### Bảng 3: `risk_metrics` (Nhật ký biến động NAV & Kiểm soát rủi ro)
* `log_date` (TEXT PRIMARY KEY): Ngày ghi nhận.
* `total_nav` (REAL): Tổng giá trị tài sản ròng.
* `cash_balance` (REAL): Tiền mặt khả dụng.
* `stock_value` (REAL): Tổng giá trị cổ phiếu nắm giữ.
* `cash_weight_pct` (REAL): Tỷ lệ tiền mặt / NAV.
* `peak_nav` (REAL): Đỉnh NAV cao nhất từng đạt được.
* `drawdown_pct` (REAL): Mức sụt giảm từ đỉnh NAV hiện tại.
* `risk_status` (TEXT): Trạng thái rủi ro (`AN TOÀN`, `CẢNH BÁO`, `VI PHẠM`).

---

## 3. QUY TẮC BẢO VỆ VỐN & CẢNH BÁO RỦI RO (RISK GUARDRAILS)

1. **Giới hạn tỷ trọng cổ phiếu đơn lẻ (Concentration Limit):**
   * Tối đa **25% NAV** cho bất kỳ 1 mã cổ phiếu nào.
   * Nếu giá tăng mạnh khiến tỷ trọng vượt quá 25% NAV ➔ Hệ thống kích hoạt cảnh báo `REBALANCE`: Khuyến nghị chốt lời một phần để tái cân bằng danh mục.
2. **Giới hạn sụt giảm danh mục tối đa (Max Drawdown Limit):**
   * Nếu NAV danh mục sụt giảm **$> 7\%$** từ đỉnh NAV gần nhất ➔ Hệ thống kích hoạt trạng thái `DEFENSIVE MODE`: Tạm dừng mở vị thế mua mới, rà soát nâng mức Stop Loss của toàn bộ các mã đang nắm giữ.
3. **Giới hạn tỷ lệ tiền mặt an toàn:**
   * Luôn duy trì tối thiểu **10% – 15% NAV** ở dạng tiền mặt khả dụng để chủ động bắt đáy khi thị trường hoảng loạn.

