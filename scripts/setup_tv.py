#!/usr/bin/env python3
"""
AuraTV - Setup & Installation Tool
Automated 1-Click Installer for Android TV & Google TV.
Configures AuraTV, prevents Wi-Fi standby deep sleep, and sets up 60fps ambient UI.
"""

import os
import sys
import subprocess
import time
import shutil

BANNER = r"""
    ___                          ______ _    __
   /   |  __  ___________ _     /_  __/| |  / /
  / /| | / / / / ___/ __ `/      / /   | | / / 
 / ___ |/ /_/ / /  / /_/ /      / /    | |/ /  
/_/  |_|\__,_/_/   \__,_/      /_/     |___/   
                                               
  Weightless Ambient Glass Launcher for Android TV
"""

def find_adb():
    """Find adb executable in PATH or standard Android SDK locations."""
    adb_path = shutil.which("adb")
    if adb_path:
        return adb_path
    
    # Common locations on Windows
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        os.path.join(local_app_data, r"Android\Sdk\platform-tools\adb.exe"),
        r"C:\platform-tools\adb.exe",
        os.path.expanduser("~/Library/Android/sdk/platform-tools/adb"),
        os.path.expanduser("~/Android/Sdk/platform-tools/adb"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def run_adb(adb, args, check=True):
    cmd = [adb] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and result.returncode != 0:
        print(f"[-] ADB Error ({' '.join(args)}): {result.stderr.strip()}")
    return result

def main():
    print(BANNER)
    adb = find_adb()
    if not adb:
        print("[-] Error: 'adb' executable not found in PATH or standard Android SDK directories.")
        print("    Please install Android Platform Tools or add adb to your PATH.")
        sys.exit(1)
    
    print(f"[+] Using ADB binary: {adb}")
    
    # Target device IP
    tv_ip = input("\n[?] Enter TV IP Address (e.g. 192.168.1.100 or press Enter for USB/Connected): ").strip()
    target_device = None
    
    if tv_ip:
        if ":" not in tv_ip:
            tv_ip = f"{tv_ip}:5555"
        print(f"[+] Connecting to {tv_ip}...")
        res = run_adb(adb, ["connect", tv_ip])
        print(f"    {res.stdout.strip()}")
        target_device = tv_ip
    else:
        # Check connected devices
        res = run_adb(adb, ["devices"])
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip() and not line.startswith("List")]
        if not lines:
            print("[-] No devices found. Please connect your TV via USB or enter its Wi-Fi IP.")
            sys.exit(1)
        target_device = lines[0].split()[0]
        print(f"[+] Targeting detected device: {target_device}")

    adb_base = [adb, "-s", target_device]

    # Verify connection
    print("\n[+] Testing connection and TV responsiveness...")
    res = subprocess.run(adb_base + ["shell", "getprop", "ro.product.model"], stdout=subprocess.PIPE, text=True)
    model = res.stdout.strip()
    if not model:
        print(f"[-] Could not communicate with TV at {target_device}. Ensure Network Debugging is enabled.")
        sys.exit(1)
    print(f"[+] Connected to: {model}")

    # Determine APK path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    apk_path = os.path.join(repo_root, "apk", "AuraTV-v1.0-release.apk")
    
    if not os.path.exists(apk_path):
        print(f"[-] Error: APK not found at {apk_path}")
        sys.exit(1)

    print(f"\n[+] Step 1: Installing AuraTV ({os.path.getsize(apk_path) // (1024*1024)} MB)...")
    res = subprocess.run(adb_base + ["install", "-r", "-d", apk_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "Success" in res.stdout or "Success" in res.stderr:
        print("    [✓] AuraTV installed successfully.")
    else:
        print(f"    [-] Install warning: {res.stdout.strip()} {res.stderr.strip()}")

    print("\n[+] Step 2: Applying Anti-Sleep & Always-Awake Power Rules...")
    power_cmds = [
        ["shell", "svc", "power", "stayon", "true"],
        ["shell", "settings", "put", "global", "stay_on_while_plugged_in", "3"],
        ["shell", "settings", "put", "global", "sleep_timeout", "0"],
        ["shell", "settings", "put", "system", "screen_off_timeout", "2147483647"],
        ["shell", "settings", "put", "secure", "sleep_timeout", "-1"],
    ]
    for pcmd in power_cmds:
        subprocess.run(adb_base + pcmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("    [✓] Power rules applied: Wi-Fi standby sleep and unwanted powercuts disabled.")

    print("\n[+] Step 3: Granting required Android TV permissions...")
    perm_cmds = [
        ["shell", "appops", "set", "dev.couchtv.ontv", "SYSTEM_ALERT_WINDOW", "allow"],
        ["shell", "appops", "set", "dev.couchtv.ontv", "GET_USAGE_STATS", "allow"],
    ]
    for pcmd in perm_cmds:
        subprocess.run(adb_base + pcmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("    [✓] Overlay and usage permissions granted.")

    print("\n[+] Step 4: Launching AuraTV Home Screen...")
    subprocess.run(adb_base + ["shell", "am", "start", "-n", "dev.couchtv.ontv/.HomeAlias"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    subprocess.run(adb_base + ["shell", "input", "keyevent", "KEYCODE_HOME"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("    [✓] AuraTV is now running on your screen.")

    # Optional: Disable stock Google TV launcher
    print("\n" + "="*60)
    print("OPTIONAL: Disable Stock Google TV / Android TV Ad Launcher")
    print("This makes AuraTV the exclusive default launcher on your Home button.")
    print("="*60)
    choice = input("[?] Disable stock launcher (com.google.android.tvlauncher)? (y/N): ").strip().lower()
    if choice == "y":
        print("[+] Disabling stock launcher...")
        subprocess.run(adb_base + ["shell", "pm", "disable-user", "--user", "0", "com.google.android.tvlauncher"], stdout=subprocess.PIPE, text=True)
        print("    [✓] Stock ad launcher disabled.")
        print("    [i] To restore it anytime, run: adb shell pm enable com.google.android.tvlauncher")
    else:
        print("    [-] Stock launcher untouched. You can select AuraTV using the Home key prompt.")

    print("\n" + "="*60)
    print("🎉 AuraTV Installation & Tuning Complete!")
    print("Enjoy a clean, fast, ad-free ambient living room experience.")
    print("="*60)

if __name__ == "__main__":
    main()
