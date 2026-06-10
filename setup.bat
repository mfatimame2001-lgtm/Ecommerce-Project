@echo off
echo ============================================
echo   ShopEase E-Commerce - Setup ^& Run
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

if not exist "venv" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/3] Virtual environment already exists, skipping...
)

echo [2/3] Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt --quiet

echo [3/3] Seeding demo data...
python seed.py

echo.
echo ============================================
echo   App is running at: http://127.0.0.1:8000
echo   Admin:  admin@shop.com / 1234567@
echo   Press Ctrl+C to stop the server
echo ============================================
echo.
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
