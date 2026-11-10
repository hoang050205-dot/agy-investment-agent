@echo off
chcp 65001 > nul
title AGY Investment Agent - Push to GitHub
echo ===============================================================================
echo [AGY INVEST] ĐỒNG BỘ TOÀN BỘ WORKSPACE LÊN GITHUB REPOSITORY
echo Repo: https://github.com/hoang050205-dot/agy-investment-agent.git
echo ===============================================================================
echo.

set REPO_URL=https://github.com/hoang050205-dot/agy-investment-agent.git

echo [*] Đang kiểm tra cấu hình Git Remote...
git remote remove origin > nul 2>&1
git remote add origin %REPO_URL%
git branch -M main

echo [*] Đang thực hiện git push lên GitHub main branch...
echo [*] Lưu ý: Trình duyệt hoặc cửa sổ Git Credential Manager có thể sẽ hiện lên 
echo     để bạn xác thực tài khoản GitHub (1-Click OAuth). Hãy bấm "Authorize"!
echo.

git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ===============================================================================
    echo [THÀNH CÔNG 100%] Toàn bộ hệ thống AGY Investment Agent đã được đẩy lên GitHub!
    echo Bạn có thể truy cập repo tại: %REPO_URL%
    echo Người nhận chỉ cần git clone %REPO_URL% là dùng được ngay!
    echo ===============================================================================
) else (
    echo.
    echo ===============================================================================
    echo [LỖI HOẶC CẦN TOKEN XÁC THỰC]
    echo Nếu cửa sổ trình duyệt không tự mở hoặc xác thực thất bại:
    echo 1. Hãy tạo Personal Access Token tại: https://github.com/settings/tokens/new (quyền 'repo')
    echo 2. Sau đó chạy lệnh sau trong PowerShell:
    echo    git push https://<TOKEN_CUA_BAN>@github.com/hoang050205-dot/agy-investment-agent.git main
    echo ===============================================================================
)

echo.
pause

