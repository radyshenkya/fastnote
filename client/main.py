import sys

from ui import main_ui
from utils import get_rendered_markdown

from notes.LocalNote import LocalNote

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)
        self.init_ui()
        self.init_logic()

    def init_ui(self):
        self.update_render_panel()

    def init_logic(self):
        self.edit_panel.textChanged.connect(self.update_render_panel)

    def update_render_panel(self):
        md_str = self.edit_panel.toPlainText()
        rendered_text = get_rendered_markdown(md_str)
        self.render_panel.setHtml(rendered_text)

    # def open_file(self)


def main():
    app = QApplication(sys.argv)
    # app.setStyle("Windows")
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
