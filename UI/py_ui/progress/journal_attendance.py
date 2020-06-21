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

from database.models import Attendance, Grade, PassSafety, Safety, Work
from transform.items import set_items_to_table


class UiJournalAttendanceWindow(object):
    def __init__(self, main_window):
        self.group_number: str = ''
        self.discipline_name: str = ''
        self.session = main_window.session
        self.journal_attendance_window = main_window.journal_attendance_window
        self.journal_attendance_window.setObjectName("MainWindow")
        self.journal_attendance_window.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self.journal_attendance_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 10, 191, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_teacher_journal_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(590, 10, 191, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_journal_safety_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(670, 530, 121, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.close)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 10, 171, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 58, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 30, 101, 16))
        self.label_4.setObjectName("label_4")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 60, 761, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 530, 251, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.attended)
        self.journal_attendance_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.journal_attendance_window)
        self.statusbar.setObjectName("statusbar")
        self.journal_attendance_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.journal_attendance_window)
        QtCore.QMetaObject.connectSlotsByName(self.journal_attendance_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Журнал посещаемости"))
        self.pushButton.setText(_translate("MainWindow", "Оценки"))
        self.pushButton_2.setText(_translate("MainWindow", "Техника безопасности"))
        self.pushButton_3.setText(_translate("MainWindow", "Закрыть"))
        self.label.setText(_translate("MainWindow", "Дисциплина:"))
        self.label_2.setText(_translate("MainWindow", "Математическая логика"))
        self.label_3.setText(_translate("MainWindow", "Группа:"))
        self.label_4.setText(_translate("MainWindow", "№4323424"))
        self.pushButton_4.setText(_translate("MainWindow", "Присутстовавал / отсутствовал"))

    def close(self):
        self.journal_attendance_window.close()

    def attended(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            col = self.tableWidget.column(i)
            header = self.tableWidget.horizontalHeaderItem(col).text()
            date = header.split('|')[0]
            class_format = header.split('|')[1]
            row = self.tableWidget.row(i)
            student = self.tableWidget.item(row, 0).text()

            a = Attendance()
            a.update(self.session, date, class_format, student)

            value = self.tableWidget.item(row, col).text()
            if value == 'Н':
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(" "))
            else:
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem("Н"))

            break

        self.journal_attendance_window.hide()
        self.journal_attendance_window.show()

    def show_teacher_journal_window(self):
        work = Work()
        grade = Grade()
        table_content: np.ndarray = grade.all(self.session, self.discipline_name, self.group_number)
        self.teacher_journal_ui.tableWidget = set_items_to_table(self.teacher_journal_ui.tableWidget, table_content)

        table_header: list = work.show_name(self.session, self.group_number, self.discipline_name, flag_header=True)
        self.teacher_journal_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.teacher_journal_ui.tableWidget.resizeColumnsToContents()

        self.teacher_journal_ui.group_number = self.group_number
        self.teacher_journal_ui.discipline_name = self.discipline_name
        d = "Дисциплина: " + str(self.discipline_name)
        self.teacher_journal_ui.label.setText(d)
        g = "Группа: №" + str(self.group_number)
        self.teacher_journal_ui.label_2.setText(g)
        self.teacher_journal_window.show()

        self.teacher_journal_ui.teacher_journal_ui = self.teacher_journal_ui
        self.teacher_journal_ui.teacher_journal_window = self.teacher_journal_window
        self.teacher_journal_ui.journal_attendance_window = self.journal_attendance_window
        self.teacher_journal_ui.journal_attendance_ui = self.journal_attendance_ui
        self.teacher_journal_ui.journal_safety_window = self.journal_safety_window
        self.teacher_journal_ui.journal_safety_ui = self.journal_safety_ui

        self.teacher_journal_window.show()
        self.journal_attendance_window.close()

    def show_journal_safety_window(self):
        safety = Safety()
        pass_safety = PassSafety()
        table_content: np.ndarray = pass_safety.all(self.session, self.discipline_name, self.group_number)
        self.journal_safety_ui.tableWidget = set_items_to_table(self.journal_safety_ui.tableWidget, table_content)

        table_header: list = safety.all_name(self.session, self.discipline_name, self.group_number, flag_header=True)
        self.journal_safety_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.journal_safety_ui.tableWidget.resizeColumnsToContents()

        self.journal_safety_ui.group_number = self.group_number
        self.journal_safety_ui.discipline_name = self.discipline_name
        self.journal_safety_ui.label_2.setText(self.discipline_name)
        self.journal_safety_ui.label_4.setText(self.group_number)

        self.journal_safety_ui.teacher_journal_ui = self.teacher_journal_ui
        self.journal_safety_ui.teacher_journal_window = self.teacher_journal_window
        self.journal_safety_ui.journal_attendance_window = self.journal_attendance_window
        self.journal_safety_ui.journal_attendance_ui = self.journal_attendance_ui
        self.journal_safety_ui.journal_safety_window = self.journal_safety_window
        self.journal_safety_ui.journal_safety_ui = self.journal_safety_ui

        self.journal_safety_window.show()
        self.journal_attendance_window.close()
