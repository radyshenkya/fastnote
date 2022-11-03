import os

from language import LanguageManager

SETTINGS_FILE_PATH = os.getcwd() + "/settings.json"
PLUGINS_DIR_PATH = os.getcwd() + "/plugins/installed"
DEFAULT_SERVER = "https://5e02-46-181-148-140.eu.ngrok.io"
RECENT_FILES_DB_PATH = os.getcwd() + "/recent_files.db"
LANGUAGE_FILE = os.getcwd() + "/languages/default.json"
MAX_RECENT_FILES_IN_DB = 10

LANG_MANAGER = LanguageManager(LANGUAGE_FILE)
