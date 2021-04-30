import json
import platform

DEFAULT_OS_NAME = platform.uname().system

with open('config/config.json') as file:
    DATA = json.load(file)
