import os

DEBUG_MESSAGES = True
SETTINGS_FILE_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/settings.json"
PLUGINS_DIR_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/plugins/installed"
DEFAULT_SERVER = "https://5e02-46-181-148-140.eu.ngrok.io"
