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


class UiUpdateSafetyStudent(object):
    def __init__(self, main_window):
        self.group_number: str = ''
        self.discipline_name: str = ''
        self.session = main_window.session
        self.table = main_window.tableWidget
        self.update_safety_student_window = main_window.update_safety_student_window
        self.update_safety_student_window.setObjectName("MainWindow")
        self.update_safety_student_window.setFixedSize(503, 222)
        self.centralwidget = QtWidgets.QWidget(self.update_safety_student_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 161, 16))
        self.label_2.setObjectName("label_2")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(20, 130, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 161, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 150, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 30, 411, 16))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 80, 401, 16))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.update_safety_student_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_safety_student_window)
        self.statusbar.setObjectName("statusbar")
        self.update_safety_student_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_safety_student_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_safety_student_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Редактировать дату прохождение инструктажа студентом"))
        self.label.setText(_translate("MainWindow", "Cтудент:"))
        self.label_2.setText(_translate("MainWindow", "Тема инструктажа:"))
        self.label_3.setText(_translate("MainWindow", "Дата прохождения"))
        self.pushButton.setText(_translate("MainWindow", "Обновить"))

    def update(self):
        fio = self.label_4.text()
        safety = self.label_5.text()
        date = self.dateEdit.date().getDate()
        new_date = str(date)

        pass_safety = PassSafety()
        pass_safety.update(self.session, fio, safety, new_date, self.discipline_name, self.group_number)

        pass_safety = PassSafety()
        table_content: np.ndarray = pass_safety.all(self.session, self.discipline_name, self.group_number)
        self.table = set_items_to_table(self.table, table_content)
        self.table.resizeColumnsToContents()

        self.update_safety_student_window.close()
