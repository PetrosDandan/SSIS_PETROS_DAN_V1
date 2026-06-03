@echo off
title Simple Student Information System (SSIS) - Launcher
cls

echo ======================================================================
echo          SIMPLE STUDENT INFORMATION SYSTEM (SSIS) - LAUNCHER
echo ======================================================================
echo.

:: Step 1: Check for Python
echo [1/2] Checking for Python installation...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is NOT installed or not added to your Windows PATH variable!
    echo.
    echo To resolve this:
    echo 1. Go to https://www.python.org/downloads/ and download Python (v3.8 or higher is recommended).
    echo 2. IMPORTANT: During installation, check the box that says:
    echo    "Add Python to PATH" or "Add python.exe to PATH" before hitting Install.
    echo 3. Restart your command line prompt and double-click or run this file again!
    echo.
    echo Opening Python downloads page for you...
    start https://www.python.org/downloads/
    echo.
    pause
    exit /b
)
echo [SUCCESS] Python is installed!
echo.

:: Step 2: Launch high-performance standalone app
echo [2/2] Launching Simple Student Information System...
echo ----------------------------------------------------------------------
echo Status: Starting... Standalone window will open in a few moments.
echo ----------------------------------------------------------------------

python ssis.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Script execution failed. Please verify that "ssis.py" exists in the root folder.
    pause
)
