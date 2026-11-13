# yourNewTV Architecture & Design Engineering

yourNewTV is an ambient, zero-ad, high-performance home launcher designed for Android TV and Google TV devices. It combines the local-first, low-overhead foundation of Couch TV with the aesthetic, frosted-glass design language inspired by GlassOS and Apple TV.

---

## 1. System Overview

```
                      +---------------------------------------+
                      |           Android TV System           |
                      |  (Xiaomi, Sony, TCL, Chromecast, etc.)|
                      +-------------------+-------------------+
                                          |
                      +-------------------v-------------------+
                      |      yourNewTV Android Native Wrapper    |
                      |   - dev.couchtv.ontv / HomeActivity   |
                      |   - FLAG_KEEP_SCREEN_ON Window Policy |
                      |   - Hardware Accelerated WebView      |
                      +-------------------+-------------------+
                                          |
                      +-------------------v-------------------+
                      |         Local Web UI Engine           |
                      |  - Elevated Floating Dock (4.5rem)    |
                      |  - GlassOS Control Center (2D Grid)   |
                      |  - Frosted Settings Drawer            |
                      |  - Top-Right Quick Access Cluster     |
                      |  - 100% Transparent Vector SVGs       |
                      |  - Dynamic Depth Clock Layer          |
                      +-------------------+-------------------+
                                          |
                      +-------------------v-------------------+
                      |       Local-First Data & Storage      |
                      |  - IndexedDB Persistence (Dexie)      |
                      |  - Zero Paid APIs / Zero Cloud Servers|
                      +---------------------------------------+
```

---

## 2. Core Architectural Components

### 2.1 Native Android Wrapper (`HomeActivity.kt`)
- **Single-Task Launcher Intent**: Handles `android.intent.category.HOME` and `android.intent.category.DEFAULT`.
- **Stay-Awake Guard**: Injects `WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON` on the active window hierarchy to prevent aggressive OEM power managers (especially Xiaomi TV / PatchWall) from suspending the system and severing Wi-Fi interfaces during media pauses.
- **Hardware Acceleration**: Enables Chromium GPU rasterization (`setLayerType(View.LAYER_TYPE_HARDWARE, null)`), delivering 60 FPS transitions on low-memory ARM chips.

### 2.2 GlassOS Control Center & 2D D-Pad Navigation Engine
- **Trigger**: Invoked instantaneously via the remote's `MENU` key or navigating to the top-right Quick Access cluster (`#q-cc`).
- **2D Discrete Navigation**: Uses a mathematical grid coordinate system:
  $$\text{Target Index} = \text{Current Index} + \Delta x + (\Delta y \times \text{Row Length})$$
  Features boundary wrapping, visual focus rings, and dedicated footer navigation to TV System Settings and GlassOS Settings.
- **Dismissal**: Smoothly dismisses upon pressing the `BACK` key or navigating outside the modal boundaries.

### 2.3 Transparent Vector Icon Rendering Pipeline (`clearicon.js`)
- **Problem**: Stock Android TV apps supply irregular, low-resolution 320x180 banners or ugly rectangular tiles.
- **Solution**:
  1. A high-resolution SVG vector dictionary matches installed package identifiers (e.g. SmartTube, Netflix, Prime Video, Hotstar, JioCinema, Sony LIV, Send Files To TV, VLC, X-plore).
  2. For uncached apps, `clearicon.js` analyzes the app icon bitmap, removes solid square backgrounds via alpha-luminance thresholding, and renders a floating transparent silhouette.
  3. Dynamic SVG drop-shadows provide depth over bright or dark wallpapers without boxy containment.

### 2.4 Ergonomic Floating Dock (`app.css`)
- **Dock Elevation**: Raised to `bottom: 4.5rem` (`~72px`), completely eliminating bezel collision and safe-zone clipping on overscan TV panels.
- **Fluid Spring Physics**: Utilizes custom cubic-bezier timing curves:
  $$\text{Focus Curve} = \text{cubic-bezier}(0.16, 1, 0.3, 1)$$
  Delivers immediate, zero-lag tactile response to remote D-pad presses.

---

## 3. Power Stability & Deep-Sleep Prevention

Many Android TVs (notably Xiaomi / Redmi / PatchWall) aggressively shut down the Wi-Fi card after 15 minutes of inactivity:
1. **OS Settings Override**:
   - `svc power stayon true`: Disables AC power sleep timer.
   - `settings put global stay_on_while_plugged_in 3`: Keeps CPU and Wi-Fi active while connected to power.
   - `settings put global sleep_timeout 0`: Eliminates system idle timeout.
   - `settings put system screen_off_timeout 2147483647`: Maximizes display standby threshold.
2. **Watchdog Neutralization**: In `app.js`, `SMART_IDLE` is set to `home_idle_minutes: 0` by default, preventing unexpected autonomous standby triggers.

