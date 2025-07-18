@echo off
title ENHANCED POWER BI REPORT MERGER - ANALYTIC ENDEAVORS
color 0A

echo.
echo ================================================
echo   ENHANCED POWER BI REPORT MERGER v1.0
echo   Built by Reid Havens of Analytic Endeavors
echo   Website: https://www.analyticendeavors.com
echo ================================================
echo.
echo Professional-grade tool for intelligent PBIP report consolidation
echo.
echo Key Features:
echo - Enhanced user interface with professional branding
echo - Comprehensive help system and about dialog
echo - Smart conflict resolution and theme management
echo - Real-time progress tracking and detailed logging
echo - Auto-path cleaning and validation
echo - Keyboard shortcuts and accessibility features
echo - Modular architecture for easy maintenance
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again.
    echo.
    echo Visit: https://python.org/downloads
    pause
    exit /b 1
)

REM Check if the Python script exists in ui subdirectory
if not exist "ui\merger_ui.py" (
    echo ERROR: ui\merger_ui.py not found
    echo Please ensure the Python script is in the ui directory.
    pause
    exit /b 1
)

REM Check if core components exist
if not exist "core\merger_core.py" (
    echo ERROR: core\merger_core.py not found
    echo Please ensure all components are in the core directory.
    pause
    exit /b 1
)

if not exist "core\constants.py" (
    echo ERROR: core\constants.py not found
    echo Please ensure the core directory and constants file exist.
    pause
    exit /b 1
)

REM Set Python path and run the Enhanced Python application
echo Starting Enhanced Power BI Report Merger (Organized Version)...
echo.
set PYTHONPATH=%cd%;%PYTHONPATH%
python ui\merger_ui.py

REM Check if Python script ran successfully
if errorlevel 1 (
    echo.
    echo ERROR: Enhanced application encountered an error
    echo Please check the console output above for details.
    echo.
    echo For support, visit: https://www.analyticendeavors.com
    pause
    exit /b 1
)

echo.
echo Enhanced Power BI Report Merger session completed!
echo Visit us at: https://www.analyticendeavors.com
pause