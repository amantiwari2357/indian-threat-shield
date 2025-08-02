@echo off
echo ========================================
echo    TMEN SIEM - Security Information and Event Management
echo ========================================
echo.
echo Starting TMEN SIEM Backend Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
pip install -r requirements.txt

REM Start the backend server
echo.
echo 🚀 Starting TMEN SIEM Backend Server...
echo 📍 Backend API: http://localhost:5000
echo 📊 Frontend: Open tmen_siem_simple.html in your browser
echo.
echo 🔧 API Endpoints:
echo    - GET  /api/system/metrics
echo    - GET  /api/logs
echo    - POST /api/logs/generate
echo    - GET  /api/alerts
echo    - GET  /api/network/threats
echo    - GET  /api/files/integrity
echo    - GET  /api/agents
echo    - GET  /api/rules
echo    - GET  /api/dashboard/overview
echo.
python tmen_siem_backend.py

pause 