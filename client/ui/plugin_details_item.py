# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './uic_files/plugin_details_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(561, 185)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plugin_name = QtWidgets.QLabel(Form)
        self.plugin_name.setObjectName("plugin_name")
        self.verticalLayout.addWidget(self.plugin_name)
        self.plugin_description = QtWidgets.QTextBrowser(Form)
        self.plugin_description.setObjectName("plugin_description")
        self.verticalLayout.addWidget(self.plugin_description)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.plugin_name.setText(_translate("Form", "Plugin Name"))