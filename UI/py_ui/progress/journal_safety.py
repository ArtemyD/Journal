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

from database.models import (Attendance, Grade, PassSafety, Safety, Student,
                             Work)
from transform.date import str_to_date_2
from transform.items import set_items_to_table
from UI.py_ui.progress.add_safety import UiAddSafetyWindow
from UI.py_ui.progress.add_safety_student import UiAddSafetyStudent
from UI.py_ui.progress.update_safety_student import UiUpdateSafetyStudent


class UiJournalSafetyWindow(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.group_number: str = ''
        self.discipline_name: str = ''
        self.journal_safety_window = main_window.journal_safety_window
        self.journal_safety_window.setObjectName("MainWindow")
        self.journal_safety_window.setFixedSize(800, 630)
        self.centralwidget = QtWidgets.QWidget(self.journal_safety_window)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 771, 461))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 10, 161, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 58, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 30, 81, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(500, 0, 141, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_add_safety_student_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 30, 141, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_update_safety_student_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(640, 0, 141, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_teacher_journal_window)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(640, 30, 141, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.show_journal_attendance_window)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(670, 530, 112, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.close_window)

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 530, 231, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.show_add_safety_window)

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 560, 231, 32))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.delete_safety)

        self.journal_safety_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.journal_safety_window)
        self.statusbar.setObjectName("statusbar")
        self.journal_safety_window.setStatusBar(self.statusbar)

        self.add_safety_window = QtWidgets.QMainWindow()
        self.add_safety_ui = UiAddSafetyWindow(self)

        self.add_safety_student_window = QtWidgets.QMainWindow()
        self.add_safety_student_ui = UiAddSafetyStudent(self)

        self.update_safety_student_window = QtWidgets.QMainWindow()
        self.update_safety_student_ui = UiUpdateSafetyStudent(self)

        self.retranslateUi(self.journal_safety_window)
        QtCore.QMetaObject.connectSlotsByName(self.journal_safety_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Журнал техники безопасности"))
        self.label.setText(_translate("MainWindow", "Дисциплина:"))
        self.label_2.setText(_translate("MainWindow", "Математическая логика"))
        self.label_3.setText(_translate("MainWindow", "Группа:"))
        self.label_4.setText(_translate("MainWindow", "№423432"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_3.setText(_translate("MainWindow", "Оценки"))
        self.pushButton_4.setText(_translate("MainWindow", "Посещаемость"))
        self.pushButton_5.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_6.setText(_translate("MainWindow", "Добавить тему инструктажа"))
        self.pushButton_7.setText(_translate("MainWindow", "Удалить тему инструктажа"))

    # Дабавить тему инструктажа
    def show_add_safety_window(self):
        self.add_safety_ui.group_number = self.group_number
        self.add_safety_ui.discipline_name = self.discipline_name
        self.add_safety_ui.lineEdit.clear()
        self.add_safety_window.show()

    # Удалить тему инструктажа
    def delete_safety(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            col = self.tableWidget.column(i)

            safety = Safety()
            safe_name = safety.all_name(self.session, self.discipline_name, self.group_number)
            choosen_safe = safe_name[col - 1]

            safety.delete(self.session, choosen_safe, self.discipline_name, self.group_number)
            self.tableWidget.setRowCount(0)

            pass_safety = PassSafety()
            table_content: np.ndarray = pass_safety.all(self.session, self.discipline_name, self.group_number)
            self.tableWidget = set_items_to_table(self.tableWidget, table_content)

            table_header: list = safety.all_name(self.session, self.discipline_name, self.group_number,
                                                 flag_header=True)
            self.tableWidget.setHorizontalHeaderLabels(table_header)

            self.tableWidget.resizeColumnsToContents()

            break

    # Добавить дату прохождения инструктажа студентом
    def show_add_safety_student_window(self):
        student = Student()
        s_name = student.show_name(self.session, self.group_number)
        self.add_safety_student_ui.comboBox.clear()
        self.add_safety_student_ui.comboBox.addItems(s_name)

        safety = Safety()
        safe_name = safety.all_name(self.session, self.discipline_name, self.group_number)
        self.add_safety_student_ui.comboBox_2.clear()
        self.add_safety_student_ui.comboBox_2.addItems(safe_name)

        date_now = self.add_safety_student_ui.dateEdit.date().currentDate()
        self.add_safety_student_ui.dateEdit.setDate(date_now)

        self.add_safety_student_ui.group_number = self.group_number
        self.add_safety_student_ui.discipline_name = self.discipline_name
        self.add_safety_student_window.show()

    # Редактировать дату прохождения инструктажа студентом
    def show_update_safety_student_window(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            row = self.tableWidget.row(i)
            col = self.tableWidget.column(i)
            fio = self.tableWidget.item(row, 0).text()
            date = self.tableWidget.item(row, col).text()
            date = str_to_date_2(date)
            self.update_safety_student_ui.dateEdit.setDate(date)

            safety = Safety()
            safe_name = safety.all_name(self.session, self.discipline_name, self.group_number)

            choosen_safe = safe_name[col-1]
            self.update_safety_student_ui.label_4.setText(fio)
            self.update_safety_student_ui.label_5.setText(choosen_safe)
            break

        self.update_safety_student_ui.group_number = self.group_number
        self.update_safety_student_ui.discipline_name = self.discipline_name
        self.update_safety_student_window.show()

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

        self.teacher_journal_ui.journal_attendance_ui = self.journal_attendance_ui
        self.teacher_journal_ui.journal_attendance_window = self.journal_attendance_window
        self.teacher_journal_ui.journal_safety_ui = self.journal_safety_ui
        self.teacher_journal_ui.journal_safety_window = self.journal_safety_window
        self.teacher_journal_ui.teacher_journal_ui = self.teacher_journal_ui
        self.teacher_journal_ui.teacher_journal_window = self.teacher_journal_window

        self.teacher_journal_window.show()
        self.journal_safety_window.close()

    def close_window(self):
        self.tableWidget.setRowCount(0)
        self.journal_safety_window.close()

    def show_journal_attendance_window(self):
        self.journal_attendance_ui.label_2.setText(self.discipline_name)
        self.journal_attendance_ui.label_4.setText(self.group_number)

        a = Attendance()
        table_content: np.ndarray = a.all(self.session, self.discipline_name, self.group_number)
        self.journal_attendance_ui.tableWidget = set_items_to_table(self.journal_attendance_ui.tableWidget, table_content)

        table_header: list = a.show_name(self.session, self.group_number, self.discipline_name, flag_header=True)
        self.journal_attendance_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.journal_attendance_ui.tableWidget.resizeColumnsToContents()

        self.journal_attendance_ui.group_number = self.group_number
        self.journal_attendance_ui.discipline_name = self.discipline_name

        self.journal_attendance_ui.teacher_journal_ui = self.teacher_journal_ui
        self.journal_attendance_ui.teacher_journal_window = self.teacher_journal_window
        self.journal_attendance_ui.journal_safety_ui = self.journal_safety_ui
        self.journal_attendance_ui.journal_safety_window = self.journal_safety_window
        self.journal_attendance_ui.journal_attendance_ui = self.journal_attendance_ui
        self.journal_attendance_ui.journal_attendance_window= self.journal_attendance_window

        self.journal_attendance_window.show()
        self.journal_safety_window.close()
