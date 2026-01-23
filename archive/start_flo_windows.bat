@echo off
REM ============================================================
REM One-click startup for FLO v2 on Windows
REM Prerequisites:
REM 1. WSL2 + Ubuntu installed
REM 2. VcXsrv installed and running
REM 3. usbipd-win installed
REM ============================================================

echo ======================================
echo FLO v2 Robot System - Windows Launcher
echo ======================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo [1/5] Checking VcXsrv...
tasklist /FI "IMAGENAME eq vcxsrv.exe" 2>NUL | find /I /N "vcxsrv.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   VcXsrv is running
) else (
    echo   WARNING: VcXsrv is not running!
    echo   Please start VcXsrv manually before continuing
    echo   Double-click the VcXsrv config on your desktop
    pause
)

echo.
echo [2/5] Listing USB devices...
usbipd list
echo.

echo [3/5] Attaching USB devices to WSL2...
echo   NOTE: Update the BUSID below to match your devices!
echo   Edit this .bat file and replace 1-4 with your actual BUSID

REM TODO: Replace 1-4 with your actual Dynamixel BUSID
set DYNAMIXEL_BUSID=1-4
REM TODO: Replace 2-3 with your actual camera BUSID (or leave empty if no camera)
set CAMERA_BUSID=2-3

echo   Attaching Dynamixel (BUSID: %DYNAMIXEL_BUSID%)...
usbipd attach --wsl --busid %DYNAMIXEL_BUSID%
if %errorLevel% neq 0 (
    echo   WARNING: Failed to attach Dynamixel. Check BUSID!
)

if not "%CAMERA_BUSID%"=="" (
    echo   Attaching Camera (BUSID: %CAMERA_BUSID%)...
    usbipd attach --wsl --busid %CAMERA_BUSID%
)

timeout /t 2 /nobreak >nul

echo.
echo [4/5] Verifying devices in WSL2...
wsl bash -c "ls -l /dev/ttyUSB* /dev/video* 2>/dev/null || echo 'No devices found'"

echo.
echo [5/5] Starting Docker container in WSL2...
echo   This will open a new WSL2 terminal with the Docker container
echo.

REM Start in a new WSL window
wsl bash -c "cd ~/FloSystemV2/gazebo_simulation_and_control && ./run_docker_wsl2.sh"

echo.
echo Container exited.
pause

