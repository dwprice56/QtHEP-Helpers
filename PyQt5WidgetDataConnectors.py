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

# ==============================================================================
# Python has two different types of variables: mutable variables such as lists,
# dictionaries & class objects and immutable variables such as ints, floats &
# bools. Mutable variables are passed to methods by reference and immutable
# variables are passed by value.
# ==============================================================================

from collections import MutableSequence

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox,
    QComboBox,
    QLineEdit,
    QPlainTextEdit,
    QRadioButton,
    QSpinBox,
    QTableWidgetItem)

class AbstractWidgetMutableDataConnector(object):
    """ Base class for all other connectors.

        The data item must be of a mutable type.

        The groupFlags may be set to control the transferToWindow(),
        transferFromWindow() methods.  When supplied, only the controls
        with matching groups will be transfered.
    """

    # SAMPLE_CONTROL_GROUP_A = 0x0001
    # SAMPLE_CONTROL_GROUP_B = 0x0002
    # SAMPLE_CONTROL_GROUP_C = 0x0004

    def __init__(self, groupFlags=0):
        self._widget = None
        self._mutableDataItem = None
        self._groupFlags = groupFlags

    def _transferToWidget(self):
        """ Virtual method for transferring data from the dataItem to the widget.
            Must be overridden in the child classes.
        """
        assert(False)

    def _transferFromWidget(self):
        """ Virtual method for transferring data from the widget to the dataItem.
            Must be overridden in the child classes.
        """
        assert(False)

    def connect(self, widget, mutableDataItem, groupFlags=0):
        """ Connect the widget to the dataItem.  This should be overridden in
            the child classes to check the widget type.
        """
        self._widget = widget
        self._mutableDataItem = mutableDataItem
        self._groupFlags = groupFlags

    def isGroupMember(self, groupFlags):
        """ Is this item a member of any of the groups?  The groupFlags may
            contain more the one group.
        """
        return (groupFlags & self._groupFlags)

    def setGroupFlags(self, groupFlags):
        """ The groupFlags may be set to control the transferToWindow(),
            transferFromWindow() methods.  When supplied, only the controls
            with matching groups will be transfered.
        """
        self._groupFlags = groupFlags

class AbstractWidgetImmutableDataConnector(AbstractWidgetMutableDataConnector):
    """ Base class connectors that deal with immutable variables.

        The data item must be attached to a mutable variable.
    """

    def __init__(self, groupFlags=0):
        super().__init__(groupFlags)

        self._attributeName = None

    def connect(self, widget, mutableDataItem, attributeName, groupFlags=0):
        """ Connect the widget to the dataItem.  This should be overridden in
            the child classes to check the widget type.
        """
        super().connect(widget, mutableDataItem, groupFlags)
        self._attributeName = attributeName

class QCheckBoxDataConnector(AbstractWidgetImmutableDataConnector):
    """ A connectors that transfers a boolean attribute to/from a QCheckBox.
    """

    def __init__(self, widget, mutableDataItem, attributeName, groupFlags=0):
        super().__init__(groupFlags)

        self.connect(widget, mutableDataItem, attributeName, groupFlags)

    def _transferToWidget(self):
        """ Virtual method for transferring data from the dataItem to the widget.
            Must be overridden in the child classes.
        """
        dataItem = getattr(self._mutableDataItem, self._attributeName)
        self._widget.setChecked(dataItem)

    def _transferFromWidget(self):
        """ Virtual method for transferring data from the widget to the dataItem.
            Must be overridden in the child classes.
        """
        setattr(self._mutableDataItem, self._attributeName, self._widget.isChecked())

    def connect(self, widget, mutableDataItem, attributeName, groupFlags=0):
        """ Connect the widget to the dataItem.  This should be overridden in
            the child classes to check the widget type.
        """
        assert(isinstance(widget, QCheckBox))
        dataItem = getattr(mutableDataItem, attributeName)
        assert(isinstance(dataItem, bool))

        super().connect(widget, mutableDataItem, attributeName, groupFlags)

