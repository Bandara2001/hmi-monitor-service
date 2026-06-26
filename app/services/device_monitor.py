import time
from datetime import datetime, timezone

from app.database.mongo import device_collection

OFFLINE_THRESHOLD_SECONDS = 30
CHECK_INTERVAL = 10


def run_device_monitor():
    print("Device monitor started...")

    while True:
        now = datetime.now(timezone.utc)

        devices = list(device_collection.find({}))

        for device in devices:
            device_id = device.get("device_id")
            last_seen = device.get("last_seen")
            current_status = device.get("connectivity_status")

            # -------------------------
            # CASE 1: DEVICE NEVER SENT HEARTBEAT
            # -------------------------
            if not last_seen:
                if current_status != "OFFLINE":
                    device_collection.update_one(
                        {"device_id": device_id},
                        {
                            "$set": {
                                "connectivity_status": "OFFLINE",
                                "offline_reason": "NO_HEARTBEAT_YET",
                                "offline_at": now
                            }
                        }
                    )
                    print(f"Device OFFLINE (no heartbeat): {device_id}")
                continue

            # -------------------------
            # NORMALIZE TIME
            # -------------------------
            if last_seen.tzinfo is None:
                last_seen = last_seen.replace(tzinfo=timezone.utc)

            diff_seconds = (now - last_seen).total_seconds()

            # -------------------------
            # OFFLINE CONDITION
            # -------------------------
            if diff_seconds > OFFLINE_THRESHOLD_SECONDS:
                if current_status != "OFFLINE":
                    device_collection.update_one(
                        {"device_id": device_id},
                        {
                            "$set": {
                                "connectivity_status": "OFFLINE",
                                "offline_reason": "HEARTBEAT_TIMEOUT",
                                "offline_at": now
                            }
                        }
                    )
                    print(f"Device OFFLINE: {device_id}")

            # -------------------------
            # ONLINE CONDITION
            # -------------------------
            else:
                if current_status != "ONLINE":
                    device_collection.update_one(
                        {"device_id": device_id},
                        {
                            "$set": {
                                "connectivity_status": "ONLINE",
                                "offline_reason": None,
                                "offline_at": None
                            }
                        }
                    )
                    print(f"Device ONLINE: {device_id}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_device_monitor()