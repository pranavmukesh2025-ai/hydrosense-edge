# hydrosense-edge
# 💧 HydroSense Edge

### Smart Non-Invasive Hydration Monitoring using Multi-Sensor Fusion

<p align="center">
  <b>An ESP32-powered hydration monitoring system combining bioimpedance, PPG, motion and environmental sensing with a Flutter mobile application.</b>
</p>

<p align="center">

![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B?logo=flutter)
![Dart](https://img.shields.io/badge/Dart-3.x-0175C2?logo=dart)
![ESP32](https://img.shields.io/badge/ESP32-Embedded-E7352C?logo=espressif)
![BLE](https://img.shields.io/badge/Bluetooth-Low%20Energy-0082FC)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

</p>

---

##  Project Preview

> **Screenshots will be added here**

<!-- Add your screenshots here -->

| Dashboard    | Measurement  | Analytics    |
| ------------ | ------------ | ------------ |
| *Screenshot* | *Screenshot* | *Screenshot* |

| Alerts       | Device       | Settings     |
| ------------ | ------------ | ------------ |
| *Screenshot* | *Screenshot* | *Screenshot* |

---

#  Overview

**HydroSense Edge** is a prototype smart hydration-monitoring system designed to estimate a user's hydration state using multiple physiological and environmental parameters.

The system combines:

* **Bioelectrical impedance**
*  **Heart rate**
*  **SpO₂**
* **Motion sensing**
* **Temperature**
* Humidity**
*  **Device battery status**

An **ESP32** acts as the embedded sensing and communication platform, while a **Flutter mobile application** provides real-time monitoring, guided measurements, alerts and historical analytics.

The system communicates through **Bluetooth Low Energy (BLE)**.

> ⚠️ **Disclaimer:** HydroSense Edge is an experimental research prototype. The Hydration Index is not clinically validated and must not be used for medical diagnosis or treatment.

---

# 🎯 Problem Statement

Dehydration can negatively affect physical performance, concentration and overall wellbeing.

Traditional hydration assessment can be inconvenient and may depend on subjective symptoms such as thirst.

**HydroSense Edge explores a non-invasive, sensor-based approach to hydration monitoring by combining multiple physiological signals instead of relying on a single parameter.**

---

# 💡 Proposed Solution

HydroSense Edge follows a multi-stage sensing and processing pipeline:

```text
             PHYSIOLOGICAL SENSORS
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
  Bioimpedance     PPG           Motion
       │          HR + SpO₂        │
       │             │             │
       └─────────────┼─────────────┘
                     │
                     ▼
                  ESP32
                     │
                    BLE
                     │
                     ▼
              Flutter Mobile App
                     │
                     ▼
              Sensor Processing
                     │
                     ▼
              Hydration Index
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Status       Alerts      Analytics
```

---

# ✨ Key Features

###  Multi-Sensor Hydration Monitoring

The system combines multiple sensor inputs to generate an experimental hydration estimate.

| Parameter        | Source               | Purpose                               |
| ---------------- | -------------------- | ------------------------------------- |
| Tissue Impedance | Bioimpedance circuit | Primary hydration-related measurement |
| Heart Rate       | MAX30102 / PPG       | Physiological parameter               |
| SpO₂             | MAX30102 / PPG       | Oxygen saturation                     |
| Motion           | MPU6050              | Motion artifact detection             |
| Temperature      | DHT11                | Environmental information             |
| Humidity         | DHT11                | Environmental information             |
| Battery          | ESP32                | Device monitoring                     |

---

##  Hydration Index

HydroSense Edge generates an experimental **Hydration Index from 0–100**.

The prototype combines impedance-based information with additional physiological and environmental parameters.

```text
Bioimpedance
     │
     ▼
Base Hydration Estimate
     │
     ├── Heart Rate
     ├── Temperature
     ├── Humidity
     └── Motion / Signal Quality
              │
              ▼
        Hydration Index
              │
       ┌──────┼──────┐
       ▼      ▼      ▼
   HYDRATED  ATTENTION  HIGH RISK
```

### Prototype Classification

| Hydration Index | Status       |
| --------------: | ------------ |
|        **≥ 70** | 🟢 HYDRATED  |
|       **40–69** | 🟠 ATTENTION |
|        **< 40** | 🔴 HIGH RISK |

> These thresholds are prototype parameters and have not been clinically validated.

---

# 🔬 Guided Measurement

The application provides a structured measurement workflow.

### Measurement Process

```text
1. Electrode Contact Verification
              ↓
2. Optical PPG Acquisition
              ↓
3. Bioimpedance Measurement
              ↓
4. Motion & Environmental Compensation
              ↓
5. Hydration Index Calculation
```

The system also evaluates movement during measurement.

If excessive movement is detected:

```text
Motion Detected
      ↓
Measurement Paused
      ↓
User Remains Still
      ↓
Motion Stabilizes
      ↓
Measurement Resumes
```

This improves the reliability of the measurement process by reducing motion-related artifacts.

---

#  Analytics

HydroSense Edge stores historical measurements and provides a dedicated analytics dashboard.

### Analytics include

* 📈 Hydration Index trends
* Average hydration
* Peak hydration
* Minimum hydration
* Measurement confidence
* Historical measurements
* Hydration stability

### Supported periods

* Today
* Last 7 Days
* Last 30 Days

---

#  Alert System

The application continuously evaluates sensor and hydration data to identify potentially important conditions.

### Alerts include

🔴 **High-Risk Hydration**

Triggered when the Hydration Index falls below the configured critical threshold.

🟠 **Attention**

Triggered when hydration enters the warning range.

🏃 **Motion Warning**

Indicates excessive movement during measurement.

📉 **Low Confidence**

Indicates that the measurement quality may be unreliable.

🔋 **Low Battery**

Indicates that the sensing device requires charging.

---

#  Bluetooth Low Energy Communication

The ESP32 communicates with the Flutter application using **Bluetooth Low Energy**.

The software uses a dedicated BLE abstraction layer so that the application is not tightly coupled to the physical BLE implementation.

```text
Flutter UI
    │
    ▼
Hydration Provider
    │
    ▼
BLE Service Interface
    │
    ├───────────────┐
    ▼               ▼
Real BLE        Mock BLE
    │               │
    ▼               ▼
 ESP32          Demo Mode
```

### BLE Service

```text
Service UUID:
4fafc201-1fb5-459e-8fcc-c5c9c331914b

Characteristic UUID:
beb5483e-36e1-4688-b7f5-ea07361b26a8
```

The ESP32 transmits sensor telemetry to the mobile application using structured JSON data.

Example:

```json
{
  "hydration": 78.4,
  "status": "HYDRATED",
  "confidence": 91.5,
  "heartRate": 74,
  "spo2": 98,
  "impedance": 1.42,
  "motion": "STABLE",
  "temperature": 28.1,
  "humidity": 62.4,
  "battery": 84
}
```

---

# 🏃 Motion & Measurement Quality

Movement can introduce unwanted artifacts into physiological measurements.

HydroSense Edge therefore monitors motion and measurement confidence.

### Signal Quality

| Condition                          | Quality |
| ---------------------------------- | ------- |
| Stable + high confidence           | 🟢 Good |
| Moderate confidence                | 🟠 Fair |
| Significant movement / poor signal | 🔴 Poor |

The user is informed when a measurement may not be reliable.

---

#  Data Storage

Measurement history is stored locally using **SQLite**.

Each measurement can contain:

```text
Timestamp
Hydration Index
Status
Confidence
Heart Rate
SpO₂
Impedance
Motion
Temperature
Humidity
Notes
```

The application also provides a fallback storage mechanism so that the application can continue operating if persistent database storage is unavailable.

---

#  Software Architecture

The Flutter application follows a modular architecture.

```text
┌─────────────────────────────┐
│          UI Layer           │
│                             │
│ Home │ Measurement          │
│ Analytics │ Alerts          │
│ Device │ Settings           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      State Management       │
│                             │
│ HydrationProvider           │
│ DeviceProvider              │
│ AlertsProvider              │
│ SettingsProvider            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Service Layer        │
│                             │
│ Hydration Service           │
│ BLE Service                 │
│ Storage Service             │
└──────────────┬──────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
      ESP32         SQLite
```

### Major Components

| Component           | Responsibility                             |
| ------------------- | ------------------------------------------ |
| `HydrationProvider` | Hydration state and measurement workflow   |
| `DeviceProvider`    | Device and BLE management                  |
| `AlertsProvider`    | Alert management                           |
| `HydrationService`  | Hydration estimation and sensor processing |
| `BleService`        | BLE abstraction                            |
| `BleServiceImpl`    | Physical ESP32 BLE implementation          |
| `MockBleService`    | Demo/simulated sensor data                 |
| `StorageService`    | Local database operations                  |
| `HydrationUtils`    | Hydration and signal-quality logic         |

---

#  Project Structure

```text
hydrosense/
│
├── android/
├── ios/
├── web/
│
├── assets/
│   └── icon/
│
├── lib/
│   ├── app/
│   │   ├── app.dart
│   │   ├── routes.dart
│   │   └── theme.dart
│   │
│   ├── models/
│   │   ├── alert_item.dart
│   │   ├── device_status.dart
│   │   ├── hydration_data.dart
│   │   └── sensor_data.dart
│   │
│   ├── providers/
│   │   ├── alerts_provider.dart
│   │   ├── device_provider.dart
│   │   ├── hydration_provider.dart
│   │   └── settings_provider.dart
│   │
│   ├── screens/
│   │   ├── home_screen.dart
│   │   ├── measurement_screen.dart
│   │   ├── analytics_screen.dart
│   │   ├── alerts_screen.dart
│   │   ├── device_screen.dart
│   │   ├── settings_screen.dart
│   │   └── about_screen.dart
│   │
│   ├── services/
│   │   ├── ble_service.dart
│   │   ├── ble_service_impl.dart
│   │   ├── mock_ble_service.dart
│   │   ├── hydration_service.dart
│   │   └── storage_service.dart
│   │
│   ├── utils/
│   │   ├── constants.dart
│   │   ├── formatters.dart
│   │   └── hydration_utils.dart
│   │
│   ├── widgets/
│   │   ├── hydration_gauge.dart
│   │   ├── hydration_chart.dart
│   │   ├── sensor_card.dart
│   │   ├── alert_card.dart
│   │   └── battery_card.dart
│   │
│   └── main.dart
│
├── test/
│   ├── hydration_data_test.dart
│   └── hydration_utils_test.dart
│
├── pubspec.yaml
├── HydroSense_Edge.apk
└── README.md
```

---

#  Hardware Architecture

The proposed hardware system consists of an ESP32 and multiple sensing modules.

```text
                    ┌──────────────┐
                    │    ESP32     │
                    │ Main Control │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   Bioimpedance         MAX30102         MPU6050
      Circuit              │                │
          │            HR + SpO₂          Motion
          │
          └────────────────┐
                           ▼
                         DHT11
                           │
                    Temperature +
                       Humidity
```

### Hardware Components

* ESP32 development board
* Bioimpedance measurement circuit
* MAX30102 PPG sensor
* MPU6050 IMU
* DHT11 temperature/humidity sensor
* Electrodes
* Portable power source
* Supporting electronic components

---

# 🔄 End-to-End Data Flow

```text
        Sensors
           │
           ▼
        ESP32
           │
       Sensor Data
           │
           ▼
         BLE
           │
           ▼
     Flutter Application
           │
           ▼
     Data Processing
           │
           ▼
    Hydration Estimation
           │
     ┌─────┼─────┐
     ▼     ▼     ▼
  Dashboard Alerts Analytics
```

---

# 🧪 Demo Mode

HydroSense Edge includes a **Demo Mode** that allows the complete application to be evaluated without the physical ESP32 device.

Demo Mode simulates:

* Hydration Index
* Heart rate
* SpO₂
* Impedance
* Motion
* Temperature
* Humidity
* Battery
* Measurement confidence

It also provides simulated historical measurements for testing the analytics interface.

### Why Demo Mode?

It allows evaluators to explore the complete application without requiring hardware:

```text
Dashboard       ✓
Measurement     ✓
Alerts          ✓
Analytics       ✓
Device UI       ✓
History         ✓
```

---

#  Getting Started

## Prerequisites

Install:

* Flutter SDK
* Dart SDK
* Android Studio
* Android SDK
* Android device or emulator

For hardware testing:

* ESP32 development environment
* Required sensor modules
* ESP32 firmware implementing the HydroSense BLE service

---

## Clone the Repository

```bash
git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPOSITORY>.git

cd <YOUR-REPOSITORY>
```

---

## Install Dependencies

```bash
flutter pub get
```

---

## Run the Application

```bash
flutter run
```

---

## Build APK

```bash
flutter build apk --release
```

The generated APK will be available at:

```text
build/app/outputs/flutter-apk/
```

---

#  Testing

Run the automated tests using:

```bash
flutter test
```

The project contains unit tests for core hydration data and utility functionality.

---

# Application Modules

| Module         | Description                                |
| -------------- | ------------------------------------------ |
| Dashboard   | Real-time hydration and sensor information |
| Measurement | Guided hydration measurement               |
| Analytics   | Historical trends and statistics           |
| Alerts      | Hydration and device warnings              |
| Device      | ESP32/BLE device management                |
| Settings    | Application configuration                  |
| About       | Project and prototype information          |

---

#  Future Improvements

### Hardware

* PCB-based hardware integration
* Improved bioimpedance analog front-end
* Better electrode design
* Sensor calibration
* Lower power consumption
* Compact wearable enclosure
* Rechargeable battery system

### Signal Processing

* Advanced filtering
* Motion artifact removal
* Improved signal-quality estimation
* Adaptive sensor fusion
* Real-time waveform analysis

### Hydration Estimation

The current Hydration Index uses experimental rule-based processing.

Future development could involve:

```text
Real Sensor Data
       ↓
Signal Processing
       ↓
Feature Extraction
       ↓
Large Experimental Dataset
       ↓
Machine Learning
       ↓
Personalized Calibration
       ↓
Validated Hydration Estimation
```

### Application

* Cloud synchronization
* User accounts
* Long-term health trends
* Personalized hydration recommendations
* Wearable notifications
* Improved BLE reconnection
* Remote monitoring
* Firmware updates

---

#  Limitations

HydroSense Edge is currently a **prototype**.

### Current limitations

1. The Hydration Index is not clinically validated.
2. The current estimation method is experimental.
3. Demo Mode uses simulated telemetry.
4. Physical sensor readings require hardware calibration.
5. BLE communication requires compatible ESP32 firmware.
6. The system is not intended for medical diagnosis.

---


#  Technology Stack

### Embedded

* **ESP32**
* MAX30102
* MPU6050
* DHT11
* Bioimpedance circuit

### Mobile

* **Flutter**
* **Dart**
* **Provider**
* **flutter_blue_plus**
* **SQLite / sqflite**
* **FL Chart**
* **Shared Preferences**

### Communication

* Bluetooth Low Energy
* GATT
* JSON telemetry

---

#  Team

| Team Member | Responsibility              |
| ----------- | --------------------------- |
| ``    | Embedded Systems / Hardware |
| `<NAME>`    | Flutter Application         |
| `<NAME>`    | Signal Processing           |
| `<NAME>`    | Integration / Testing       |

---

# 📜 License

This project is developed for **educational, research and prototype purposes**.

---

# 💧 HydroSense Edge

> **Measure. Analyze. Understand.**

HydroSense Edge demonstrates the integration of **embedded systems, physiological sensing, wireless communication, sensor fusion and mobile application development** into a unified hydration-monitoring prototype.

<p align="center">
  <b>ESP32 + Multi-Sensor Fusion + BLE + Flutter</b>
</p>

