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

from database.models import Group


class UiAddGroupWindow(object):
    def __init__(self, main_window):
        self.combo = main_window.combo
        self.table = main_window.tableWidget
        self.session = main_window.session
        self.add_group_window = main_window.add_group_window
        self.add_group_window.setObjectName("MainWindow")
        self.add_group_window.setFixedSize(338, 302)
        self.centralwidget = QtWidgets.QWidget(self.add_group_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 70, 131, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 90, 311, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 230, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 230, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 131, 16))
        self.label_2.setObjectName("label_2")

        # Специальности
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(0, 30, 331, 32))
        self.comboBox.setObjectName("comboBox")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 58, 16))
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 140, 311, 74))
        self.textEdit.setObjectName("textEdit")
        self.add_group_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_group_window)
        self.statusbar.setObjectName("statusbar")
        self.add_group_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_group_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_group_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить группу"))
        self.label.setText(_translate("MainWindow", "Номер группы"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.label_2.setText(_translate("MainWindow", "Специальность"))
        self.label_3.setText(_translate("MainWindow", "Заметка"))

    def add(self):
        number = self.lineEdit.text()
        note = self.textEdit.toPlainText()
        spec: str = self.comboBox.currentText()

        group = Group()
        group.add(self.session, number, note, spec)

        row = self.table.rowCount()

        self.table.setRowCount(row + 1)
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(spec))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(number))
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(note))

        self.combo.addItem(number)

        self.add_group_window.close()

    def close_window(self):
        self.add_group_window.close()
