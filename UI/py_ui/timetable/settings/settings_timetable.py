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

from database.models import Audience, ClassFormat, Settings
from transform.items import set_items_to_table
from UI.py_ui.timetable.settings.add_semester import UiAddSemester
from UI.py_ui.timetable.settings.audience_list import UiAudienceList
from UI.py_ui.timetable.settings.training_formats_list import \
    UiTrainingFormatsList


class UiSettingsTimetableWindow(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.settings_timetable_window = main_window.settings_timetable_window
        self.settings_timetable_window.setObjectName("MainWindow")
        self.settings_timetable_window.setFixedSize(408, 183)
        self.centralwidget = QtWidgets.QWidget(self.settings_timetable_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 171, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_audience_list_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 40, 171, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_training_formats_list_window)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(200, 30, 201, 32))
        self.comboBox.setObjectName("comboBox")
        ls = ['1 неделя', '2 недели']
        self.comboBox.addItems(ls)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 10, 181, 16))
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 120, 112, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 70, 171, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.show_add_semester_window)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(200, 70, 201, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.save)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(180, 10, 20, 101))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 110, 381, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.settings_timetable_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.settings_timetable_window)
        self.statusbar.setObjectName("statusbar")
        self.settings_timetable_window.setStatusBar(self.statusbar)

        self.add_semester_window = QtWidgets.QMainWindow()
        self.add_semester_ui = UiAddSemester(self)

        self.audience_list_window = QtWidgets.QMainWindow()
        self.audience_list_ui = UiAudienceList(self)

        self.training_formats_list_window = QtWidgets.QMainWindow()
        self.training_formats_list_ui = UiTrainingFormatsList(self)

        self.retranslateUi(self.settings_timetable_window)
        QtCore.QMetaObject.connectSlotsByName(self.settings_timetable_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Параметры"))
        self.pushButton.setText(_translate("MainWindow", "Аудитории"))
        self.pushButton_2.setText(_translate("MainWindow", "Форматы занятий"))
        self.label.setText(_translate("MainWindow", "Формат расписания"))
        self.pushButton_3.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_4.setText(_translate("MainWindow", "Добавить семестр"))
        self.pushButton_5.setText(_translate("MainWindow", "Сохранить"))

    def show_add_semester_window(self):
        date_now = self.add_semester_ui.dateEdit.date().currentDate()
        self.add_semester_ui.dateEdit.setDate(date_now)
        self.add_semester_ui.dateEdit_2.setDate(date_now)
        self.add_semester_window.show()

    def show_audience_list_window(self):
        audience = Audience()
        ls_all = audience.show_all(self.session)
        ls_all = np.array(ls_all)
        self.audience_list_ui.tableWidget = set_items_to_table(self.audience_list_ui.tableWidget, ls_all)
        self.audience_list_ui.tableWidget.resizeColumnsToContents()
        self.audience_list_window.show()

    def show_training_formats_list_window(self):
        class_format = ClassFormat()
        ls_all = class_format.show_all(self.session)
        ls_all = np.array(ls_all)
        self.training_formats_list_ui.tableWidget = set_items_to_table(self.training_formats_list_ui.tableWidget, ls_all)
        self.training_formats_list_ui.tableWidget.resizeColumnsToContents()
        self.training_formats_list_window.show()

    def save(self):
        new_value = self.comboBox.currentIndex()
        s = Settings()
        s.set(self.session, new_value)
        self.settings_timetable_window.close()

    def close(self):
        self.settings_timetable_window.close()
