---
name: invest:excel-ops
description: "Trạm Vận Hành Master Excel Dashboard & Tự Động Hóa Báo Cáo Doanh Nghiệp (Excel Ops & Automated Dossier Generator). Vận hành 100% hệ thống đầu tư trên Microsoft Office & Standalone BI HTML không cần Web App: Master Excel 5 Sheet (KPI Cards, Screener, Radar Tín Hiệu, Sổ Cái Danh Mục Live Formulas, Lịch Sử Khớp Lệnh), xuất bản Hồ Sơ Phân Tích Doanh Nghiệp Word chuẩn Corporate, Executive BI Dashboard HTML Glassmorphism 60fps và đồng bộ 1-Click BAT."
user-invocable: true
when_to_use: "Sử dụng khi cần cập nhật Master Excel Dashboard 5 sheet, xuất hồ sơ báo cáo phân tích doanh nghiệp Word, xuất Executive BI Dashboard HTML hoặc kích hoạt đồng bộ 1-click toàn diện."
category: investment
keywords: [invest:excel-ops, excel-dashboard, word-dossier, bi-dashboard, sync-engine, no-web]
metadata:
  author: "AGY Investment Team"
  brand: "AGY Invest"
  framework: "MICRO"
  version: "1.2.0"
---

# `invest:excel-ops` — Trạm Vận Hành Master Excel Dashboard & Báo Cáo Tự Động

Bộ kỹ năng thuộc Hệ sinh thái **AI Investment Agent (`invest:stock-agent`)**, giải quyết bài toán vận hành đầu tư thực chiến chuyên nghiệp **hoàn toàn trên nền tảng Microsoft Office (Excel & Word)**, tối ưu cho nhà đầu tư thích quản trị bảng tính cục bộ, bảo mật offline 100%, không cần qua giao diện Web.

---

## 1. KHUNG KIẾN TRÚC 5 SHEET MASTER EXCEL (`Excel_Master_Investment_Dashboard.xlsx`)

Hệ thống bảng tính được thiết kế theo chuẩn **Corporate Financial Model**: Font Times New Roman, Header Xanh Navy `#1B365D`, Subtotal Slate `#E2E8F0`, màu sắc tín hiệu tài chính chuẩn (Xanh lá `#1B5E20` cho Lãi/Buy, Đỏ `#B71C1C` cho Lỗ/Sell/SL, Cam `#E65100` cho Chờ duyệt):

1. **Sheet 1: `Tong_Quan_Dashboard` (Executive KPI Dashboard):**
   * 5 Thẻ KPI lớn: Tổng NAV (`1,003,330,720 VND`), Tiền mặt khả dụng (`700,030,720 VND` / 69.8%), Cổ phiếu (`303,300,000 VND`), Lãi tạm tính (`+3,780,000 VND`), Trạng thái rủi ro `🟢 AN TOÀN TUYỆT ĐỐI (ALL GREEN)`.
   * Bảng phân bổ tài sản, tỷ trọng so với trần 25% NAV.
   * Bảng Top Tín Hiệu Hành Động Nổi Bật (Signal Radar).
2. **Sheet 2: `Bo_Loc_Screener_Fsen` (Stock Screener Combined Score):**
   * Bảng xếp hạng toàn thị trường với công thức Combined Score đa tầng: FA 30% + Định Giá 30% + TA 25% + Sóng 15%.
   * Phân loại theo 5 Presets chiến lược, AutoFilter và Freeze Panes cố định tiêu đề.
3. **Sheet 3: `Radar_Tin_Hieu_Va_Lenh` (Signal Radar & Human Checkpoint Gate):**
   * Cửa ngõ kiểm soát phê duyệt lệnh HITL (AI chỉ lập kế hoạch tác chiến, Nhà đầu tư duyệt lệnh).
   * Thông số chi tiết: Vùng Entry, Cắt lỗ vô hiệu hóa (SL), TP1, TP2, Tỷ lệ R/R $\ge 1:2.5$, Backtest 5 năm (Win Rate, Profit Factor) và Trạng thái duyệt.
4. **Sheet 4: `So_Cai_Danh_Muc` (Live Portfolio Ledger):**
   * Sổ cái vị thế đang nắm giữ với **công thức Excel thật** (`=SUM()`, `=C*D`, `=G-F`, `=H/F`, `=G/NAV`).
   * Tự động cập nhật lãi/lỗ chưa chốt, tỷ trọng danh mục và ngưỡng cắt lỗ bảo vệ.
5. **Sheet 5: `Lich_Su_Giao_Dich` (Trade History & Audit Log):**
   * Nhật ký lưu vết toàn bộ các lệnh đã khớp trong quá khứ, minh bạch 100% đối soát.

---

## 2. HỒ SƠ PHÂN TÍCH DOANH NGHIỆP WORD (`Bao_Cao_Phan_Tich_Doanh_Nghiep_Master.docx`)

Tự động trích xuất và kết xuất hồ sơ thẩm định doanh nghiệp hoàn chỉnh 6 phần chuẩn Corporate:
1. Tổng quan xếp hạng Screener & Biên an toàn MOS (Thẻ KPI 5 cột).
2. Hệ thống đèn cảnh báo BCTC 5 năm (CĐKT, KQKD, LCTT) & 7 Lợi thế kinh tế (Economic Moat).
3. Kết quả mô hình định giá đôi (DCF 10 năm + Tài sản ròng bóc tách nợ).
4. Phân tích kỹ thuật 6 Trụ Cột Fsen & Bản đồ Sóng Elliott Pro (chèn ảnh sắc nét).
5. Kế hoạch tác chiến lệnh (Signal Card, R/R, Stop Loss vô hiệu hóa, Chốt lời TP1/TP2).
6. Kế hoạch giải ngân danh mục tuân thủ nghiêm ngặt hạn mức rủi ro $\le 25\%$ NAV.

---

## 3. CƠ CHẾ ĐIỀU PHỐI 1-CLICK (`DONG_BO_EXCEL_MASTER.bat`)

Người dùng chỉ cần nhấp đúp tệp [`DONG_BO_EXCEL_MASTER.bat`](fil./DONG_BO_EXCEL_MASTER.bat):
1. Hệ thống tự động kích hoạt `excel_master_sync_engine.py`.
2. Đồng bộ CSDL SQLite `investment.db` sang 5 sheet Excel Master.
3. Tự động biên dịch Báo cáo Doanh nghiệp Word mới nhất.
4. Tự động mở cả file Excel và Word trên màn hình máy tính của bạn.

