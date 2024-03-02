from typing import Optional

class Temperature:
    def __init__(self):
        pass

    def read(self) -> Optional[float]:
        """
        Read the temperature value from the sensor.

        Returns:
            The temperature value if it was read, None otherwise.
        """
        pass

    def stop(self) -> None:
        """
        Stop the sensor.
        """
        pass