from PyQt5.QtCore import QThread, pyqtSignal

from utils import get_rendered_markdown


class MarkdownTranslatorThread(QThread):
    finish_signal = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.markdown_text = None

    def run(self):
        self.finish_signal.emit(get_rendered_markdown(self.markdown_text))
