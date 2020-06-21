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

from database.models import Specialty


class UiUpdateSpecialty(object):
    def __init__(self, main_window):

        self.update_value: str = ''
        self.row: int = 0
        self.table = main_window.tableWidget

        self.session = main_window.session
        self.update_specialty_window = main_window.update_specialty_window
        self.update_specialty_window.setObjectName("MainWindow")
        self.update_specialty_window.setFixedSize(395, 202)
        self.centralwidget = QtWidgets.QWidget(self.update_specialty_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 151, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 351, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 141, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 90, 351, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(211, 130, 161, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.update_specialty_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_specialty_window)
        self.statusbar.setObjectName("statusbar")
        self.update_specialty_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_specialty_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_specialty_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить специальность"))
        self.label.setText(_translate("MainWindow", "Код специальности"))
        self.label_2.setText(_translate("MainWindow", "Наименование"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить"))

    def update(self):
        name = self.lineEdit_2.text()
        code = self.lineEdit.text()

        specialty = Specialty()
        specialty.update(self.session, self.update_value, code, name)

        self.table.setItem(self.row, 0, QtWidgets.QTableWidgetItem(code))
        self.table.setItem(self.row, 1, QtWidgets.QTableWidgetItem(name))

        self.update_specialty_window.close()
