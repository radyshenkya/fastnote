# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './uic_files/table_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button {\n"
"    height: 0px;\n"
"    width: 0px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(Dialog)
        self.table.setShowGrid(True)
        self.table.setCornerButtonEnabled(True)
        self.table.setRowCount(2)
        self.table.setColumnCount(2)
        self.table.setObjectName("table")
        self.verticalLayout.addWidget(self.table)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.rows_spinbox = QtWidgets.QSpinBox(Dialog)
        self.rows_spinbox.setMinimum(1)
        self.rows_spinbox.setObjectName("rows_spinbox")
        self.horizontalLayout.addWidget(self.rows_spinbox)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.cols_spinbox = QtWidgets.QSpinBox(Dialog)
        self.cols_spinbox.setMinimum(1)
        self.cols_spinbox.setObjectName("cols_spinbox")
        self.horizontalLayout.addWidget(self.cols_spinbox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "???????????????? ??????????????"))
        self.table.setSortingEnabled(False)
        self.label.setText(_translate("Dialog", "??????????"))
        self.label_2.setText(_translate("Dialog", "????????????????"))
