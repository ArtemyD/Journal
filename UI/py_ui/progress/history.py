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


class UiHistoryWindow(object):
    def __init__(self, main_window):
        self.history_window = main_window.history_window
        self.history_window.setObjectName("MainWindow")
        self.history_window.setFixedSize(800, 609)
        self.centralwidget = QtWidgets.QWidget(self.history_window)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 771, 521))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ФИО студента", "Название работы", "Тип изменения", "Дата изменения", "Оценка"])
        self.tableWidget.setRowCount(0)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(670, 540, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)
        self.history_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.history_window)
        self.statusbar.setObjectName("statusbar")
        self.history_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.history_window)
        QtCore.QMetaObject.connectSlotsByName(self.history_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "История изменения оценок"))
        self.pushButton.setText(_translate("MainWindow", "Закрыть"))

    def close_window(self):
        self.history_window.close()
