import logging
import sys
import threading
import time
import traceback
from abc import ABC, abstractmethod

from influxdb_client import Point

from collector.influx.influx_controller import InfluxController

class Asset(ABC):
    """
    An asset that can be collected.
    """

    stop_flag: threading.Event = threading.Event()
    influx_controller: InfluxController = InfluxController()
    sensor_read_interval: int = 5

    def set_sensor_read_interval(self, sensor_read_interval: int) -> None:
        """
        Set the sensor read interval.

        Args:
            sensor_read_interval: The sensor read interval.
        """
        self.sensor_read_interval = sensor_read_interval

    @abstractmethod
    def to_point(self) -> Point:
        """
        Convert the asset to an InfluxDB point.

        Returns:
            The InfluxDB point.
        """
        pass

    def collect(self) -> None:
        """
        Collect the asset data.
        """
        while not self.stop_flag.is_set():
            try:
                point = self.to_point()
                self.influx_controller.write(point)
                time.sleep(self.sensor_read_interval)
            except Exception as e:
                logging.error(f'Error collecting asset data: {e}')
                logging.error(traceback.format_exc())
                sys.exit(1)

    def start(self) -> None:
        """
        Start collecting the asset data.
        """
        self.stop_flag.clear()
        thread = threading.Thread(target=self.collect)
        thread.start()