from influxdb_client import InfluxDBClient, Point
from app.config.settings import (
    INFLUX_URL,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_BUCKET
)


class InfluxDB:

    def __init__(self):
        self.client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=INFLUX_ORG
        )

        self.write_api = self.client.write_api()
        self.query_api = self.client.query_api()

    def write_status_event(
        self,
        device_id,
        organization_id,
        plant_id,
        status
    ):

        point = (
            Point("device_status")
            .tag("device_id", device_id)
            .tag("organization_id", organization_id)
            .tag("plant_id", plant_id)
            .tag("status", status)
            .field("value", 1)
        )

        self.write_api.write(
            bucket=INFLUX_BUCKET,
            record=point
        )

    def close(self):
        self.client.close()


influx_instance = InfluxDB()