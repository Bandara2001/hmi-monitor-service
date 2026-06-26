# HMI Monitor Service

Detects HMI Online/Offline status using MQTT heartbeat messages.

Heartbeat Interval : 10 seconds

Offline Threshold : 30 seconds

MongoDB:
- Device metadata
- Last seen timestamp
- Current connectivity status

InfluxDB:
- Heartbeat history

MQTT Topic

factory/hmi/heartbeat