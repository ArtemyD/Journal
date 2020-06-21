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

from database.models import ClassFormat
from transform.items import set_items_to_table


class UiAddTrainingFormats(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.table = main_window.tableWidget
        self.add_training_formats_window = main_window.add_training_formats_window
        self.add_training_formats_window.setObjectName("MainWindow")
        self.add_training_formats_window.setFixedSize(348, 120)
        self.centralwidget = QtWidgets.QWidget(self.add_training_formats_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 60, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 311, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 261, 16))
        self.label.setObjectName("label")
        self.add_training_formats_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_training_formats_window)
        self.statusbar.setObjectName("statusbar")
        self.add_training_formats_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_training_formats_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_training_formats_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить формат занятий"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.label.setText(_translate("MainWindow", "Наименование формата занятий"))

    def add(self):
        class_format = ClassFormat()
        name = self.lineEdit.text()
        class_format.add(self.session, name)

        ls_all = class_format.show_all(self.session)
        ls_all = np.array(ls_all)
        self.table = set_items_to_table(self.table, ls_all)
        self.table.resizeColumnsToContents()
        self.add_training_formats_window.close()
