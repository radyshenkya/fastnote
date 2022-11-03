import os

from language import LanguageManager

ROOT_DIR_PATH = os.path.dirname(__file__)

SETTINGS_FILE_PATH = ROOT_DIR_PATH + "/settings.json"
PLUGINS_DIR_PATH = ROOT_DIR_PATH + "/plugins/installed"
DEFAULT_SERVER = "https://5e02-46-181-148-140.eu.ngrok.io"
RECENT_FILES_DB_PATH = ROOT_DIR_PATH + "/recent_files.db"
LANGUAGE_FILE = ROOT_DIR_PATH + "/languages/default.json"
MAX_RECENT_FILES_IN_DB = 10

LANG_MANAGER = LanguageManager(LANGUAGE_FILE)
