@echo off
echo Running Battery Health Check...
cd /d "%~dp0"
python "%~dp0battery_health_checker.py"
echo.
echo You can find the detailed battery report in 'battery-report.html'
pause