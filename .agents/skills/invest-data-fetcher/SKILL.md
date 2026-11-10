---
name: invest:data-fetcher
description: "Trạm thu thập & chuẩn hóa dữ liệu tài chính chứng khoán Việt Nam (HOSE/HNX/UPCOM): Báo cáo tài chính 5 năm (CĐKT, KQKD, LCTT), nến OHLCV đa khung (W, D, 4H, 1H) và thông tin hồ sơ doanh nghiệp."
user-invocable: true
metadata:
  framework: MICRO
  category: investment
  version: 1.0.0
---

# Invest: Data Fetcher — Trạm Thu Thập & Chuẩn Hóa Dữ Liệu Chứng Khoán

## 1. Mục Tiêu (Objective)
Cung cấp dữ liệu thô chuẩn hóa cho toàn bộ hệ thống phân tích và định giá:
- Báo cáo tài chính 5 năm liền kề (Bảng CĐKT, KQKD, LCTT).
- Chuỗi nến lịch sử đa khung thời gian (Tuần, Ngày, 4H, 1H).
- Hồ sơ doanh nghiệp (vốn điều lệ, số CPLH, ngành nghề, vốn hóa).

## 2. Input & Output Contract
- **Input:** Mã cổ phiếu (VD: `SIP`, `FPT`, `HPG`, `VNM`), số năm BCTC (mặc định 5 năm).
- **Output:** Tệp dữ liệu JSON lưu trữ tại `sample-data/stock/{SYMBOL}/` gồm:
  - `profile.json`: Thông tin cơ bản, vốn hóa, số CPLH.
  - `financials_5y.json`: BCTC 5 năm (CĐKT, KQKD, LCTT).
  - `ohlcv_daily.json`: Dữ liệu nến ngày 1 năm gần nhất.

## 3. Cách Sử Dụng
Chạy qua môi trường ảo `$HOME\.venv`:
```powershell
& "$HOME\.venv\Scripts\python.exe" .agents/skills/invest-data-fetcher/scripts/fetch_stock_data.py --symbol SIP
```

