# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CollectedMaterials.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CollectedMaterials(object):
    def setupUi(self, CollectedMaterials):
        CollectedMaterials.setObjectName("CollectedMaterials")
        CollectedMaterials.resize(960, 540)
        self.centralwidget = QtWidgets.QWidget(CollectedMaterials)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(220, 90, 500, 300))
        self.tableView.setObjectName("tableView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 50, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.redButton = QtWidgets.QPushButton(self.centralwidget)
        self.redButton.setGeometry(QtCore.QRect(420, 410, 101, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.redButton.setFont(font)
        self.redButton.setObjectName("redButton")
        CollectedMaterials.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CollectedMaterials)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 21))
        self.menubar.setObjectName("menubar")
        CollectedMaterials.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CollectedMaterials)
        self.statusbar.setObjectName("statusbar")
        CollectedMaterials.setStatusBar(self.statusbar)

        self.retranslateUi(CollectedMaterials)
        QtCore.QMetaObject.connectSlotsByName(CollectedMaterials)

    def retranslateUi(self, CollectedMaterials):
        _translate = QtCore.QCoreApplication.translate
        CollectedMaterials.setWindowTitle(_translate("CollectedMaterials", "Собранные материалы"))
        self.label.setText(_translate("CollectedMaterials", "Список добытых материалов"))
        self.redButton.setText(_translate("CollectedMaterials", "Редактировать"))
