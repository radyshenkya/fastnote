from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QTextCursor

# FOR HELP IN ADDING TOOLS: https://doc.qt.io/qt-5/richtext-cursor.html#cursor-based-editing
class BaseTool:
    NAME = "BaseTool"
    SHORTCUT = None

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit):
        raise NotImplementedError()
        # cursor = text_edit.textCursor()
        # cursor.beginEditBlock()
        # cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        # cursor.insertText("[BASETOOL]")
        # cursor.endEditBlock()
