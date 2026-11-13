#!/usr/bin/env python3
"""
YourNewTV - Rebuild & Packaging Tool
Autonomous script to package web assets into YourNewTV APK, zipalign, and sign.
"""

import base64
import os
import sys
import subprocess
import zipfile
import shutil
import glob

# 1. High-fidelity transparent vector SVGs for TV applications
SVGS = {
    # SmartTube
    "org.smarttube.stable": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="st_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF334B"/>
      <stop offset="100%" stop-color="#D6001C"/>
    </linearGradient>
  </defs>
  <rect x="8" y="18" width="84" height="64" rx="20" fill="url(#st_grad)"/>
  <polygon points="40,34 68,50 40,66" fill="#FFFFFF"/>
  <path d="M72 37c3.5 4 5 8.5 5 13s-1.5 9-5 13" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" fill="none"/>
  <path d="M79 31c5.5 5.5 8 12 8 19s-2.5 13.5-8 19" stroke="rgba(255,255,255,0.7)" stroke-width="4" stroke-linecap="round" fill="none"/>
</svg>''',

    # NetMirrorTV
    "app.netmirror.newtv": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="nm_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF1E27"/>
      <stop offset="100%" stop-color="#990007"/>
    </linearGradient>
  </defs>
  <path d="M22 14h16v72H22z" fill="#8B0000"/>
  <path d="M62 14h16v72H62z" fill="#8B0000"/>
  <path d="M22 14h16l40 72H62z" fill="url(#nm_grad)"/>
  <polygon points="48,42 62,50 48,58" fill="#FFFFFF"/>
</svg>''',

    # JioHotstar
    "in.startv.hotstar": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="hs_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#002BFF"/>
      <stop offset="50%" stop-color="#0066FF"/>
      <stop offset="100%" stop-color="#00E5FF"/>
    </linearGradient>
  </defs>
  <polygon points="50,10 61,38 90,38 67,56 76,84 50,68 24,84 33,56 10,38 39,38" fill="url(#hs_grad)"/>
  <polygon points="50,22 58,42 78,42 62,54 68,74 50,62 32,74 38,54 22,42 42,42" fill="#FFFFFF" opacity="0.9"/>
</svg>''',

    # Netflix
    "com.netflix.ninja": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="nf_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E50914"/>
      <stop offset="100%" stop-color="#B20710"/>
    </linearGradient>
  </defs>
  <path d="M24 10h16v80H24z" fill="#8C050B"/>
  <path d="M60 10h16v80H60z" fill="#8C050B"/>
  <path d="M24 10h16l36 80H60z" fill="url(#nf_grad)"/>
</svg>''',

    # Prime Video
    "com.amazon.amazonvideo.livingroom": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="pv_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00A8E1"/>
      <stop offset="100%" stop-color="#007EB9"/>
    </linearGradient>
  </defs>
  <text x="50" y="44" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-weight="900" font-size="28" text-anchor="middle" fill="#FFFFFF">prime</text>
  <text x="50" y="66" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-weight="700" font-size="18" text-anchor="middle" fill="#00A8E1">video</text>
  <path d="M25 76c16 8 34 8 50 0 1.6-.8 3.6 1 2.2 2.4-8 7.5-25.5 11-42.5 5.5-1.6-.5-2.4-2.8-1.3-4.2l.2-.2" fill="#00A8E1"/>
  <path d="M75 75l5 3.5-6 3.5 1-7" fill="#00A8E1"/>
</svg>''',

    # Sony LIV
    "com.sonyliv": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="liv_grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF007F"/>
      <stop offset="35%" stop-color="#FF7F00"/>
      <stop offset="70%" stop-color="#FFD700"/>
      <stop offset="100%" stop-color="#00E5FF"/>
    </linearGradient>
  </defs>
  <text x="50" y="32" font-family="'Arial Black', Impact, sans-serif" font-weight="900" font-size="18" letter-spacing="3" text-anchor="middle" fill="#FFFFFF">SONY</text>
  <text x="50" y="78" font-family="'Arial Black', Impact, sans-serif" font-weight="900" font-size="44" letter-spacing="1" text-anchor="middle" fill="url(#liv_grad)">liv</text>
  <rect x="22" y="85" width="56" height="5" rx="2.5" fill="url(#liv_grad)"/>
</svg>''',

    # Send Files To TV
    "com.yablio.sendfilestotv": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sftv_down" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00F2FE"/>
      <stop offset="100%" stop-color="#4FACFE"/>
    </linearGradient>
    <linearGradient id="sftv_up" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00E676"/>
      <stop offset="100%" stop-color="#00B0FF"/>
    </linearGradient>
  </defs>
  <path d="M36 82V36H20l20-22 20 22H48v46z" fill="url(#sftv_up)"/>
  <path d="M64 18v46h16l-20 22-20-22h12V18z" fill="url(#sftv_down)"/>
</svg>''',

    # JioCinema
    "com.jio.media.ondemand": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="jc_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E20074"/>
      <stop offset="100%" stop-color="#A50050"/>
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="44" fill="url(#jc_grad)"/>
  <polygon points="40,32 70,50 40,68" fill="#FFFFFF"/>
</svg>''',

    # VLC
    "org.videolan.vlc": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="vlc_cone" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF5722"/>
      <stop offset="50%" stop-color="#FF9800"/>
      <stop offset="100%" stop-color="#E64A19"/>
    </linearGradient>
  </defs>
  <ellipse cx="50" cy="85" rx="38" ry="10" fill="#E64A19"/>
  <ellipse cx="50" cy="83" rx="34" ry="8" fill="#FFFFFF"/>
  <path d="M44 14h12l10 32H34z" fill="url(#vlc_cone)"/>
  <path d="M34 46h32l4 14H30z" fill="#FFFFFF"/>
  <path d="M30 60h40l5 16H25z" fill="url(#vlc_cone)"/>
  <path d="M25 76h50l3 7H22z" fill="#FFFFFF"/>
  <ellipse cx="50" cy="14" rx="6" ry="3" fill="#FFB74D"/>
</svg>''',

    # X-plore
    "com.lonelycatgames.Xplore": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="16" width="38" height="68" rx="5" fill="#37474F"/>
  <rect x="52" y="16" width="38" height="68" rx="5" fill="#455A64"/>
  <path d="M22 28v40m0-28h14m-14 14h14m-14 14h14" stroke="#81D4FA" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="36" cy="28" r="4.5" fill="#FFD54F"/>
  <circle cx="36" cy="42" r="4.5" fill="#FFD54F"/>
  <circle cx="36" cy="56" r="4.5" fill="#FFD54F"/>
  <path d="M44 46a5 5 0 0 1 5-5h12l4 4h20a5 5 0 0 1 5 5v26a5 5 0 0 1-5 5H49a5 5 0 0 1-5-5z" fill="#FFB300"/>
</svg>''',

    # MX Player
    "com.mxtech.videoplayer.ad": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="mx_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00C0FF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="42" fill="url(#mx_grad)"/>
  <polygon points="40,32 70,50 40,68" fill="#FFFFFF"/>
  <text x="50" y="85" font-family="'Arial Black', sans-serif" font-weight="900" font-size="14" text-anchor="middle" fill="#FFFFFF">MX</text>
</svg>''',

    # YouTube Music
    "com.google.android.youtube.tvmusic": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="42" fill="#FF0000"/>
  <circle cx="50" cy="50" r="26" fill="none" stroke="#FFFFFF" stroke-width="6"/>
  <polygon points="44,38 62,50 44,62" fill="#FFFFFF"/>
</svg>''',

    # Aptoide TV
    "cm.aptoidetv.pt": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="12" y="16" width="76" height="68" rx="18" fill="#FF7700"/>
  <path d="M30 40 L50 62 L70 40" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>''',

    # Projectivy Launcher
    "com.spocky.projengmenu": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="prj_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4A00E0"/>
      <stop offset="100%" stop-color="#8E2DE2"/>
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="42" fill="url(#prj_grad)"/>
  <path d="M30 50 L50 30 L70 50 L50 70 Z" fill="#FFFFFF"/>
</svg>'''
}

def find_android_tools():
    """Locate zipalign and apksigner."""
    zipalign = shutil.which("zipalign")
    apksigner = shutil.which("apksigner")
    
    if not zipalign or not apksigner:
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        build_tools_root = os.path.join(local_app_data, r"Android\Sdk\build-tools")
        if os.path.exists(build_tools_root):
            versions = sorted(os.listdir(build_tools_root), reverse=True)
            for v in versions:
                v_path = os.path.join(build_tools_root, v)
                za = os.path.join(v_path, "zipalign.exe" if os.name == "nt" else "zipalign")
                as_ = os.path.join(v_path, "apksigner.bat" if os.name == "nt" else "apksigner")
                if os.path.exists(za) and (os.path.exists(as_) or os.path.exists(as_.replace(".bat", ""))):
                    return za, as_
    return zipalign, apksigner

def main():
    print("[+] YourNewTV - Rebuild & Packaging Engine")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    web_dir = os.path.join(repo_root, "src", "web")
    apk_dir = os.path.join(repo_root, "apk")
    
    app_js_path = os.path.join(web_dir, "app.js")
    app_css_path = os.path.join(web_dir, "app.css")
    clearicon_js_path = os.path.join(web_dir, "clearicon.js")
    index_html_path = os.path.join(web_dir, "index.html")

    target_apk = os.path.join(apk_dir, "YourNewTV-v1.0-release.apk")
    temp_apk = os.path.join(apk_dir, "YourNewTV-temp.apk")

    if not os.path.exists(target_apk):
        print(f"[-] Base APK not found at {target_apk}")
        sys.exit(1)

    print("[+] Packaging updated Web UI assets into APK...")
    with zipfile.ZipFile(target_apk, 'r') as zin:
        with zipfile.ZipFile(temp_apk, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename.startswith("META-INF/"):
                    continue
                if item.filename == "assets/www/tv/app.js":
                    zout.write(app_js_path, item.filename)
                elif item.filename == "assets/www/tv/app.css":
                    zout.write(app_css_path, item.filename)
                elif item.filename == "assets/www/tv/clearicon.js":
                    zout.write(clearicon_js_path, item.filename)
                elif item.filename == "assets/www/tv/index.html":
                    zout.write(index_html_path, item.filename)
                else:
                    zout.writestr(item, zin.read(item.filename))

    zipalign, apksigner = find_android_tools()
    if not zipalign or not apksigner:
        print("[!] Warning: zipalign or apksigner not found. Keeping updated unaligned APK.")
        shutil.move(temp_apk, target_apk)
        return

    print("[+] Zipaligning APK...")
    aligned_apk = os.path.join(apk_dir, "YourNewTV-aligned.apk")
    if os.path.exists(aligned_apk):
        os.remove(aligned_apk)
    subprocess.run([zipalign, "-p", "-f", "4", temp_apk, aligned_apk], check=True)
    os.remove(temp_apk)

    # Signing
    keystore = os.path.expanduser("~/.android/debug.keystore")
    if not os.path.exists(keystore):
        print("[+] Creating temporary debug keystore...")
        keytool = shutil.which("keytool")
        if keytool:
            os.makedirs(os.path.dirname(keystore), exist_ok=True)
            subprocess.run([
                keytool, "-genkeypair", "-v",
                "-keystore", keystore,
                "-storepass", "android",
                "-alias", "androiddebugkey",
                "-keypass", "android",
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-dname", "CN=Android Debug,O=Android,C=US"
            ], check=True)

    print("[+] Signing APK...")
    sign_cmd = [
        apksigner, "sign",
        "--ks", keystore,
        "--ks-pass", "pass:android",
        aligned_apk
    ]
    subprocess.run(sign_cmd, check=True, shell=(os.name == "nt"))

    if os.path.exists(target_apk):
        os.remove(target_apk)
    shutil.move(aligned_apk, target_apk)
    print(f"[✓] YourNewTV release APK rebuilt successfully: {target_apk}")

if __name__ == "__main__":
    main()
