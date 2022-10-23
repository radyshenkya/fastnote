from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices

import requests

# QTextBrowser with custom resource loading and anchors opening
class TextBrowser(QTextBrowser):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.cached_links = {}
        self.setOpenLinks(False)
        self.anchorClicked.connect(self.handle_links)

    def loadResource(self, type, name):
        url = name
        if not url.scheme():
            url = QUrl.fromLocalFile(url.url())

        try:
            if not url.url() in self.cached_links.keys():
                if url.url()[-3:] == "gif":
                    print("Gifs currently not supported")
                pic_data = requests.get(url.url(), allow_redirects=True).content
                pixmap = QPixmap()
                pixmap.loadFromData(pic_data)
                self.cached_links[url.url()] = pixmap
                return pixmap

            return self.cached_links[url.url()]
        except:
            return QPixmap()

    def handle_links(self, url):
        if not url.scheme():
            url = QUrl.fromLocalFile(url.url())
        QDesktopServices.openUrl(url)