# AGENTS.md - YourNewTV Governing Contract

This document is the authoritative engineering contract and protocol specification for all AI agents, contributors, and automation tools working on **YourNewTV**.

---

## 1. Project Mission & Identity

- **Application Name**: **YourNewTV** (Strict branding; never use legacy names).
- **Core Purpose**: Ultra-lightweight, hardware-accelerated, 60 FPS ambient launcher for Android TV and Google TV with an elevated floating dock, multi-layer depth wallpapers, and an instant-access Control Center.
- **Privacy & Telemetry**: **Strict $0 rule and zero-telemetry**. Zero background tracking beacons, zero advertising scrapers, zero external cloud analytics. 100% local-first computation.
- **Platform Scope**: Android TV 7.1 through Android TV 14 (API 25 to 34), Google TV, Fire OS, and Leanback television platforms.

---

## 2. Architecture & Design Principles

1. **Static SPA Frontend**:
   - Built on pure ES6 vanilla JavaScript, CSS Grid/Flexbox, and hardware-accelerated GPU transforms (`translateZ(0)`).
   - Zero heavyweight web framework overhead; memory footprint stays under **60 MB RAM** on 1.5 GB / 2 GB Android TV devices.
2. **Native Android Wrapper**:
   - Thin Android WebView host (`dev.couchtv.ontv.HomeActivity`) handling Leanback remote keyevents (`KEYCODE_DPAD_*`, `KEYCODE_MENU`, `KEYCODE_BACK`, `KEYCODE_SETTINGS`).
   - Android Bridge service exposing hardware-level Wi-Fi, power, sleep timer, package resolver, and volume APIs via safe JavascriptInterface and local loopback HTTP.
3. **Glassmorphism & Contrast**:
   - High-contrast typography and focus rings meeting WCAG AAA standard (>= 7:1 contrast ratio against blurred backdrops).
   - Stationarily-scoped frosted glass blur (`-webkit-backdrop-filter: blur(24px)`) on modals and popups, with dock elements kept lightweight for 60 FPS remote scrolling.

---

## 3. Remote Navigation Contract

| Remote Key | Action |
|:---|:---|
| `KEYCODE_DPAD_LEFT` / `RIGHT` | Navigate horizontal application dock. In Control Center: 2D grid toggle selection. |
| `KEYCODE_DPAD_UP` | Move focus from dock to Top-Left Profile Switcher (`Family`/`Kids`) or Top-Right Quick Access Cluster (`⚙️ Settings`, `🎚️ Control Center`, `🌙 Sleep`). |
| `KEYCODE_DPAD_DOWN` | Return focus from top header down to application dock. In dock: expand full app grid. |
| `KEYCODE_DPAD_CENTER` | Launch focused app, toggle setting, or open focused top-right menu. |
| `KEYCODE_MENU` (Key 82) | Toggle the GlassOS Control Center modal from anywhere. |
| `KEYCODE_BACK` (Key 4) | Dismiss open modal, drawer, or sleep popup. From home: no-op (prevents home exit). |
| `KEYCODE_HOME` (Key 3) | Reset focus to primary dock and return immediately to the clean ambient home. |

---

## 4. Hardware Verification & Quality Assurance Protocol

- **Real Hardware Verification**:
  - Emulators or browser-only mockups are strictly prohibited for certification. All visual and behavioral changes must be verified on live physical Android TV hardware via ADB (`192.168.29.141:5555`).
- **Clean As You Go**:
  - Zero junk policy. After test execution passes, remove temporary test scripts and capture dumps from root workspaces.
- **Evidence or Fail**:
  - Never claim a defect is resolved without capturing empirical verification evidence (1080p ADB screencap, log output, or unit test pass).

---

## 5. Licensing & Upstream Governance

- Licensed under the **MIT License**.
- Upstream intellectual property, code, and assets from Couch TV, CleanYourTV, GlassOS TV, Google Fonts (Antonio, Inter), and Wikimedia Commons are preserved and attributed in `CREDITS.md` and `LICENSE`.
