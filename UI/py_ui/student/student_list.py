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
import csv
import numpy as np

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from transform.items import set_items_to_table

from database.models import Student
from UI.py_ui.student.add_student import UiAddStudentWindow
from UI.py_ui.student.update_student import UiUpdateStudent
from UI.py_ui.moodle import UiMoodleWindow


class UiStudentListWindow(object):
    def __init__(self, main_window):
        self.group_number: str = ''
        self.session = main_window.session
        self.student_list_window = main_window.student_list_window
        self.student_list_window.setObjectName("MainWindow")
        self.student_list_window.setFixedSize(661, 456)
        self.centralwidget = QtWidgets.QWidget(self.student_list_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 241, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 360, 141, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_update_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 390, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 631, 321))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["ФИО", "Номер зачетной книжки", "Заметка"])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 360, 112, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_add_student_window)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(270, 360, 141, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.delete)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(130, 390, 141, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.import_csv)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(270, 390, 141, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.import_moodle)
        self.student_list_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.student_list_window)
        self.statusbar.setObjectName("statusbar")
        self.student_list_window.setStatusBar(self.statusbar)

        self.add_student_window = QtWidgets.QMainWindow()
        self.add_student_ui = UiAddStudentWindow(self)

        self.update_student_window = QtWidgets.QMainWindow()
        self.update_student_ui = UiUpdateStudent(self)

        self.moodle_window = QtWidgets.QMainWindow()
        self.moodle_ui = UiMoodleWindow(self)

        self.retranslateUi(self.student_list_window)
        QtCore.QMetaObject.connectSlotsByName(self.student_list_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Список группы"))
        self.label.setText(_translate("MainWindow", "Список группы: № 345675"))
        self.pushButton.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_3.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_5.setText(_translate("MainWindow", "Импорт из .csv"))
        self.pushButton_6.setText(_translate("MainWindow", "Импорт из Moodle"))

    def show_add_student_window(self):
        self.add_student_ui.group_number = self.group_number
        self.add_student_window.show()

    def show_update_window(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            row = self.tableWidget.row(i)

            fio = self.tableWidget.item(row, 0).text()
            number = self.tableWidget.item(row, 1).text()
            note = self.tableWidget.item(row, 2).text()

            self.update_student_ui.lineEdit.setText(fio)
            self.update_student_ui.lineEdit_2.setText(number)
            self.update_student_ui.textEdit.setText(note)
            self.update_student_ui.update_value = number
            self.update_student_ui.row = row
            self.update_student_window.show()
            break

    def delete(self):
        items = self.tableWidget.selectedItems()
        for i in items:
            row = self.tableWidget.row(i)
            number = self.tableWidget.item(row, 1).text()

            student = Student()
            student.delete(self.session, number)

            self.tableWidget.removeRow(row)

    def close_window(self):
        self.tableWidget.setRowCount(0)
        self.student_list_window.close()

    def import_csv(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        try:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self.student_list_window, "Open Image", ".",
                                                            "Image Files (*.csv)")

            with open(path, "r") as f_obj:
                reader = csv.reader(f_obj)
                student = Student()
                students = student.show_name(self.session, self.group_number)

                for row in reader:
                    fio = row[0]
                    number = row[1]
                    note = row[2]
                    flag_s = 0
                    for s in students:
                        if fio == s:
                            flag_s = 1
                            break

                    if flag_s == 0:
                        student.add(self.session, fio, number, note, self.group_number)
                        number_row = self.tableWidget.rowCount()
                        self.tableWidget.setRowCount(number_row + 1)
                        self.tableWidget.setItem(number_row, 0, QtWidgets.QTableWidgetItem(fio))
                        self.tableWidget.setItem(number_row, 1, QtWidgets.QTableWidgetItem(str(number)))
                        self.tableWidget.setItem(number_row, 2, QtWidgets.QTableWidgetItem(str(note)))
                        self.tableWidget.resizeColumnsToContents()

            msg.setText("Импорт выполнен")
            msg.setInformativeText('Импорт данных из CSV выполнен.')
            msg.setWindowTitle("Импорт выполнен")

        except:
            msg.setText("Импорт не выполнен")
            msg.setInformativeText('Импорт данных из CSV не выполнен.')
            msg.setWindowTitle("Импорт не выполнен")
        msg.exec_()

    def import_moodle(self):
        self.moodle_ui.flag_discipline = False
        self.moodle_ui.flag_group = False
        self.moodle_ui.flag_student = True
        self.moodle_ui.group_number = self.group_number
        self.moodle_ui.student_list_ui = self
        self.moodle_window.show()

    def update(self):
        student = Student()
        group_number: str = self.group_number
        ls_all: list = student.show_all(self.session, group_number)
        ls_all: np.ndarray = np.array(ls_all)
        self.tableWidget = set_items_to_table(self.tableWidget, ls_all)
        self.tableWidget.resizeColumnsToContents()
        self.label.setText("Список группы: №" + str(group_number))
        self.group_number = str(group_number)

