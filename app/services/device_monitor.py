import time
from datetime import datetime, timezone

from app.database.mongo import device_collection
from app.database.influx import influx_instance

OFFLINE_THRESHOLD_SECONDS = 30
CHECK_INTERVAL = 5


def update_status(device, new_status, reason=None):
    """
    Update MongoDB and InfluxDB only if the device status changes.
    """

    device_id = device["device_id"]

    if device.get("connectivity_status") == new_status:
        return

    now = datetime.now(timezone.utc)

    update_data = {
        "connectivity_status": new_status,
        "offline_reason": reason if new_status == "OFFLINE" else None,
        "offline_at": now if new_status == "OFFLINE" else None,
    }

    device_collection.update_one(
        {"device_id": device_id},
        {"$set": update_data}
    )

    influx_instance.write_status_event(
        device_id=device_id,
        organization_id=device["organization_id"],
        plant_id=device["plant_id"],
        status=new_status
    )

    print(f"{device_id} -> {new_status}")


def run_device_monitor():

    print("Device monitor started...")

    while True:

        now = datetime.now(timezone.utc)

        devices = list(device_collection.find({}))

        for device in devices:

            last_seen = device.get("last_seen")

            # -----------------------------------
            # Never received heartbeat
            # -----------------------------------
            if last_seen is None:
                update_status(
                    device,
                    "OFFLINE",
                    "NO_HEARTBEAT_YET"
                )
                continue

            # -----------------------------------
            # Make timezone aware if necessary
            # -----------------------------------
            if last_seen.tzinfo is None:
                last_seen = last_seen.replace(tzinfo=timezone.utc)

            diff = (now - last_seen).total_seconds()

            # -----------------------------------
            # Device is ONLINE
            # -----------------------------------
            if diff <= OFFLINE_THRESHOLD_SECONDS:

                update_status(
                    device,
                    "ONLINE"
                )

            # -----------------------------------
            # Device is OFFLINE
            # -----------------------------------
            else:

                update_status(
                    device,
                    "OFFLINE",
                    "HEARTBEAT_TIMEOUT"
                )

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_device_monitor()