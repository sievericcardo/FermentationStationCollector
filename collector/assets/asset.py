import logging
import sys
import threading
import time
import traceback
from abc import ABC, abstractmethod

from influxdb_client import Point

from collector.influx.influx_controller import InfluxController
from collector.sensors.read_serial import SerialReader
from collector.assets.measurement import Measurement

class Asset(ABC):
    """
    An asset that can be collected.
    """
    def __init__(self, port, baudrate, timeout) -> None:
        super().__init__()
        self.serial_reader = SerialReader(int(port), baudrate, timeout)

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


    def __process_data(self, data: str) -> None:
        """
        Process the data from the serial port.

        Args:
            data: The data from the serial port.
        """
        values = data.split(',')

        if len(values) <= 2:
            logging.error(f'Invalid data: {data}')
            return
        
        if values[0] == 'TH':
            id = values[1]
            temperature = float(values[2])
            humidity = float(values[3])

            t = Point(Measurement.TEMPERATURE.get_measurement_name()) \
                .tag('th_sensor', id) \
                .field('value', temperature)
            self.influx_controller.write(t)

            h = Point(Measurement.HUMIDITY.get_measurement_name()) \
                .tag('th_sensor', id) \
                .field('value', humidity)
            self.influx_controller.write(h)
        elif values[0] == 'PH':
            id = values[1]
            ph = float(values[2])

            p = Point(Measurement.PH.get_measurement_name()) \
                .tag('ph_sensor', id) \
                .field('value', ph)
            self.influx_controller.write(p)

    def __collect(self) -> None:
        """
        Collect the asset data.
        """
        while not self.stop_flag.is_set():
            try:
                data = self.serial_reader.read()
                self.__process_data(data)

                # point = self.to_point()
                # self.influx_controller.write(point)
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
        thread = threading.Thread(target=self.__collect)
        thread.start()