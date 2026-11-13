# Privacy Policy & Architecture

**YourNewTV is built on a simple foundation: your TV belongs to you, not to advertisers.**

Most factory TV operating systems (Android TV, Google TV, Fire TV, webOS) operate background telemetry services, ad-tracking scrapers, and analytics daemons that transmit viewing habits, app launch history, and hardware identifiers to advertising exchanges.

YourNewTV eliminates this entirely.

---

## 1. Zero Telemetry & Tracking

- **No Remote Analytics:** YourNewTV contains zero analytics SDKs (no Firebase Analytics, no Google Analytics, no Mixpanel, no Sentry, no telemetry beacons).
- **No Advertising Networks:** There are no ad networks, tracking pixels, or sponsored recommendations embedded anywhere in the code.
- **Zero Background Reporting:** The launcher does not make outbound network requests to report your usage, installed applications, or remote interactions.

---

## 2. Local-First Processing

- **App Discovery:** Queries for installed applications run directly on your television hardware through Android's local `PackageManager` APIs. Application metadata never leaves the device.
- **Preferences & Configuration:** All visual customizations, dock layouts, wallpapers, and profiles are persisted locally in device storage (`localStorage` and SQLite/SharedPreferences).
- **Network Independence:** YourNewTV remains 100% functional offline without an active internet connection.

---

## 3. Network Access Transparency

The only outbound network requests YourNewTV can ever make are strictly user-initiated:
1. **Local Weather (Optional):** If you enable ambient weather on the clock widget, the launcher queries an open meteorological API (such as Open-Meteo) using approximate coordinates or city names configured by you. No user identity or device identifier is transmitted.
2. **Local Media Metadata (Optional):** If you connect local DLNA/UPnP media libraries, queries execute solely across your local home network (LAN).

---

## 4. Permissions Disclosure

YourNewTV requests only the bare minimum Android system permissions necessary to operate as a TV home launcher:

| Permission | Technical Purpose |
|:---|:---|
| `QUERY_ALL_PACKAGES` | Required to discover installed TV apps and render them on your floating dock. |
| `ACCESS_NETWORK_STATE` | Required to display real-time Wi-Fi connectivity icons in the Control Center. |
| `INTERNET` | Optional; utilized only for ambient weather forecasts if enabled. |
| `SET_WALLPAPER` | Allows the launcher to update local desktop wallpapers. |
| `WAKE_LOCK` | Used to manage standby states and prevent abnormal Wi-Fi sleep disconnects. |

YourNewTV will never ask for contacts, camera, microphone, SMS, phone state, or location hardware permissions.

---

## 5. Security & Verification

Because YourNewTV is 100% open source under the MIT License, anyone can inspect, audit, and build the APK directly from source. You can monitor device network traffic via ADB (`adb shell tcpdump` or Wireshark) to verify zero outbound telemetry.
