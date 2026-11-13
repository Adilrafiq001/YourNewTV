@echo off
setlocal enabledelayedexpansion
title AuraTV - Windows 1-Click Installer
color 0B

echo ================================================================
echo       AuraTV - Ambient Glass Launcher for Android TV
echo ================================================================
echo.

:: Check for ADB
where adb >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set ADB_CMD=adb
) else (
    if exist "%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" (
        set ADB_CMD="%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
    ) else if exist "C:\platform-tools\adb.exe" (
        set ADB_CMD="C:\platform-tools\adb.exe"
    ) else (
        echo [ERROR] adb.exe was not found in PATH or standard SDK locations.
        echo Please ensure Android Platform Tools are installed.
        pause
        exit /b 1
    )
)

echo [OK] Using ADB: %ADB_CMD%
echo.

set /p TV_IP="Enter your TV's Wi-Fi IP address (e.g. 192.168.1.100) or press Enter if USB connected: "
if not "%TV_IP%"=="" (
    echo [CONNECTING] Connecting to %TV_IP%:5555...
    %ADB_CMD% connect %TV_IP%:5555
    set DEVICE_ARG=-s %TV_IP%:5555
) else (
    set DEVICE_ARG=
)

echo.
echo [1/4] Installing AuraTV release APK...
%ADB_CMD% %DEVICE_ARG% install -r -d "%~dp0..\apk\AuraTV-v1.0-release.apk"

echo.
echo [2/4] Applying anti-sleep and power stability optimizations...
%ADB_CMD% %DEVICE_ARG% shell svc power stayon true
%ADB_CMD% %DEVICE_ARG% shell settings put global stay_on_while_plugged_in 3
%ADB_CMD% %DEVICE_ARG% shell settings put global sleep_timeout 0
%ADB_CMD% %DEVICE_ARG% shell settings put system screen_off_timeout 2147483647
%ADB_CMD% %DEVICE_ARG% shell settings put secure sleep_timeout -1

echo.
echo [3/4] Granting system alert and usage permissions...
%ADB_CMD% %DEVICE_ARG% shell appops set dev.couchtv.ontv SYSTEM_ALERT_WINDOW allow
%ADB_CMD% %DEVICE_ARG% shell appops set dev.couchtv.ontv GET_USAGE_STATS allow

echo.
echo [4/4] Starting AuraTV Home Screen...
%ADB_CMD% %DEVICE_ARG% shell am start -n dev.couchtv.ontv/.HomeAlias
timeout /t 1 /nobreak >nul
%ADB_CMD% %DEVICE_ARG% shell input keyevent KEYCODE_HOME

echo.
echo ================================================================
echo  AuraTV installation complete!
echo  Press MENU on your remote to open the GlassOS Control Center.
echo ================================================================
echo.
pause
