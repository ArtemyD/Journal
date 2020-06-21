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
from PyQt5 import QtCore, QtGui, QtWidgets

from database.models import Audience
from UI.py_ui.timetable.settings.add_audience import UiAddAudience
from UI.py_ui.timetable.settings.update_audience import UiUpdateAudience


class UiAudienceList(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.audience_list_window = main_window.audience_list_window
        self.audience_list_window.setObjectName("MainWindow")
        self.audience_list_window.setFixedSize(552, 434)
        self.centralwidget = QtWidgets.QWidget(self.audience_list_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 370, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 370, 141, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.update_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 370, 112, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(430, 370, 112, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.close)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 531, 351))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Корпус", "Аудитория"])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.audience_list_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.audience_list_window)
        self.statusbar.setObjectName("statusbar")
        self.audience_list_window.setStatusBar(self.statusbar)

        self.add_audience_window = QtWidgets.QMainWindow()
        self.add_audience_ui = UiAddAudience(self)

        self.update_audience_window = QtWidgets.QMainWindow()
        self.update_audience_ui = UiUpdateAudience(self)

        self.retranslateUi(self.audience_list_window)
        QtCore.QMetaObject.connectSlotsByName(self.audience_list_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Аудитории"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_3.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_4.setText(_translate("MainWindow", "Закрыть"))

    def add_window(self):
        self.add_audience_ui.lineEdit.clear()
        self.add_audience_ui.lineEdit_2.clear()
        self.add_audience_window.show()

    def update_window(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            row = self.tableWidget.row(i)

            corps = self.tableWidget.item(row, 0).text()
            number = self.tableWidget.item(row, 1).text()

            self.update_audience_ui.lineEdit.setText(corps)
            self.update_audience_ui.lineEdit_2.setText(number)

            self.update_audience_ui.update_value = number
            self.update_audience_ui.row = row

            self.update_audience_window.show()
            break

    def delete(self):
        items = self.tableWidget.selectedItems()
        for i in items:
            row = self.tableWidget.row(i)
            number = self.tableWidget.item(row, 1).text()
            audience = Audience()
            audience.delete(self.session, number)
            self.tableWidget.removeRow(row)

    def close(self):
        self.audience_list_window.close()
