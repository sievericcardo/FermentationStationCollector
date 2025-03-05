import serial
import time
import logging
from typing import Tuple
import threading

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
        self.lock = threading.Lock()
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout) 

    def read(self) -> Tuple[str, str]:
        """
        Read the serial data.

        Returns:
            The serial data.
        """
        with self.lock:
            self.ser.flushInput()
            self.ser.flushOutput()
            # time.sleep(1)
            data = self.ser.readline().decode('utf-8').strip()
            logging.debug(f'Read serial data: {data}')
            return data
