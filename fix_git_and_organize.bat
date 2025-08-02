@echo off
echo ========================================
echo    TMEN SIEM - Git Organization Fix
echo ========================================
echo.

echo Step 1: Removing Git submodule tracking...
git rm --cached wazuh
if exist wazuh\.git (
    echo Removing embedded Git repository...
    rmdir /s /q wazuh\.git
)

echo Step 2: Adding wazuh folder as regular files...
git add wazuh/

echo Step 3: Committing the organized structure...
git commit -m "Organize TMEN SIEM files in wazuh folder - Remove submodule tracking"

echo Step 4: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo    Organization Complete!
echo ========================================
echo.
echo All TMEN SIEM files are now organized in the wazuh folder:
echo - tmen_siem_dashboard.html (Main dashboard)
echo - tmen_siem_backend.py (Backend API)
echo - requirements.txt (Python dependencies)
echo - run_tmen_siem.bat (Startup script)
echo - README_TMEN_SIEM.md (Documentation)
echo.
echo To run the system:
echo 1. Navigate to wazuh folder: cd wazuh
echo 2. Run: run_tmen_siem.bat
echo.
pause 