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
from PyQt5 import QtCore, QtWidgets

from database.models import Discipline


class UiUpdateSubjectWindow(object):
    def __init__(self, main_window):
        self.update_value = ''
        self.session = main_window.session
        self.subject_list = main_window.listWidget
        self.update_subject_window = main_window.update_subject_window
        self.update_subject_window.setObjectName("MainWindow")
        self.update_subject_window.setFixedSize(504, 136)
        self.centralwidget = QtWidgets.QWidget(self.update_subject_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 471, 21))
        self.lineEdit.setObjectName("lineEdit")
        # self.lineEdit.setText(update_value)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 70, 181, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.update_subject7)
        self.update_subject_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_subject_window)
        self.statusbar.setObjectName("statusbar")
        self.update_subject_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_subject_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_subject_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Редактировать дисциплину"))
        self.label.setText(_translate("MainWindow", "Наименование"))
        self.pushButton_2.setText(_translate("MainWindow", "Сохранить изменения"))

    def update_subject7(self):
        name_of_subject = self.lineEdit.text()

        subject = Discipline()
        subject.update(self.session, self.update_value, name_of_subject)
        self.subject_list.addItem(name_of_subject)

        self.update_subject_window.close()
