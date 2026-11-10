# HƯỚNG DẪN CÀI ĐẶT & VẬN HÀNH HỆ SINH THÁI AGY INVESTMENT AGENT

> **Bản quyền chuyển giao:** AGY Investment Agentic Ecosystem  
> **Phiên bản:** v3.0 Pro  
> **Ngôn ngữ:** Python 3.10+, Pine Script v6, Web HTML/JS (Lightweight Charts 60fps)

---

## I. CẤU TRÚC WORKSPACE ĐÃ ĐÓNG GÓI

```
packaged_investment_workspace/
├── .agents/
│   ├── rules/
│   │   └── AGENTS.md                  # Quy tắc vận hành & 4 thiết luật Fsen
│   └── skills/                        # 9 Trạm nghiệp vụ AI chuyên biệt
│       ├── invest-data-fetcher/       # Thu thập BCTC 5 năm & nến OHLCV
│       ├── invest-fundamental/        # 3 hệ thống đèn cảnh báo & 7 Moats
│       ├── invest-valuation-engine/   # Định giá đôi DCF & Net Asset
│       ├── invest-technical-analyzer/ # 6 trụ cột Fsen & MA10/20/50
│       ├── invest-wave-analyst/       # Đếm sóng Fsen & MACD Bulltrap Gate v2.0
│       ├── invest-stock-screener/     # Sàng lọc Combined Score 4 lớp
│       ├── invest-signal-agent/       # Signal Cards & Backtest Engine
│       ├── invest-portfolio-tracker/  # Quản trị danh mục SQLite Real-time
│       └── invest-excel-ops/          # Master Excel 5 Sheet & Dashboard BI
│
├── core engines (Mã nguồn thực thi độc lập):
│   ├── invest_fsen_projection_engine.py      # Dự báo sóng 3 thành tố (Sóng - Biên độ - Thời gian)
│   ├── invest_fsen_elliott_engine.py         # Kiểm định 3 quy tắc bất biến & MACD
│   ├── wave_analyzer_engine.py               # Động cơ đếm sóng điều chỉnh động 100%
│   ├── build_multiframe_realtime_dashboard.py# Sinh Biểu đồ Web tương tác Master 60fps
│   ├── build_excel_master_dashboard.py       # Tạo Sổ Master Excel 5 Sheet tự động
│   ├── export_valuation_word.py              # Xuất Báo cáo Định giá Word (.docx)
│   ├── export_master_technical_reports.py    # Xuất Báo cáo Kỹ thuật Tuần (.docx)
│   ├── server_investment_charts.py           # Web Server nội bộ phục vụ biểu đồ
│   ├── test_phase1_investment.py             # Kiểm thử toàn diện Phase 1 (FA & Định giá)
│   ├── test_phase2_investment.py             # Kiểm thử toàn diện Phase 2 (TA & Sóng)
│   └── test_phase3_investment.py             # Kiểm thử toàn diện Phase 3 (Screener & Danh mục)
│
├── knowledge-base/
│   ├── AGY_Fsen_Elliott_Scanner.pine         # Chỉ báo TradingView Pine Script v6 chuẩn
│   └── AGY_Fsen_Elliott_Wave_Pro.pine        # Chỉ báo TradingView Kỹ thuật & Sóng tổng hợp
│
├── sample-data/stock/                        # Dữ liệu nến mẫu sạch (VND, FPT, SIP, BTCUSD, XAUUSD)
├── outputs/investment/                       # Thư mục chứa báo cáo và biểu đồ sau khi chạy
├── CODEX_CHATGPT_INSTRUCTIONS.md             # Hướng dẫn cấu hình cho ChatGPT & OpenAI Codex
├── requirements.txt                          # Danh sách thư viện Python
├── MO_BIEU_DO_WEB.bat                        # 1-Click mở Web Interactive Dashboard
├── MO_TRADINGVIEW_PINE_EDITOR.bat            # 1-Click mở TradingView và nạp code Pine
└── CHAY_KIEM_THU_TOAN_BO_PIPELINE.bat        # 1-Click chạy toàn bộ quy trình đầu tư
```

---

## II. HƯỚNG DẪN CÀI ĐẶT NHANH (QUICK START)

### Bước 1: Cài đặt Python & Thư viện
1. Cài đặt Python 3.10 trở lên từ [python.org](https://www.python.org/).
2. Mở cửa sổ dòng lệnh (Terminal / Command Prompt / PowerShell) tại thư mục này và chạy:
   ```bash
   pip install -r requirements.txt
   ```

### Bước 2: Chạy kiểm thử toàn bộ hệ thống (1-Click)
- **Trên Windows:** Nhấp đúp chuột vào file `CHAY_KIEM_THU_TOAN_BO_PIPELINE.bat`.
- **Hoặc qua dòng lệnh:**
  ```bash
  python test_phase1_investment.py
  python test_phase2_investment.py
  python test_phase3_investment.py
  python invest_fsen_projection_engine.py
  python build_multiframe_realtime_dashboard.py
  ```
Toàn bộ dữ liệu phân tích, báo cáo Word, Excel và Web Dashboard sẽ tự động được sinh ra trong thư mục `outputs/investment/`.

---

## III. HƯỚNG DẪN SỬ DỤNG CÁC TÍNH NĂNG ĐỈNH CAO

### 1. Khởi động Biểu đồ Web Tương Tác 60fps (Interactive Chart)
- Nhấp đúp vào `MO_BIEU_DO_WEB.bat`.
- Trình duyệt web sẽ tự động mở trang:
  **`http://localhost:8888/chart_scenario_interactive_MASTER.html`**
- **Tính năng nổi bật:**
  * Xem đa tài sản: VND (Chứng khoán), FPT, BTCUSD (Crypto), XAUUSD (Vàng).
  * Xem đa khung thời gian: Tháng (1M), Tuần (1W), Ngày (1D), Giờ (1H).
  * Hộp **Dự Báo Sóng Fsen Góc Trái** hiển thị trực quan: Dạng Sóng Dự Kiến - Biên Độ Fibo - Thời Gian Chu Kỳ.
  * Các nhãn sóng tương lai `3?`, `4?`, `5?`, `A?`, `B?`, `C?` và vùng hộp vàng mục tiêu PRZ.

### 2. Cài đặt Chỉ báo lên TradingView (1-Click Pine Script v6)
- Nhấp đúp vào `MO_TRADINGVIEW_PINE_EDITOR.bat`.
- Hệ thống sẽ **tự động sao chép toàn bộ mã nguồn Pine Script v6 vào Clipboard của bạn** và mở trang TradingView.
- Bạn chỉ cần:
  1. Mở tab **Pine Editor** ở phía dưới biểu đồ TradingView.
  2. Xóa hết code cũ, nhấn `Ctrl + V` để dán mã mới.
  3. Bấm **Add to chart (Thêm vào biểu đồ)** và **Save (Lưu)**.
- Biểu đồ sẽ xuất hiện đầy đủ nhãn sóng, dải hộp vàng, đường Invalidation và Hộp Dự Báo Sóng góc trái!

### 3. Vận hành cùng AI (ChatGPT, Claude Code, OpenAI Codex)
- Xem hướng dẫn chi tiết tại file [`CODEX_CHATGPT_INSTRUCTIONS.md`](file:///CODEX_CHATGPT_INSTRUCTIONS.md) để biết cách cấu hình Custom GPTs hoặc cấp quyền cho Codex vận hành workspace này một cách tự động.

