from pathlib import Path
import json


class SettingsNamesEnum:
    SERVER_ENDPOINT_ADDRESS = "server_endpoint"
    USER_TOKEN = "user_token"


# TODO: NE RABOTAET, PEREPISAT POD CSV FILE
class SettingsManager:
    def __init__(self, file_path: str, default_settings) -> None:
        if not Path(file_path).is_file():
            open(file_path, "w").write(json.dumps(default_settings))

        self.file_path = file_path
        self.settings_parsed = json.loads(open(file_path, "r").read())

    def get_setting(self, setting_name, default_value):
        try:
            return self.settings_parsed[setting_name]
        except:
            return default_value

    def set_setting(self, setting_name, new_value):
        self.settings_parsed[setting_name] = new_value

    def save(self):
        open(self.file_path, "w").write(json.dumps(self.settings_parsed))
