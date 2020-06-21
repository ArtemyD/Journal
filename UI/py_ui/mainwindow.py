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

import datetime

import numpy as np
from PyQt5 import QtCore, QtWidgets

from database.models import Discipline, Group, Occupation
from settings import my_months
from transform.items import set_items_to_table
from UI.py_ui.discipline.subject_list import UiSubjectList

from UI.py_ui.progress.grades import UiGradesWindow
from UI.py_ui.student.student import UiStudentWindow
from UI.py_ui.timetable.timetable import UiTimetableWindow


class FormMainWindow(object):
    def __init__(self, main_window, session):
        self.user = None
        self.session = session
        self.main_window = main_window
        main_window.setObjectName("MainWindow")
        main_window.resize(841, 543)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.show_timetable_window)
        self.gridLayout.addWidget(self.pushButton_5, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_subject_list_window)
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 8, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 2, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 2, 1, 2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.open_grade_window)
        self.gridLayout.addWidget(self.pushButton_3, 0, 3, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_student_window)
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_2, 5, 2, 1, 2)
        self.tableWidget_5 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(5)
        self.tableWidget_5.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_5.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_5, 9, 2, 1, 2)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 2)
        self.tableWidget_4 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(5)
        self.tableWidget_4.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_4.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_4, 9, 0, 1, 2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 4)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.previous_week)
        self.gridLayout.addWidget(self.pushButton_7, 3, 4, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.next_week)
        self.gridLayout.addWidget(self.pushButton_8, 3, 5, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.close_app)
        self.gridLayout.addWidget(self.pushButton_4, 0, 5, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 1, 0, 1, 6)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 6)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_3.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_3, 5, 4, 1, 2)
        self.tableWidget_6 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_6.setObjectName("tableWidget_6")
        self.tableWidget_6.setColumnCount(5)
        self.tableWidget_6.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_6.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_6, 9, 4, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 8, 4, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 4, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.login_window = QtWidgets.QMainWindow()


        self.subject_list_window = QtWidgets.QMainWindow()
        self.subject_list_ui = UiSubjectList(self)

        self.student_window = QtWidgets.QMainWindow()
        self.student_ui = UiStudentWindow(self)

        self.timetable_window = QtWidgets.QMainWindow()
        self.timetable_ui = UiTimetableWindow(self)

        self.grade_window = QtWidgets.QMainWindow()
        self.grade_ui = UiGradesWindow(self)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Личный кабинет преподавтеля"))
        self.pushButton_5.setText(_translate("MainWindow", "Расписание"))
        self.pushButton.setText(_translate("MainWindow", "Дисциплины"))
        self.label_2.setText(_translate("MainWindow", "Четверг"))
        self.label.setText(_translate("MainWindow", "Понедельник"))
        self.label_4.setText(_translate("MainWindow", "Вторник"))
        self.label_5.setText(_translate("MainWindow", "Пятница"))
        self.pushButton_3.setText(_translate("MainWindow", "Успеваемость"))
        self.pushButton_2.setText(_translate("MainWindow", "Студенты"))
        self.pushButton_7.setText(_translate("MainWindow", "Предыдущая неделя"))
        self.pushButton_8.setText(_translate("MainWindow", "Следующая неделя"))
        self.pushButton_4.setText(_translate("MainWindow", "Выход"))
        self.label_3.setText(_translate("MainWindow", "Расписание занятий (с 13 по 18 апреля)"))
        self.label_7.setText(_translate("MainWindow", "Суббота"))
        self.label_6.setText(_translate("MainWindow", "Среда"))

    def show(self):
        self.main_window.show()
        # self.show_login_window()
        # self.main_window.hide()

    def set_default_date(self):
        now = datetime.date.today()
        monday = now
        while monday.weekday() != 0:
            monday -= datetime.timedelta(days=1)

        saturday = now
        if now.weekday() != 6:
            while saturday.weekday() != 5:
                saturday += datetime.timedelta(days=1)
        else:
            while saturday.weekday() != 5:
                saturday -= datetime.timedelta(days=1)

        day_begin = monday.day
        day_end = saturday.day
        months_begin = my_months[monday.month % 12-1]
        months_end = my_months[saturday.month % 12-1]

        label = "Расписание занятий (с " + str(day_begin) + " " + months_begin + " по " + str(day_end) + " " +\
                months_end + ")"
        self.label_3.setText(label)
        self.set_defualt_timetable(monday, saturday)

    def set_defualt_timetable(self, monday, saturday):
        tuesday = monday + datetime.timedelta(days=1)
        wednesday = monday + datetime.timedelta(days=2)
        thursday = monday + datetime.timedelta(days=3)
        friday = monday + datetime.timedelta(days=4)

        o = Occupation()
        monday_ls = o.show_all(self.session, monday)
        tuesday_ls = o.show_all(self.session, tuesday)
        wednesday_ls = o.show_all(self.session, wednesday)
        thursday_ls = o.show_all(self.session, thursday)
        friday_ls = o.show_all(self.session, friday)
        saturday_ls = o.show_all(self.session, saturday)

        monday_ls = np.array(monday_ls)
        self.tableWidget.setRowCount(0)
        self.tableWidget = set_items_to_table(self.tableWidget, monday_ls)
        self.tableWidget.resizeColumnsToContents()

        tuesday_ls = np.array(tuesday_ls)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2 = set_items_to_table(self.tableWidget_2, tuesday_ls)
        self.tableWidget_2.resizeColumnsToContents()

        wednesday_ls = np.array(wednesday_ls)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3 = set_items_to_table(self.tableWidget_3, wednesday_ls)
        self.tableWidget_3.resizeColumnsToContents()

        thursday_ls = np.array(thursday_ls)
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4 = set_items_to_table(self.tableWidget_4, thursday_ls)
        self.tableWidget_4.resizeColumnsToContents()

        friday_ls = np.array(friday_ls)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5 = set_items_to_table(self.tableWidget_5, friday_ls)
        self.tableWidget_5.resizeColumnsToContents()

        saturday_ls = np.array(saturday_ls)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6 = set_items_to_table(self.tableWidget_6, saturday_ls)
        self.tableWidget_6.resizeColumnsToContents()

    def previous_week(self):
        pre_label = self.label_3.text()
        day_begin_old = pre_label.split("с ")[1].split(" ")[0]
        month_begin_old = pre_label.split("с ")[1].split(" ")[1]
        month_begin_old = my_months.index(month_begin_old) + 1

        date_begin_old = datetime.date(2020, month_begin_old, int(day_begin_old))
        monday = date_begin_old - datetime.timedelta(days=7)
        saturday = date_begin_old - datetime.timedelta(days=2)

        day_begin = monday.day
        day_end = saturday.day
        months_begin = my_months[monday.month % 12 - 1]
        months_end = my_months[saturday.month % 12 - 1]

        label = "Расписание занятий (с " + str(day_begin) + " " + months_begin + " по " + str(day_end) + " " + \
                months_end + ")"

        self.label_3.setText(label)
        self.set_defualt_timetable(monday, saturday)
        self.main_window.hide()
        self.main_window.show()

    def next_week(self):
        pre_label = self.label_3.text()
        day_end_old = pre_label.split("с ")[1].split(" ")[3]
        month_end_old = pre_label.split("с ")[1].split(" ")[4].split(')')[0]

        month_end_old = my_months.index(month_end_old) + 1

        date_end_old = datetime.date(2020, month_end_old, int(day_end_old))
        monday = date_end_old + datetime.timedelta(days=2)
        saturday = date_end_old + datetime.timedelta(days=7)

        day_begin = monday.day
        day_end = saturday.day
        months_begin = my_months[monday.month % 12 - 1]
        months_end = my_months[saturday.month % 12 - 1]

        label = "Расписание занятий (с " + str(day_begin) + " " + months_begin + " по " + str(day_end) + " " + \
                months_end + ")"

        self.label_3.setText(label)
        self.set_defualt_timetable(monday, saturday)
        self.main_window.hide()
        self.main_window.show()

    def show_login_window(self):
        self.login_window.show()

    def show_subject_list_window(self):
        self.subject_list_window.show()

    def show_student_window(self):
        group = Group()
        ls_name = group.show_name(self.session)
        self.student_ui.comboBox.clear()
        self.student_ui.comboBox.addItems(ls_name)
        self.student_window.show()

    def show_timetable_window(self):
        self.timetable_ui.set_default_date()
        self.timetable_window.show()

    def open_grade_window(self):
        discipline = Discipline()
        d_name = discipline.show_name(self.session)
        self.grade_ui.comboBox.clear()
        self.grade_ui.comboBox.addItems(d_name)

        group = Group()
        ls_name = group.show_name(self.session)
        self.grade_ui.comboBox_2.clear()
        self.grade_ui.comboBox_2.addItems(ls_name)
        self.grade_window.show()

    def close_app(self):
        self.main_window.close()
