#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2017 David Price
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path, sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

def AddItemToTableWidgetCell(tableWidget, row, column, value, data=None,
    readOnly=False, textAlignment=(Qt.AlignRight | Qt.AlignBottom)):
    """ Create and add a QTableWidgetItem to a QTableWidget cell.

        The value parameter is attached as setData(Qt.EditRole).
        The data parameter is attached as setData(Qt.UserRole).

        The Qt.ItemIsEditable flag is cleared if the readOnly parameter is True.

        Returns the item that was created.
    """

    item = QTableWidgetItem()
    if (value is not None):
        item.setData(Qt.EditRole, value)
    if (data is not None):
        item.setData(Qt.UserRole, data)
    if (textAlignment is not None):
        item.setTextAlignment(textAlignment)
    if (readOnly):
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    tableWidget.setItem(row, column, item)

    return item

def SetTextComboBoxSelection(comboBox, text):
    """ Selects an item a QComboBox, if it's present.

        Returns True if the item is found, False if it's not there.
    """

    found = comboBox.findText(text)
    if (found == -1):
        return False

    comboBox.setCurrentText(text)
    return True

def UpdateComboBox(comboBox, stringList):
    """ Updates the list of items in a QComboBox, preserving the current selection
        (if possible).
    """

    currentText = comboBox.currentText()
    comboBox.clear()
    comboBox.addItems(stringList)
    if (currentText in stringList):
        comboBox.setCurrentText(currentText)
