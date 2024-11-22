import json
import logging
import os
import signal
import sys
import traceback
import stomp
import socket
import re
import yaml

from sys import argv
from threading import Thread
from time import sleep
from typing import Dict, List, Tuple

from collector.config import CONFIG_PATH
from collector.config import CONFIG_YML
from collector.assets import Asset
from collector.assets import utils
from collector.queue.subscriber import Subscriber
from collector.influx.influx_controller import InfluxController

from configparser import ConfigParser

with open(CONFIG_YML, 'r') as file:
    CONFIG = yaml.safe_load(file)

conf: ConfigParser = ConfigParser()
conf.read(CONFIG_PATH)

def main():
    """
    Main function that starts the collector.

    Returns:
        None
    """
    thread = Thread(target=_wait_message)
    thread.start()

    utils.setup_logging(CONFIG['logging']['level'])
    
    signal.signal(signal.SIGINT, __signal_handler)

    asset_list = __init_thread()
    logging.info('Collector started')


def __load_env_file(env_file_path=".env"):
    """"
    Load environment variables from a file.

    Attributes:
        env_file_path: The path to the environment file.
    
    Returns:
        None
    """
    try:
        with open(env_file_path, 'r') as file:
            for line in file:
                if not line.strip() or line.startswith("#"):
                    continue

                key, value = line.strip().split("=", 1)
                os.environ[key] = value
    except FileNotFoundError:
        print(f"Environment file not found: {env_file_path}")
        logging.warning(f"Environment file not found: {env_file_path}")


def _wait_message():
    print("Waiting for message")

# def __wait_message():
    # """
    # Wait for a message from the message broker.

    # Returns:
    #     None
    # """
    # __load_env_file()
    # url = os.getenv("BROKER_URL")
    # port = int(os.getenv("BROKER_PORT"))
    # user = os.getenv("BROKER_USERNAME")
    # password = os.getenv("BROKER_PASSWORD")

    # hostname = socket.gethostname()
    # r = re.compile("([a-zA-Z]+)([0-9]+)")
    # m = r.match(hostname)

    # # Match the tuple to listen
    # queue_destination = m.group(1) + "." + m.group(2) + ".config"

    # try:
    #     conn = stomp.Connection([url, port])
    #     conn.set_listener('', Subscriber(conn, conf, CONFIG_YML))
    #     conn.start()
    #     conn.connect(user, password, wait=True)

    #     conn.subscribe(destination=queue_destination, id=1, ack='auto')

    #     while True:
    #         sleep(1)

    # except Exception as e:
    #     logging.error(f'Error waiting for message: {e}')
    #     logging.error(traceback.format_exc())
    #     sys.exit(1)

def __signal_handler(sig, frame):
    """
    Handle signals.

    Args:
        sig: The signal number.
        frame: The current stack frame.
    """
    logging.info('Shutting down collector...')
    sys.exit(0)


def __init_thread() -> List[Tuple[Asset, Thread]]:
    """
    Initialize the threads for the assets. For each asset a thread is created
    """
    asset_list: List[Tuple[Asset, Thread]] = []

    try:
        influx_controller = InfluxController()
    except Exception as e:
        print(f'Error initializing InfluxDB controller: {e}')
        logging.error(f'Error initializing InfluxDB controller: {e}')
        logging.error(traceback.format_exc())
        sys.exit(1)

    try:
        influx_controller.create_bucket(CONFIG['influx']['bucket'])
    except Exception as e:
        print(f'Error creating InfluxDB bucket: {e}')
        logging.error(f'Error creating InfluxDB bucket: {e}')
        logging.error(traceback.format_exc())
        sys.exit(1)

    logging.info(f'InfluxDB bucket {CONFIG["influx"]["bucket"]} created')
    logging.info('Initialising threads')

    for asset in CONFIG['assets']:
        a = Asset(int(asset['port']), asset['baudrate'], asset['timeout'])
        t = Thread(target=a.start)
        asset_list.append((a, t))
        t.start()


if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == "--demo":
            pass # to add a demo portion
        else:
            print("Invalid argument")
            sys.exit(1)
    else:
        main()
