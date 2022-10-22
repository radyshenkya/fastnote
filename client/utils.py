from jinja2 import Template
from markdown import markdown

_FILE_RENDER_TEMPLATE = Template(open("./templates/file_render.html").read())


def get_rendered_markdown(md: str) -> str:
    content = markdown(md, extensions=["tables"])
    return _FILE_RENDER_TEMPLATE.render(content=content)
