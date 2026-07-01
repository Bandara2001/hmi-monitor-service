import json
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

from app.database.mongo import device_collection
from app.database.influx import influx_instance

BROKER = "localhost"
PORT = 1883
TOPIC = "factory/hmi/heartbeat"


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    device_id = data["device_id"]
    org_id = data["organization_id"]
    plant_id = data["plant_id"]

    print("Received:", data)

    now = datetime.now(timezone.utc)

    # -------------------------------
    # UPSERT DEVICE (ENSURE IT EXISTS)
    # -------------------------------
    result = device_collection.update_one(
        {"device_id": device_id},
        {
            "$set": {
                "last_seen": now,
                "connectivity_status": "ONLINE"
            }
        },
        upsert=True
    )

    print("Mongo matched:", result.matched_count, "modified:", result.modified_count)

    


client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

print("Subscriber running...")

client.loop_forever()