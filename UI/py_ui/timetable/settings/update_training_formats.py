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

from database.models import ClassFormat


class UiUpdateTrainingFormats(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.table = main_window.tableWidget
        self.update_value = ''
        self.row = ''
        self.update_training_formats_window = main_window.update_training_formats_window
        self.update_training_formats_window.setObjectName("MainWindow")
        self.update_training_formats_window.setFixedSize(348, 120)
        self.centralwidget = QtWidgets.QWidget(self.update_training_formats_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 60, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 311, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 261, 16))
        self.label.setObjectName("label")
        self.update_training_formats_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_training_formats_window)
        self.statusbar.setObjectName("statusbar")
        self.update_training_formats_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_training_formats_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_training_formats_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Редактировать формат занятий"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить"))
        self.label.setText(_translate("MainWindow", "Наименование формата занятий"))

    def update(self):
        c = ClassFormat()
        name = self.lineEdit.text()

        c.update(self.session, self.update_value, name)

        self.table.setItem(self.row, 0, QtWidgets.QTableWidgetItem(name))
        self.table.resizeColumnsToContents()
        self.update_training_formats_window.close()
