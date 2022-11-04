"""
Utils for markdown content
"""

from jinja2 import Template
from typing import List
from markdown import markdown
from config import ROOT_DIR_PATH

_FILE_RENDER_TEMPLATE = Template(
    open(
        ROOT_DIR_PATH +
        "/templates/file_render.html"
    ).read()
)


def get_rendered_markdown(md: str) -> str:
    content = markdown(md, extensions=["tables"])
    return _FILE_RENDER_TEMPLATE.render(content=content)


def table_to_markdown(table: List[List[str]]):
    text = "|".join(map(str, table[0])) + "\n" + \
        "|".join(["---" for el in table[0]]) + "\n"
    for row in table[1:]:
        text += "|".join(map(str, row)) + "\n"

    return text
