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
from transform.items import set_items_to_table
import numpy as np
import datetime
from database.models import Occupation
from settings import my_months


class UiUpdateClass(object):
    def __init__(self, main_window):
        self.discipline_old = ""
        self.group_old = ''
        self.class_format_old = ''
        self.label_7 = main_window.label_7
        self.tableWidget = main_window.tableWidget
        self.tableWidget_2 = main_window.tableWidget_2
        self.tableWidget_3 = main_window.tableWidget_3
        self.tableWidget_4 = main_window.tableWidget_4
        self.tableWidget_5 = main_window.tableWidget_5
        self.tableWidget_6 = main_window.tableWidget_6
        self.timetable_window = main_window.timetable_window
        self.session = main_window.session
        self.update_class_window = main_window.update_class_window
        self.update_class_window.setObjectName("MainWindow")
        self.update_class_window.setFixedSize(327, 363)
        self.centralwidget = QtWidgets.QWidget(self.update_class_window)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 30, 301, 32))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 181, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 58, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(20, 90, 301, 32))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 58, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(20, 150, 301, 32))
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 190, 161, 16))
        self.label_4.setObjectName("label_4")
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(20, 210, 301, 32))
        self.comboBox_4.setObjectName("comboBox_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 250, 58, 16))
        self.label_5.setObjectName("label_5")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(30, 270, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 300, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.update_class_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_class_window)
        self.statusbar.setObjectName("statusbar")
        self.update_class_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_class_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_class_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Редактировать занятие"))
        self.label.setText(_translate("MainWindow", "Дисциплины"))
        self.label_2.setText(_translate("MainWindow", "Формат"))
        self.label_3.setText(_translate("MainWindow", "Группа"))
        self.label_4.setText(_translate("MainWindow", "Аудитория"))
        self.label_5.setText(_translate("MainWindow", "Время"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить"))

    def update(self):
        discipline = self.comboBox.currentText()
        group = self.comboBox_3.currentText()
        class_format = self.comboBox_2.currentText()
        audience = self.comboBox_4.currentText()

        o = Occupation()
        o.update(self.session, self.discipline_old, self.group_old, self.class_format_old, discipline, group,
                 class_format, audience)

        self.set_default_date()
        self.timetable_window.hide()
        self.timetable_window.show()
        self.update_class_window.close()

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