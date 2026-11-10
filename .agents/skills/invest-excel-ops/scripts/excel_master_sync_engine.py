"""
excel_master_sync_engine.py
Bộ máy Điều Phối Tự Động Hóa Hệ Thống Master Excel, Báo Cáo Word & BI Dashboard (No-Web Suite)
1. Cập nhật số liệu từ SQLite (knowledge-base/investment.db)
2. Tái tạo 5 Sheet Master Excel Dashboard (Excel_Master_Investment_Dashboard.xlsx)
3. Tái xuất bản Hồ Sơ Thẩm Định Doanh Nghiệp Word (Bao_Cao_Phan_Tich_Doanh_Nghiep_Master.docx)
4. Tái xuất bản Executive BI Dashboard HTML Glassmorphism 60fps (Investment_BI_Executive_Dashboard.html)
"""

import os
import sys
import subprocess
from datetime import datetime

PYTHON_EXE = r"C:\Users\ADMIN\.venv\Scripts\python.exe"

def run_sync_pipeline():
    print("=" * 65)
    print("🚀 BẮT ĐẦU ĐỒNG BỘ HỆ THỐNG MASTER EXCEL, WORD & BI DASHBOARD")
    print("=" * 65)
    
    # 1. Cập nhật Master Excel Dashboard 5 Sheets
    print("\n[*] Bước 1: Khởi tạo & Cập nhật Master Excel Dashboard (5 Sheets)...")
    res1 = subprocess.run([PYTHON_EXE, "build_excel_master_dashboard.py"], capture_output=True, text=True)
    if res1.returncode != 0:
        print(f"[!] Lỗi khi chạy build_excel_master_dashboard.py:\n{res1.stderr}")
        return False
    print(res1.stdout.strip())

    # 2. Xuất bản Hồ sơ Báo Cáo Word Chuyên Sâu
    print("\n[*] Bước 2: Xuất bản Hồ Sơ Báo Cáo Doanh Nghiệp Word Chuẩn Corporate...")
    res2 = subprocess.run([PYTHON_EXE, "export_enterprise_investment_dossier.py"], capture_output=True, text=True)
    if res2.returncode != 0:
        print(f"[!] Lỗi khi chạy export_enterprise_investment_dossier.py:\n{res2.stderr}")
        return False
    print(res2.stdout.strip())

    # 3. Xuất bản Executive BI Dashboard HTML
    print("\n[*] Bước 3: Xuất bản Executive BI Dashboard HTML Glassmorphism 60fps...")
    res3 = subprocess.run([PYTHON_EXE, "export_investment_bi_dashboard.py"], capture_output=True, text=True)
    if res3.returncode != 0:
        print(f"[!] Lỗi khi chạy export_investment_bi_dashboard.py:\n{res3.stderr}")
        return False
    print(res3.stdout.strip())

    print("\n" + "=" * 65)
    print("✅ HOÀN TẤT ĐỒNG BỘ 100% TOÀN BỘ HỆ THỐNG MASTER EXCEL, WORD & BI HTML!")
    print("📁 Tệp Excel: outputs/investment/Excel_Master_Investment_Dashboard.xlsx")
    print("📁 Tệp Word:  outputs/investment/Bao_Cao_Phan_Tich_Doanh_Nghiep_Master.docx")
    print("📁 Tệp BI:    outputs/investment/Investment_BI_Executive_Dashboard.html")
    print("=" * 65)
    return True

if __name__ == "__main__":
    run_sync_pipeline()
