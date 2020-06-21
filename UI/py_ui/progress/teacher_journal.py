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

from database.models import (Attendance, Grade, GradeScale, HistoryGrade,
                             PassSafety, Safety, Work)
from transform.items import set_items_to_table
from UI.py_ui.progress.add_grade import UiAddGradeWindow
from UI.py_ui.progress.add_work import UiAddWorkWindow
from UI.py_ui.progress.detail_grade import UiDetailGradeWindow
from UI.py_ui.progress.detail_work import UiDetailWorkWindow
from UI.py_ui.progress.history import UiHistoryWindow


class UiTeacherJournalWindow(object):
    def __init__(self, main_window):
        self.group_number: str = ''
        self.discipline_name: str = ''
        self.session = main_window.session
        self.teacher_journal_window = main_window.teacher_journal_window
        self.teacher_journal_window.setObjectName("MainWindow")
        self.teacher_journal_window.setFixedSize(880, 704)
        self.centralwidget = QtWidgets.QWidget(self.teacher_journal_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 640, 112, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setStyleSheet("t")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 851, 561))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(490, 40, 181, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_detail_grade_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 640, 171, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_history_window)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 640, 181, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.show_add_work_window)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(190, 640, 181, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.show_detail_window)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(670, 10, 191, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.show_journal_attendance_window)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(670, 40, 191, 32))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.show_journal_safety_window)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(490, 10, 181, 32))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.show_add_grade_window)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 141, 16))
        self.label_2.setObjectName("label_2")
        self.teacher_journal_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.teacher_journal_window)
        self.statusbar.setObjectName("statusbar")
        self.teacher_journal_window.setStatusBar(self.statusbar)

        self.add_work_window = QtWidgets.QMainWindow()
        self.add_work_ui = UiAddWorkWindow(self)

        self.detail_work_window = QtWidgets.QMainWindow()
        self.detail_work_ui = UiDetailWorkWindow(self)

        self.add_grade_window = QtWidgets.QMainWindow()
        self.add_grade_ui = UiAddGradeWindow(self)

        self.detail_grade_window = QtWidgets.QMainWindow()
        self.detail_grade_ui = UiDetailGradeWindow(self)

        self.history_window = QtWidgets.QMainWindow()
        self.history_ui = UiHistoryWindow(self)

        self.retranslateUi(self.teacher_journal_window)
        QtCore.QMetaObject.connectSlotsByName(self.teacher_journal_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Оценки"))
        self.pushButton.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_2.setText(_translate("MainWindow", "Подробнее об оценке"))
        self.pushButton_3.setText(_translate("MainWindow", "История оценок"))
        self.pushButton_4.setText(_translate("MainWindow", "Добавить работу"))
        self.pushButton_5.setText(_translate("MainWindow", "Подбробнее о работе"))
        self.pushButton_6.setText(_translate("MainWindow", "Посещаемость"))
        self.pushButton_7.setText(_translate("MainWindow", "Техника безопасности"))
        self.pushButton_8.setText(_translate("MainWindow", "Добавить оценку"))
        self.label.setText(_translate("MainWindow", "Дисциплина: Математическая логика"))
        self.label_2.setText(_translate("MainWindow", "Группа: №543543"))

    def show_add_work_window(self):
        grade_scale = GradeScale()
        grade_scale_all = grade_scale.all(self.session)
        self.add_work_ui.comboBox.clear()
        self.add_work_ui.comboBox.addItems(grade_scale_all)
        self.add_work_ui.lineEdit.clear()
        self.add_work_ui.textEdit.clear()
        self.add_work_ui.textEdit_2.clear()

        date_now = self.add_work_ui.dateEdit.date().currentDate()
        self.add_work_ui.dateEdit.setDate(date_now)
        self.add_work_ui.group_number = self.group_number
        self.add_work_ui.discipline_name = self.discipline_name

        self.add_work_window.show()

    def show_add_grade_window(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            col = self.tableWidget.column(i)
            work = Work()
            work_name = work.show_name(self.session, self.group_number, self.discipline_name)
            work_choosen = work_name[int((col + 1) / 2 - 1)]

            w = work.get(self.session, self.group_number, self.discipline_name, work_choosen)
            min = w.grade_scale.min
            max = w.grade_scale.max
            grade_scale = "Оценка (от " + str(min) + ' до ' + str(max) + ")"
            self.add_grade_ui.label_4.setText(grade_scale)
            self.add_grade_ui.lineEdit.clear()

            row = self.tableWidget.row(i)
            name = self.tableWidget.item(row, 0).text()

            self.add_grade_ui.lineEdit_2.setText(name)
            self.add_grade_ui.lineEdit_2.setReadOnly(True)
            self.add_grade_ui.lineEdit_3.setText(w.name)
            self.add_grade_ui.lineEdit_3.setReadOnly(True)

            date_now = self.add_grade_ui.dateEdit.date().currentDate()
            self.add_grade_ui.dateEdit.setDate(date_now)

            self.add_grade_ui.group_number = self.group_number
            self.add_grade_ui.discipline_name = self.discipline_name
            self.add_grade_ui.id_work = w.id_work

            self.add_grade_window.show()

    def show_detail_grade_window(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            col = self.tableWidget.column(i)
            work = Work()
            work_name = work.show_name(self.session, self.group_number, self.discipline_name)
            work_choosen = work_name[int((col + 1) / 2 - 1)]
            row = self.tableWidget.row(i)
            name = self.tableWidget.item(row, 0).text()

            self.detail_grade_ui.lineEdit_2.setText(name)
            self.detail_grade_ui.lineEdit_2.setReadOnly(True)

            w = work.get(self.session, self.group_number, self.discipline_name, work_choosen)
            grade = Grade()
            g = grade.get(self.session, w.id_work, name)
            grade_value = str(g.value)
            self.detail_grade_ui.lineEdit.setText(grade_value)
            self.detail_grade_ui.lineEdit.setReadOnly(True)

            self.detail_grade_ui.lineEdit_3.setText(w.name)
            self.detail_grade_ui.lineEdit_3.setReadOnly(True)

            self.detail_grade_ui.dateEdit.setDate(g.date)
            self.detail_grade_ui.textEdit.setText(g.feedback)
            self.detail_grade_ui.textEdit_2.setText(g.note)
            self.detail_grade_ui.textEdit_2.setReadOnly(True)
            self.detail_grade_ui.textEdit.setReadOnly(True)

            self.detail_grade_ui.path_file = g.path_file
            self.detail_grade_ui.group_number = self.group_number
            self.detail_grade_ui.discipline_name = self.discipline_name
            self.detail_grade_ui.id_grade = g.id_grade
            self.detail_grade_ui.id_work = w.id_work

            self.detail_grade_window.show()

    def show_detail_window(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            col = self.tableWidget.column(i)

            work = Work()
            work_name = work.show_name(self.session, self.group_number, self.discipline_name)
            work_choosen = work_name[int((col + 1) / 2 - 1)]

            w = work.get(self.session, self.group_number, self.discipline_name, work_choosen)
            self.detail_work_ui.id_work = w.id_work
            min = w.grade_scale.min
            max = w.grade_scale.max
            grade_scale = str(min) + '-' + str(max)
            self.detail_work_ui.lineEdit_2.setText(grade_scale)
            self.detail_work_ui.lineEdit_2.setReadOnly(True)
            self.detail_work_ui.lineEdit.setText(w.name)
            self.detail_work_ui.lineEdit.setReadOnly(True)
            self.detail_work_ui.textEdit.setText(w.task)
            self.detail_work_ui.textEdit.setReadOnly(True)
            self.detail_work_ui.textEdit_2.setText(w.note)
            self.detail_work_ui.textEdit_2.setReadOnly(True)

            if w.isdeadline == True:
                self.detail_work_ui.checkBox.setChecked(True)
                self.detail_work_ui.dateEdit.setDate(w.deadline)
                self.detail_work_ui.dateEdit.show()
            else:
                self.detail_work_ui.checkBox.setChecked(False)
                self.detail_work_ui.dateEdit.hide()

        self.detail_work_ui.group_number = self.group_number
        self.detail_work_ui.discipline_name = self.discipline_name
        self.detail_work_window.show()

    def show_history_window(self):
        history_grade = HistoryGrade()
        table_content: np.ndarray = history_grade.all(self.session, self.discipline_name, self.group_number)
        self.history_ui.tableWidget = set_items_to_table(self.history_ui.tableWidget, table_content)
        self.history_ui.tableWidget.resizeColumnsToContents()
        self.history_window.show()

    def show_journal_safety_window(self):
        safety = Safety()

        pass_safety = PassSafety()
        table_content: np.ndarray = pass_safety.all(self.session, self.discipline_name, self.group_number)
        self.journal_safety_ui.tableWidget = set_items_to_table(self.journal_safety_ui.tableWidget, table_content)

        table_header: list = safety.all_name(self.session, self.discipline_name, self.group_number, flag_header=True)
        self.journal_safety_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.journal_safety_ui.tableWidget.resizeColumnsToContents()

        self.journal_safety_ui.group_number = self.group_number
        self.journal_safety_ui.discipline_name = self.discipline_name
        self.journal_safety_ui.label_2.setText(self.discipline_name)
        self.journal_safety_ui.label_4.setText(self.group_number)

        self.journal_safety_ui.teacher_journal_ui = self.teacher_journal_ui
        self.journal_safety_ui.teacher_journal_window = self.teacher_journal_window
        self.journal_safety_ui.journal_attendance_window = self.journal_attendance_window
        self.journal_safety_ui.journal_attendance_ui = self.journal_attendance_ui
        self.journal_safety_ui.journal_safety_window = self.journal_safety_window
        self.journal_safety_ui.journal_safety_ui = self.journal_safety_ui

        self.journal_safety_window.show()
        self.teacher_journal_window.close()

    def close_window(self):
        self.tableWidget.setRowCount(0)
        self.teacher_journal_window.close()

    def show_journal_attendance_window(self):
        self.journal_attendance_ui.label_2.setText(self.discipline_name)
        self.journal_attendance_ui.label_4.setText(self.group_number)

        a = Attendance()
        table_content: np.ndarray = a.all(self.session, self.discipline_name, self.group_number)
        self.journal_attendance_ui.tableWidget = set_items_to_table(self.journal_attendance_ui.tableWidget, table_content)

        table_header: list = a.show_name(self.session, self.group_number, self.discipline_name, flag_header=True)
        self.journal_attendance_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.journal_attendance_ui.tableWidget.resizeColumnsToContents()

        self.journal_attendance_ui.group_number = self.group_number
        self.journal_attendance_ui.discipline_name = self.discipline_name

        self.journal_attendance_ui.teacher_journal_ui = self.teacher_journal_ui
        self.journal_attendance_ui.teacher_journal_window = self.teacher_journal_window
        self.journal_attendance_ui.journal_attendance_window = self.journal_attendance_window
        self.journal_attendance_ui.journal_attendance_ui = self.journal_attendance_ui
        self.journal_attendance_ui.journal_safety_window = self.journal_safety_window
        self.journal_attendance_ui.journal_safety_ui = self.journal_safety_ui

        self.journal_attendance_window.show()
        self.teacher_journal_window.close()
