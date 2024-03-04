import serial
import time
import logging
from typing import Tuple

class SerialReader:
    """
    A class to read serial data from a serial port.
    """

    def __init__(self, port: str, baudrate: int, timeout: int):
        """
        Initialize the serial reader.

        Args:
            port: The serial port.
            baudrate: The baudrate.
            timeout: The timeout.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def read(self) -> Tuple[str, str]:
        """
        Read the serial data.

        Returns:
            The serial data.
        """
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
            ser.flushInput()
            ser.flushOutput()
            # time.sleep(1)
            data = ser.readline().decode('utf-8').strip()
            logging.debug(f'Read serial data: {data}')
            return data