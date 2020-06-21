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

from database.models import PassSafety
from transform.items import set_items_to_table


class UiAddSafetyStudent(object):
    def __init__(self, main_window):
        self.table = main_window.tableWidget
        self.group_number: str = ''
        self.discipline_name: str = ''
        self.session = main_window.session
        self.table = main_window.tableWidget
        self.add_safety_student_window = main_window.add_safety_student_window
        self.add_safety_student_window.setObjectName("MainWindow")
        self.add_safety_student_window.setFixedSize(448, 252)
        self.centralwidget = QtWidgets.QWidget(self.add_safety_student_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 431, 32))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 161, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 90, 431, 32))
        self.comboBox_2.setObjectName("comboBox_2")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(20, 150, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 161, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 180, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.add_safety_student_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_safety_student_window)
        self.statusbar.setObjectName("statusbar")
        self.add_safety_student_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_safety_student_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_safety_student_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Дата прохождение инструктажа студентом"))
        self.label.setText(_translate("MainWindow", "Cтудент"))
        self.label_2.setText(_translate("MainWindow", "Тема инструктажа"))
        self.label_3.setText(_translate("MainWindow", "Дата прохождения"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))

    def add(self):
        student = self.comboBox.currentText()
        safety = self.comboBox_2.currentText()
        date = self.dateEdit.date().getDate()
        new_date = str(date)

        pass_safety = PassSafety()
        pass_safety.add(self.session, student, safety, new_date, self.discipline_name, self.group_number)

        pass_safety = PassSafety()
        table_content: np.ndarray = pass_safety.all(self.session, self.discipline_name, self.group_number)
        self.table = set_items_to_table(self.table, table_content)
        self.table.resizeColumnsToContents()

        self.add_safety_student_window.close()
