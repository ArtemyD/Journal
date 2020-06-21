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

from database.models import Discipline


class UiAddSubjectWindow(object):
    def __init__(self, main_window):
        self.subject_list = main_window.listWidget
        self.session = main_window.session

        self.add_subject_window = main_window.add_subject_window
        self.add_subject_window.setObjectName("MainWindow")
        self.add_subject_window.setFixedSize(504, 136)
        self.centralwidget = QtWidgets.QWidget(self.add_subject_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 471, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 70, 131, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.add_subject)
        self.add_subject_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_subject_window)
        self.statusbar.setObjectName("statusbar")
        self.add_subject_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_subject_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_subject_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить дисциплину"))
        self.label.setText(_translate("MainWindow", "Наименование"))
        self.pushButton_2.setText(_translate("MainWindow", "Добавить"))

    def add_subject(self):
        name_of_subject = self.lineEdit.text()

        subject = Discipline()
        subject.add(self.session, name_of_subject)
        self.subject_list.addItem(name_of_subject)

        self.add_subject_window.close()
