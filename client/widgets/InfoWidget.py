"""
Widget with title and markdown text as body
"""

from PyQt5.QtWidgets import QWidget
from ui.plugin_details_item import Ui_Form


class InfoWidget(QWidget, Ui_Form):

    def __init__(self, parent=None, info_title="", info_text="") -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.plugin_name.setText(info_title)
        self.plugin_description.setMarkdown(info_text)
