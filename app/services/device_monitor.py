import time
from datetime import datetime, timezone

from app.database.mongo import device_collection
from app.database.influx import influx_instance

OFFLINE_THRESHOLD_SECONDS = 30
CHECK_INTERVAL = 5


TARGET_DEVICE_ID = "6a16c4929c4147a3c7b1ce35"


def update_status(device, new_status, reason=None):

    device_id = device.get("device_id")
    if not device_id:
        return

    current_status = device.get("connectivity_status")

    
    if current_status == new_status:
        return

    now = datetime.now(timezone.utc)

    update_data = {
        "connectivity_status": new_status,
        "offline_reason": reason if new_status == "OFFLINE" else None,
        "offline_at": now if new_status == "OFFLINE" else None,
        "last_status_change": now
    }

    device_collection.update_one(
        {"device_id": device_id},
        {"$set": update_data}
    )

    influx_instance.write_status_event(
        device_id=device_id,
        organization_id=device.get("organization_id"),
        plant_id=device.get("device_plant_id"),
        status=new_status
    )

    print(f" {device_id} -> {new_status}")


def run_device_monitor():

    print(" DEVICE MONITOR STARTED ")

    while True:

        now = datetime.now(timezone.utc)

        
        device = device_collection.find_one({"device_id": TARGET_DEVICE_ID})

        if not device:
            print(" Device not found:", TARGET_DEVICE_ID)
            time.sleep(CHECK_INTERVAL)
            continue

        last_seen = device.get("last_seen")

        # -------------------
        # NO HEARTBEAT
        # -------------------
        if not last_seen:
            update_status(device, "OFFLINE", "NO_HEARTBEAT_YET")
            time.sleep(CHECK_INTERVAL)
            continue

        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(tzinfo=timezone.utc)

        diff = (now - last_seen).total_seconds()

        # -------------------
        # ONLINE
        # -------------------
        if diff <= OFFLINE_THRESHOLD_SECONDS:
            update_status(device, "ONLINE")

        # -------------------
        # OFFLINE
        # -------------------
        else:
            update_status(device, "OFFLINE", "HEARTBEAT_TIMEOUT")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_device_monitor()