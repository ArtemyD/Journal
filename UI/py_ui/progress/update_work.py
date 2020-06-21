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

from database.models import Grade, Work
from transform.items import set_items_to_table


class UiUpdateWorkWindow(object):
    def __init__(self, main_window):
        self.table = main_window.table
        self.id_work: int = 0
        self.session = main_window.session
        self.group_number: str = ''
        self.discipline_name: str = ''
        self.detail_work_window = main_window.detail_work_window
        self.update_work_window = main_window.update_work_window
        self.update_work_window.setObjectName("MainWindow")
        self.update_work_window.setFixedSize(622, 397)
        self.centralwidget = QtWidgets.QWidget(self.update_work_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 221, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 591, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 80, 251, 32))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 151, 16))
        self.label_2.setObjectName("label_2")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(300, 90, 261, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(300, 60, 211, 20))
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(460, 330, 151, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 230, 58, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 58, 16))
        self.label_4.setObjectName("label_4")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 150, 591, 74))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 250, 591, 74))
        self.textEdit_2.setObjectName("textEdit_2")
        self.update_work_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_work_window)
        self.statusbar.setObjectName("statusbar")
        self.update_work_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_work_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_work_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Редактировать работу"))
        self.label.setText(_translate("MainWindow", "Название работы"))
        self.label_2.setText(_translate("MainWindow", "Шкала оценок"))
        self.checkBox.setText(_translate("MainWindow", "Срок выполнения"))
        self.pushButton.setText(_translate("MainWindow", "Редактировать"))
        self.label_3.setText(_translate("MainWindow", "Заметка"))
        self.label_4.setText(_translate("MainWindow", "Задание"))

    def update(self):
        name = self.lineEdit.text()
        task = self.textEdit.toPlainText()
        note = self.textEdit_2.toPlainText()
        grade_scale = self.comboBox.currentText()

        date = self.dateEdit.date().getDate()
        new_date = str(date)
        isdeadline: bool = self.checkBox.isChecked()

        work = Work()
        work.update(self.session, self.id_work, name, task, note, grade_scale, new_date,isdeadline)

        grade = Grade()
        table_content: np.ndarray = grade.all(self.session, self.discipline_name, self.group_number)
        self.table = set_items_to_table(self.table, table_content)

        table_header: list = work.show_name(self.session, self.group_number, self.discipline_name, flag_header=True)
        self.table.setHorizontalHeaderLabels(table_header)

        self.table.resizeColumnsToContents()
        self.detail_work_window.close()
        self.update_work_window.close()
