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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from database.models import Group
from database.models import Specialty
from UI.py_ui.student.add_group import UiAddGroupWindow
from UI.py_ui.student.update_group import UiUpdateGroup
from UI.py_ui.moodle import UiMoodleWindow


class UiGroupListWindow(object):
    def __init__(self, main_window):
        self.combo = main_window.comboBox
        self.session = main_window.session
        self.group_list_window = main_window.group_list_window
        self.group_list_window.setObjectName("MainWindow")
        self.group_list_window.setFixedSize(661, 456)
        self.centralwidget = QtWidgets.QWidget(self.group_list_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 360, 141, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 390, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 631, 341))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Специальность", "Номер", "Заметка"])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 360, 112, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_add_group_window)
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
        self.group_list_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.group_list_window)
        self.statusbar.setObjectName("statusbar")
        self.group_list_window.setStatusBar(self.statusbar)

        self.add_group_window = QtWidgets.QMainWindow()
        self.add_group_ui = UiAddGroupWindow(self)

        self.update_group_window = QtWidgets.QMainWindow()
        self.update_group_ui = UiUpdateGroup(self)

        self.moodle_window = QtWidgets.QMainWindow()
        self.moodle_ui = UiMoodleWindow(self)

        self.retranslateUi(self.group_list_window)
        QtCore.QMetaObject.connectSlotsByName(self.group_list_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Список группы"))
        self.pushButton.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_3.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_5.setText(_translate("MainWindow", "Импорт из .csv"))
        self.pushButton_6.setText(_translate("MainWindow", "Импорт из Moodle"))

    def show_add_group_window(self):
        specialty = Specialty()
        ls_name = specialty.show_name(self.session)
        self.add_group_ui.comboBox.clear()
        self.add_group_ui.comboBox.addItems(ls_name)
        self.add_group_window.show()

    def delete(self):
        items = self.tableWidget.selectedItems()
        for i in items:
            row = self.tableWidget.row(i)
            number = self.tableWidget.item(row, 1).text()

            group = Group()
            group.delete(self.session, number)

            self.tableWidget.removeRow(row)
            self.combo.clear()
            ls_name = group.show_name(self.session)
            self.combo.addItems(ls_name)

    def update(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            row = self.tableWidget.row(i)

            specialty = self.tableWidget.item(row, 0).text()
            number = self.tableWidget.item(row, 1).text()
            note = self.tableWidget.item(row, 2).text()

            self.update_group_ui.lineEdit.setText(number)
            self.update_group_ui.textEdit.setText(note)

            s = Specialty()
            ls_name = s.show_name(self.session)
            self.update_group_ui.comboBox.addItems(ls_name)
            current_index = ls_name.index(specialty)
            self.update_group_ui.comboBox.setCurrentIndex(current_index)

            self.update_group_ui.update_value = number
            self.update_group_ui.row = row

            self.update_group_window.show()
            break

    def close_window(self):
        self.group_list_window.close()

    def import_csv(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        try:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self.group_list_window, "Open Image", ".",
                                                            "Image Files (*.csv)")

            with open(path, "r") as f_obj:
                reader = csv.reader(f_obj)
                group = Group()
                groups = group.show_name(self.session)

                for row in reader:
                    specialty = row[0]
                    number = row[1]
                    note = row[2]
                    flag_g = 0
                    for g in groups:
                        if number == g:
                            flag_g = 1
                            break

                    if flag_g == 0:
                        group.add(self.session, number, note, specialty)
                        number_row = self.tableWidget.rowCount()
                        self.tableWidget.setRowCount(number_row + 1)
                        self.tableWidget.setItem(number_row, 0, QtWidgets.QTableWidgetItem(specialty))
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
        self.moodle_ui.flag_group = True
        self.moodle_ui.flag_student = False
        self.moodle_window.show()