from dataclasses import dataclass

from influxdb_client import Point

from collector.assets.asset import Asset
from collector.assets.measurement import Measurement
from collector.sensors.humidity import Humidity
from collector.sensors.temperature import Temperature

@dataclass
class FermentationStationAsset(Asset):
    """
    A fermentation station asset.
    """