@echo off
chcp 65001 > nul
echo ===============================================================================
echo [AGY INVEST] ĐỒNG BỘ & PUSH LÊN GITHUB REPOSITORY RIÊNG
echo ===============================================================================
echo.
echo Bước 1: Hãy chắc chắn bạn đã vào https://github.com/new để tạo một repo mới trống
echo (Ví dụ tên repo: agy-investment-agent)
echo.
set /p REPO_URL="Nhập URL Repo của bạn (mặc định: https://github.com/hoang050205-dot/agy-investment-agent.git): "
if "%REPO_URL%"=="" (
    set REPO_URL=https://github.com/hoang050205-dot/agy-investment-agent.git
)

echo.
echo [*] Đang cấu hình Remote Origin: %REPO_URL%
git remote remove origin > nul 2>&1
git remote add origin %REPO_URL%
git branch -M main

echo [*] Đang đẩy toàn bộ mã nguồn lên GitHub...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ===============================================================================
    echo [THÀNH CÔNG 100%] Đã đẩy toàn bộ hệ thống AGY Investment Agent lên GitHub!
    echo Xem repo tại: %REPO_URL%
    echo ===============================================================================
) else (
    echo.
    echo ===============================================================================
    echo [HƯỚNG DẪN XỬ LÝ NẾU CẦN XÁC THỰC]
    echo Nếu GitHub yêu cầu Personal Access Token (PAT):
    echo 1. Vào https://github.com/settings/tokens/new
    echo 2. Chọn quyền 'repo' rồi bấm Generate Token
    echo 3. Nhập token vào cửa sổ Git Credential Manager khi được hỏi.
    echo ===============================================================================
)
pause
