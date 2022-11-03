import os

from language import LanguageManager

SETTINGS_FILE_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/settings.json"
PLUGINS_DIR_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/plugins/installed"
DEFAULT_SERVER = "https://5e02-46-181-148-140.eu.ngrok.io"
RECENT_FILES_DB_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/recent_files.db"
LANGUAGE_FILE = os.path.dirname(
    os.path.realpath(__file__)) + "/languages/default.json"
MAX_RECENT_FILES_IN_DB = 10

LANG_MANAGER = LanguageManager(LANGUAGE_FILE)
