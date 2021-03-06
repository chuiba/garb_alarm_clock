# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(652, 282)
        font = QtGui.QFont()
        font.setKerning(True)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.garb_name = QtWidgets.QLabel(self.centralwidget)
        self.garb_name.setGeometry(QtCore.QRect(80, 40, 161, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.garb_name.setFont(font)
        self.garb_name.setObjectName("garb_name")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 60, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.number = QtWidgets.QLabel(self.centralwidget)
        self.number.setGeometry(QtCore.QRect(20, 130, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.number.setFont(font)
        self.number.setObjectName("number")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 180, 60, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.cur_date = QtWidgets.QLabel(self.centralwidget)
        self.cur_date.setGeometry(QtCore.QRect(20, 210, 131, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.cur_date.setFont(font)
        self.cur_date.setObjectName("cur_date")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(515, 195, 105, 32))
        self.pushButton.setObjectName("pushButton")
        self.item_id = QtWidgets.QLineEdit(self.centralwidget)
        self.item_id.setGeometry(QtCore.QRect(520, 140, 95, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_id.sizePolicy().hasHeightForWidth())
        self.item_id.setSizePolicy(sizePolicy)
        self.item_id.setAlignment(QtCore.Qt.AlignCenter)
        self.item_id.setObjectName("item_id")
        self.interval = QtWidgets.QLineEdit(self.centralwidget)
        self.interval.setGeometry(QtCore.QRect(520, 170, 95, 21))
        self.interval.setAlignment(QtCore.Qt.AlignCenter)
        self.interval.setObjectName("interval")
        self.avator = QtWidgets.QLabel(self.centralwidget)
        self.avator.setGeometry(QtCore.QRect(25, 25, 40, 40))
        self.avator.setText("")
        self.avator.setObjectName("avator")
        self.alarm_id = QtWidgets.QLineEdit(self.centralwidget)
        self.alarm_id.setGeometry(QtCore.QRect(520, 110, 95, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alarm_id.sizePolicy().hasHeightForWidth())
        self.alarm_id.setSizePolicy(sizePolicy)
        self.alarm_id.setAlignment(QtCore.Qt.AlignCenter)
        self.alarm_id.setObjectName("alarm_id")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "?????????????????????"))
        self.garb_name.setText(_translate("MainWindow", "????????????"))
        self.label_2.setText(_translate("MainWindow", "FANS NO."))
        self.number.setText(_translate("MainWindow", "000001"))
        self.label_3.setText(_translate("MainWindow", "DATE"))
        self.cur_date.setText(_translate("MainWindow", "2021/01/01 23:59:59"))
        self.pushButton.setText(_translate("MainWindow", "??????"))
        self.item_id.setText(_translate("MainWindow", "????????????"))
        self.interval.setText(_translate("MainWindow", "60"))
        self.alarm_id.setText(_translate("MainWindow", "????????????"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
