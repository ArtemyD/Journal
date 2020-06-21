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
from PyQt5 import QtCore, QtWidgets

from database.models import Attendance, Grade, PassSafety, Safety, Work
from transform.items import set_items_to_table
from UI.py_ui.progress.journal_attendance import UiJournalAttendanceWindow
from UI.py_ui.progress.journal_safety import UiJournalSafetyWindow
from UI.py_ui.progress.teacher_journal import UiTeacherJournalWindow


class UiGradesWindow(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.grades_window = main_window.grade_window
        self.grades_window.setObjectName("MainWindow")
        self.grades_window.setFixedSize(474, 172)
        self.centralwidget = QtWidgets.QWidget(self.grades_window)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 100, 211, 32))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 44, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 40, 211, 32))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 161, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 40, 211, 32))
        self.pushButton.clicked.connect(self.show_teacher_journal_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 70, 211, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_journal_attendance_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 100, 211, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_journal_safety_window)
        self.grades_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.grades_window)
        self.statusbar.setObjectName("statusbar")
        self.grades_window.setStatusBar(self.statusbar)

        self.journal_safety_window = QtWidgets.QMainWindow()
        self.journal_safety_ui = UiJournalSafetyWindow(self)

        self.journal_attendance_window = QtWidgets.QMainWindow()
        self.journal_attendance_ui = UiJournalAttendanceWindow(self)

        self.teacher_journal_window = QtWidgets.QMainWindow()
        self.teacher_journal_ui = UiTeacherJournalWindow(self)

        self.retranslateUi(self.grades_window)
        QtCore.QMetaObject.connectSlotsByName(self.grades_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Успеваемость"))
        self.label_2.setText(_translate("MainWindow", "Группа"))
        self.label.setText(_translate("MainWindow", "Дисциплина"))
        self.pushButton.setText(_translate("MainWindow", "Оценки"))
        self.pushButton_2.setText(_translate("MainWindow", "Посещаемость"))
        self.pushButton_3.setText(_translate("MainWindow", "Техника безопасности"))

    def show_journal_safety_window(self):
        safety = Safety()
        group_number: str = self.comboBox_2.currentText()
        discipline_name: str = self.comboBox.currentText()

        pass_safety = PassSafety()
        table_content: np.ndarray = pass_safety.all(self.session, discipline_name, group_number)
        self.journal_safety_ui.tableWidget = set_items_to_table(self.journal_safety_ui.tableWidget, table_content)

        table_header: list = safety.all_name(self.session, discipline_name, group_number, flag_header=True)
        self.journal_safety_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.journal_safety_ui.tableWidget.resizeColumnsToContents()

        self.journal_safety_ui.group_number = group_number
        self.journal_safety_ui.discipline_name = discipline_name
        self.journal_safety_ui.label_2.setText(discipline_name)
        self.journal_safety_ui.label_4.setText(group_number)

        self.journal_safety_ui.teacher_journal_ui = self.teacher_journal_ui
        self.journal_safety_ui.teacher_journal_window = self.teacher_journal_window
        self.journal_safety_ui.journal_attendance_window = self.journal_attendance_window
        self.journal_safety_ui.journal_attendance_ui = self.journal_attendance_ui
        self.journal_safety_ui.journal_safety_ui = self.journal_safety_ui
        self.journal_safety_ui.journal_safety_window = self.journal_safety_window

        self.journal_safety_window.show()

    def show_journal_attendance_window(self):
        group_number: str = self.comboBox_2.currentText()
        discipline_name: str = self.comboBox.currentText()
        self.journal_attendance_ui.label_2.setText(discipline_name)
        self.journal_attendance_ui.label_4.setText(group_number)

        a = Attendance()
        table_content: np.ndarray = a.all(self.session, discipline_name, group_number)
        self.journal_attendance_ui.tableWidget = set_items_to_table(self.journal_attendance_ui.tableWidget, table_content)

        table_header: list = a.show_name(self.session, group_number, discipline_name, flag_header=True)
        self.journal_attendance_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.journal_attendance_ui.tableWidget.resizeColumnsToContents()

        self.journal_attendance_ui.group_number = group_number
        self.journal_attendance_ui.discipline_name = discipline_name

        self.journal_attendance_ui.teacher_journal_ui = self.teacher_journal_ui
        self.journal_attendance_ui.teacher_journal_window = self.teacher_journal_window
        self.journal_attendance_ui.journal_safety_ui = self.journal_safety_ui
        self.journal_attendance_ui.journal_safety_window = self.journal_safety_window
        self.journal_attendance_ui.journal_attendance_ui = self.journal_attendance_ui
        self.journal_attendance_ui.journal_attendance_window = self.journal_attendance_window

        self.journal_attendance_window.show()

    def show_teacher_journal_window(self):
        work = Work()
        group_number: str = self.comboBox_2.currentText()
        discipline_name: str = self.comboBox.currentText()

        grade = Grade()
        table_content: np.ndarray = grade.all(self.session, discipline_name, group_number)
        self.teacher_journal_ui.tableWidget = set_items_to_table(self.teacher_journal_ui.tableWidget, table_content)

        table_header: list = work.show_name(self.session, group_number, discipline_name, flag_header=True)
        self.teacher_journal_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.teacher_journal_ui.tableWidget.resizeColumnsToContents()

        self.teacher_journal_ui.group_number = group_number
        self.teacher_journal_ui.discipline_name = discipline_name
        d = "Дисциплина: " + str(discipline_name)
        self.teacher_journal_ui.label.setText(d)
        g = "Группа: №" + str(group_number)
        self.teacher_journal_ui.label_2.setText(g)

        self.teacher_journal_ui.teacher_journal_ui = self.teacher_journal_ui
        self.teacher_journal_ui.teacher_journal_window = self.teacher_journal_window
        self.teacher_journal_ui.journal_safety_ui = self.journal_safety_ui
        self.teacher_journal_ui.journal_safety_window = self.journal_safety_window
        self.teacher_journal_ui.journal_attendance_ui = self.journal_attendance_ui
        self.teacher_journal_ui.journal_attendance_window = self.journal_attendance_window

        self.teacher_journal_window.show()
