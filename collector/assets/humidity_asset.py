from dataclasses import dataclass

from influxdb_client import Point

from collector.assets.asset import Asset
from collector.assets.measurement import Measurement
from collector.sensors.humidity import Humidity
from collector.sensors.temperature import Temperature

@dataclass
class HumidityAsset(Asset):
    """
    A fermentation station asset.

    Attributes:
    """
    sensor_id: str

    def to_point(self) -> Point:
        """
        Convert the asset to an InfluxDB point.

        Returns:
            The InfluxDB point.
        """
        point = Point(Measurement.HUMIDITY.get_measurement_name())
        point.tag("th_sensor", self.sensor_id)
        point.field("value", self.value)
        return point
