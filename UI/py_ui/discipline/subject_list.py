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
import csv

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from database.models import Discipline
from transform.query import query_to_list_of_name
from UI.py_ui.discipline.add_subject import UiAddSubjectWindow
from UI.py_ui.discipline.update_subject import UiUpdateSubjectWindow
from UI.py_ui.moodle import UiMoodleWindow


class UiSubjectList(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.subject_list_window = main_window.subject_list_window
        self.subject_list_window.setObjectName("MainWindow")
        self.subject_list_window.setFixedSize(700, 375)
        self.centralwidget = QtWidgets.QWidget(self.subject_list_window)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 681, 231))
        self.listWidget.setObjectName("listWidget")
        subject = Discipline()
        query_list = subject.show_all(self.session)
        ls = query_to_list_of_name(query_list)
        self.listWidget.addItems(ls)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 171, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 280, 151, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_add_subject_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 280, 151, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.update_subject)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(540, 310, 151, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.close_window)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(310, 280, 151, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.delete_subject)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(161, 310, 151, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.import_csv)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(310, 310, 151, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.import_moodle)
        self.subject_list_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.subject_list_window)
        self.statusbar.setObjectName("statusbar")
        self.subject_list_window.setStatusBar(self.statusbar)

        self.add_subject_window = QtWidgets.QMainWindow()
        self.add_subject_ui = UiAddSubjectWindow(self)

        self.update_subject_window = QtWidgets.QMainWindow()
        self.update_subject_ui = UiUpdateSubjectWindow(self)

        self.moodle_window = QtWidgets.QMainWindow()
        self.moodle_ui = UiMoodleWindow(self)

        self.retranslateUi(self.subject_list_window)
        QtCore.QMetaObject.connectSlotsByName(self.subject_list_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Диспциплины"))
        self.label.setText(_translate("MainWindow", "Диспциплины"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_3.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_5.setText(_translate("MainWindow", "Импорт из .csv"))
        self.pushButton_6.setText(_translate("MainWindow", "Импорт из Moodle"))

    def show_add_subject_window(self):
        self.add_subject_window.show()

    def close_window(self):
        self.subject_list_window.close()

    def update_subject(self):

        items = self.listWidget.selectedItems()
        for i in items:
            name = i.text()
            self.update_subject_ui.lineEdit.setText(name)
            self.update_subject_ui.update_value = name
            self.update_subject_window.show()
            self.listWidget.takeItem(self.listWidget.row(i))
            break

    def delete_subject(self):
        items = self.listWidget.selectedItems()

        for i in items:
            name = i.text()
            subject = Discipline()
            subject.delete(self.session, name)
            self.listWidget.takeItem(self.listWidget.row(i))

            break

    def import_csv(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        try:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self.subject_list_window, "Open Image", ".",
                                                            "Image Files (*.csv)")

            with open(path, "r") as f_obj:
                reader = csv.reader(f_obj)
                dicsipline = Discipline()
                dicsiplines = dicsipline.show_name(self.session)

                for row in reader:
                    name = row[0]
                    flag_d = 0
                    for d in dicsiplines:
                        if name == d:
                            flag_d = 1
                            break

                    if flag_d == 0:
                        dicsipline.add(self.session, name)
                        self.listWidget.addItem(name)

            msg.setText("Импорт выполнен")
            msg.setInformativeText('Импорт данных из CSV выполнен.')
            msg.setWindowTitle("Импорт выполнен")

        except:
                msg.setText("Импорт не выполнен")
                msg.setInformativeText('Импорт данных из CSV не выполнен.')
                msg.setWindowTitle("Импорт не выполнен")
        msg.exec_()

    def import_moodle(self):
        self.moodle_ui.flag_discipline = True
        self.moodle_ui.flag_group = False
        self.moodle_ui.flag_student = False
        self.moodle_window.show()