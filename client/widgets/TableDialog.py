from PyQt5.QtWidgets import QDialog

from ui.table_dialog_ui import Ui_Dialog

from PyQt5.QtWidgets import QLineEdit


class TableDialog(QDialog, Ui_Dialog):
    def __init__(self, on_ok_function, parent=None) -> None:
        super().__init__(parent)

        self.on_ok_func = on_ok_function

        self.setupUi(self)
        self.init_logic()

        self.buttonBox.accepted.connect(self.on_ok)

    def on_ok(self):
        table = []

        for row in range(self.table.rowCount()):
            table.append(
                [
                    (lambda x: "" if x is None else x.text())(self.table.item(row, col))
                    for col in range(self.table.columnCount())
                ]
            )

        self.on_ok_func(table)

    def init_logic(self):
        self.rows_spinbox.valueChanged.connect(self.on_rows_changed)
        self.cols_spinbox.valueChanged.connect(self.on_cols_changed)

    def on_rows_changed(self):
        self.table.setRowCount(self.rows_spinbox.value())

    def on_cols_changed(self):
        self.table.setColumnCount(self.cols_spinbox.value())
