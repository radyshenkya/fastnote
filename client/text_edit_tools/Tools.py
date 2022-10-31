from utils import table_to_markdown
from text_edit_tools.BaseTool import BaseTool
from PyQt5.QtWidgets import QPlainTextEdit, QInputDialog
from PyQt5.QtGui import QTextCursor

from widgets.TableDialog import TableDialog

# Add image template at cursor position


class AddImageTool(BaseTool):
    NAME = "Добавить картинку (Ctrl+Shift+i)"
    SHORTCUT = "Ctrl+Shift+i"

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit, parent=None):
        image_link, ok_pressed = QInputDialog.getText(
            parent, "Insert Image", "Image link:"
        )

        if ok_pressed:
            cursor = text_edit.textCursor()
            cursor.beginEditBlock()
            cursor.insertText(f"![]({image_link})")
            cursor.endEditBlock()


# SelectedTextStyleTool (Abstract tool)
class SelectedTextStyleTool(BaseTool):
    APPEND_SYMBOLS = ""

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit, parent=None):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        if len(cursor.selection().toPlainText()) == 0:
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)

        selection = cursor.selection().toPlainText()
        new_text = selection

        # if selection starts and stops with desired symbold, remove this symbols
        if (
            selection[: len(cls.APPEND_SYMBOLS)] == cls.APPEND_SYMBOLS
            and selection[-(len(cls.APPEND_SYMBOLS)):] == cls.APPEND_SYMBOLS
        ):
            new_text = selection[len(cls.APPEND_SYMBOLS)
                                     : -(len(cls.APPEND_SYMBOLS))]
        else:  # else append this symbold
            new_text = f"{cls.APPEND_SYMBOLS}{cursor.selection().toPlainText()}{cls.APPEND_SYMBOLS}"

        cursor.removeSelectedText()
        cursor.insertText(new_text)

        cursor.endEditBlock()


class BoldTool(SelectedTextStyleTool):
    NAME = "Жирный шрифт (Ctrl+b)"
    SHORTCUT = "Ctrl+b"
    APPEND_SYMBOLS = "**"


class ItalicTool(SelectedTextStyleTool):
    NAME = "Курсив (Ctrl+i)"
    SHORTCUT = "Ctrl+i"
    APPEND_SYMBOLS = "*"


class HeaderTool(BaseTool):
    NAME = "Заголовок (Ctrl+h)"
    SHORTCUT = "Ctrl+h"

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit, parent=None):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.select(cursor.SelectionType.LineUnderCursor)

        if not cursor.selection().toPlainText().startswith("######"):
            cursor.insertText("#" + cursor.selection().toPlainText())

        cursor.endEditBlock()


class DeleteHeaderTool(BaseTool):
    NAME = "Убрать заголовок (Ctrl+Shift+h)"
    SHORTCUT = "Ctrl+Shift+h"

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit, parent=None):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.select(cursor.SelectionType.LineUnderCursor)

        if cursor.selection().toPlainText().startswith('#'):
            cursor.insertText(cursor.selection().toPlainText()[1:])

        cursor.endEditBlock()


class TableTool(BaseTool):
    NAME = "Новая таблица (Ctrl+t)"
    SHORTCUT = "Ctrl+t"

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit, parent=None):
        def on_table_accept(table):
            one_row = ""
            cursor = text_edit.textCursor()
            cursor.beginEditBlock()

            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)

            text_to_insert = table_to_markdown(table)

            cursor.insertText(text_to_insert)

            cursor.endEditBlock()

        table_dialog = TableDialog(on_table_accept, parent)
        table_dialog.show()
