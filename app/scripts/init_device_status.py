from app.database.mongo import device_collection

def init_device_status():
    result = device_collection.update_many(
        {},
        {
            "$set": {
                "last_seen": None,
                "connectivity_status": "OFFLINE",
                "offline_reason": "INIT"
            }
        }
    )

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)
    print("Device status initialized")

if __name__ == "__main__":
    init_device_status()