@echo off
echo ========================================
echo    TMEN SIEM - Starting System
echo ========================================
echo.

echo Step 1: Navigating to wazuh folder...
cd wazuh

echo Step 2: Running TMEN SIEM...
call run_tmen_siem.bat

echo.
echo ========================================
echo    TMEN SIEM Started Successfully!
echo ========================================
pause 