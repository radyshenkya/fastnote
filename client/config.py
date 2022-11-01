import os

DEBUG_MESSAGES = True
SETTINGS_FILE_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/settings.json"
PLUGINS_DIR_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/plugins/installed"
DEFAULT_SERVER = "https://5e02-46-181-148-140.eu.ngrok.io"
RECENT_FILES_DB_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/recent_files.sqlite"
MAX_RECENT_FILES_IN_DB = 10
