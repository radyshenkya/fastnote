from plugins.BasePlugin import BasePlugin
from PyQt5.QtWidgets import QPlainTextEdit, QFileDialog, QInputDialog
from PyQt5.QtGui import QTextCursor
from utils import table_to_markdown, debug
from pathlib import Path

import sqlite3


class Plugin(BasePlugin):
    NAME = "Вставить таблицу из SQLite файла"
    DESCRIPTION = "Вставляет выбранную таблицу из SQLite файла базы данных в текущий документ."
    AUTHOR = "Rodion Sarygin"
    SHORTCUT = None

    @classmethod
    def on_init(self, parent=None):
        pass

    @classmethod
    def on_call(self, text_edit: QPlainTextEdit, parent=None):
        sqlite_file_path = QFileDialog.getOpenFileName(
            parent, "Выбрать SQLite файл", "", "SQLite База данных (*.sqlite *.sqlite3 *.db *.db3 *.s3db *.sl3);; Все файлы (*)"
        )[0]

        if not Path(sqlite_file_path).is_file():
            return

        cursor = sqlite3.connect(sqlite_file_path).cursor()

        try:
            cursor.execute(
                "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        except Exception as e:
            debug("Can not import tables")
            debug("Exception:", e)
            return

        table_names = [el[0] for el in cursor.fetchall()]

        table, is_ok = QInputDialog.getItem(
            parent, "Выберите Таблицу для вставки", "Имя таблицы для вставки:", table_names, 0, False)

        if not is_ok:
            return

        cursor.execute("SELECT * FROM " + table)
        table_list = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        table_list.insert(0, column_names)
        text_to_insert = table_to_markdown(table_list)

        cursor = text_edit.cursor()
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.insertText(text_to_insert)
        cursor.endEditBlock()
