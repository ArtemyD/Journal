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

from PyQt5 import QtWidgets
from UI.py_ui.mainwindow import FormMainWindow
import sys
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from settings import my_databases


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    # engine = create_engine(my_databases, pool_size=10, max_overflow=20)
    engine = create_engine(my_databases)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()

    ui_main = FormMainWindow(main_window, session)
    ui_main.set_default_date()
    ui_main.show()
    sys.exit(app.exec_())
