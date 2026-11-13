#!/usr/bin/env bash
# yourNewTV - macOS / Linux 1-Click Installer
set -e

echo "================================================================"
echo "      yourNewTV - Ambient Glass Launcher for Android TV"
echo "================================================================"
echo ""

# Find ADB
if command -v adb >/dev/null 2>&1; then
    ADB_CMD="adb"
elif [ -f "$HOME/Library/Android/sdk/platform-tools/adb" ]; then
    ADB_CMD="$HOME/Library/Android/sdk/platform-tools/adb"
elif [ -f "$HOME/Android/Sdk/platform-tools/adb" ]; then
    ADB_CMD="$HOME/Android/Sdk/platform-tools/adb"
else
    echo "[-] Error: 'adb' command not found. Please install platform-tools."
    exit 1
fi

echo "[+] Using ADB: $ADB_CMD"
echo ""

read -p "Enter TV Wi-Fi IP address (or press Enter if USB connected): " TV_IP

if [ -n "$TV_IP" ]; then
    echo "[+] Connecting to $TV_IP:5555..."
    $ADB_CMD connect "$TV_IP:5555"
    DEVICE_ARG="-s $TV_IP:5555"
else
    DEVICE_ARG=""
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APK_PATH="$DIR/../apk/yourNewTV-v1.0-release.apk"

echo ""
echo "[1/4] Installing yourNewTV release APK..."
$ADB_CMD $DEVICE_ARG install -r -d "$APK_PATH"

echo ""
echo "[2/4] Applying anti-sleep and power stability optimizations..."
$ADB_CMD $DEVICE_ARG shell svc power stayon true
$ADB_CMD $DEVICE_ARG shell settings put global stay_on_while_plugged_in 3
$ADB_CMD $DEVICE_ARG shell settings put global sleep_timeout 0
$ADB_CMD $DEVICE_ARG shell settings put system screen_off_timeout 2147483647
$ADB_CMD $DEVICE_ARG shell settings put secure sleep_timeout -1

echo ""
echo "[3/4] Granting system alert and usage permissions..."
$ADB_CMD $DEVICE_ARG shell appops set dev.couchtv.ontv SYSTEM_ALERT_WINDOW allow
$ADB_CMD $DEVICE_ARG shell appops set dev.couchtv.ontv GET_USAGE_STATS allow

echo ""
echo "[4/4] Starting yourNewTV Home Screen..."
$ADB_CMD $DEVICE_ARG shell am start -n dev.couchtv.ontv/.HomeAlias
sleep 1
$ADB_CMD $DEVICE_ARG shell input keyevent KEYCODE_HOME

echo ""
echo "================================================================"
echo "🎉 yourNewTV installation complete!"
echo "   Press MENU on your remote to open the GlassOS Control Center."
echo "================================================================"

