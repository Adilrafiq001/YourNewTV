# YourNewTV Troubleshooting & FAQ Guide

---

## 1. Remote Control Mappings

| Remote Key | YourNewTV Action |
|:---|:---|
| **D-Pad Left / Right** | Cycle horizontally through elevated dock apps |
| **D-Pad Up** | Move focus to Top-Right Quick Access Cluster (Settings, Control Center, Sleep) |
| **D-Pad Down** | Return focus from Top-Right Cluster back to the Dock |
| **Center / OK** | Launch highlighted application or activate toggle |
| **MENU** | Open / Close GlassOS Control Center modal |
| **BACK** | Dismiss Control Center or Settings drawer back to Home Screen |
| **HOME** | Instant return to YourNewTV Home Screen |

---

## 2. Deep Sleep & Wi-Fi Disconnection Fix

### Symptoms
- TV goes to sleep unexpectedly without user command.
- ADB reports `Connection refused` or `Host failed to respond (10060)` when TV has been idle for 15+ minutes.
- Wi-Fi drops out when the TV display goes blank.

### Root Cause
OEM power management (especially on Xiaomi / Redmi TVs) aggressively enters deep sleep state S3, disabling the internal Wi-Fi chip to reduce standby wattage.

### Permanent Resolution
Execute the following commands via ADB:
```bash
adb shell svc power stayon true
adb shell settings put global stay_on_while_plugged_in 3
adb shell settings put global sleep_timeout 0
adb shell settings put system screen_off_timeout 2147483647
adb shell settings put secure sleep_timeout -1
```
*Note: YourNewTV's `HomeActivity.kt` also includes `FLAG_KEEP_SCREEN_ON` to prevent runtime sleeps.*

---

## 3. Disabling & Re-enabling Stock Android TV Launcher

### To Make YourNewTV the Exclusive Default Launcher
Disable the stock Google TV / Android TV launcher:
```bash
adb shell pm disable-user --user 0 com.google.android.tvlauncher
```

### To Restore the Stock Android TV Launcher (Undo)
If you ever want to return completely to the factory Google TV / Android TV home screen:
```bash
adb shell pm enable com.google.android.tvlauncher
adb shell am start -n com.google.android.tvlauncher/.MainActivity
```

---

## 4. ADB Connection Issues

### "device unauthorized"
- Look at your TV screen. A dialog will prompt: *"Allow USB debugging?"*
- Check the box **"Always allow from this computer"** and select **OK**.

### "device offline" / "connection refused"
1. Verify TV and computer are on the exact same Wi-Fi subnet (disable VPNs or guest Wi-Fi isolation).
2. On your TV, navigate to **Settings > Device Preferences > Developer Options**.
3. Toggle **Network Debugging** OFF and then back ON.
4. Reconnect: `adb connect <TV_IP_ADDRESS>:5555`.

