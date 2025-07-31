@echo off
title Power BI Report Merger - Security Enhanced Edition
color 0A

echo.
echo ================================================
echo   POWER BI REPORT MERGER - SECURITY ENHANCED
echo   Built by Reid Havens of Analytic Endeavors
echo   Website: https://www.analyticendeavors.com
echo ================================================
echo.
echo 🔒 Enhanced with comprehensive security audit logging
echo 📊 Professional-grade Power BI report consolidation
echo 🌐 Enterprise-ready architecture
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again.
    echo.
    echo Visit: https://python.org/downloads
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ ERROR: main.py not found
    echo Please ensure all files are present.
    pause
    exit /b 1
)

REM Check if core components exist
if not exist "ui\merger_ui.py" (
    echo ❌ ERROR: ui\merger_ui.py not found
    echo Please ensure all components are present.
    pause
    exit /b 1
)

echo 🔐 Initializing security context...
echo 📊 Loading business intelligence components...
echo 🎨 Preparing professional user interface...
echo.

REM Run the security-enhanced application
python main.py

REM Check if application ran successfully
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Application encountered an error
    echo Check the console output above for details.
    echo.
    echo 📞 For support, visit: https://www.analyticendeavors.com
    pause
    exit /b 1
)

echo.
echo ✅ Power BI Report Merger session completed!
echo 🌐 Visit us at: https://www.analyticendeavors.com
echo 🔒 Security logs saved to: %%USERPROFILE%%\AppData\Local\AnalyticEndeavors\Logs
pause
