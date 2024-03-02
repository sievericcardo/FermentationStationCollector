import datetime
import logging
import os
from typing import List

import pytz
from influxdb_client import Point

from collector.assets.asset import Asset

TIMEZONE = pytz.timezone('Etc/UTC')


def assets_to_points(assets: List[Asset]) -> List[Point]:
    """
    Convert a list of assets to a list of InfluxDB points.

    Args:
        assets: The list of assets.

    Returns:
        The list of InfluxDB points.
    """
    return [measurement.to_point() for measurement in assets]


def setup_logging(demo: bool=False):
    """
    Setup logging for the collector.

    Args:
        demo: Whether or not to set up logging for the demo.

    Returns:
        None
    """
    if demo:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_path = os.path.join(os.path.dirname(__file__), 'logs')

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    f = open(os.path.join(log_path, 'collector.log'), 'w')
    f.close()

    logging.basicConfig(
        filename=os.path.join(log_path, 'collector.log'), 
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logging.info(f'Collector PID: {os.getpid()}')

