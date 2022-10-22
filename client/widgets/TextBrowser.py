from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import QUrl, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QMovie, QPixmap

import requests


class TextBrowser(QTextBrowser):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.cached_links = {}

    def loadResource(self, type, name):
        url = name
        if not url.scheme():
            url = QUrl.fromLocalFile(url.url())

        try:
            if not url.url() in self.cached_links.keys():
                pic_data = requests.get(url.url(), allow_redirects=True).content
                pixmap = QPixmap()
                pixmap.loadFromData(pic_data)
                self.cached_links[url.url()] = pixmap
                return pixmap

            return self.cached_links[url.url()]
        except:
            return QPixmap()
