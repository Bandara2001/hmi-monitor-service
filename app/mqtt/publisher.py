
import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPIC = "factory/hmi/heartbeat"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

DEVICE_ID = "6a16c4929c4147a3c7b1ce35"
ORG_ID = "6a168f2852441533fd8f39c0"
PLANT_ID = "6a16bf134694c80ad78ea4d2"

while True:
    payload = {
        "device_id": DEVICE_ID,
        "organization_id": ORG_ID,
        "plant_id": PLANT_ID,
        "timestamp": datetime.utcnow().isoformat()
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Sent:", payload)

    time.sleep(10)