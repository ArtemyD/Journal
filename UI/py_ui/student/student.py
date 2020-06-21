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

from database.models import Group, Student
from transform.items import set_items_to_table
from UI.py_ui.student.group_list import UiGroupListWindow
from UI.py_ui.student.specialty_list import UiSpecialtyListWindow
from UI.py_ui.student.student_list import UiStudentListWindow


class UiStudentWindow(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.student_window = main_window.student_window
        self.student_window.setObjectName("MainWindow")
        self.student_window.setFixedSize(510, 239)
        self.centralwidget = QtWidgets.QWidget(self.student_window)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 90, 241, 32))
        self.comboBox.setObjectName("comboBox")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 70, 141, 16))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 170, 141, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 90, 241, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_student_list_window)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 10, 151, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_specialty_list_window)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 10, 151, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.show_group_list_window)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 50, 491, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 150, 491, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.student_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.student_window)
        self.statusbar.setObjectName("statusbar")
        self.student_window.setStatusBar(self.statusbar)

        self.student_list_window = QtWidgets.QMainWindow()
        self.student_list_ui = UiStudentListWindow(self)

        self.specialty_list_window = QtWidgets.QMainWindow()
        self.specialty_list_ui = UiSpecialtyListWindow(self)

        self.group_list_window = QtWidgets.QMainWindow()
        self.group_list_ui = UiGroupListWindow(self)

        self.retranslateUi(self.student_window)
        QtCore.QMetaObject.connectSlotsByName(self.student_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Студенты"))
        self.label.setText(_translate("MainWindow", "Выберите группу"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_3.setText(_translate("MainWindow", "Просмотреть список группы"))
        self.pushButton.setText(_translate("MainWindow", "Специальности"))
        self.pushButton_4.setText(_translate("MainWindow", "Группы"))

    def show_student_list_window(self):
        student = Student()
        group_number: str = self.comboBox.currentText()
        ls_all: list = student.show_all(self.session, group_number)
        ls_all: np.ndarray = np.array(ls_all)
        self.student_list_ui.tableWidget = set_items_to_table(self.student_list_ui.tableWidget, ls_all)
        self.student_list_ui.tableWidget.resizeColumnsToContents()
        self.student_list_ui.label.setText("Список группы: №" + str(group_number))
        self.student_list_ui.group_number = str(group_number)
        self.student_list_window.show()

    def show_specialty_list_window(self):
        self.specialty_list_window.show()

    def show_group_list_window(self):
        group = Group()
        ls_all = group.show_all(self.session)
        ls_all = np.array(ls_all)
        self.group_list_ui.tableWidget = set_items_to_table(self.group_list_ui.tableWidget, ls_all)
        self.group_list_ui.tableWidget.resizeColumnsToContents()
        self.group_list_window.show()

    def close_window(self):
        self.student_window.close()
