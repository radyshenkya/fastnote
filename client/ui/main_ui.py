# Form implementation generated from reading ui file './uic_files/main.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(834, 758)
        MainWindow.setStyleSheet("* {\n"
"    background-color: rgb(55, 57, 61);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.edit_panel = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_panel.sizePolicy().hasHeightForWidth())
        self.edit_panel.setSizePolicy(sizePolicy)
        self.edit_panel.setMinimumSize(QtCore.QSize(400, 0))
        self.edit_panel.setStyleSheet("* {\n"
"    background-color: rgb(32, 33, 36);\n"
"    color: #fff;\n"
"}")
        self.edit_panel.setObjectName("edit_panel")
        self.main_layout.addWidget(self.edit_panel)
        self.verticalLayout_2.addLayout(self.main_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fast Note"))
