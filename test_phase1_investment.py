"""
Test Phase 1 Investment Pipeline — Kiểm thử thực nghiệm Phase 1
Chạy trọn gói: Thu thập dữ liệu -> Phân tích BCTC & Moat -> Định giá đôi (DCF & Tài sản)
Đối soát với tài liệu gốc QUY TRÌNH ĐỊNH GIÁ CỔ PHIẾU SIP.docx
"""

import os
import sys
import json
import subprocess
from datetime import datetime

PYTHON_EXE = os.path.expandvars(r"$HOME\.venv\Scripts\python.exe")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd_list):
    res = subprocess.run(cmd_list, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        print("Lỗi thực thi:", res.stderr)
    return res.stdout

def generate_markdown_report(symbol, profile, fundamental, valuation, out_path):
    moat = fundamental.get("economic_moat", {})
    warn = fundamental.get("warnings", {})
    asset = valuation.get("asset_valuation", {})
    dcf = valuation.get("dcf_valuation", {})

    tv_symbol = f"BINANCE:{symbol}T" if "BTC" in symbol else (f"OANDA:{symbol}" if "XAU" in symbol else f"HOSE:{symbol}")
    tv_url = f"https://www.tradingview.com/chart/?symbol={tv_symbol}"
    tv_layout_url = f"https://www.tradingview.com/chart/iboM2olW/?symbol={tv_symbol}"
    chart_png = f"chart_scenario_{symbol}_pro.png"
    chart_html = f"chart_scenario_{symbol}.html"

    content = f"""# BÁO CÁO THẨM ĐỊNH BCTC & ĐỊNH GIÁ CỔ PHIẾU {symbol}
**Ngày phân tích:** {datetime.now().strftime('%d/%m/%Y')}  
**Doanh nghiệp:** {profile.get('name', symbol)}  
**Phương pháp:** AI Investment Agent (Khung chuẩn Fsen & Định Giá Nội Bộ)

---

> ### 📊 TRUY CẬP BIỂU ĐỒ 1-CLICK (CHART ACCESS)
> - 🚀 **[MỞ BIỂU ĐỒ TRỰC TIẾP TRÊN TRADINGVIEW (LIVE REAL-TIME ↗)]({tv_url})** — *Nhấp để mở ngay đồ thị nến Real-time tích hợp bộ chỉ báo AGY Wave Pro!*
> - 🖥️ **[MỞ TRÊN GIAO DIỆN CÁ NHÂN HOANG050205 TRADINGVIEW ↗]({tv_layout_url})** — *Mở trực tiếp layout cá nhân đã lưu.*
> - 📈 **[MỞ BIỂU ĐỒ KỊCH BẢN NỘI BỘ (HTML INTERACTIVE ↗)]({chart_html})** — *Xem mô hình nến, sóng và kênh giá offline.*
> - 🖼️ **[XEM ẢNH BIỂU ĐỒ NẾN ĐỘ PHÂN GIẢI CAO 4K (PNG ↗)]({chart_png})**

---

## 1. THÔNG TIN CƠ BẢN DOANH NGHIỆP
- **Mã chứng khoán:** `{symbol}`
- **Ngành nghề:** {profile.get('industry', 'N/A')}
- **Giá thị trường hiện tại:** {profile.get('current_price', 0):,.0f} VND ({valuation.get('asset_valuation', {}).get('inputs', {}).get('current_price_k', 0):.2f} nghìn đồng)
- **Vốn hóa thị trường:** {profile.get('market_cap', 0)/1e9:,.1f} tỷ đồng
- **Số cổ phiếu lưu hành:** {profile.get('shares_outstanding', 0)/1e6:,.2f} triệu cổ phiếu
- **Chỉ số thị trường:** P/E = {profile.get('pe', 'N/A')} | P/B = {profile.get('pb', 'N/A')} | ROE = {profile.get('roe', 0):.2f}% | ROA = {profile.get('roa', 0):.2f}%

---

## 2. PHÂN TÍCH BCTC & HỆ THỐNG 3 ĐÈN CẢNH BÁO

### 📑 A. Bảng Cân Đối Kế Toán
"""
    for w in warn.get("balance_sheet", []):
        icon = "🔴" if w['status'] == "RED" else ("🟢" if "GREEN" in w['status'] else "🟡")
        content += f"- {icon} **{w['metric']}:** {w['value']} (Chuẩn: {w['threshold']}) — *{w['message']}*\n"

    content += """
### 📑 B. Báo Cáo Kết Quả Kinh Doanh
"""
    for w in warn.get("income_statement", []):
        icon = "🔴" if w['status'] == "RED" else ("🟠" if w['status'] == "ORANGE" else "🟢")
        content += f"- {icon} **{w['metric']}:** {w['value']} (Chuẩn: {w['threshold']}) — *{w['message']}*\n"

    content += """
### 📑 C. Báo Cáo Lưu Chuyển Tiền Tệ
"""
    for w in warn.get("cash_flow", []):
        icon = "🔴" if w['status'] == "RED" else "🟢"
        content += f"- {icon} **{w['metric']}:** {w['value']} (Chuẩn: {w['threshold']}) — *{w['message']}*\n"

    content += f"""
### 🏰 D. Lợi Thế Cạnh Tranh Lâu Bền (Economic Moat)
- **Xếp hạng:** **{moat.get('classification', 'N/A')}** ({moat.get('moats_count', 0)} lợi thế được nhận diện)
"""
    for m in moat.get("details", []):
        content += f"- 🛡️ **{m['name']}:** {m['evidence']}\n"

    content += f"""
---

## 3. KẾT QUẢ ĐỊNH GIÁ ĐÔI (INTRINSIC VALUATION)

### 🏢 Phương Pháp 1: Định Giá Tài Sản Ròng (Bóc Tách Nợ Chiếm Dụng)
*Áp dụng tri thức thực tiễn từ tài liệu QT DG TS AI.docx:*
- **Tổng tài sản:** {asset.get('inputs', {}).get('total_assets_bil', 0):,.2f} tỷ đồng
- **Tổng nợ phải trả:** {asset.get('inputs', {}).get('total_liabilities_bil', 0):,.2f} tỷ đồng
- **Nợ chiếm dụng (Doanh thu chưa thực hiện & Người mua trả trước):** {asset.get('inputs', {}).get('unearned_advances_bil', 0):,.2f} tỷ đồng
- **Nợ tính lại (Nợ chịu lãi thực tế):** {asset.get('recalculated_debt_bil', 0):,.2f} tỷ đồng
- **Giá trị doanh nghiệp:** {asset.get('enterprise_value_bil', 0):,.2f} tỷ đồng
- **👉 Giá trị thực trên một cổ phiếu:** **{asset.get('intrinsic_value_per_share', 0):.2f} nghìn đồng**
- **👉 Biên an toàn (Margin of Safety):** **{asset.get('margin_of_safety_pct', 0):.2f}%**
- **Kết luận:** {asset.get('recommendation', '')}

### 📈 Phương Pháp 2: Chiết Khấu Dòng Tiền 10 Năm (DCF)
*Áp dụng tri thức từ tài liệu QT DG AI.docx (Lạm phát 7%, Chiết khấu 10%):*
- **Tốc độ tăng trưởng đề xuất:** {dcf.get('growth_rates', {}).get('g_proposed', 0)*100:.2f}%
- **Tốc độ tăng trưởng ước tính:** {dcf.get('growth_rates', {}).get('g_estimated', 0)*100:.2f}%/năm
- **Tổng giá trị hiện tại dòng tiền (EV):** {dcf.get('enterprise_value_bil', 0):,.2f} tỷ đồng
- **👉 Giá trị thực trên một cổ phiếu:** **{dcf.get('intrinsic_value_per_share', 0):.2f} nghìn đồng**
- **👉 Biên an toàn (Margin of Safety):** **{dcf.get('margin_of_safety_pct', 0):.2f}%**
- **Kết luận:** {dcf.get('recommendation', '')}

---

## 4. TỔNG KẾT KHUYẾN NGHỊ & HÀNH ĐỘNG
- **Đánh giá tổng hợp:** **{valuation.get('final_recommendation', '')}**
- **Nguyên tắc cốt lõi:** *"Chỉ vào lệnh khi có xác nhận bởi yếu tố Chu kỳ VÀ Sóng."*
- **Bước tiếp theo (Phase 2):** Chuyển sang Trạm Phân Tích Kỹ Thuật 6 Trụ Cột và Đếm Sóng Elliott để tìm vùng giải ngân tối ưu!
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    os.makedirs("outputs/investment", exist_ok=True)
    symbols = ["SIP", "FPT"]

    for sym in symbols:
        print(f"\n=======================================================")
        print(f"🚀 BẮT ĐẦU CHẠY PIPELINE PHASE 1 CHO MÃ: {sym}")
        print(f"=======================================================")

        # 1. Fetch data
        print(f"[1/3] Thu thập dữ liệu {sym}...")
        fetch_script = os.path.join(BASE_DIR, ".agents", "skills", "invest-data-fetcher", "scripts", "fetch_stock_data.py")
        run_cmd([PYTHON_EXE, fetch_script, "--symbol", sym])

        # 2. Analyze fundamental
        print(f"[2/3] Phân tích BCTC 5 năm & Moat {sym}...")
        fund_script = os.path.join(BASE_DIR, ".agents", "skills", "invest-fundamental", "scripts", "analyze_fundamental.py")
        run_cmd([PYTHON_EXE, fund_script, "--symbol", sym])

        # 3. Valuation
        print(f"[3/3] Tính toán định giá đôi (DCF & Tài sản) {sym}...")
        val_script = os.path.join(BASE_DIR, ".agents", "skills", "invest-valuation-engine", "scripts", "calculate_valuation.py")
        run_cmd([PYTHON_EXE, val_script, "--symbol", sym])

        # 4. Generate report
        data_dir = os.path.join(BASE_DIR, "sample-data", "stock", sym)
        with open(os.path.join(data_dir, "profile.json"), "r", encoding="utf-8") as f:
            profile = json.load(f)
        with open(os.path.join(data_dir, "fundamental_analysis.json"), "r", encoding="utf-8") as f:
            fundamental = json.load(f)
        with open(os.path.join(data_dir, "valuation_result.json"), "r", encoding="utf-8") as f:
            valuation = json.load(f)

        report_path = os.path.join(BASE_DIR, "outputs", "investment", f"valuation_report_{sym}.md")
        generate_markdown_report(sym, profile, fundamental, valuation, report_path)
        print(f"[SUCCESS] Đã xuất bản báo cáo hoàn chỉnh: outputs/investment/valuation_report_{sym}.md")

        # Đối soát với mã chuẩn SIP
        if sym == "SIP":
            asset_val = valuation["asset_valuation"]["intrinsic_value_per_share"]
            mos = valuation["asset_valuation"]["margin_of_safety_pct"]
            print(f"\n🎯 KẾT QUẢ ĐỐI SOÁT VỚI TÀI LIỆU GỐC CỦA HOÀNG (MÃ SIP):")
            print(f"   • Giá trị thực tính được: {asset_val} nghìn đồng (Tài liệu gốc: 81.28)")
            print(f"   • Biên an toàn tính được: {mos}% (Tài liệu gốc: 32.59%)")
            assert abs(asset_val - 81.28) < 0.05, "Sai lệch giá trị thực SIP!"
            assert abs(mos - 32.59) < 0.05, "Sai lệch biên an toàn SIP!"
            print(f"   ✅ ĐỐI SOÁT CHÍNH XÁC 100% VỚI BẢNG TÍNH GỐC CỦA HOÀNG!")

    print(f"\n✨ TOÀN BỘ PIPELINE PHASE 1 ĐÃ HOÀN TẤT THÀNH CÔNG VÀ CHÍNH XÁC!")

if __name__ == "__main__":
    main()

