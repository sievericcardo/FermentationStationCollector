from typing import Optional

class Humidity:
    def __init__(self):
        pass

    def read(self) -> Optional[float]:
        """
        Read the humidity value from the sensor.

        Returns:
            The humidity value if it was read, None otherwise.
        """
        pass

    def stop(self) -> None:
        """
        Stop the sensor.
        """
        pass