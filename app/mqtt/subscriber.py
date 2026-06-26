
import json
import paho.mqtt.client as mqtt
from datetime import datetime

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

    # MongoDB update
    device_collection.update_one(
        {"device_id": device_id},
        {
            "$set": {
                "last_seen": datetime.utcnow(),
                "connectivity_status": "ONLINE"
            }
        }
    )

    # InfluxDB write
    influx_instance.write_heartbeat(
        device_id=device_id,
        organization_id=org_id,
        plant_id=plant_id
    )


client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

print("Subscriber running...")

client.loop_forever()