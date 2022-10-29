from plugins.BasePlugin import BasePlugin
from PyQt5.QtWidgets import QPlainTextEdit, QFileDialog
from PyQt5.QtGui import QTextCursor
from utils import table_to_markdown
from pathlib import Path

import csv


class Plugin(BasePlugin):
    NAME = "Вставить CSV таблицу из файла"
    SHORTCUT = None
    AUTHOR = "Rodion Sarygin"

    @classmethod
    def on_init(cls, parent=None):
        pass

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit, parent=None):
        csv_file_path = QFileDialog.getOpenFileName(
            parent, "Выбрать CSV файл", "", "CSV Таблица (*.csv);; Все файлы (*)"
        )[0]

        if not Path(csv_file_path).is_file():
            return
        text_to_insert = ""
        with open(csv_file_path, encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            text_to_insert = table_to_markdown(list(reader))

        cursor = text_edit.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.insertText(text_to_insert)
        cursor.endEditBlock()
