#!/bin/python3

from functools import partial
from importlib import util
from os import path
import sys
from widgets.SettingsDialog import SettingsDialog

from ui import main_ui
from utils import (
    alert_message_box,
    debug,
    get_rendered_markdown,
    generate_user_token,
    list_files_in_dir,
    try_function,
)

from notes.LocalNote import LocalNote
from notes.RemoteNote import RemoteNote

from config import DEFAULT_SERVER, SETTINGS_FILE_PATH, PLUGINS_DIR_PATH

from settings_manager import SettingsManager, SettingsNamesEnum

from text_edit_tools.Tools import *

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QFileDialog,
    QInputDialog,
    QAction,
    QMenu,
)

TOOLS = [AddImageTool, TableTool, BoldTool, ItalicTool, HeaderTool]
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
        self.init_toolbar()
        self.init_plugins()

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
        # new
        new_action = QAction("Новый документ", self)
        new_action.setShortcut("Ctrl+n")
        new_action.triggered.connect(self.new_file)
        # save
        save_action = QAction("Сохранить", self)
        save_action.setShortcut("Ctrl+s")
        save_action.triggered.connect(self.save_file)
        # save as
        save_as_action = QAction("Сохранить как", self)
        save_as_action.setShortcut("Ctrl+Shift+s")
        save_as_action.triggered.connect(self.save_file_as)
        # open
        open_action = QAction("Открыть", self)
        open_action.setShortcut("Ctrl+o")
        open_action.triggered.connect(self.open_file)
        # open remote
        open_remote_action = QAction("Открыть с сервера", self)
        open_remote_action.setShortcut("Ctrl+Shift+o")
        open_remote_action.triggered.connect(self.open_remote)
        # get notes from server
        server_notes_list_action = QAction("Список записей с сервера", self)
        server_notes_list_action.setShortcut("Ctrl+l")
        server_notes_list_action.triggered.connect(self.get_user_notes)
        # save to server
        save_to_server_action = QAction("Загрузить на сервер", self)
        save_to_server_action.setShortcut("Ctrl+u")
        save_to_server_action.triggered.connect(self.upload_to_server)
        # settings
        open_settings_action = QAction("Настройки", self)
        open_settings_action.triggered.connect(self.open_settings_dialog)

        # MENU BAR
        file_menu = QMenu("&Файл", self)
        file_menu.addActions(
            [
                new_action,
                save_action,
                save_as_action,
                save_to_server_action,
                server_notes_list_action,
                open_action,
                open_remote_action,
                open_settings_action,
            ]
        )
        self.menu_bar.addMenu(file_menu)

    def init_toolbar(self):
        for tool in TOOLS:
            new_action = QAction(tool.NAME, self)
            if not tool.SHORTCUT is None:
                new_action.setShortcut(tool.SHORTCUT)
            new_action.triggered.connect(partial(tool.on_call, self.edit_panel, self))
            self.toolBar.addAction(new_action)

    def init_plugins(self):
        # Listing all plugins in plugins/installed as modules
        plugin_files = list_files_in_dir(PLUGINS_DIR_PATH)
        plugins = []

        for file in plugin_files:
            try:
                module_path = path.join(PLUGINS_DIR_PATH, file)
                module_name = file.split(".")[0]

                spec = util.spec_from_file_location(module_name, module_path)
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)
                plugins.append(module.Plugin)
            except Exception as e:
                debug("Failed to load plugin", file)
                debug(e)

        # Creating plugin list
        plugin_menu = QMenu("&Плагины", self)

        for plugin in plugins:
            plugin.on_init(self)
            plugin_action = QAction(plugin.NAME, self)
            if not plugin.SHORTCUT is None:
                plugin_action.setShortcut(plugin.SHORTCUT)
            plugin_action.triggered.connect(
                partial(plugin.on_call, self.edit_panel, self)
            )
            plugin_menu.addAction(plugin_action)
        self.menu_bar.addMenu(plugin_menu)

    def open_settings_dialog(self):
        def update_settings(changed_settings):
            self.settings_manager.settings_parsed = changed_settings
            self.settings_manager.save()

        dial = SettingsDialog(
            self.settings_manager.settings_parsed, update_settings, self
        )
        dial.show()

    def new_file(self):
        self.note = None
        self.edit_panel.setPlainText("# Hello World")
        self.update_current_path_label()
        self.update_render_panel()

    @try_function(fail_message="Проблемы с сервером")
    def get_user_notes(self, *args):
        server_enpoint = self.settings_manager.get_setting(
            SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS,
            DEFAULT_SETTINGS[SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS],
        )

        user_token = self.settings_manager.get_setting(
            SettingsNamesEnum.USER_TOKEN,
            DEFAULT_SETTINGS[SettingsNamesEnum.USER_TOKEN],
        )

        notes = RemoteNote.fetch_notes_from_server(server_enpoint, user_token)

        note_id, ok_pressed = QInputDialog.getItem(
            self, "Выберите запись для открытия", "Запись:", notes, 1, False
        )

        if ok_pressed:
            self.note = RemoteNote.load_note_from_server(
                server_enpoint, user_token, note_id
            )
            self.update_ui()

    @try_function(fail_message="Файл не удалось открыть")
    def open_file(self, *args):
        # Opening file
        file_name = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Markdown Format (*.md);;All Files (*)"
        )[0]
        self.note = LocalNote.get_or_create_file(file_name)

        # Updating editor
        self.update_ui()

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

            self.update_ui()

    @try_function(fail_message="Проблемы с сервером")
    def upload_to_server(self, *args):
        server_enpoint = self.settings_manager.get_setting(
            SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS,
            DEFAULT_SETTINGS[SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS],
        )

        user_token = self.settings_manager.get_setting(
            SettingsNamesEnum.USER_TOKEN,
            DEFAULT_SETTINGS[SettingsNamesEnum.USER_TOKEN],
        )
        self.note = RemoteNote.new_note(server_enpoint, user_token)
        self.note.set_text(self.edit_panel.toPlainText())
        self.note.save()
        self.update_ui()

    def update_render_panel(self):
        md_str = self.edit_panel.toPlainText()
        rendered_text = get_rendered_markdown(md_str)
        self.render_panel.setHtml(rendered_text)

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

    def update_ui(self):
        self.update_current_path_label()
        self.update_edit_panel_from_note()
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
