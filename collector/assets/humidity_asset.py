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

    def to_point(self, sensor_id: str, value: float) -> Point:
        """
        Convert the asset to an InfluxDB point.

        Returns:
            The InfluxDB point.
        """
        point = Point(Measurement.HUMIDITY.get_measurement_name())
        point.tag("th_sensor", sensor_id)
        point.field("value", value)
        return point
