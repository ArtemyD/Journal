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

from database.models import Student


class UiUpdateStudent(object):
    def __init__(self, main_window):
        self.row: int = 0
        self.table = main_window.tableWidget
        self.update_value: str = ''
        self.session = main_window.session
        self.update_student_window = main_window.update_student_window
        self.update_student_window.setObjectName("MainWindow")
        self.update_student_window.setFixedSize(386, 296)
        self.centralwidget = QtWidgets.QWidget(self.update_student_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 230, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 230, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 351, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 201, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 201, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 90, 351, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 150, 351, 74))
        self.textEdit.setObjectName("textEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 201, 16))
        self.label_4.setObjectName("label_4")
        self.update_student_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_student_window)
        self.statusbar.setObjectName("statusbar")
        self.update_student_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_student_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_student_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить студента"))
        self.pushButton.setText(_translate("MainWindow", "Обновить"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.label_2.setText(_translate("MainWindow", "ФИО студента"))
        self.label_3.setText(_translate("MainWindow", "Номер зачетной книжки"))
        self.label_4.setText(_translate("MainWindow", "Заметка"))

    def update(self):
        note = self.textEdit.toPlainText()
        number = self.lineEdit_2.text()
        fio = self.lineEdit.text()

        student = Student()
        student.update(self.session, self.update_value, fio, number, note)

        self.table.setItem(self.row, 0, QtWidgets.QTableWidgetItem(fio))
        self.table.setItem(self.row, 1, QtWidgets.QTableWidgetItem(number))
        self.table.setItem(self.row, 2, QtWidgets.QTableWidgetItem(note))
        self.table.resizeColumnsToContents()

        self.update_student_window.close()

    def close_window(self):
        self.update_student_window.close()
