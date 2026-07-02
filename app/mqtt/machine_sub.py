import json
import paho.mqtt.client as mqtt

from datetime import datetime, timezone
from app.database.mongo import machine_collection
from app.database.influx import influx_instance
from app.mqtt.topics import MACHINE_STATUS_TOPIC


BROKER = "localhost"
PORT = 1883


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    machine_id = data["machine_id"]
    status = data["status"]
    org_id = data["organization_id"]
    plant_id = data["plant_id"]

    now = datetime.now(timezone.utc)

    machine = machine_collection.find_one({"machine_id": machine_id})

    # If no change → ignore (VERY IMPORTANT)
    if machine and machine.get("machine_status") == status:
        return

    print(f" MACHINE STATUS CHANGE: {machine_id} -> {status}")

    # -------------------------
    # UPDATE MONGO
    # -------------------------
    machine_collection.update_one(
        {"machine_id": machine_id},
        {
            "$set": {
                "machine_status": status,
                "last_updated": now
            }
        },
        upsert=True
    )

    # -------------------------
    # WRITE INFLUX
    # -------------------------
    influx_instance.write_machine_status(
        machine_id,
        status,
        plant_id,
        org_id
    )


client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(MACHINE_STATUS_TOPIC)

print(" Machine Subscriber Running...")
client.loop_forever()