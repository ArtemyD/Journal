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

from database.models import (Audience, ClassFormat, Discipline, Group,
                             Occupation, Settings)
from settings import my_months
from transform.items import set_items_to_table
from UI.py_ui.timetable.add_class import UiAddClassWindow
from UI.py_ui.timetable.add_class_once import UiAddClassOnceWindow
from UI.py_ui.timetable.settings.settings_timetable import \
    UiSettingsTimetableWindow
from UI.py_ui.timetable.update_class import UiUpdateClass


class UiTimetableWindow(object):
    def __init__(self, main_window):
        self.label_3_main = main_window.label_3
        self.tableWidget_main = main_window.tableWidget
        self.tableWidget_2_main = main_window.tableWidget_2
        self.tableWidget_3_main = main_window.tableWidget_3
        self.tableWidget_4_main = main_window.tableWidget_4
        self.tableWidget_5_main = main_window.tableWidget_5
        self.tableWidget_6_main = main_window.tableWidget_6
        self.timetable_window = main_window.timetable_window

        self.session = main_window.session
        self.timetable_window = main_window.timetable_window
        self.timetable_window.setObjectName("MainWindow")
        self.timetable_window.setFixedSize(943, 622)
        self.centralwidget = QtWidgets.QWidget(self.timetable_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 150, 921, 421))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.tableWidget_4 = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(5)
        self.tableWidget_4.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_4.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_4, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_2.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_2, 1, 1, 1, 1)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_3.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_3, 1, 2, 1, 1)
        self.tableWidget_5 = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(5)
        self.tableWidget_5.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_5.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_5, 3, 1, 1, 1)
        self.tableWidget_6 = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget_6.setObjectName("tableWidget_6")
        self.tableWidget_6.setColumnCount(5)
        self.tableWidget_6.setHorizontalHeaderLabels(["Время", "Дисциплина", "Формат", "Группа", "Аудитория"])
        self.tableWidget_6.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget_6, 3, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 40, 241, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_add_class_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 10, 241, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_add_class_once_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(250, 10, 151, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_update_window)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(770, 10, 161, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.show_settings_timetable_window)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 271, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(600, 110, 171, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.previous_week)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(770, 110, 161, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.next_week)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(820, 580, 112, 32))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.close)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(250, 40, 151, 32))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.delete)
        self.timetable_window.setCentralWidget(self.centralwidget)

        self.settings_timetable_window = QtWidgets.QMainWindow()
        self.settings_timetable_ui = UiSettingsTimetableWindow(self)

        self.add_class_window = QtWidgets.QMainWindow()
        self.add_class_ui = UiAddClassWindow(self)

        self.update_class_window = QtWidgets.QMainWindow()
        self.update_class_ui = UiUpdateClass(self)

        self.add_class_once_window = QtWidgets.QMainWindow()
        self.add_class_once_ui = UiAddClassOnceWindow(self)

        self.retranslateUi(self.timetable_window)
        QtCore.QMetaObject.connectSlotsByName(self.timetable_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Расписание"))
        self.label_3.setText(_translate("MainWindow", "Вторник"))
        self.label_2.setText(_translate("MainWindow", "Четверг"))
        self.label.setText(_translate("MainWindow", "Понедельник"))
        self.label_4.setText(_translate("MainWindow", "Среда"))
        self.label_5.setText(_translate("MainWindow", "Пятница"))
        self.label_6.setText(_translate("MainWindow", "Суббота"))
        self.pushButton.setText(_translate("MainWindow", "Добавить периодичное занятие"))
        self.pushButton_2.setText(_translate("MainWindow", "Добавить единичное занятие"))
        self.pushButton_3.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_4.setText(_translate("MainWindow", "Параметры"))
        self.label_7.setText(_translate("MainWindow", "Расписание с 1 по 6 февраля"))
        self.pushButton_5.setText(_translate("MainWindow", "Предыдущая неделя"))
        self.pushButton_6.setText(_translate("MainWindow", "Следующая неделя"))
        self.pushButton_7.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_8.setText(_translate("MainWindow", "Удалить"))

    def show_settings_timetable_window(self):
        s = Settings()
        schedule_format = s.get(self.session)
        self.settings_timetable_ui.comboBox.setCurrentIndex(int(schedule_format))
        self.settings_timetable_window.show()

    def show_add_class_window(self):
        discipline = Discipline()
        d_name = discipline.show_name(self.session)
        self.add_class_ui.comboBox.clear()
        self.add_class_ui.comboBox.addItems(d_name)

        group = Group()
        ls_name = group.show_name(self.session)
        self.add_class_ui.comboBox_6.clear()
        self.add_class_ui.comboBox_6.addItems(ls_name)

        c = ClassFormat()
        c_name = c.show_name(self.session)
        self.add_class_ui.comboBox_2.clear()
        self.add_class_ui.comboBox_2.addItems(c_name)

        a = Audience()
        a_name = a.show_name(self.session)
        self.add_class_ui.comboBox_5.clear()
        self.add_class_ui.comboBox_5.addItems(a_name)

        s = Settings()
        schedule_format = s.get(self.session)
        if schedule_format == 0:
            s_name = ['Каждую неделю']
        else:
            s_name = ['Каждую неделю', '1-ая неделя', '2-ая неделя']
        self.add_class_ui.comboBox_4.clear()
        self.add_class_ui.comboBox_4.addItems(s_name)

        date_now = self.add_class_ui.dateEdit.date().currentDate()
        self.add_class_ui.dateEdit.setDate(date_now)
        self.add_class_ui.dateEdit_2.setDate(date_now)
        time_now = self.add_class_ui.timeEdit.time().currentTime()
        self.add_class_ui.timeEdit.setTime(time_now)

        self.add_class_window.show()

    def show_add_class_once_window(self):
        discipline = Discipline()
        d_name = discipline.show_name(self.session)
        self.add_class_once_ui.comboBox.clear()
        self.add_class_once_ui.comboBox.addItems(d_name)

        c = ClassFormat()
        c_name = c.show_name(self.session)
        self.add_class_once_ui.comboBox_2.clear()
        self.add_class_once_ui.comboBox_2.addItems(c_name)

        group = Group()
        ls_name = group.show_name(self.session)
        self.add_class_once_ui.comboBox_4.clear()
        self.add_class_once_ui.comboBox_4.addItems(ls_name)

        a = Audience()
        a_name = a.show_name(self.session)
        self.add_class_once_ui.comboBox_3.clear()
        self.add_class_once_ui.comboBox_3.addItems(a_name)

        date_now = self.add_class_once_ui.dateEdit.date().currentDate()
        self.add_class_once_ui.dateEdit.setDate(date_now)
        time_now = self.add_class_once_ui.timeEdit.time().currentTime()
        self.add_class_once_ui.timeEdit.setTime(time_now)

        self.add_class_once_window.show()

    def close(self):
        self.set_default_date_main_window()
        self.timetable_window.close()

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

    def previous_week(self):
        pre_label = self.label_7.text()
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

        self.label_7.setText(label)
        self.set_defualt_timetable(monday, saturday)
        self.timetable_window.hide()
        self.timetable_window.show()

    def next_week(self):
        pre_label = self.label_7.text()
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

        self.label_7.setText(label)
        self.set_defualt_timetable(monday, saturday)
        self.timetable_window.hide()
        self.timetable_window.show()

    def show_update_window(self):
        discipline = Discipline()
        d_name = discipline.show_name(self.session)
        self.update_class_ui.comboBox.clear()
        self.update_class_ui.comboBox.addItems(d_name)

        group = Group()
        ls_name = group.show_name(self.session)
        self.update_class_ui.comboBox_3.clear()
        self.update_class_ui.comboBox_3.addItems(ls_name)

        c = ClassFormat()
        c_name = c.show_name(self.session)
        self.update_class_ui.comboBox_2.clear()
        self.update_class_ui.comboBox_2.addItems(c_name)

        a = Audience()
        a_name = a.show_name(self.session)
        self.update_class_ui.comboBox_4.clear()
        self.update_class_ui.comboBox_4.addItems(a_name)

        items_1 = self.tableWidget.selectedItems()
        items_2 = self.tableWidget_2.selectedItems()
        items_3 = self.tableWidget_3.selectedItems()
        items_4 = self.tableWidget_4.selectedItems()
        items_5 = self.tableWidget_5.selectedItems()
        items_6 = self.tableWidget_6.selectedItems()

        for i in items_1:
            row = self.tableWidget.row(i)
            time_item = self.tableWidget.item(row, 0).text()
            discipline = self.tableWidget.item(row, 1).text()
            group = self.tableWidget.item(row, 3).text()
            o = Occupation
            update_value = o.get(self.session, time_item, discipline, group)

        for i in items_2:
            row = self.tableWidget_2.row(i)
            time_item = self.tableWidget_2.item(row, 0).text()
            discipline = self.tableWidget_2.item(row, 1).text()
            group = self.tableWidget_2.item(row, 3).text()
            o = Occupation
            update_value = o.get(self.session, time_item, discipline, group)

        for i in items_3:
            row = self.tableWidget_3.row(i)
            time_item = self.tableWidget_3.item(row, 0).text()
            discipline = self.tableWidget_3.item(row, 1).text()
            group = self.tableWidget_3.item(row, 3).text()
            o = Occupation
            update_value = o.get(self.session, time_item, discipline, group)

        for i in items_4:
            row = self.tableWidget_4.row(i)
            time_item = self.tableWidget_4.item(row, 0).text()
            discipline = self.tableWidget_4.item(row, 1).text()
            group = self.tableWidget_4.item(row, 3).text()
            o = Occupation
            update_value = o.get(self.session, time_item, discipline, group)

        for i in items_5:
            row = self.tableWidget_5.row(i)
            time_item = self.tableWidget_5.item(row, 0).text()
            discipline = self.tableWidget_5.item(row, 1).text()
            group = self.tableWidget_5.item(row, 3).text()
            o = Occupation
            update_value = o.get(self.session, time_item, discipline, group)

        for i in items_6:
            row = self.tableWidget_6.row(i)
            time_item = self.tableWidget_6.item(row, 0).text()
            discipline = self.tableWidget_6.item(row, 1).text()
            group = self.tableWidget_6.item(row, 3).text()
            o = Occupation
            update_value = o.get(self.session, time_item, discipline, group)

        try:
            discipline = update_value.discipline.name
            self.update_class_ui.discipline_old = discipline
            index = self.update_class_ui.comboBox.findText(discipline)
            self.update_class_ui.comboBox.setCurrentIndex(index)

            class_format = update_value.class_format.name
            self.update_class_ui.class_format_old = class_format
            index = self.update_class_ui.comboBox_2.findText(class_format)
            self.update_class_ui.comboBox_2.setCurrentIndex(index)

            group = update_value.group.number
            self.update_class_ui.group_old = group
            index = self.update_class_ui.comboBox_3.findText(group)
            self.update_class_ui.comboBox_3.setCurrentIndex(index)

            audience = update_value.audience.corps + " " + update_value.audience.number
            index = self.update_class_ui.comboBox_4.findText(audience)
            self.update_class_ui.comboBox_4.setCurrentIndex(index)

            format = '%H:%M'
            time = datetime.datetime.strptime(time_item, format).time()
            self.update_class_ui.timeEdit.setTime(time)

        except:
            return


        self.update_class_window.show()

    def delete(self):
        items_1 = self.tableWidget.selectedItems()
        items_2 = self.tableWidget_2.selectedItems()
        items_3 = self.tableWidget_3.selectedItems()
        items_4 = self.tableWidget_4.selectedItems()
        items_5 = self.tableWidget_5.selectedItems()
        items_6 = self.tableWidget_6.selectedItems()

        for i in items_1:
            row = self.tableWidget.row(i)
            time = self.tableWidget.item(row, 0).text()
            discipline = self.tableWidget.item(row, 1).text()
            group = self.tableWidget.item(row, 3).text()
            o = Occupation
            o.delete(self.session, time, discipline, group)
            self.tableWidget.removeRow(row)
            return

        for i in items_2:
            row = self.tableWidget_2.row(i)
            time = self.tableWidget_2.item(row, 0).text()
            discipline = self.tableWidget_2.item(row, 1).text()
            group = self.tableWidget_2.item(row, 3).text()
            o = Occupation
            o.delete(self.session, time, discipline, group)
            self.tableWidget_2.removeRow(row)
            return

        for i in items_3:
            row = self.tableWidget_3.row(i)
            time = self.tableWidget_3.item(row, 0).text()
            discipline = self.tableWidget_3.item(row, 1).text()
            group = self.tableWidget_3.item(row, 3).text()
            o = Occupation
            o.delete(self.session, time, discipline, group)
            self.tableWidget_3.removeRow(row)
            return

        for i in items_4:
            row = self.tableWidget_4.row(i)
            time = self.tableWidget_4.item(row, 0).text()
            discipline = self.tableWidget_4.item(row, 1).text()
            group = self.tableWidget_4.item(row, 3).text()
            o = Occupation
            o.delete(self.session, time, discipline, group)
            self.tableWidget_4.removeRow(row)
            return

        for i in items_5:
            row = self.tableWidget_5.row(i)
            time = self.tableWidget_5.item(row, 0).text()
            discipline = self.tableWidget_5.item(row, 1).text()
            group = self.tableWidget_5.item(row, 3).text()
            o = Occupation
            o.delete(self.session, time, discipline, group)
            self.tableWidget_5.removeRow(row)
            return

        for i in items_6:
            row = self.tableWidget_6.row(i)
            time = self.tableWidget_6.item(row, 0).text()
            discipline = self.tableWidget_6.item(row, 1).text()
            group = self.tableWidget_6.item(row, 3).text()
            o = Occupation
            o.delete(self.session, time, discipline, group)
            self.tableWidget_6.removeRow(row)
            return

    def set_default_date_main_window(self):
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
        self.label_3_main.setText(label)
        self.set_defualt_timetable_main_window(monday, saturday)

    def set_defualt_timetable_main_window(self, monday, saturday):
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
        self.tableWidget_main.setRowCount(0)
        self.tableWidget_main = set_items_to_table(self.tableWidget_main, monday_ls)
        self.tableWidget_main.resizeColumnsToContents()

        tuesday_ls = np.array(tuesday_ls)
        self.tableWidget_2_main.setRowCount(0)
        self.tableWidget_2_main = set_items_to_table(self.tableWidget_2_main, tuesday_ls)
        self.tableWidget_2_main.resizeColumnsToContents()

        wednesday_ls = np.array(wednesday_ls)
        self.tableWidget_3_main.setRowCount(0)
        self.tableWidget_3_main = set_items_to_table(self.tableWidget_3_main, wednesday_ls)
        self.tableWidget_3_main.resizeColumnsToContents()

        thursday_ls = np.array(thursday_ls)
        self.tableWidget_4_main.setRowCount(0)
        self.tableWidget_4_main = set_items_to_table(self.tableWidget_4_main, thursday_ls)
        self.tableWidget_4_main.resizeColumnsToContents()

        friday_ls = np.array(friday_ls)
        self.tableWidget_5_main.setRowCount(0)
        self.tableWidget_5_main = set_items_to_table(self.tableWidget_5_main, friday_ls)
        self.tableWidget_5_main.resizeColumnsToContents()

        saturday_ls = np.array(saturday_ls)
        self.tableWidget_6_main.setRowCount(0)
        self.tableWidget_6_main = set_items_to_table(self.tableWidget_6_main, saturday_ls)
        self.tableWidget_6_main.resizeColumnsToContents()