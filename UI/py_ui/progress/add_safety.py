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

from database.models import PassSafety, Safety
from transform.items import set_items_to_table


class UiAddSafetyWindow(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.group_number: str = ''
        self.discipline_name: str = ''
        self.table = main_window.tableWidget
        self.add_safety_window = main_window.add_safety_window
        self.add_safety_window.setObjectName("MainWindow")
        self.add_safety_window.setFixedSize(347, 147)
        self.centralwidget = QtWidgets.QWidget(self.add_safety_window)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 311, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 141, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 80, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.add_safety_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_safety_window)
        self.statusbar.setObjectName("statusbar")
        self.add_safety_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_safety_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_safety_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить тему инструктажа"))
        self.label.setText(_translate("MainWindow", "Тема инструктажа"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))

    def add(self):
        name: str = self.lineEdit.text()
        safety = Safety()
        safety.add(self.session, self.discipline_name, self.group_number, name)

        pass_safety = PassSafety()
        table_content: np.ndarray = pass_safety.all(self.session, self.discipline_name, self.group_number)
        self.table = set_items_to_table(self.table, table_content)

        table_header: list = safety.all_name(self.session, self.discipline_name, self.group_number, flag_header=True)
        self.table.setHorizontalHeaderLabels(table_header)

        self.table.resizeColumnsToContents()
        self.add_safety_window.close()
