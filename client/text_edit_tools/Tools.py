from sqlite3 import Cursor
from text_edit_tools.BaseTool import BaseTool
from PyQt5.QtWidgets import QPlainTextEdit, QInputDialog
from PyQt5.QtGui import QTextCursor

# Add image template at cursor position
class AddImageTool(BaseTool):
    NAME = "Add Image (Ctrl+Shift+i)"
    SHORTCUT = "Ctrl+Shift+i"

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit):
        image_link, ok_pressed = QInputDialog.getText(
            None, "Insert Image", "Image link:"
        )

        if ok_pressed:
            cursor = text_edit.textCursor()
            cursor.beginEditBlock()
            cursor.insertText(f"![]({image_link})")
            cursor.endEditBlock()


class BoldTool(BaseTool):
    NAME = "Bold Text (Ctrl+b)"
    SHORTCUT = "Ctrl+b"

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()
        new_text = f"**{cursor.selection().toPlainText()}**"

        cursor.removeSelectedText()
        cursor.insertText(new_text)

        cursor.endEditBlock()


class ItalicTool(BaseTool):
    NAME = "Italic Text (Ctrl+i)"
    SHORTCUT = "Ctrl+i"

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        if len(cursor.selection().toPlainText()) == 0:
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        new_text = f"*{cursor.selection().toPlainText()}*"

        cursor.removeSelectedText()
        cursor.insertText(new_text)

        cursor.endEditBlock()


class HeaderTool(BaseTool):
    NAME = "Header (Ctrl+h)"
    SHORTCUT = "Ctrl+h"

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit):
        cursor = text_edit.textCursor()
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.insertText("#")

        cursor.endEditBlock()
