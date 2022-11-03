#!/bin/python3

from functools import partial
import sys
from managers.recent_files import RecentFilesManager
from widgets.InfoWidget import InfoWidget
from managers.plugins import PluginManager
from widgets.SettingsDialog import SettingsDialog

from ui import main_ui
from util.server import generate_user_token
from util.decorators import try_function

from notes.LocalNote import LocalNote
from notes.RemoteNote import RemoteNote

from config import DEFAULT_SERVER, SETTINGS_FILE_PATH, PLUGINS_DIR_PATH, MAX_RECENT_FILES_IN_DB, RECENT_FILES_DB_PATH, LANG_MANAGER

from managers.settings import SettingsManager, SettingsNamesEnum

from text_edit_tools.Tools import *

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QFileDialog,
    QInputDialog,
    QVBoxLayout,
    QDialog,
    QAction,
    QMenu,
)

TOOLS = [AddImageTool, TableTool, BoldTool,
         ItalicTool, HeaderTool, DeleteHeaderTool]
DEFAULT_SETTINGS = {
    SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS: DEFAULT_SERVER,
    SettingsNamesEnum.USER_TOKEN: generate_user_token(),
}


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)
        self.init_logic()
        self.init_toolbar()
        self.init_plugins()
        self.init_recent_files()
        self.init_ui()

    def init_ui(self):
        self.update_render_panel()

    def init_logic(self):
        # Initing settings file
        self.settings_manager = SettingsManager(
            SETTINGS_FILE_PATH, DEFAULT_SETTINGS)

        self.note = None
        self.update_current_path_label()

        # EVENTS CONNECTION
        self.edit_panel.textChanged.connect(self.update_render_panel)

        # ACTIONS
        # new
        new_action = QAction(LANG_MANAGER.get(LANG_MANAGER.NEW_DOC), self)
        new_action.setShortcut("Ctrl+n")
        new_action.triggered.connect(self.new_file)
        # save
        save_action = QAction(LANG_MANAGER.get(LANG_MANAGER.SAVE_DOC), self)
        save_action.setShortcut("Ctrl+s")
        save_action.triggered.connect(self.save_file)
        # save as
        save_as_action = QAction(LANG_MANAGER.get(
            LANG_MANAGER.SAVE_AS_DOC), self)
        save_as_action.setShortcut("Ctrl+Shift+s")
        save_as_action.triggered.connect(self.save_file_as)
        # open
        open_action = QAction(LANG_MANAGER.get(LANG_MANAGER.OPEN_DOC), self)
        open_action.setShortcut("Ctrl+o")
        open_action.triggered.connect(self.open_file)
        # open remote
        open_remote_action = QAction(LANG_MANAGER.get(
            LANG_MANAGER.OPEN_REMOTE_DOC), self)
        open_remote_action.setShortcut("Ctrl+Shift+o")
        open_remote_action.triggered.connect(self.open_remote)
        # get notes from server
        server_notes_list_action = QAction(
            LANG_MANAGER.get(LANG_MANAGER.LIST_REMOTE_DOC), self)
        server_notes_list_action.setShortcut("Ctrl+l")
        server_notes_list_action.triggered.connect(self.get_user_notes)
        # save to server
        save_to_server_action = QAction(
            LANG_MANAGER.get(LANG_MANAGER.UPLOAD_DOC), self)
        save_to_server_action.setShortcut("Ctrl+u")
        save_to_server_action.triggered.connect(self.upload_to_server)
        # settings
        open_settings_action = QAction(
            LANG_MANAGER.get(LANG_MANAGER.OPEN_SETTINGS), self)
        open_settings_action.triggered.connect(self.open_settings_dialog)

        # MENU BAR
        self.file_menu = QMenu(LANG_MANAGER.get(LANG_MANAGER.FILE_MENU), self)
        # New document
        self.file_menu.addAction(new_action)
        self.file_menu.addSeparator()
        # Local files
        self.file_menu.addActions([
            open_action,
            save_action,
            save_as_action
        ])
        self.file_menu.addSeparator()
        # Remote notes
        self.file_menu.addActions([
            open_remote_action,
            server_notes_list_action,
            save_to_server_action
        ])
        self.file_menu.addSeparator()
        # Settings
        self.file_menu.addAction(open_settings_action)

        self.menu_bar.addMenu(self.file_menu)

    def init_toolbar(self):
        for tool in TOOLS:
            new_action = QAction(tool.NAME, self)
            if not tool.SHORTCUT is None:
                new_action.setShortcut(tool.SHORTCUT)
            new_action.triggered.connect(
                partial(tool.on_call, self.edit_panel, self))
            self.toolBar.addAction(new_action)

    def init_recent_files(self):
        # Initing recent files manager
        self.recent_files_manager = RecentFilesManager(
            RECENT_FILES_DB_PATH, MAX_RECENT_FILES_IN_DB)

        self.file_menu.addSeparator()
        self.recent_files_actions = []

        self.update_recent_files()

    def update_recent_files(self):
        # Removing all actions
        for i in range(len(self.recent_files_actions)):
            self.recent_files_actions[i].setParent(None)

        self.recent_files_actions = []

        # Adding new ones
        for i, file_path in self.recent_files_manager.get_files():
            def load_note_from_path(note_path: str):
                self.note = LocalNote.get_or_create_file(note_path)
                self.update_ui()
                self.recent_files_manager.push(str(self.note))
                self.update_recent_files()

            open_file_action = QAction(file_path, self)
            open_file_action.triggered.connect(
                partial(load_note_from_path, file_path))
            self.recent_files_actions.append(open_file_action)
            self.file_menu.addAction(open_file_action)

    def init_plugins(self):
        # Loading plugin manager
        self.plugin_manager = PluginManager.load_from_folder(PLUGINS_DIR_PATH)
        self.plugin_manager.init_plugins(self)

        # Creating plugin list
        plugin_menu = QMenu(LANG_MANAGER.get(LANG_MANAGER.PLUGINS_MENU), self)

        for plugin in self.plugin_manager.plugins:
            plugin_action = QAction(plugin.NAME, self)
            if not plugin.SHORTCUT is None:
                plugin_action.setShortcut(plugin.SHORTCUT)
            plugin_action.triggered.connect(
                partial(plugin.on_call, self.edit_panel, self)
            )
            plugin_menu.addAction(plugin_action)
        plugin_menu.addSeparator()
        plugin_details = QAction(LANG_MANAGER.get(
            LANG_MANAGER.PLUGINS_DETAILS), self)
        plugin_details.triggered.connect(self.show_plugins_details)
        plugin_menu.addAction(plugin_details)
        self.menu_bar.addMenu(plugin_menu)

    def show_plugins_details(self):
        details_dialog = QDialog(self)
        details_dialog.setWindowTitle(
            LANG_MANAGER.get(LANG_MANAGER.PLUGINS_DETAILS))

        vertical_layout = QVBoxLayout(details_dialog)

        for plugin in self.plugin_manager.plugins:
            vertical_layout.addWidget(InfoWidget(
                self, f"{plugin.NAME} ({LANG_MANAGER.get(LANG_MANAGER.PLUGIN_AUTHOR_PREFIX)} - {plugin.AUTHOR})", plugin.DESCRIPTION))

        details_dialog.setLayout(vertical_layout)
        details_dialog.show()

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
        self.edit_panel.setPlainText("")
        self.update_current_path_label()
        self.update_render_panel()

    @try_function(fail_message=LANG_MANAGER.get(LANG_MANAGER.ERR_SERVER_PROBLEMS))
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

    @try_function(fail_message=LANG_MANAGER.get(LANG_MANAGER.ERR_OPEN_NOTE))
    def open_file(self, *args):
        # Opening file
        file_name = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Markdown Format (*.md);;All Files (*)"
        )[0]
        self.note = LocalNote.get_or_create_file(file_name)

        # Updating editor
        self.update_ui()

        # Recent file update
        self.recent_files_manager.push(str(self.note))
        self.update_recent_files()

    @try_function(fail_message=LANG_MANAGER.get(LANG_MANAGER.ERR_SAVE_NOTE))
    def save_file_as(self, *args):
        file_name = QFileDialog.getSaveFileName(
            self, LANG_MANAGER.get(
                LANG_MANAGER.SAVE_AS_DOC), "", "Markdown Format (*.md);;All Files (*)"
        )[0]

        self.note = LocalNote.get_or_create_file(file_name)
        self.save_file()

    @try_function(fail_message=LANG_MANAGER.get(LANG_MANAGER.ERR_SAVE_NOTE))
    def save_file(self, *args):
        if self.note is None:
            self.save_file_as()
            return

        assert not self.note.readonly
        self.note.set_text(self.edit_panel.toPlainText())
        self.note.save()

        self.update_current_path_label()

        # Changing status bar
        self.statusBar.showMessage(str(self.note) + " saved!", 2000)

        if type(self.note) == LocalNote:
            self.recent_files_manager.push(str(self.note))
            self.update_recent_files()

    @try_function(fail_message=LANG_MANAGER.get(LANG_MANAGER.ERR_NOTE_NOT_FOUND))
    def open_remote(self, *args):
        id, ok_pressed = QInputDialog.getText(
            self, LANG_MANAGER.get(LANG_MANAGER.OPEN_REMOTE_DOC), "ID:")

        if ok_pressed:
            server_enpoint = self.settings_manager.get_setting(
                SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS,
                DEFAULT_SETTINGS[SettingsNamesEnum.SERVER_ENDPOINT_ADDRESS],
            )

            user_token = self.settings_manager.get_setting(
                SettingsNamesEnum.USER_TOKEN,
                DEFAULT_SETTINGS[SettingsNamesEnum.USER_TOKEN],
            )
            self.note = RemoteNote.load_note_from_server(
                server_enpoint, user_token, id)

            self.update_ui()

    @try_function(fail_message=LANG_MANAGER.get(LANG_MANAGER.ERR_SERVER_PROBLEMS))
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
        self.render_panel.setTextInMarkdown(md_str)

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
    app.setStyle('Fusion')
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
