import os
from random import choices

from jinja2 import Template
from PyQt5.QtWidgets import QMessageBox
from hashlib import md5

from markdown import markdown

from config import DEBUG_MESSAGES

_FILE_RENDER_TEMPLATE = Template(
    open(
        os.path.dirname(os.path.realpath(__file__)) + "/templates/file_render.html"
    ).read()
)


def get_rendered_markdown(md: str) -> str:
    content = markdown(md, extensions=["tables"])
    return _FILE_RENDER_TEMPLATE.render(content=content)


def debug(*args, **kwargs):
    if DEBUG_MESSAGES:
        print("[DEBUG]", *args, **kwargs)


def alert_message_box(title: str, message: str):
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    return msg_box.exec()


def generate_user_token() -> str:
    USER_TOKEN_ITERATIONS = 32
    GENERATION_ALPHABET = "abcdefghijklmnopqrst1234567890"
    return md5(
        ("".join(choices(GENERATION_ALPHABET, k=USER_TOKEN_ITERATIONS))).encode("utf-8")
    ).hexdigest()


def try_function(fail_message="Error"):
    def wrapper_with_args(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except IOError as e:
                alert_message_box("Ошибка!", fail_message)

        return wrapper

    return wrapper_with_args
