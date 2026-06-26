from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DATABASE", "IoT")

# InfluxDB
INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

# MQTT (later use)
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# Heartbeat config
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", 10))
OFFLINE_THRESHOLD = int(os.getenv("OFFLINE_THRESHOLD", 30))