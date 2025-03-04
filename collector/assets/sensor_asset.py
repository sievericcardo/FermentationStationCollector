from influxdb_client import Point

from collector.assets.asset import Asset

from collector.assets.measurement import Measurement

class SensorAsset(Asset):
    """
    A concrete implementation of Asset for sensors that report TH or PH values.
    """
    def __init__(self, port: str, baudrate: int, timeout: int) -> None:
        super().__init__(port, baudrate, timeout)

    def to_point(self) -> Point:
        """
        This method is required by the abstract class but not used in this implementation
        since the point creation is handled in __process_data.
        
        Returns:
            A dummy Point object
        """
        return Point("point") 