class QComboBoxDataConnector(AbstractWidgetImmutableDataConnector):
    """ A connectors that transfers a boolean attribute to/from a QComboBox.
    """

    def __init__(self, widget, mutableDataItem, attributeName, groupFlags=0):
        super().__init__(groupFlags)

        self.connect(widget, mutableDataItem, attributeName, groupFlags)

    def _transferToWidget(self):
        """ Virtual method for transferring data from the dataItem to the widget.
            Must be overridden in the child classes.
        """
        dataItem = getattr(self._mutableDataItem, self._attributeName)

        found = self._widget.findText(dataItem)
        if (found == -1):
            if (self._widget.count()):
                self._widget.setCurrentIndex(0)
            return

        self._widget.setCurrentText(dataItem)

    def _transferFromWidget(self):
        """ Virtual method for transferring data from the widget to the dataItem.
            Must be overridden in the child classes.
        """
        setattr(self._mutableDataItem, self._attributeName, self._widget.currentText())

    def connect(self, widget, mutableDataItem, attributeName, groupFlags=0):
        """ Connect the widget to the dataItem.  This should be overridden in
            the child classes to check the widget type.
        """
        assert(isinstance(widget, QComboBox))
        dataItem = getattr(mutableDataItem, attributeName)
        assert(isinstance(dataItem, str))

        super().connect(widget, mutableDataItem, attributeName, groupFlags)

class QLineEditDataConnector(AbstractWidgetImmutableDataConnector):
    """ A connectors that transfers a boolean attribute to/from a QLineEdit.
    """

    def __init__(self, widget, mutableDataItem, attributeName, groupFlags=0):
        super().__init__(groupFlags)

        self.connect(widget, mutableDataItem, attributeName, groupFlags)

    def _transferToWidget(self):
        """ Virtual method for transferring data from the dataItem to the widget.
            Must be overridden in the child classes.
        """
        dataItem = getattr(self._mutableDataItem, self._attributeName)
        self._widget.setText(dataItem)

    def _transferFromWidget(self):
        """ Virtual method for transferring data from the widget to the dataItem.
            Must be overridden in the child classes.
        """
        setattr(self._mutableDataItem, self._attributeName, self._widget.text())

    def connect(self, widget, mutableDataItem, attributeName, groupFlags=0):
        """ Connect the widget to the dataItem.  This should be overridden in
            the child classes to check the widget type.
        """
        assert(isinstance(widget, QLineEdit))
        dataItem = getattr(mutableDataItem, attributeName)
        assert(isinstance(dataItem, str))

        super().connect(widget, mutableDataItem, attributeName, groupFlags)

class QPlainTextEditDataConnector(AbstractWidgetImmutableDataConnector):
    """ A connectors that transfers a boolean attribute to/from a QPlainTextEdit.
    """

    def __init__(self, widget, mutableDataItem, attributeName, groupFlags=0):
        super().__init__(groupFlags)

        self.connect(widget, mutableDataItem, attributeName, groupFlags)

    def _transferToWidget(self):
        """ Virtual method for transferring data from the dataItem to the widget.
            Must be overridden in the child classes.
        """
        dataItem = getattr(self._mutableDataItem, self._attributeName)
        self._widget.setPlainText(dataItem)

    def _transferFromWidget(self):
        """ Virtual method for transferring data from the widget to the dataItem.
            Must be overridden in the child classes.
        """
        setattr(self._mutableDataItem, self._attributeName, self._widget.toPlainText())

    def connect(self, widget, mutableDataItem, attributeName, groupFlags=0):
        """ Connect the widget to the dataItem.  This should be overridden in
            the child classes to check the widget type.
        """
        assert(isinstance(widget, QPlainTextEdit))
        dataItem = getattr(mutableDataItem, attributeName)
        assert(isinstance(dataItem, str))

        super().connect(widget, mutableDataItem, attributeName, groupFlags)

class QRadioButtonGroupDataConnector(AbstractWidgetImmutableDataConnector):
    """ A connectors that uses a data attribute to set an entry in a list
        of QRadioButtons.

        The connector uses a list of QRadioButtons and a matching list values.
        In transferToWindow() the list of values is searched for a value that
        matches the data item; the corresponding QRadioButton is set.  In
        transferFromWindow() the list of QRadioButtons is searched for the one
        that's set; the data item is set to the corresponding value.

        The self.widget attribute will be None because it's not used; this
        class will use a self.widgets attribute instead.
    """

    def __init__(self, widgetList, valueList, mutableDataItem, attributeName, groupFlags=0):
        super().__init__(groupFlags)

        self.connect(widgetList, valueList, mutableDataItem, attributeName, groupFlags)

    def _transferToWidget(self):
        """ Virtual method for transferring data from the dataItem to the widget.
            Must be overridden in the child classes.
        """
        dataItem = getattr(self._mutableDataItem, self._attributeName)

        for idx in range(len(self._valueList)):
            if (dataItem == self._valueList[idx]):
                self._widgetList[idx].setChecked(True)
                return

    def _transferFromWidget(self):
        """ Virtual method for transferring data from the widget to the dataItem.
            Must be overridden in the child classes.
        """
        for idx in range(len(self._widgetList)):
            if (self._widgetList[idx].isChecked()):
                setattr(self._mutableDataItem, self._attributeName, self._valueList[idx])

    def connect(self, widgetList, valueList, mutableDataItem, attributeName, groupFlags=0):
        """ Connect the widgetList and the valueList to the dataItem.  This
            should be overridden in the child classes to check the widget type.
        """
        assert(isinstance(widgetList, list))
        assert(isinstance(valueList, list))
        assert(len(widgetList) == len(valueList))
        for widget in widgetList:
            assert(isinstance(widget, QRadioButton))

        super().connect(None, mutableDataItem, attributeName, groupFlags)
        self._widgetList = widgetList
        self._valueList = valueList

