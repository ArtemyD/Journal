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

from database.models import ScheduledDay


class UiAddSemester(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.add_semester_window = main_window.add_semester_window
        self.add_semester_window .setObjectName("MainWindow")
        self.add_semester_window .setFixedSize(250, 186)
        self.centralwidget = QtWidgets.QWidget(self.add_semester_window )
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 120, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 120, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close)
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(10, 30, 231, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(10, 80, 231, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 231, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label_2.setObjectName("label_2")
        self.add_semester_window .setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_semester_window )
        self.statusbar.setObjectName("statusbar")
        self.add_semester_window .setStatusBar(self.statusbar)

        self.retranslateUi(self.add_semester_window )
        QtCore.QMetaObject.connectSlotsByName(self.add_semester_window )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить семестр"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.label.setText(_translate("MainWindow", "Конец семестра"))
        self.label_2.setText(_translate("MainWindow", "Начало семестра"))

    def add(self):
        date_begin = self.dateEdit.date().getDate()
        date_end = self.dateEdit_2.date().getDate()
        date_begin = str(date_begin)
        date_end = str(date_end)

        s = ScheduledDay()
        s.add_day_from_period(self.session, date_begin, date_end)
        self.add_semester_window.close()

    def close(self):
        self.add_semester_window.close()
