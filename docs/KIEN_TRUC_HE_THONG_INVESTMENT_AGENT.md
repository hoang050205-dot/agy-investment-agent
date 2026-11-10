# ĐẶC TẢ KIẾN TRÚC HỆ THỐNG AGY INVESTMENT AGENT

> **Hệ sinh thái:** AGY Investment Agentic Ecosystem  
> **Kiến trúc:** Multi-Agent System (MAS) kết hợp Human-in-the-Loop Gate  
> **Phương pháp luận:** Chuẩn đầu tư Fsen & Định giá Tài chính Doanh nghiệp

---

## I. MÔ THỨC PHÂN TÍCH 4 LỚP ĐỊNH LƯỢNG (COMBINED SCORE)

Hệ thống sàng lọc và thẩm định tài sản dựa trên trọng số chuẩn hóa 100%:

$$\text{Combined Score} = 30\% \times \text{FA} + 30\% \times \text{Valuation} + 25\% \times \text{TA} + 15\% \times \text{Wave}$$

```mermaid
graph TD
    subgraph Lớp 1: Phân Tích Cơ Bản (FA 30%)
        FA1["3 Hệ thống đèn cảnh báo BCTC (CĐKT, KQKD, LCTT)"]
        FA2["Nhận diện 7 Lợi thế cạnh tranh bền vững (Economic Moat)"]
    end

    subgraph Lớp 2: Định Giá Đôi (Valuation 30%)
        VAL1["Định giá Chiết khấu Dòng tiền (DCF 10 năm)"]
        VAL2["Định giá Giá trị Tài sản Ròng (Net Asset Value)"]
        VAL3["Biên An Toàn (Margin of Safety >= 25%)"]
    end

    subgraph Lớp 3: Phân Tích Kỹ Thuật (TA 25%)
        TA1["6 Trụ cột Fsen (Đỉnh đáy, Hỗ trợ/Kháng cự, Kênh giá)"]
        TA2["Hệ thống MA10 / MA20 / MA50 & Nến đảo chiều"]
        TA3["Chỉ báo động lượng RSI & MACD"]
    end

    subgraph Lớp 4: Sóng Elliott & Chu Kỳ (Wave 15%)
        W1["5 Sóng Đẩy (1-2-3-4-5) & 4 Họ Sóng Điều Chỉnh (Zigzag, Flat, Triangle, WXY)"]
        W2["Bộ lọc Bẫy Sóng B Bulltrap (Phân kỳ âm MACD)"]
        W3["Thợ săn Đáy Sóng C (Phân kỳ dương MACD)"]
        W4["Hộp Dự Báo 3 Thành Tố (Dạng Sóng - Biên Độ - Thời Gian)"]
    end

    Lớp 1 --> Screener["STOCK SCREENER ENGINE<br>Xếp hạng Combined Score toàn thị trường"]
    Lớp 2 --> Screener
    Lớp 3 --> Screener
    Lớp 4 --> Screener

    Screener --> Signal["SIGNAL AGENT<br>Tạo Signal Card R/R >= 1:2.5"]
    Signal --> Gate["HUMAN CHECKPOINT GATE<br>Nhà đầu tư phê duyệt lệnh"]
    Gate --> Ledger["PORTFOLIO TRACKER<br>Sổ cái SQLite & Quản trị rủi ro"]
    Ledger --> Master["EXCEL & WEB MASTER OPS<br>Master Excel 5 Sheet & Web Interactive 60fps"]
```

---

## II. DANH SÁCH 9 TRẠM AGENT & VAI TRÒ CHUYÊN BIỆT

| STT | Trạm Agent | Tên Skill | Chức năng nghiệp vụ chính |
| :---: | :--- | :--- | :--- |
| **1** | **Data Fetcher** | `invest:data-fetcher` | Thu thập dữ liệu tài chính BCTC 5 năm và nến OHLCV đa khung (W, D, 4H, 1H). |
| **2** | **Fundamental Analyzer** | `invest:fundamental-analyzer` | Quét 3 hệ thống đèn cảnh báo tài chính và nhận diện 7 lợi thế kinh tế (Economic Moats). |
| **3** | **Valuation Engine** | `invest:valuation-engine` | Tính toán định giá đôi (DCF 10 năm + Tài sản ròng bóc tách nợ chiếm dụng). |
| **4** | **Technical Analyzer** | `invest:technical-analyzer` | Phân tích 6 trụ cột kỹ thuật Fsen, cấu trúc xu hướng và các đường trung bình động. |
| **5** | **Wave Analyst v2.0 Pro** | `invest:wave-analyst` | Đếm 5 sóng đẩy và 4 họ sóng điều chỉnh, bắt bẫy Sóng B bulltrap và dự báo 3 thành tố. |
| **6** | **Stock Screener** | `invest:stock-screener` | Sàng lọc toàn thị trường theo 5 bộ presets và xếp hạng điểm số tổng hợp. |
| **7** | **Signal & Backtest** | `invest:signal-agent` | Tạo Signal Card chuẩn R/R $\ge 1:2.5$, chạy backtest kiểm thử xác suất thắng lịch sử. |
| **8** | **Portfolio Tracker** | `invest:portfolio-tracker` | Quản trị danh mục đầu tư trên SQLite, theo dõi NAV real-time và cảnh báo rủi ro. |
| **9** | **Excel & BI Ops** | `invest:excel-ops` | Xuất bản Master Excel 5 Sheet, Hồ sơ doanh nghiệp Word và Web Dashboard 60fps. |

---

## III. DÒNG DỮ LIỆU ĐỘNG (DATA FLOW PIPELINE)

1. **Giai đoạn Ingestion:** `sample-data/stock/{SYMBOL}/` nạp các tệp nến JSON hoặc gọi trực tiếp API chứng khoán qua `fetch_multiframe_data.py`.
2. **Giai đoạn Computation:**
   - `wave_analyzer_engine.py` tính toán đỉnh đáy Fractal, tỷ lệ Fibo và phân kỳ MACD.
   - `invest_fsen_projection_engine.py` dự phóng tương lai: $P_3, P_4, P_5, A, B, C$ và mốc thời gian Fibonacci Time $T_3, T_4, T_5, T_C$.
3. **Giai đoạn Synthesis & Export:**
   - `build_multiframe_realtime_dashboard.py` sinh `outputs/investment/chart_scenario_interactive_MASTER.html`.
   - `build_excel_master_dashboard.py` sinh `outputs/investment/Excel_Master_Investment_Dashboard.xlsx`.
   - `export_valuation_word.py` sinh các hồ sơ phân tích Word chuyên nghiệp `.docx`.