class QSpinBoxDataConnector(AbstractWidgetImmutableDataConnector):
    """ A connectors that transfers a boolean attribute to/from a QSpinBox.
    """

    def __init__(self, widget, mutableDataItem, attributeName, groupFlags=0):
        super().__init__(groupFlags)

        self.connect(widget, mutableDataItem, attributeName, groupFlags)

    def _transferToWidget(self):
        """ Virtual method for transferring data from the dataItem to the widget.
            Must be overridden in the child classes.
        """
        dataItem = getattr(self._mutableDataItem, self._attributeName)
        self._widget.setValue(dataItem)

    def _transferFromWidget(self):
        """ Virtual method for transferring data from the widget to the dataItem.
            Must be overridden in the child classes.
        """
        setattr(self._mutableDataItem, self._attributeName, self._widget.value())

    def connect(self, widget, mutableDataItem, attributeName, groupFlags=0):
        """ Connect the widget to the dataItem.  This should be overridden in
            the child classes to check the widget type.
        """
        assert(isinstance(widget, QSpinBox))
        dataItem = getattr(mutableDataItem, attributeName)
        assert(isinstance(dataItem, int))

        super().connect(widget, mutableDataItem, attributeName, groupFlags)

class QTableWidgetItemDataConnector(AbstractWidgetImmutableDataConnector):
    """ A connectors that transfers a value to/from a QTableWidgetItem.
    """

    def __init__(self, widget, mutableDataItem, attributeName, groupFlags=0):
        super().__init__(groupFlags)

        self.connect(widget, mutableDataItem, attributeName, groupFlags)

    def _transferToWidget(self):
        """ Virtual method for transferring data from the dataItem to the widget.
            Must be overridden in the child classes.
        """
        dataItem = getattr(self._mutableDataItem, self._attributeName)
        self._widget.setData(Qt.DisplayRole, dataItem)

    def _transferFromWidget(self):
        """ Virtual method for transferring data from the widget to the dataItem.
            Must be overridden in the child classes.
        """
        setattr(self._mutableDataItem, self._attributeName, self._widget.data(Qt.DisplayRole))

    def connect(self, widget, mutableDataItem, attributeName, groupFlags=0):
        """ Connect the widget to the dataItem.  This should be overridden in
            the child classes to check the widget type.
        """
        assert(isinstance(widget, QTableWidgetItem))
        super().connect(widget, mutableDataItem, attributeName, groupFlags)

class WidgetDataConnectors(MutableSequence):
    """ Contains a list widget/data connectors.
    """

    def __init__(self):
        super().__init__()

        self.connectors = []

    def __str__(self):
        return 'WidgetDataConnectors: len: {}'.format(len(self.connectors))

    # MutableSequence abstract methods
    # ==========================================================================
    def __getitem__(self, idx):
        return self.connectors[idx]

    def __setitem__(self, idx, obj):
        assert(isinstance(obj, AbstractWidgetDataConnector))
        self.connectors[idx] = obj

    def __delitem__(self, idx):
        del self.connectors[idx]

    def __len__(self):
        return len(self.connectors)

    def insert(self, idx, obj):
        assert(isinstance(obj, AbstractWidgetMutableDataConnector))
        self.connectors.insert(idx, obj)
    # ==========================================================================

    def clear(self):
        """Remove all connectors from the list."""

        del self.connectors[:]

    def transferFromWidgets(self, groupFlags=0):
        """ Transfer data from the widgets to the dataItems.

            If groupFlags are specified, only transfer matching connectors.
        """
        for connector in self.connectors:
            if (groupFlags):
                if (connector.isGroupMember(groupFlags)):
                    connector._transferFromWidget()
            else:
                connector._transferFromWidget()

    def transferToWidgets(self, groupFlags=0):
        """ Transfer data from the dataItems to the widgets.

            If groupFlags are specified, only transfer matching connectors.
        """
        for connector in self.connectors:
            if (groupFlags):
                if (connector.isGroupMember(groupFlags)):
                    connector._transferToWidget()
            else:
                connector._transferToWidget()
