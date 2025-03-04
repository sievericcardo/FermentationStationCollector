import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")
CONFIG_YML = os.path.join(os.path.dirname(__file__), "config.yml")

if not os.path.isfile(CONFIG_PATH):
    raise FileNotFoundError("Config ini file not found")
if not os.path.isfile(CONFIG_YML):
    raise FileNotFoundError("Config yml file not found")
