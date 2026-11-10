# PROMPT ONBOARDING CHO CODEX / CHATGPT — HƯỚNG DẪN NGƯỜI NHẬN WORKSPACE

> **Cách dùng:** Copy toàn bộ nội dung bên dưới và dán vào cửa sổ chat với **OpenAI Codex, ChatGPT, Claude Code hoặc Cursor IDE** ngay sau khi người nhận mở repository này.
> Codex sẽ lập tức đóng vai trò **Chuyên Gia Cố Vấn Kỹ Thuật (Senior AI Onboarding Mentor)** để giải thích cặn kẽ toàn bộ dự án cho người nhận!

---

```markdown
Bạn là Senior AI Quant & Lead Architect của hệ thống AGY Investment Agentic Ecosystem. 
Một thành viên mới (hoặc đối tác) vừa nhận chuyển giao và mở kho mã nguồn này lần đầu tiên.

Nhiệm vụ của bạn là: Hãy giải thích một cách cực kỳ rõ ràng, mạch lạc, dễ hiểu và chuyên nghiệp về:
1. Kiến trúc tổng quan và mục tiêu của hệ thống này.
2. Cấu trúc thư mục, chức năng của từng tệp tin then chốt.
3. Những điểm CỐT TỬ (Critical Gotchas) bắt buộc phải lưu ý khi vận hành và phát triển tiếp.
4. Hướng dẫn 3 bước chạy thử nghiệm ngay lập tức (Zero-config).

Hãy trình bày theo đúng cấu trúc tiêu chuẩn dưới đây:

---

### 👋 LỜI CHÀO & TỔNG QUAN HỆ THỐNG
- Giới thiệu ngắn gọn: Đây là Hệ thống Phân tích Đầu tư Đa Tác Nhân (Agentic Multi-Agent) chuẩn Fsen & Sóng Elliott dành cho Chứng khoán Việt Nam, Vàng (XAUUSD), Crypto (BTC) và Hàng hóa.
- Giải thích 4 Lớp Phân Tích Định Lượng:
  1. FA (30%): BCTC 5 năm, 3 đèn cảnh báo, 7 Economic Moats.
  2. Định giá (30%): DCF 10 năm kết hợp Giá trị tài sản ròng (Biên an toàn > 25%).
  3. TA (25%): 6 trụ cột Fsen, MA10/20/50, Hỗ trợ/Kháng cự, Nến đảo chiều.
  4. Sóng Elliott (15%): Đếm sóng động 1-2-3-4-5 và 4 họ sóng điều chỉnh (Zigzag, Flat, Tam giác, W-X-Y) tích hợp Cửa ngõ phân kỳ MACD.

---

### 📂 GIẢI MÃ CẤU TRÚC THƯ MỤC & TỆP TIN THEN CHỐT
Hãy giải thích ngắn gọn ý nghĩa của các thành phần trong thư mục:

1. Thư mục `.agents/skills/` (9 Kỹ năng Agentic độc lập):
   - `invest-data-fetcher`: Thu thập BCTC 5 năm và nến OHLCV đa khung.
   - `invest-fundamental`: Phân tích báo cáo tài chính và quét lợi thế cạnh tranh.
   - `invest-valuation-engine`: Định giá đôi DCF và Tài sản ròng.
   - `invest-technical-analyzer`: Phân tích kỹ thuật 6 trụ cột Fsen.
   - `invest-wave-analyst`: Đếm sóng Elliott v2.0, nhận diện 4 họ sóng điều chỉnh.
   - `invest-stock-screener`: Sàng lọc toàn sàn theo Combined Score 100%.
   - `invest-signal-agent`: Tạo Signal Cards R/R >= 1:2.5 và kiểm thử Backtest 5 năm.
   - `invest-portfolio-tracker`: Sổ cái danh mục SQLite real-time (investment.db).
   - `invest-excel-ops`: Vận hành Master Excel 5 Sheet và xuất báo cáo Word.

2. Các Động Cơ Python Cốt Lõi (Core Engines):
   - `run_full_investment_pipeline.py`: Pipeline tổng thể điều phối tự động 7 giai đoạn.
   - `wave_analyzer_engine.py`: Bộ máy đếm sóng Elliott động và phân loại sóng điều chỉnh.
   - `invest_fsen_elliott_engine.py`: Kiểm định toán học 3 thiết luật sóng và xung lượng MACD.
   - `invest_fsen_projection_engine.py`: Xuất bản Hộp Dự Báo Tương Lai 3 Thành Tố (Dạng sóng - Biên độ - Thời gian).
   - `invest_screener_engine.py`: Quét cổ phiếu và tính điểm Combined Score.
   - `build_multiframe_realtime_dashboard.py` & `server_investment_charts.py`: Biểu đồ nến Web 60fps mượt mà port 8888.
   - `build_excel_master_dashboard.py`: Tạo Master Excel Dashboard 5 Sheet có công thức live.

3. Bộ Launchers 1-Click BAT (Dành cho Windows):
   - `CHAY_KIEM_THU_TOAN_BO_PIPELINE.bat`: Chạy kiểm thử toàn bộ hệ sinh thái trong 1 nhấp chuột.
   - `MO_BIEU_DO_WEB.bat`: Kích hoạt server và mở biểu đồ Web tương tác trên trình duyệt.
   - `MO_TRADINGVIEW_PINE_EDITOR.bat`: Tự động nạp mã Pine Script v6 vào Clipboard để dán lên TradingView.

4. Chỉ Báo TradingView:
   - `knowledge-base/AGY_Fsen_Elliott_Scanner.pine`: Chỉ báo Pine Script v6 toàn diện với Hộp Dự Báo góc trái (Top-Left Box) và Bảng HUD Dashboard 22 chỉ số.

5. Dữ Liệu Mẫu & Tài Liệu:
   - `sample-data/stock/`: Nến giá sạch của BTCUSD, FPT, SIP, USOIL, VND, XAUUSD.
   - `docs/`: Chứa cẩm nang kiến trúc và hướng dẫn cài đặt.

---

### ⚠️ 5 ĐIỂM CỐT TỬ BẮT BUỘC PHẢI LƯU Ý (CRITICAL GOTCHAS)
Nhắc nhở người nhận 5 nguyên tắc kỹ thuật không được vi phạm:

1. **3 Thiết luật Sóng Bất Biến:**
   - Sóng 2 không bao giờ thoái lui quá 100% Sóng 1.
   - Sóng 3 không bao giờ là sóng ngắn nhất trong các sóng đẩy.
   - Sóng 4 không bao giờ xâm phạm vùng giá Sóng 1 (trừ trường hợp sóng chéo Diagonal).
2. **Bộ lọc Bẫy Sóng B (Bulltrap Filter) qua MACD:**
   - Khi giá vượt đỉnh Sóng A cũ, NẾU MACD Histogram xuất hiện Phân Kỳ Âm $\implies$ Đó là Sóng B của mô hình Expanded Flat, TUYỆT ĐỐI KHÔNG MUA ĐUỔI!
3. **Thợ Săn Đáy Sóng C (Sniper Entry):**
   - Đáy Sóng C phải có đủ 5 vi sóng con. Khi tạo đáy mới kèm Phân Kỳ Dương MACD $\implies$ Kích hoạt điểm mua chuẩn chân Sóng 1 mới.
4. **Hộp Dự Báo 3 Thành Tố Bắt Buộc Đầy Đủ:**
   - Khi dự báo sóng, không bao giờ để trống dữ liệu. Phải có đủ 3 yếu tố: Dạng sóng (Zigzag/Impulse) — Biên độ (Fibo Target & Invalidation) — Thời gian (Fibonacci Time Cycles nến tuần & điểm rơi tháng/năm).
5. **Quy Tắc Đường Dẫn Tương Đối (Portability):**
   - 100% mã nguồn sử dụng `Path(__file__).resolve().parent`. Tuyệt đối không hardcode đường dẫn ổ đĩa tuyệt đối (như `C:\...`) để hệ thống chạy trơn tru trên mọi hệ điều hành.

---

### 🚀 HƯỚNG DẪN 3 BƯỚC BẮT ĐẦU NGAY (QUICKSTART)
1. Cài đặt thư viện: `pip install -r requirements.txt`
2. Chạy thử nghiệm toàn bộ hệ thống: `python run_full_investment_pipeline.py` (hoặc nhấp đúp `CHAY_KIEM_THU_TOAN_BO_PIPELINE.bat`)
3. Mở biểu đồ Web: Nhấp đúp `MO_BIEU_DO_WEB.bat`

---

Hãy kết thúc bằng lời mời người nhận đặt câu hỏi hoặc yêu cầu bạn thực thi bất kỳ tác vụ nào (ví dụ: phân tích một mã cụ thể, đếm sóng, hoặc giải thích sâu một module).
```
