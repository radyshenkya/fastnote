"""
Base class for tools on "EditTools" row in editor.
It is very similar to BasePlugin, instead this class do not have on_init() method and AUTHOR field.
"""

from PyQt5.QtWidgets import QPlainTextEdit


class BaseTool:
    NAME = "BaseTool"
    SHORTCUT = None

    @classmethod
    def on_call(cls, text_edit: QPlainTextEdit, parent=None):
        raise NotImplementedError()
