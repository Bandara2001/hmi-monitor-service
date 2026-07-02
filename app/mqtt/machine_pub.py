import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime, timezone
from app.mqtt.topics import MACHINE_STATUS_TOPIC

BROKER = "localhost"
PORT = 1883

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

MACHINE_ID = "6a2685536f69fa969ff2f19f"
ORG_ID = "6a168f2852441533fd8f39c0"
PLANT_ID = "6a192a3e2375914806aa199c"

while True:

    command = input("START / STOP: ").strip().upper()

    if command not in ["START", "STOP"]:
        continue

    payload = {
        "machine_id": MACHINE_ID,
        "organization_id": ORG_ID,
        "plant_id": PLANT_ID,
        "status": "RUNNING" if command == "START" else "STOPPED",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    client.publish(MACHINE_STATUS_TOPIC, json.dumps(payload))
    print("Sent:", payload)