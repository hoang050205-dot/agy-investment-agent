# CẨM NANG BÀN GIAO & VẬN HÀNH WORKSPACE AGY INVESTMENT AGENT
## Hướng Dẫn Vận Hành Độc Lập Cho Người Nhận & Cấu Hình OpenAI Codex / ChatGPT

> **Hệ sinh thái:** AGY Investment Agentic Ecosystem (v3.0 Pro)  
> **Tình trạng:** 100% Khử sạch dữ liệu cá nhân (Zero PII), 100% đường dẫn tương đối (Plug & Play).  
> **Kho lưu trữ GitHub:** [https://github.com/hoang050205-dot/agy-investment-agent](https://github.com/hoang050205-dot/agy-investment-agent)  
> **Tương thích:** Windows, macOS, Linux, OpenAI Codex, ChatGPT Plus (Custom GPTs), Claude Code, Cursor IDE, VS Code Copilot.

---

## I. TỔNG QUAN TÀI NGUYÊN ĐƯỢC CHUYỂN GIAO

Người nhận kho mã nguồn này sẽ sở hữu một hệ sinh thái phân tích đầu tư và đếm sóng hoàn chỉnh bao gồm:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📦 BỘ TÀI NGUYÊN BÀN GIAO TRỌN GÓI TRÊN GITHUB                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. 9 Kỹ năng Agentic (.agents/skills/):                                     │
│    • invest-data-fetcher: Thu thập BCTC 5 năm & nến OHLCV đa khung.         │
│    • invest-fundamental: 3 hệ thống đèn cảnh báo BCTC & 7 Economic Moats.   │
│    • invest-valuation-engine: Định giá đôi DCF 10 năm & Giá trị tài sản ròng.│
│    • invest-technical-analyzer: 6 trụ cột kỹ thuật Fsen & MA10/20/50.       │
│    • invest-wave-analyst: Đếm sóng Elliott v2.0 & Bắt bẫy Sóng B / Đáy C.  │
│    • invest-stock-screener: Sàng lọc toàn sàn Combined Score 4 lớp.        │
│    • invest-signal-agent: Tạo Signal Cards R/R >= 1:2.5 & Backtest Engine.  │
│    • invest-portfolio-tracker: Quản trị danh mục SQLite Real-time.          │
│    • invest-excel-ops: Vận hành Master Excel 5 Sheet & Word Dossier.        │
│ 2. Động cơ phân tích Python động:                                           │
│    • wave_analyzer_engine.py: Đếm sóng Elliott 4 họ điều chỉnh.             │
│    • invest_fsen_elliott_engine.py: Kiểm định 3 thiết luật bất biến & MACD. │
│    • invest_fsen_projection_engine.py: Hộp dự báo tương lai 3 thành tố.     │
│ 3. Chỉ báo TradingView Pine Script v6:                                      │
│    • knowledge-base/AGY_Fsen_Elliott_Scanner.pine (Hộp góc trái + HUD Table).│
│ 4. Biểu đồ Web Tương tác 60fps & Server Localhost port 8888.                │
│ 5. Bộ Launchers 1-Click: Pipeline test, Mở biểu đồ Web, Mở Pine Script.    │
│ 6. Cẩm nang cấu hình OpenAI Codex / ChatGPT Custom GPTs.                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## II. HƯỚNG DẪN 3 BƯỚC DÀNH CHO NGƯỜI NHẬN WORKSPACE

### Bước 1: Tải về và Cài đặt Thư viện
Mở Terminal (Command Prompt / PowerShell trên Windows hoặc Terminal trên macOS/Linux) và chạy:

```bash
git clone https://github.com/hoang050205-dot/agy-investment-agent.git
cd agy-investment-agent
pip install -r requirements.txt
```

### Bước 2: Khởi chạy và Kiểm thử 1-Click (Không cần cấu hình)
- **Trên Windows (1-Click):** Nhấp đúp vào `CHAY_KIEM_THU_TOAN_BO_PIPELINE.bat`.
- **Dòng lệnh (Mọi hệ điều hành):**
  ```bash
  python run_full_investment_pipeline.py
  ```
- **Kết quả:** Hệ thống tự động phân tích BCTC, tính định giá DCF, đếm sóng Elliott, quét Screener và xuất toàn bộ file vào `outputs/investment/`.

### Bước 3: Xem Biểu Đồ Web & Cài Đặt Lên TradingView
- **Xem Biểu đồ Web Master:** Nhấp đúp `MO_BIEU_DO_WEB.bat` (hoặc chạy `python server_investment_charts.py` rồi mở `http://localhost:8888/chart_scenario_interactive_MASTER.html`).
- **Dùng trên TradingView:** Nhấp đúp `MO_TRADINGVIEW_PINE_EDITOR.bat` $\implies$ Mã Pine Script v6 tự động nạp vào Clipboard, người dùng chỉ việc mở TradingView và ấn `Ctrl + V` vào Pine Editor.

---

## III. HƯỚNG DẪN CẤU HÌNH ĐỂ OPENAI CODEX & CHATGPT HOẠT ĐỘNG NHƯ ANTIGRAVITY

Để OpenAI Codex, ChatGPT Plus (Custom GPTs), hoặc Cursor IDE có thể hiểu được toàn bộ logic:

### 1. Cấu hình Custom GPT trên ChatGPT Plus / Team
1. Vào ChatGPT $\to$ **Explore GPTs** $\to$ **Create** $\to$ Chọn tab **Configure**.
2. **Name:** `AGY Investment Agent Pro`
3. **Instructions:** Copy nội dung từ file `CODEX_SYSTEM_PROMPT.txt` (hoặc Mục III trong `CODEX_CHATGPT_INSTRUCTIONS.md`) dán vào.
4. **Knowledge:** Nạp file nén zip hoặc các thư mục `.agents/skills/` và `knowledge-base/AGY_Fsen_Elliott_Scanner.pine`.
5. **Capabilities:** Bắt buộc tích chọn **Code Interpreter & Data Analysis**.

### 2. Sử dụng với OpenAI Codex / Claude Code / Cursor IDE
Khi bạn mở thư mục này trong Cursor IDE hoặc VS Code:
- Codex và Copilot sẽ tự động đọc file `.github/copilot-instructions.md` và `.agents/rules/AGENTS.md`.
- Các câu lệnh mẫu bạn có thể hỏi ngay:
  * *"Hãy đếm sóng và dự báo tương lai 3 thành tố cho XAUUSD"* $\implies$ AI sẽ gọi `wave_analyzer_engine.py`.
  * *"Hãy chạy sàng lọc cổ phiếu và tính Combined Score"* $\implies$ AI sẽ gọi `invest_screener_engine.py`.
  * *"Hãy xuất báo cáo định giá đôi cho FPT"* $\implies$ AI sẽ gọi `export_valuation_word.py`.

---

## IV. BẢNG ĐỐI CHIẾU AN TOÀN & BẢO MẬT (SECURITY AUDIT)

| Tiêu chí bảo mật | Kết quả kiểm tra | Ghi chú kỹ thuật |
| :--- | :---: | :--- |
| **Tên cá nhân người dùng** | **SẠCH 100% (0 kết quả)** | Định danh bằng `AGY Investment Team` / `AGY Analyst`. |
| **Đường dẫn ổ đĩa tuyệt đối** | **SẠCH 100% (0 kết quả)** | 100% code dùng `Path(__file__).resolve().parent`. |
| **Thông tin tài khoản, API Token** | **SẠCH 100% (0 kết quả)** | Không chứa bất kỳ API key hay số điện thoại nào. |
| **Dữ liệu nến mẫu đi kèm** | **AN TOÀN** | Chỉ bao gồm nến giá công khai (VND, FPT, SIP, BTCUSD, XAUUSD). |
| **Tính độc lập (Portability)** | **ĐẠT 100%** | Chạy độc lập trên mọi hệ điều hành (Windows, macOS, Linux). |
