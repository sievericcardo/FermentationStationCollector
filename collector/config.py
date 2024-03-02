import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yml")

if not os.path.isfile(CONFIG_PATH):
    raise FileNotFoundError("Config file not found")
