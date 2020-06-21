"""
Copyright 2020 Artem Dyachenko

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from database.models import Audience
from transform.items import set_items_to_table


class UiAddAudience(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.table = main_window.tableWidget
        self.add_audience_window = main_window.add_audience_window
        self.add_audience_window.setObjectName("MainWindow")
        self.add_audience_window.setFixedSize(351, 173)
        self.centralwidget = QtWidgets.QWidget(self.add_audience_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 60, 221, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 58, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 321, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 80, 321, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(230, 110, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.add_audience_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_audience_window)
        self.statusbar.setObjectName("statusbar")
        self.add_audience_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_audience_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_audience_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить аудиторию"))
        self.label.setText(_translate("MainWindow", "Номер аудитории"))
        self.label_2.setText(_translate("MainWindow", "Корпус"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))

    def add(self):
        audience = Audience()
        corps = self.lineEdit.text()
        number = self.lineEdit_2.text()
        audience.add(self.session, corps, number)

        ls_all = audience.show_all(self.session)
        ls_all = np.array(ls_all)
        self.table = set_items_to_table(self.table, ls_all)
        self.table.resizeColumnsToContents()
        self.add_audience_window.close()
