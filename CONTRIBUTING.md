# Contributing to YourNewTV

We welcome contributions from developers, designers, and home theater enthusiasts! Whether you are fixing a remote navigation bug, enhancing 60 FPS animation performance, or adding support for new Android TV devices, your help is appreciated.

---

## 1. Development Principles

When contributing to YourNewTV, please adhere to our core engineering tenets:

1. **Ad-Free & Local-First:** Never introduce third-party ad SDKs, telemetry beacons, or external cloud dependencies.
2. **60 FPS Hardware Performance:** Keep JavaScript and DOM operations lean. Test on memory-constrained hardware (e.g. 1GB–2GB RAM Android TV sticks).
3. **10-Foot UI & D-Pad First:** Every UI component must be 100% operable via physical remote D-Pad (`DPAD_UP`, `DPAD_DOWN`, `DPAD_LEFT`, `DPAD_RIGHT`, `DPAD_CENTER`, `BACK`, `MENU`).
4. **Surgical Changes:** Keep PRs focused and minimal. Do not mix refactoring with feature additions.

---

## 2. Project Structure

- `src/android/`: Native Android project hosting the standalone Android TV wrapper and system bridge (`dev.couchtv.ontv`).
- `src/web/`: Modern HTML5, CSS3, and JavaScript frontend that runs inside the hardware-accelerated WebView.
- `assets/`: Scalable vector logos, branding marks, and transparent visual assets.
- `scripts/`: Cross-platform ADB installation and TV provisioning scripts.
- `docs/`: Technical architecture documentation, screenshots, and troubleshooting manuals.

---

## 3. Getting Started Locally

### Prerequisites
- Node.js (v18+) or Python 3.10+ for serving static web assets
- Android SDK (API Level 30+) and Gradle 8+ (for building native APK)
- Physical Android TV or Android Emulator with ADB enabled

### Testing Web Interface in Browser
You can preview the interface directly on your computer:
```bash
# Serve web assets with any HTTP server
python -m http.server 8080 --directory src/web

# Open in browser with mock environment enabled:
# http://localhost:8080/index.html?mock=1&pointer=1
```

### Rebuilding the Release APK
```bash
python scripts/rebuild_apk.py
```
This compiles the native Android wrapper and packages `src/web` into `apk/YourNewTV-v1.0-release.apk`.

### Deploying to Physical TV via ADB
```bash
# Ensure TV is on the same local network with USB/Network Debugging enabled
adb connect <TV_IP_ADDRESS>:5555
python scripts/setup_tv.py
```

---

## 4. Submitting a Pull Request

1. Fork the repository and create your feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Commit your changes with concise, conventional commit messages:
   ```bash
   git commit -m "feat(ui): add high-contrast focus ring for quick toggles"
   ```
3. Push to your branch and open a Pull Request against `main`.
4. Provide a clear description and include screenshots or screencasts if the change touches the visual UI.
