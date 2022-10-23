import os

from jinja2 import Template
from markdown import markdown

from hashlib import md5

_FILE_RENDER_TEMPLATE = Template(
    open(
        os.path.dirname(os.path.realpath(__file__)) + "/templates/file_render.html"
    ).read()
)


def get_rendered_markdown(md: str) -> str:
    content = markdown(md, extensions=["tables"])
    return _FILE_RENDER_TEMPLATE.render(content=content)


def hash_value(val: str) -> str:
    return md5(md5(val.encode("utf-8")).hexdigest().encode("utf-8")).hexdigest()
