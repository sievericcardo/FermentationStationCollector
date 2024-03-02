from enum import Enum

ASSET_MODEL_PREFIX = 'ast:'

class Measurement(Enum):
    """
    The measurement types.
    """
    HUMIDITY = 'humidity'
    TEMPERATURE = 'temperature'
    PH: 'ph'

    def get_measurement_name(self) -> str:
        """
        Get the measurement name.

        Returns:
            The measurement name.
        """
        return f'{ASSET_MODEL_PREFIX}{self.value}'