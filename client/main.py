import sys

from ui import main_ui
from utils import get_rendered_markdown
from PyQt6.QtWebEngineWidgets import QWebEngineView

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QUrl


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)
        self.init_ui()
        self.init_logic()

    def init_ui(self):
        # INITIALIZING WEB ENGINE WIDGET
        self.render_panel = QWebEngineView(self)
        self.render_panel.setHtml("<h1>ASDASD</h1>")
        self.render_panel.setMinimumSize(400, 400)
        self.main_layout.addWidget(self.render_panel, stretch=1)

    def init_logic(self):
        self.edit_panel.textChanged.connect(self.update_render_panel)

    def update_render_panel(self):
        md_str = self.edit_panel.toPlainText()
        rendered_text = get_rendered_markdown(md_str)
        self.render_panel.setHtml(rendered_text)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
