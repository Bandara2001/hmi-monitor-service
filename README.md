# HMI Monitor Service

This service monitors industrial HMI devices using MQTT heartbeat messages and detects real-time ONLINE / OFFLINE status.

---

## Task 1: Device Connectivity Monitoring

### Goal
Detect whether an HMI device is ONLINE or OFFLINE based on heartbeat messages.

---

## ⚙️ How It Works

### 1. MQTT Heartbeat
Devices send heartbeat messages every **10 seconds**.

**MQTT Topic:**

factory/hmi/heartbeat


**Payload Example:**
```json

{
  "device_id": "6a16c4929c4147a3c7b1ce35",
  "organization_id": "6a168f2852441533fd8f39c0",
  "plant_id": "6a16bf134694c80ad78ea4d2",
  "timestamp": "2026-06-26T10:12:36.855Z"
}
```

## 2. MongoDB (Device State)

Stores:

Device metadata
Last heartbeat time (last_seen)
Connectivity status (ONLINE / OFFLINE)
Offline reason

Logic:

If heartbeat received → ONLINE
If no heartbeat for 30 seconds → OFFLINE

## 3. Offline Detection Logic
Condition	Status
Heartbeat received within 30s	ONLINE
No heartbeat > 30s	OFFLINE

## 4. InfluxDB (Time Series)

Stores:

All heartbeat events for analytics/history

Services to Run

You must run these in separate terminals:

1. MQTT Subscriber
python -m app.mqtt.subscriber
2. Device Monitor (Offline Checker)
python -m app.services.device_monitor
3. MQTT Publisher (Simulation)
python -m app.mqtt.publisher

How to Test Task 1

Step 1: Start all services
  Subscriber
  Monitor
  Publisher

Step 2: Observe
  Device shows ONLINE

Step 3: Stop Publisher
  Wait 30 seconds
  Device becomes OFFLINE

Step 4: Restart Publisher
  Device becomes ONLINE again automatically
