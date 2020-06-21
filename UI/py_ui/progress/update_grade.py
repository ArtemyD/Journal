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
import shutil

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from database.models import Grade, HistoryGrade
from settings import my_path_file
from transform.items import set_items_to_table


class UiUpdateGradeWindow(object):
    def __init__(self, main_window):
        self.group_number: str = ''
        self.discipline_name: str = ''
        self.session = main_window.session
        self.table = main_window.table
        self.id_grade: str = ''
        self.id_work: str = ''
        self.path_file: str = ''
        self.detail_grade_window = main_window.detail_grade_window
        self.update_grade_window = main_window.update_grade_window
        self.update_grade_window.setObjectName("MainWindow")
        self.update_grade_window.setFixedSize(552, 609)
        self.centralwidget = QtWidgets.QWidget(self.update_grade_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 58, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 58, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 58, 16))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 141, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 150, 271, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 180, 58, 16))
        self.label_5.setObjectName("label_5")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 200, 491, 301))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 510, 181, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.file_save)
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(310, 30, 211, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(320, 10, 58, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(320, 60, 58, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 30, 271, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 90, 271, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(230, 540, 141, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.update)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(370, 540, 141, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.close_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 540, 181, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(310, 80, 201, 111))
        self.textEdit_2.setObjectName("textEdit_2")
        self.update_grade_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_grade_window)
        self.statusbar.setObjectName("statusbar")
        self.update_grade_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_grade_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_grade_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Редактировать оценку"))
        self.label.setText(_translate("MainWindow", "Студент"))
        self.label_2.setText(_translate("MainWindow", "Работа"))
        self.label_4.setText(_translate("MainWindow", "Оценка (от 0 до 100)"))
        self.label_5.setText(_translate("MainWindow", "Отзыв"))
        self.pushButton.setText(_translate("MainWindow", "Прикрепленная работа"))
        self.label_6.setText(_translate("MainWindow", "Дата"))
        self.label_7.setText(_translate("MainWindow", "Заметка"))
        self.pushButton_3.setText(_translate("MainWindow", "Сохранить"))
        self.pushButton_4.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_2.setText(_translate("MainWindow", "Прикрепить работу"))

    def update(self):
        grade = Grade()
        value = self.lineEdit.text()
        date = self.dateEdit.date().getDate()
        new_date = str(date)
        feedback = self.textEdit.toPlainText()
        note = self.textEdit_2.toPlainText()
        grade.update(self.session, self.id_grade,  value, new_date, self.path_file, note, feedback)

        history = HistoryGrade()
        action = "Редактирование"
        date = self.dateEdit.date().currentDate().getDate()
        date = str(date)
        student = self.lineEdit_2.text()
        value = self.lineEdit.text()
        history.add(self.session, self.id_work, student, value, action, date)

        table_content: np.ndarray = grade.all(self.session, self.discipline_name, self.group_number)
        self.table = set_items_to_table(self.table, table_content)

        self.table.resizeColumnsToContents()
        self.detail_grade_window.close()
        self.update_grade_window.close()

    def file_save(self):
        try:
            name = QtWidgets.QFileDialog.getSaveFileName(self.update_grade_window, 'Save File', self.path_file)
            new_path = name[0]
            path = my_path_file + self.path_file
            shutil.copy(path, new_path)
        except:
            return

    def attach(self):
        try:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self.update_grade_window, "Выбрать файл", ".","")

            self.new_path_file = "attachments"
            copy_path = my_path_file + self.new_path_file
            shutil.copy(path, copy_path)

            p = path.split('/')
            self.new_path_file = self.new_path_file + '/' + p[-1]
            self.pushButton.setText("Прикреплено")

        except:
            return

    def close_window(self):
        self.update_grade_window.close()
