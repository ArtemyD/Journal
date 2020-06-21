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

from database.models import Specialty
from transform.items import set_items_to_table
from transform.query import query_to_list_of_specialty_all
from UI.py_ui.student.add_specialty import UiAddSpecialty
from UI.py_ui.student.update_specialty import UiUpdateSpecialty


class UiSpecialtyListWindow(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.specialty_list_window = main_window.specialty_list_window
        self.specialty_list_window.setObjectName("MainWindow")
        self.specialty_list_window.setFixedSize(625, 416)
        self.centralwidget = QtWidgets.QWidget(self.specialty_list_window)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 601, 301))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        specialty = Specialty()
        ls_all = specialty.show_all(self.session)
        ls = query_to_list_of_specialty_all(ls_all)

        self.tableWidget = set_items_to_table(self.tableWidget, ls)
        self.tableWidget.setHorizontalHeaderLabels(["Код", "Наименование"])

        self.tableWidget.resizeColumnsToContents()
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 320, 151, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 320, 151, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.update)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(310, 320, 151, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(460, 350, 151, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.close_window)
        self.specialty_list_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.specialty_list_window)
        self.statusbar.setObjectName("statusbar")
        self.specialty_list_window.setStatusBar(self.statusbar)

        self.add_specialty_window = QtWidgets.QMainWindow()
        self.add_specialty_ui = UiAddSpecialty(self)

        self.update_specialty_window = QtWidgets.QMainWindow()
        self.update_specialty_ui = UiUpdateSpecialty(self)

        self.retranslateUi(self.specialty_list_window)
        QtCore.QMetaObject.connectSlotsByName(self.specialty_list_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Специальности"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_3.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_4.setText(_translate("MainWindow", "Закрыть"))

    def add(self):
        self.add_specialty_window.show()

    def update(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            row = self.tableWidget.row(i)

            code = self.tableWidget.item(row, 0).text()
            name = self.tableWidget.item(row, 1).text()

            self.update_specialty_ui.lineEdit.setText(code)
            self.update_specialty_ui.lineEdit_2.setText(name)

            self.update_specialty_ui.update_value = name
            self.update_specialty_ui.row = row

            self.update_specialty_window.show()
            break

    def delete(self):
        items = self.tableWidget.selectedItems()
        for i in items:
            row = self.tableWidget.row(i)
            name = self.tableWidget.item(row, 1).text()

            specialty = Specialty()
            specialty.delete(self.session, name)

            self.tableWidget.removeRow(row)



    def close_window(self):
        self.specialty_list_window.close()
