import os

from jinja2 import Template
from markdown import markdown

from PyQt5.QtWidgets import QMessageBox

from hashlib import md5

_FILE_RENDER_TEMPLATE = Template(
    open(
        os.path.dirname(os.path.realpath(__file__)) + "/templates/file_render.html"
    ).read()
)


def get_rendered_markdown(md: str) -> str:
    content = markdown(md, extensions=["tables"])
    return _FILE_RENDER_TEMPLATE.render(content=content)


def alert_message_box(title: str, message: str):
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    return msg_box.exec()
