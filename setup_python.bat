@echo off
setlocal enabledelayedexpansion

echo Starting Python installation and setup...

echo Checking Python installation...
winget install Python.Python.3.11 >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python installation failed
    pause
    exit /b 1
)

echo Waiting for installation to complete...
timeout /t 5 /nobreak > nul

REM Try to find Python installation directory
set "PYTHON_EXE="
for %%p in ("%LocalAppData%\Programs\Python\Python311\python.exe" "C:\Program Files\Python311\python.exe" "C:\Program Files (x86)\Python311\python.exe") do (
    if exist %%~p (
        set "PYTHON_EXE=%%~fp"
        set "PYTHON_PATH=%%~dp"
        goto :found_python
    )
)
echo Error: Could not find Python installation
pause
exit /b 1

:found_python
echo Found Python at: !PYTHON_PATH!

REM Get current PATH
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH') do set "USER_PATH=%%b"

REM Update PATH (remove quotes to avoid issues)
set "NEW_PATH=!USER_PATH!;!PYTHON_PATH!;!PYTHON_PATH!Scripts"
reg add "HKCU\Environment" /v PATH /t REG_EXPAND_SZ /d "!NEW_PATH!" /f >nul 2>&1

REM Update current session PATH
set "PATH=!NEW_PATH!"

echo Installing/Upgrading pip...
"!PYTHON_EXE!" -m pip install --upgrade pip >nul 2>&1

echo Installing required packages...
"!PYTHON_EXE!" -m pip install openpyxl pandas psutil beautifulsoup4 >nul 2>&1

echo.
echo Testing installation...
"!PYTHON_EXE!" -c "import pandas; import openpyxl; import psutil; from bs4 import BeautifulSoup; print('All packages successfully installed!')"

endlocal
pause