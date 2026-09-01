# System Instructions: HydroSense Edge

## Project Overview

Build a **complete, polished Flutter mobile app** called HydroSense Edge — a non-invasive human hydration monitoring prototype for an ESP32-based wearable. The app fuses PPG (MAX30102), tissue electrical impedance, motion (MPU6050), and environmental (DHT11) sensor data over BLE into a "Hydration Index." Ship a fully working Demo Mode so the app runs with zero hardware attached.

---

## Tech Stack

- Flutter (latest stable), Dart, null-safe, Material 3
- State management: `provider: ^6.1.2`
- BLE: `flutter_blue_plus: ^1.32.12` behind an abstract `BleService` interface
- Charts: `fl_chart: ^0.68.0`
- Local storage: `sqflite` + `path_provider`
- No deprecated Flutter/Material APIs

---

## Navigation Structure

### Bottom Navigation Tabs
- Home (default view)
- Analytics
- Device
- Settings

### Home Header Elements
- Connection indicator (● Connected / ○ Disconnected)
- Alerts bell icon with unread badge
- Dark/Light mode reflected app-wide from Settings

---

## File Structure

```
lib/
  main.dart
  app/            → app.dart, routes.dart, theme.dart
  models/         → hydration_data.dart, sensor_data.dart, device_status.dart
  screens/        → splash, onboarding, home, analytics, device, alerts, settings, about, measurement
  widgets/        → hydration_gauge, hydration_status_card, sensor_card, heart_rate_card,
                    confidence_card, battery_card, connection_status, hydration_chart,
                    alert_card, quick_stat_card
  services/       → ble_service.dart, mock_ble_service.dart, storage_service.dart, hydration_service.dart
  providers/      → hydration_provider.dart, device_provider.dart
  utils/          → constants.dart, formatters.dart, hydration_utils.dart
```
No file exceeds ~300 lines. `main.dart` only bootstraps `MultiProvider` + `runApp()`.

---

## Data Contract (BLE payload from ESP32)

```json
{
  "hydration": 72, "status": "HYDRATED", "confidence": 89,
  "heart_rate": 76, "spo2": 98, "impedance": 1.42,
  "motion": "STABLE", "temperature": 28.4, "humidity": 65,
  "battery": 84, "timestamp": 1725172471
}
```
- `HydrationData.fromJson` / `toJson` with **null-safe defaults for every field**
- Missing sensor values render as "—", never crash parsing

---

## BLE Architecture

```dart
abstract class BleService {
  Future<void> startScan();
  Future<void> stopScan();
  Future<void> connect(String deviceId);
  Future<void> disconnect();
  Stream<HydrationData> get hydrationDataStream;
  Stream<List<DiscoveredDevice>> get scanResultsStream;
  Stream<DeviceConnectionState> get connectionStateStream;
}
```
- `BleServiceImpl` — real ESP32 via `flutter_blue_plus`; comment GATT UUID placeholders clearly
- `MockBleService` — default active service; smooth, gradually-drifting values (not random jumps)

### Demo Mode Ranges
Hydration 65–85 · HR 65–95 bpm · SpO₂ 95–100% · Temp 25–32°C · Humidity 40–80% · Impedance drifts slowly · Motion mostly STABLE, occasionally MOVING · Battery slowly decreasing. Show a persistent "DEMO MODE" badge whenever active.

---

## Screens

- **Splash** — animated water-drop visual → Onboarding (first launch) or Home
- **Onboarding** — 3 pages (sensor fusion overview, ESP32 fusion, trends/alerts), Skip/Next/Get Started
- **Home** — hydration gauge (color reacts to thresholds: 70–100 green, 40–69 orange, 0–39 red), sensor card grid, quick actions
- **Measurement flow** — animated step sequence, blocks confident result on HIGH MOTION, shows Signal Quality GOOD/FAIR/POOR
- **Analytics** — fl_chart trend line, Today/7 Days/30 Days ranges, color-zoned bands, stat tiles
- **Device** — connection status, RSSI, battery, firmware, Scan/Connect/Disconnect/Refresh, discovered-device list
- **Alerts** — low hydration, critical hydration, low confidence, disconnected, low battery — icon + title + description + timestamp + severity
- **Settings** — Profile, Device, Measurement Settings, Notifications, Thresholds, Demo Mode, Dark Mode, About, Reset Data
- **About** — architecture explainer + disclaimer (see Brand Guidelines doc)

---

## Error Handling (all must be implemented, none stubbed)

Bluetooth unavailable/off, disconnected mid-session, no data yet, malformed JSON, missing fields, low confidence, high motion, low battery, storage failures — friendly messages only, never an uncaught exception.

---

## Android Configuration

Add and comment required permissions in `AndroidManifest.xml` for `flutter_blue_plus` (`BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, `ACCESS_FINE_LOCATION`), set `minSdkVersion` appropriately. Report every file touched for permissions and why.

---

## Build Order

1. Scaffold + pubspec 2. Theme + constants 3. Models 4. Routes + nav shell 5. Mock/BLE service 6. Providers 7. Home + gauge 8. Sensor widgets 9. Measurement flow 10. Storage 11. Analytics 12. Alerts 13. Device screen 14. Settings + About 15. Splash + Onboarding 16. Error/empty-state pass 17. Final polish

---

## Definition of Done

- [ ] `flutter pub get` succeeds
- [ ] `flutter analyze` — 0 issues
- [ ] `flutter test` passes (cover `HydrationData.fromJson` null-handling + threshold logic)
- [ ] Full demo flow works with zero hardware: splash → onboarding → measurement → analytics → alert
- [ ] No TODOs in core paths, no deprecated APIs, legible in light and dark mode