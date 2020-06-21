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

from database.models import ClassFormat
from UI.py_ui.timetable.settings.add_training_formats import \
    UiAddTrainingFormats
from UI.py_ui.timetable.settings.update_training_formats import \
    UiUpdateTrainingFormats


class UiTrainingFormatsList(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.training_formats_list_window = main_window.training_formats_list_window
        self.training_formats_list_window.setObjectName("MainWindow")
        self.training_formats_list_window.setFixedSize(521, 353)
        self.centralwidget = QtWidgets.QWidget(self.training_formats_list_window)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 491, 271))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Наименование"])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 290, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 290, 131, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.update_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(250, 290, 112, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(390, 290, 112, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.close)
        self.training_formats_list_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.training_formats_list_window)
        self.statusbar.setObjectName("statusbar")
        self.training_formats_list_window.setStatusBar(self.statusbar)

        self.add_training_formats_window = QtWidgets.QMainWindow()
        self.add_training_formats_ui = UiAddTrainingFormats(self)

        self.update_training_formats_window = QtWidgets.QMainWindow()
        self.update_training_formats_ui = UiUpdateTrainingFormats(self)

        self.retranslateUi(self.training_formats_list_window)
        QtCore.QMetaObject.connectSlotsByName(self.training_formats_list_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Форматы занятий"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_3.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_4.setText(_translate("MainWindow", "Закрыть"))

    def add_window(self):
        self.add_training_formats_ui.lineEdit.clear()
        self.add_training_formats_window.show()

    def update_window(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            row = self.tableWidget.row(i)

            name = self.tableWidget.item(row, 0).text()

            self.update_training_formats_ui.lineEdit.setText(name)

            self.update_training_formats_ui.update_value = name
            self.update_training_formats_ui.row = row

            self.update_training_formats_window.show()
            break

    def delete(self):
        items = self.tableWidget.selectedItems()
        for i in items:
            row = self.tableWidget.row(i)
            name = self.tableWidget.item(row, 0).text()
            c = ClassFormat()
            c.delete(self.session, name)
            self.tableWidget.removeRow(row)

    def close(self):
        self.training_formats_list_window.close()
