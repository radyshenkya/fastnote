from PyQt5.QtWidgets import QDialog

from ui.settings_dialog_ui import Ui_Dialog

from PyQt5.QtWidgets import QLineEdit


class SettingsDialog(QDialog, Ui_Dialog):
    def __init__(self, start_settings, on_ok_function, parent=None) -> None:
        super().__init__(parent)

        self.setupUi(self)

        self.changed_settings = {}

        for k, v in start_settings.items():
            self.changed_settings[k] = self.add_setting_input_field(k, v)

    def add_setting_input_field(self, key, value):
        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText(key)
        line_edit.setText(str(value))
        self.settings_layout.addWidget(line_edit)
        return line_edit
