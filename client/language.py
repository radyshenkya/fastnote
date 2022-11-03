from json import load

from util.debug import debug
from util.pyqt import alert_message_box


class LanguageManager:
    FILE_MENU = "file_menu"
    NEW_DOC = "new_doc"
    OPEN_DOC = "open_doc"
    SAVE_DOC = "save_doc"
    SAVE_AS_DOC = "save_as_doc"
    OPEN_REMOTE_DOC = "open_remote_doc"
    UPLOAD_DOC = "upload_doc"
    LIST_REMOTE_DOC = "list_remote_doc"
    OPEN_SETTINGS = "open_settings"
    PLUGINS_MENU = "plugins_menu"
    PLUGINS_DETAILS = "plugins_details"
    PLUGIN_AUTHOR_PREFIX = "plugin_author_prefix"
    ADD_IMAGE_TOOL = "add_image_tool"
    NEW_TABLE_TOOL = "new_table_tool"
    BOLD_FONT_TOOL = "bold_font_tool"
    ITALIC_FONT_TOOL = "italic_font_tool"
    ADD_HEADER_TOOL = "add_header_tool"
    REMOVE_HEADER_TOOL = "remove_header_tool"
    ERR_SERVER_PROBLEMS = "err_server_problems"
    NOTE_CHOOSE = "note_choose"
    NOTE = "note"
    ERR_OPEN_NOTE = "err_open_note"
    ERR_SAVE_NOTE = "err_save_note"
    ERR_READONLY_NOTE = "err_readonly_note"
    STATUSBAR_SAVE_POSTFIX = "statusbar_save_postfix"
    ERR_NOTE_NOT_FOUND = "err_note_not_found"
    UNSAVE_FILE_NAME = "unsaved_file_name"
    ERROR = "error"

    def __init__(self, json_file_path: str) -> None:
        try:
            self.lang = load(open(json_file_path, 'r', encoding='utf-8'))
        except Exception as e:
            print("Can not load language file " + json_file_path +
                  ".\nRename one of files in language directory into \"default.json\" to start program.")
            exit(-1)

    def get(self, string_id: str):
        res = self.lang.get(string_id, None)
        if res == None:
            debug("Can not load word with id " + string_id)
            return ""
        return self.lang.get(string_id)

    def get_with_params(self, string_id: str, *args):
        res = self.lang.get(string_id, None)
        if res == None:
            debug("Can not load word with id " + string_id)
            return ""

        for arg in args:
            res = res.replace("{$}", arg, 1)

        return res
