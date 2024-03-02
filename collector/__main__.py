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
from collector.assets import Asset
from collector.assets import utils

with open(CONFIG_PATH, 'r') as file:
    CONFIG = yaml.safe_load(file)


def main():
    """
    Main function that starts the collector.

    Returns:
        None
    """
    thread = Thread(target=__wait_message)
    thread.start()

    utils.setup_logging(CONFIG['logging']['level'])


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


def __wait_message():
    """
    Wait for a message from the message broker.

    Returns:
        None
    """
    __load_env_file()
    url = os.getenv("BROKER_URL")
    port = int(os.getenv("BROKER_PORT"))
    user = os.getenv("BROKER_USERNAME")
    password = os.getenv("BROKER_PASSWORD")

    hostname = socket.gethostname()
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    m = r.match(hostname)

    # Match the tuple to listen
    queue_destination = m.group(1) + "." + m.group(2) + ".config"

    try:
        conn = stomp.Connection([url, port])
        conn.set_listener('', Subscriber(conn, conf, CONFIG_PATH))
        conn.start()
        conn.connect(user, password, wait=True)

        conn.subscribe(destination=queue_destination, id=1, ack='auto')

        while True:
            sleep(1)

    except Exception as e:
        logging.error(f'Error waiting for message: {e}')
        logging.error(traceback.format_exc())
        sys.exit(1)

def __signal_handler(sig, frame):
    """
    Handle signals.

    Args:
        sig: The signal number.
        frame: The current stack frame.
    """
    logging.info('Shutting down collector...')
    sys.exit(0)



