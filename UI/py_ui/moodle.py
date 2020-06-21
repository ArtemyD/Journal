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
from imports.moodle import moodle_discipline, moodle_group, moodle_students
from PyQt5.QtWidgets import QMessageBox


class UiMoodleWindow(object):
    def __init__(self, main_window):
        self.session = main_window.session

        self.flag_discipline = False
        self.flag_group = False
        self.flag_student = False
        self.group_number = None

        self.moodle_window = main_window.moodle_window
        self.moodle_window.setObjectName("MainWindow")
        self.moodle_window.setFixedSize(570, 258)
        self.centralwidget = QtWidgets.QWidget(self.moodle_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 221, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 521, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 58, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 100, 521, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 58, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 160, 521, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 190, 201, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.import_moodle)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 190, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close)
        self.moodle_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.moodle_window)
        self.statusbar.setObjectName("statusbar")
        self.moodle_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.moodle_window)
        QtCore.QMetaObject.connectSlotsByName(self.moodle_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Импорт из Moodle"))
        self.label.setText(_translate("MainWindow", "Адрес панели входа"))
        self.label_2.setText(_translate("MainWindow", "Логин"))
        self.label_3.setText(_translate("MainWindow", "Пароль"))
        self.pushButton.setText(_translate("MainWindow", "Импортировать из Moodle"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))

    def import_moodle(self):
        address = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password_user = self.lineEdit_3.text()

        if self.flag_discipline == True:
            result = moodle_discipline(address, username, password_user, self.session)
        elif self.flag_group == True:
            result = moodle_group(address, username, password_user, self.session)
        elif self.flag_student == True:
            result = moodle_students(address, username, password_user, self.session, self.group_number)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        if not result:
            msg.setText("Импорт выполнен")
            msg.setInformativeText('Импорт данных из Moodle выполнен.')
            msg.setWindowTitle("Импорт выполнен")
            if self.flag_student == True:
                self.student_list_ui.update()

        else:
            msg.setText("Импорт не выполнен")
            msg.setInformativeText('Импорт данных из Moodle не выполнен.')
            msg.setWindowTitle("Импорт не выполнен")
        msg.exec_()
        self.moodle_window.close()

    def close(self):
        self.moodle_window.close()