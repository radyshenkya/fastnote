# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './uic_files/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(916, 758)
        MainWindow.setStyleSheet("* {\n"
"    background-color: #202124;\n"
"    color: #fff;\n"
"    border: 0px solid #fff;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: 2px solid rgb(211, 79, 115);\n"
"    padding: 10px 17px;\n"
"    color: #D34F73;\n"
"    font-size: 20px;\n"
"    font-family: \'Roboto\', sans-serif;\n"
"    font-weight: 300;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-color: #06BA63;\n"
"    color: #06BA63;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    width: 15px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background:#D34F73;\n"
"    width: 14px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background:#06BA63;\n"
"    width: 14px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"height: 0px;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"height: 0px;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"height: 0px;\n"
"}\n"
"\n"
"\n"
"QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"          height: 0px;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background-color: #37393D;\n"
"}\n"
"\n"
"QToolButton {\n"
"    \n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color: #37393D;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.current_file_label = QtWidgets.QLineEdit(self.centralwidget)
        self.current_file_label.setStyleSheet("* {\n"
"    color: #9A9FA6;\n"
"}")
        self.current_file_label.setReadOnly(True)
        self.current_file_label.setObjectName("current_file_label")
        self.verticalLayout_2.addWidget(self.current_file_label)
        self.edit_tools_layout = QtWidgets.QHBoxLayout()
        self.edit_tools_layout.setObjectName("edit_tools_layout")
        self.verticalLayout_2.addLayout(self.edit_tools_layout)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.edit_panel = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_panel.sizePolicy().hasHeightForWidth())
        self.edit_panel.setSizePolicy(sizePolicy)
        self.edit_panel.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.edit_panel.setFont(font)
        self.edit_panel.setStyleSheet("")
        self.edit_panel.setObjectName("edit_panel")
        self.main_layout.addWidget(self.edit_panel)
        self.render_panel = TextBrowser(self.centralwidget)
        self.render_panel.setStyleSheet("")
        self.render_panel.setObjectName("render_panel")
        self.main_layout.addWidget(self.render_panel)
        self.main_layout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.main_layout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 916, 22))
        self.menu_bar.setObjectName("menu_bar")
        MainWindow.setMenuBar(self.menu_bar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actiontext = QtWidgets.QAction(MainWindow)
        self.actiontext.setObjectName("actiontext")
        self.actiontext_2 = QtWidgets.QAction(MainWindow)
        self.actiontext_2.setObjectName("actiontext_2")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fast Note"))
        self.current_file_label.setText(_translate("MainWindow", "unsaved file"))
        self.edit_panel.setPlainText(_translate("MainWindow", "# Привет, Мир!\n"
"\n"
"Редактор **FastNote** позволяет редактировать и просматривать файлы формата [MarkDown](https://en.wikipedia.org/wiki/Markdown)\n"
"\n"
"---\n"
"\n"
"![Test Image](https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/240px-PNG_transparency_demonstration_1.png)"))
        self.render_panel.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Edit Tools"))
        self.actiontext.setText(_translate("MainWindow", "text"))
        self.actiontext_2.setText(_translate("MainWindow", "text"))
from widgets.TextBrowser import TextBrowser
