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
from PyQt5 import QtWidgets, QtCore


def set_items_to_table(table, items: np.ndarray):
    try:
        rows, columns = items.shape
    except:
        return table

    table.setRowCount(rows)
    table.setColumnCount(columns)

    for i in range(rows):
        for j in range(columns):
            table.setItem(i, j, QtWidgets.QTableWidgetItem(items[i][j]))

    return table