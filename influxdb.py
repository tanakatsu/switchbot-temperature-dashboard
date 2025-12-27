from datetime import datetime, UTC

from influxdb_client import InfluxDBClient, Point, WriteOptions


class InfluxDBWriter:
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.write_opts = WriteOptions(
            batch_size=100,
            flush_interval=1_000,
            jitter_interval=0,
            retry_interval=5_000,
        )

    def __enter__(self):
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()

    def write(
        self,
        measurement: str,
        tag_name: str,
        tag: str,
        temp_c: float,
        humidity: float,
        time: datetime | None = None,
    ) -> None:
        write_api = self.client.write_api(write_options=self.write_opts)
        if time is None:
            time = datetime.now(UTC)
        p = (
            Point(measurement)
            .tag(tag_name, tag)
            .field("temp_c", float(temp_c))
            .field("humidity", float(humidity))
            .time(time)
        )
        write_api.write(bucket=self.bucket, record=p)
        # print(f"{time.isoformat()} wrote: temp_c={temp_c:.2f}, humidity={humidity:.2f}")
