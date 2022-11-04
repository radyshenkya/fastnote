"""
Small functions based on pyqt
"""

from PyQt5.QtWidgets import QMessageBox


def alert_message_box(title: str, message: str):
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    return msg_box.exec()
