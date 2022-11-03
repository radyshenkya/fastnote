from importlib import util
import os
from random import choices
from types import ModuleType
from typing import Any, List, Tuple

from jinja2 import Template
from PyQt5.QtWidgets import QMessageBox
from hashlib import md5

from markdown import markdown

_FILE_RENDER_TEMPLATE = Template(
    open(
        os.path.dirname(os.path.realpath(__file__)) +
        "/templates/file_render.html"
    ).read()
)


def get_rendered_markdown(md: str) -> str:
    content = markdown(md, extensions=["tables"])
    return _FILE_RENDER_TEMPLATE.render(content=content)


def load_module_from_file(module_name: str, file_path: str) -> ModuleType:
    spec = util.spec_from_file_location(module_name, file_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def list_files_in_dir(path: str) -> List[str]:
    return list(
        filter(lambda item: os.path.isfile(
            os.path.join(path, item)), os.listdir(path))
    )


def list_dirs_in_dir(path: str) -> List[str]:
    return list(
        filter(lambda item: os.path.isdir(
            os.path.join(path, item)), os.listdir(path))
    )


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


def table_to_markdown(table: List[List[str]]):
    text = "|".join(map(str, table[0])) + "\n" + \
        "|".join(["---" for el in table[0]]) + "\n"
    for row in table[1:]:
        text += "|".join(map(str, row)) + "\n"

    return text


def compare_lists(original_list: list, new_list: list) -> Tuple[List[Tuple[int, Any]], list, int]:
    """Comparing lists by elements

    Returning tuple.
    First element in tuple - list[(index, to_replace)] - list with elements to replace, where index - index of element to replace, to_replace - new value
    Second el - List[to_append] - elements needed to append
    Third - index - from which index need to delete"""

    # Checking replaces
    to_replace = []
    for i in range(min(len(original_list), len(new_list))):
        if original_list[i] != new_list[i]:
            to_replace.append((i, new_list[i]))

    to_delete = -1
    to_append = []

    if len(original_list) > len(new_list):
        to_delete = len(new_list)
    elif len(original_list) < len(new_list):
        to_append = [el for el in new_list[len(original_list):]]

    return (to_replace, to_append, to_delete)
