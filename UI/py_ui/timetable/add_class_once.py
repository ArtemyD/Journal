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
from PyQt5 import QtCore, QtGui, QtWidgets

from database.models import Occupation
from settings import my_months
from transform.items import set_items_to_table


class UiAddClassOnceWindow(object):
    def __init__(self, main_window):
        self.label_7 = main_window.label_7
        self.tableWidget = main_window.tableWidget
        self.tableWidget_2 = main_window.tableWidget_2
        self.tableWidget_3 = main_window.tableWidget_3
        self.tableWidget_4 = main_window.tableWidget_4
        self.tableWidget_5 = main_window.tableWidget_5
        self.tableWidget_6 = main_window.tableWidget_6
        self.timetable_window = main_window.timetable_window
        self.session = main_window.session
        self.add_class_once_window = main_window.add_class_once_window
        self.add_class_once_window.setObjectName("MainWindow")
        self.add_class_once_window.setFixedSize(471, 257)
        self.centralwidget = QtWidgets.QWidget(self.add_class_once_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 70, 101, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 201, 32))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 111, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 90, 201, 32))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(10, 150, 201, 32))
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 101, 16))
        self.label_3.setObjectName("label_3")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(240, 100, 211, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(240, 80, 121, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(230, 190, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 190, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(240, 130, 171, 16))
        self.label_5.setObjectName("label_5")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(240, 150, 211, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(230, 30, 231, 32))
        self.comboBox_4.setObjectName("comboBox_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(240, 10, 58, 16))
        self.label_6.setObjectName("label_6")
        self.add_class_once_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_class_once_window)
        self.statusbar.setObjectName("statusbar")
        self.add_class_once_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_class_once_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_class_once_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить единичное занятие"))
        self.label.setText(_translate("MainWindow", "Формат"))
        self.label_2.setText(_translate("MainWindow", "Дисциплина"))
        self.label_3.setText(_translate("MainWindow", "Аудитория"))
        self.label_4.setText(_translate("MainWindow", "Дата занятия"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.label_5.setText(_translate("MainWindow", "Время начала занятия"))
        self.label_6.setText(_translate("MainWindow", "Группа"))

    def add(self):
        discipline = self.comboBox.currentText()
        format = self.comboBox_2.currentText()
        audience = self.comboBox_3.currentText()
        group = self.comboBox_4.currentText()
        date = self.dateEdit.date().getDate()
        time = self.timeEdit.time().toString()

        o = Occupation()
        o.add_once(self.session, discipline, format, audience, group, date, time)
        self.set_default_date()
        self.timetable_window.hide()
        self.timetable_window.show()
        self.add_class_once_window.close()

    def close(self):
        self.add_class_once_window.close()

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
        self.label_7.setText(label)
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
