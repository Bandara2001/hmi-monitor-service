from app.database.mongo import device_collection
from app.database.influx import influx_instance

# -------------------
# TEST MONGO
# -------------------
device = device_collection.find_one({
    "device_id": "6a16c4929c4147a3c7b1ce35"
})

print("MongoDB Device:", device)

# -------------------
# TEST INFLUX
# -------------------
influx_instance.write_heartbeat(
    device_id="6a16c4929c4147a3c7b1ce35",
    organization_id="6a168f2852441533fd8f39c0",
    plant_id="6a16bf134694c80ad78ea4d2"
)

print("InfluxDB heartbeat written successfully")

influx_instance.close()