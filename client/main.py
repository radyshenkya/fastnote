#!/bin/python3

import sys

from ui import main_ui
from utils import (
    alert_message_box,
    get_rendered_markdown,
    generate_user_token,
    try_function,
)

from notes.LocalNote import LocalNote
from notes.RemoteNote import RemoteNote

from settings_manager import SettingsManager, SettingsNamesEnum

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QFileDialog,
    QInputDialog,
    QShortcut,
    QAction,
    QMenu,
)


SETTINGS_FILE_PATH = "settings.json"
DEFAULT_SERVER = "https://cef5-46-181-148-140.eu.ngrok.io"
DEFAULT_SETTINGS = {
    SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS: DEFAULT_SERVER,
    SettingsNamesEnum.USER_TOKEN: generate_user_token(),
}


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)
        self.init_ui()
        self.init_logic()

    def init_ui(self):
        self.update_render_panel()

    def init_logic(self):
        # Initing settings file
        self.settings_manager = SettingsManager(SETTINGS_FILE_PATH, DEFAULT_SETTINGS)

        self.note = None
        self.update_current_path_label()

        # EVENTS CONNECTION
        self.edit_panel.textChanged.connect(self.update_render_panel)

        # ACTIONS
        # save
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+s")
        save_action.triggered.connect(self.save_file)
        # save as
        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut("Ctrl+Shift+s")
        save_as_action.triggered.connect(self.save_file_as)
        # open
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+o")
        open_action.triggered.connect(self.open_file)
        # open remote
        open_remote_action = QAction("Open Remote", self)
        open_remote_action.setShortcut("Ctrl+Shift+o")
        open_remote_action.triggered.connect(self.open_remote)

        # MENU BAR
        file_menu = QMenu("&File", self)
        file_menu.addActions(
            [save_action, save_as_action, open_action, open_remote_action]
        )
        self.menu_bar.addMenu(file_menu)

    def update_render_panel(self):
        md_str = self.edit_panel.toPlainText()
        rendered_text = get_rendered_markdown(md_str)
        self.render_panel.setHtml(rendered_text)

    @try_function(fail_message="Файл не удалось открыть")
    def open_file(self, *args):
        # Opening file
        file_name = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Markdown Format (*.md);;All Files (*)"
        )[0]
        self.note = LocalNote.get_or_create_file(file_name)

        # Updating editor
        self.update_edit_panel_from_note()
        self.update_current_path_label()

    def save_file_as(self, *args):
        file_name = QFileDialog.getSaveFileName(
            self, "Сохранить как", "", "Markdown Format (*.md);;All Files (*)"
        )[0]

        try:
            self.note = LocalNote.get_or_create_file(file_name)
            self.save_file()
        except FileNotFoundError as e:
            self.note = None
            alert_message_box("Ошибка!", "Файл не удалось сохранить.")

    @try_function(fail_message="Ошибка при сохранении файла!")
    def save_file(self, *args):
        if self.note is None:
            self.save_file_as()
            return

        if self.note.readonly:
            alert_message_box(
                "Ошибка!",
                "Данная запись предназначена только для чтения. Если вы хотите ее редактировать, нажмите на кнопку SAVE AS.",
            )
            return
        self.note.set_text(self.edit_panel.toPlainText())
        self.note.save()

        self.update_current_path_label()

        # Changing status bar
        self.statusBar.showMessage(str(self.note) + " saved!", 2000)

    @try_function(fail_message="Либо данной записи нет, либо сервер не отвечает.")
    def open_remote(self, *args):
        id, ok_pressed = QInputDialog.getText(self, "Введите ID записи.", "ID:")

        if ok_pressed:
            server_enpoint = self.settings_manager.get_setting(
                SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS,
                DEFAULT_SETTINGS[SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS],
            )

            user_token = self.settings_manager.get_setting(
                SettingsNamesEnum.USER_TOKEN,
                DEFAULT_SETTINGS[SettingsNamesEnum.USER_TOKEN],
            )
            self.note = RemoteNote.load_note_from_server(server_enpoint, user_token, id)

            self.update_current_path_label()
            self.update_edit_panel_from_note()

    def update_current_path_label(self):
        self.current_file_label.setText(
            str(self.note) if not self.note is None else "unsaved file",
        )

    def update_edit_panel_from_note(self):
        self.edit_panel.setVisible(
            not self.note.readonly if not self.note is None else True
        )
        self.edit_panel.setPlainText(self.note.text)
        self.update_render_panel()

    def closeEvent(self, event) -> None:
        self.settings_manager.save()
        return super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
