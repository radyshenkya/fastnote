import sys

from ui import main_ui
from utils import get_rendered_markdown

from notes.LocalNote import LocalNote, is_file_exists

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)
        self.init_ui()
        self.init_logic()

    def init_ui(self):
        self.update_render_panel()

    def init_logic(self):
        self.note = None

        # EVENTS CONNECTION
        self.save_as_btn.clicked.connect(self.save_file_as)
        self.save_btn.clicked.connect(self.save_file)
        self.open_btn.clicked.connect(self.open_file)
        self.edit_panel.textChanged.connect(self.update_render_panel)

    def update_render_panel(self):
        md_str = self.edit_panel.toPlainText()
        rendered_text = get_rendered_markdown(md_str)
        self.render_panel.setHtml(rendered_text)

    def open_file(self):
        # Opening file
        file_name = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Markdown Format (*.md);;All Files (*)"
        )[0]
        self.note = LocalNote.get_or_create_file(file_name)

        # Updating editor
        self.edit_panel.setPlainText(self.note.text)
        self.update_render_panel()

        self.update_current_path_label()

    def save_file_as(self):
        file_name = QFileDialog.getSaveFileName(
            self, "Сохранить как", "", "Markdown Format (*.md);;All Files (*)"
        )[0]

        self.note = LocalNote.get_or_create_file(file_name)
        self.save_file()

    def save_file(self):
        if self.note is None:
            self.save_file_as()

        self.note.set_text(self.edit_panel.toPlainText())
        self.note.save()

        self.update_current_path_label()

        # Changing status bar
        self.statusBar.showMessage(str(self.note) + " saved!", 2000)

    def update_current_path_label(self):
        self.current_file_label.setText(
            str(self.note) if not self.note is None else "unsaved file",
        )


def main():
    app = QApplication(sys.argv)
    # app.setStyle("Windows")
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
