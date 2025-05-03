# Battery Health Checker

A comprehensive Windows battery monitoring tool that provides detailed information about your laptop's battery health, usage patterns, and real-time status.

## Features

- 🔋 Real-time battery status monitoring
- 📊 Detailed battery health information
- 📈 Battery wear level calculation
- 🕒 Recent usage pattern analysis
- 📑 HTML report generation
- 🚦 Health indicators and warnings

## Requirements

- Windows Operating System
- Python 3.11 or higher
- Required Python packages:
  - psutil
  - beautifulsoup4

## Installation

1. Run the `setup_python.bat` script in the parent directory to install Python and required packages:
   ```batch
   ..\setup_python.bat
   ```

2. The script will:
   - Install Python 3.11 if not present
   - Set up Python in PATH
   - Install required packages (psutil, beautifulsoup4)

## Usage

There are three ways to run the battery health check:

1. Using the VBS script (runs silently in background):
   ```
   run_battery_check.vbs
   ```

2. Using the batch file (shows command window):
   ```
   check_battery.bat
   ```

3. Directly using Python:
   ```
   python battery_health_checker.py
   ```

## Output Information

The tool provides:

- **Current Battery Status**
  - Battery level percentage
  - Power connection status
  - Remaining time estimate

- **Battery Health Information**
  - Design capacity
  - Current capacity
  - Cycle count
  - Battery wear percentage

- **Health Indicators**
  - Battery level status (🟢 Good, 🟡 Low, 🔴 Critical)
  - Wear level status (🟢 Normal, 🟡 Moderate, 🔴 High)

- **Recent Usage Pattern**
  - Last 3 usage sessions
  - Activity duration
  - Power consumption

## Detailed Report

The tool generates a detailed HTML report (`battery-report.html`) that can be opened in any web browser for comprehensive historical data and detailed battery information.

## Note

This tool uses Windows' built-in `powercfg` command to generate detailed battery reports, combined with Python's `psutil` for real-time monitoring. The information is parsed and presented in an easy-to-read format with visual indicators for quick health assessment.
