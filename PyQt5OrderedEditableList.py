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

import copy

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem

class QOrderedEditableList(QObject):
    """ A class that connects methods to buttons that will do the following
        actions to a QListWidget:

        1) Enable, disable the buttons depending on the list selection.
        2) Add a new, default string to the end of the list.
        3) Copy the selected list item to the end of the list.  If the selected
           item has any Qt.UserRole data, the data will be copied using deepcopy().
        4) Delete the selected item from the list, unless it's the last item in the list.
        5) Move a list item up, down, to top or to bottom.

        Note: The QListWidget selectionMode must be singleSelection.

        The parent class must implement a onNewListItem(item, name) method to
        complete the initialization of a new item.  For example, items in the
        Mixdown list have a Mixdown() objected attached as data(Qt.UserRole).
        For that case, the parent.onNewListItem(item) method would need to
        create a new Mixdown() object and attach it to the new item.  The method
        may be omitted if no additional initialization is needed.

        The Qt5 signal/slot mechanism was considered but it's not practical
        because it's asynchronous.  New list items are automatically selected
        and the new item's initialization must be complete before it's selected.
        The signal/slot mechanism can't guarantee that.

        However, a Qt5 signal named listChanged is emitted whenever a button is
        used to modify the list (add, copy, delete; move up, down, top, bottom).
    """

    listChanged = pyqtSignal()

    def __init__(self, parent, listWidget, newItemButton, copyItemButton, deleteItemButton,
        itemTopButton, itemUpButton, itemDownButon, itemBottomButton, newItemDefaultString,
        onNewListItem = None):
        super().__init__(parent)

        self.__parent = parent

        self.__listWidget = listWidget
        self.__newItemButton = newItemButton
        self.__copyItemButton = copyItemButton
        self.__deleteItemButton = deleteItemButton
        self.__itemTopButton = itemTopButton
        self.__itemUpButton = itemUpButton
        self.__itemDownButon = itemDownButon
        self.__itemBottomButton = itemBottomButton
        self.__newItemDefaultString = newItemDefaultString
        self._onNewListItem = onNewListItem

        self.__listWidget.itemSelectionChanged.connect(self.enableButtons)

        self.__newItemButton.clicked.connect(self.__itemNew)
        self.__copyItemButton.clicked.connect(self.__itemCopy)
        self.__deleteItemButton.clicked.connect(self.__itemDelete)

        self.__itemTopButton.clicked.connect(self.__itemMoveTop)
        self.__itemUpButton.clicked.connect(self.__itemMoveUp)
        self.__itemDownButon.clicked.connect(self.__itemMoveDown)
        self.__itemBottomButton.clicked.connect(self.__itemMoveBottom)

        self.enableButtons()

    def __closePersistentEditor(self):
        """ Make sure the persistent editor is closed.  It really screws things
            up if it's open during list operations.
        """

        currentItem = self.__listWidget.currentItem()
        if (currentItem is not None):
            self.__listWidget.closePersistentEditor(currentItem)

    def enableButtons(self):
        """ Enable/disable the buttons based on the contents of the listWidget.
        """

        count = self.__listWidget.count()
        currentRow = self.__listWidget.currentRow()

        # If the list is empty or nothing is selected.
        if ((not count) or (currentRow < 0)):
            self.__copyItemButton.setEnabled(False)
            self.__deleteItemButton.setEnabled(False)
            self.__itemTopButton.setEnabled(False)
            self.__itemUpButton.setEnabled(False)
            self.__itemDownButon.setEnabled(False)
            self.__itemBottomButton.setEnabled(False)
            return

        # The list is not empty and something is selected.
        self.__copyItemButton.setEnabled(True)
        self.__deleteItemButton.setEnabled(count > 1)

        self.__itemTopButton.setEnabled(currentRow > 0)
        self.__itemUpButton.setEnabled(currentRow > 0)

        self.__itemDownButon.setEnabled(currentRow + 1 < count)
        self.__itemBottomButton.setEnabled(currentRow + 1 < count)

    def __itemCopy(self):
        """ Add a copy of the selected item to the end of the list.  Select the
            copy item and start editing it.
        """
        self.__closePersistentEditor()

        currentItem = self.__listWidget.currentItem()

        item = QListWidgetItem(currentItem.text(), self.__listWidget)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)

        currentItemData = currentItem.data(Qt.UserRole)
        if (currentItemData is not None):
            item.setData(Qt.UserRole, copy.deepcopy(currentItemData))

        item.setSelected(True)
        self.__listWidget.setCurrentItem(item)
        self.__listWidget.editItem(item)

        self.enableButtons()
        self.listChanged.emit()

    def __itemDelete(self):
        """ Add a copy of the selected item to the end of the list.  Select the
            copy item and start editing it.
        """
        self.__closePersistentEditor()

        if ( self.__listWidget.count() == 1):
            QMessageBox.critical(self.__parent, 'List Error',
                'The last item in the list may not be deleted.')
            return

        row = self.__listWidget.currentRow()
        self.__listWidget.closePersistentEditor(self.__listWidget.item(row))
        self.__listWidget.takeItem(row)

        count = self.__listWidget.count()
        if (count == 1):
            row = 0
        elif (row == count):
            row -= 1

        item = self.__listWidget.item(row)
        item.setSelected(True)
        self.__listWidget.setCurrentItem(item)

        self.enableButtons()
        self.listChanged.emit()

    def __itemMoveBottom(self):
        """ Move the selected item to the bottom of the list.
        """
        self.__closePersistentEditor()

        row = self.__listWidget.currentRow()
        self.__listWidget.closePersistentEditor(self.__listWidget.item(row))

        item = self.__listWidget.takeItem(row)
        self.__listWidget.addItem(item)
        self.__listWidget.setCurrentItem(item)
        item.setSelected(True)

        self.enableButtons()
        self.listChanged.emit()

    def __itemMoveDown(self):
        """ Move the selected item down one position in the list.
        """
        self.__closePersistentEditor()

        row = self.__listWidget.currentRow()
        self.__listWidget.closePersistentEditor(self.__listWidget.item(row))

        item = self.__listWidget.takeItem(row)
        self.__listWidget.insertItem(row + 1, item)
        self.__listWidget.setCurrentItem(item)
        item.setSelected(True)

        self.enableButtons()
        self.listChanged.emit()

    def __itemMoveTop(self):
        """ Move the selected item to the top of the list.
        """
        self.__closePersistentEditor()

        row = self.__listWidget.currentRow()
        self.__listWidget.closePersistentEditor(self.__listWidget.item(row))

        item = self.__listWidget.takeItem(row)
        self.__listWidget.insertItem(0, item)
        self.__listWidget.setCurrentItem(item)
        item.setSelected(True)

        self.enableButtons()
        self.listChanged.emit()

    def __itemMoveUp(self):
        """ Move the selected item up one position in the list.
        """
        self.__closePersistentEditor()

        row = self.__listWidget.currentRow()
        self.__listWidget.closePersistentEditor(self.__listWidget.item(row))

        item = self.__listWidget.takeItem(row)
        self.__listWidget.insertItem(row - 1, item)
        self.__listWidget.setCurrentItem(item)
        item.setSelected(True)

        self.enableButtons()
        self.listChanged.emit()

    def __itemNew(self):
        """ Add a new, default item to the end of the list.  Select the item
            and start editing it.
        """
        self.__closePersistentEditor()

        item = QListWidgetItem(self.__newItemDefaultString, self.__listWidget)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)

        if (self._onNewListItem is not None):
            self._onNewListItem(item, self.__newItemDefaultString)

        item.setSelected(True)
        self.__listWidget.setCurrentItem(item)
        self.__listWidget.editItem(item)

        self.enableButtons()
        self.listChanged.emit()
