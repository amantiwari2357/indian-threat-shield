@echo off
echo ========================================
echo    TMEN SIEM - Real-time System
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

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Start the backend server
echo.
echo Starting TMEN SIEM Backend Server on http://localhost:5000
echo.
start "TMEN SIEM Backend" python tmen_siem_backend.py

REM Wait a moment for the server to start
timeout /t 3 /nobreak >nul

            REM Open the frontend in default browser
            echo Opening TMEN SIEM Frontend...
            start "" "tmen_siem_complete.html"

echo.
echo ========================================
echo    TMEN SIEM is now running!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Frontend: tmen_siem_dashboard.html
echo.
echo Press any key to stop the backend server...
pause

REM Stop the backend server
taskkill /f /im python.exe >nul 2>&1
echo.
echo TMEN SIEM stopped.
pause 