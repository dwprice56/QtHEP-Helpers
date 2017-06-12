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


import pathlib
from collections import MutableSequence

from PyQt5.QtCore import QStandardPaths
from PyQt5.QtWidgets import (QApplication,
    QComboBox,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QWidget)

ERROR_BACKGROUND_STYLE = ':enabled { color: Black; background-color: Coral } :disabled { color: Black; background-color: Coral }'

_DEFAULT_TITLE   = 'Validation Error'

class QWidget_Abstract_Validator(object):
    """ Base class for all other widget validators.
    """

    __DEFAULT_MESSAGE = 'There is an error in the hightlighted field.'

    FLAG_CLEAR_HIGHLIGHT_BEFORE_VALIDATING = 0x0001
    FLAG_HIGHLIGHT_WIDGETS_WITH_ERRORS     = 0x0002
    FLAG_SHOW_ERROR_MESSAGE                = 0x0004
    FLAG_DISABLED_WIDGET_ALWAYS_VALID      = 0x0008

    def __init__(self, widget, title=_DEFAULT_TITLE, message=__DEFAULT_MESSAGE):
        self.connect(widget)
        self._flags = self.FLAG_CLEAR_HIGHLIGHT_BEFORE_VALIDATING \
            | self.FLAG_HIGHLIGHT_WIDGETS_WITH_ERRORS \
            | self.FLAG_SHOW_ERROR_MESSAGE \
            | self.FLAG_DISABLED_WIDGET_ALWAYS_VALID
        self._preExistingStyle = 0

        self._errorTitle = title
        self._errorMessage = message

    def addFlags(self, flags):
        """ Add more flags to the existing flags.
        """

        self._flags |= flags

    def removeFlags(self, flags):
        """ Set flags from the existing flags.
        """

        self._flags ^= flags

    def clearHighlight(self):
        """ Clear the error indicator.

            The default behavior is to clear the style sheet.
        """

        if (self._preExistingStyle != 0):
            self._widget.setStyleSheet(self._preExistingStyle)
            self._preExistingStyle = 0

    def connect(self, widget):
        """ Connect the widget to the validator.  This should be overridden in
            the child classes to check the widget type.
        """
        assert(isinstance(widget, QWidget))

        self._widget = widget

    def flags(self):
        """ Returns the current flags.
        """

        return self._flags

    def isValid(self):
        """ Return True if the widget is valid.

            Override in descendant objected to validate the widget.
        """

        return True

    def isHighlighted(self):
        """ Return True if the widget is highlighted.

            This is determined by the status of the pre-existing style sheet.
        """

        return (self._preExistingStyle != 0)

    def setFlags(self, flags):
        """ Set flags that control validation behavior.
        """

        self._flags = flags

    def setHighlight(self):
        """ Set the error indicator.

            The default behavior is to set the background color using a style sheet.
        """

        if (self._preExistingStyle == 0):
            self._preExistingStyle = self._widget.styleSheet()
        self._widget.setStyleSheet(ERROR_BACKGROUND_STYLE)

class QLineEditor_Abstract_Validator(QWidget_Abstract_Validator):
    """ A base class for QLineEdit fields.
    """

    __DEFAULT_MESSAGE = 'There is an error in the hightlighted field.'

    def __init__(self, widget, title=_DEFAULT_TITLE, message=__DEFAULT_MESSAGE):
        super(QLineEditor_Abstract_Validator, self).__init__(widget, title, message)

    def connect(self, widget):
        """ Connect the QLineEdit widget to the validator.
        """
        assert(isinstance(widget, QLineEdit))

        super(QLineEditor_Abstract_Validator, self).connect(widget)

    def setErrorMessage(self, message):
        """ Set the error box message that will be displayed when the field is
            not valid.
        """

        self._errorMessage = message

    def setErrorTitle(self, title):
        """ Set the title of the error message box.
        """

        self._errorTitle = title

class QLineEdit_ExecutableExists_Validator(QLineEditor_Abstract_Validator):
    """ A validator for a QLineEdit field that contains a folder.
    """

    __DEFAULT_MESSAGE = 'The highlighted field is either blank or does not point to a valid executble.'

    def __init__(self, widget, title=_DEFAULT_TITLE, message=__DEFAULT_MESSAGE):
        super(QLineEdit_ExecutableExists_Validator, self).__init__(widget, title, message)

    def isValid(self):
        """ The field is valid if:
                1) The field is not blank.
                2) The value in the field is a valid folder.

            If the field is not valid:
                1) Highlight the field.
                2) Display an error message
                3) Return False
        """

        if (self._flags & self.FLAG_CLEAR_HIGHLIGHT_BEFORE_VALIDATING):
            self.clearHighlight()

        if ((self._flags & self.FLAG_DISABLED_WIDGET_ALWAYS_VALID)
            and (not self._widget.isEnabled())):
            return True

        path = pathlib.Path(self._widget.text())
        if (path.is_file()):
            return True

        if (len(path.parts) == 1):
            result = QStandardPaths.findExecutable(path.name)
            if (result != ''):
                return True

        if (self._flags & self.FLAG_HIGHLIGHT_WIDGETS_WITH_ERRORS):
            self.setHighlight()

        if (self._flags & self.FLAG_SHOW_ERROR_MESSAGE):
            QMessageBox.critical(QApplication.instance().mainWindow, self._errorTitle, self._errorMessage)

        return False

class QLineEdit_FileExists_Validator(QLineEditor_Abstract_Validator):
    """ A validator for a QLineEdit field that contains a file.

        The file must exist.
    """

    __DEFAULT_MESSAGE = 'The highlighted field is either blank or does not point to a valid file.'

    def __init__(self, widget, title=_DEFAULT_TITLE, message=__DEFAULT_MESSAGE):
        super(QLineEdit_FileExists_Validator, self).__init__(widget, title, message)

    def isValid(self):
        """ The field is valid if:
                1) The field is not blank.
                2) The value in the field is a valid file.

            If the field is not valid:
                1) Highlight the field.
                2) Display an error message
                3) Return False
        """

        if (self._flags & self.FLAG_CLEAR_HIGHLIGHT_BEFORE_VALIDATING):
            self.clearHighlight()

        if ((self._flags & self.FLAG_DISABLED_WIDGET_ALWAYS_VALID)
            and (not self._widget.isEnabled())):
            return True

        folder = self._widget.text()
        if (folder):
            path = pathlib.Path(folder)
            if (path.is_file()):
                return True

        if (self._flags & self.FLAG_HIGHLIGHT_WIDGETS_WITH_ERRORS):
            self.setHighlight()

        if (self._flags & self.FLAG_SHOW_ERROR_MESSAGE):
            QMessageBox.critical(QApplication.instance().mainWindow, self._errorTitle, self._errorMessage)

        return False

class QLineEdit_FolderExists_Validator(QLineEditor_Abstract_Validator):
    """ A validator for a QLineEdit field that contains a folder.
    """

    __DEFAULT_MESSAGE = 'The highlighted field is either blank or does not point to a valid folder.'

    def __init__(self, widget, title=_DEFAULT_TITLE, message=__DEFAULT_MESSAGE):
        super(QLineEdit_FolderExists_Validator, self).__init__(widget, title, message)

    def isValid(self):
        """ The field is valid if:
                1) The field is not blank.
                2) The value in the field is a valid folder.

            If the field is not valid:
                1) Highlight the field.
                2) Display an error message
                3) Return False
        """

        if (self._flags & self.FLAG_CLEAR_HIGHLIGHT_BEFORE_VALIDATING):
            self.clearHighlight()

        if ((self._flags & self.FLAG_DISABLED_WIDGET_ALWAYS_VALID)
            and (not self._widget.isEnabled())):
            return True

        folder = self._widget.text()
        if (folder):
            path = pathlib.Path(folder)
            if (path.is_dir()):
                return True

        if (self._flags & self.FLAG_HIGHLIGHT_WIDGETS_WITH_ERRORS):
            self.setHighlight()

        if (self._flags & self.FLAG_SHOW_ERROR_MESSAGE):
            QMessageBox.critical(QApplication.instance().mainWindow, self._errorTitle, self._errorMessage)

        return False

class QLineEdit_NotBlank_Validator(QLineEditor_Abstract_Validator):
    """ A validator for a QLineEdit field That may not be blank.
    """

    __DEFAULT_MESSAGE = 'The highlighted field may not be blank.'

    # TDDO add field names to error messages?

    def __init__(self, widget, title=_DEFAULT_TITLE, message=__DEFAULT_MESSAGE):
        super(QLineEdit_NotBlank_Validator, self).__init__(widget, title, message)

    def isValid(self):
        """ The field is valid if:
                1) The field is not blank.

            If the field is not valid:
                1) Highlight the field.
                2) Display an error message
                3) Return False
        """

        if (self._flags & self.FLAG_CLEAR_HIGHLIGHT_BEFORE_VALIDATING):
            self.clearHighlight()

        if ((self._flags & self.FLAG_DISABLED_WIDGET_ALWAYS_VALID)
            and (not self._widget.isEnabled())):
            return True

        text = self._widget.text()
        if (text):
            return True

        if (self._flags & self.FLAG_HIGHLIGHT_WIDGETS_WITH_ERRORS):
            self.setHighlight()

        if (self._flags & self.FLAG_SHOW_ERROR_MESSAGE):
            QMessageBox.critical(QApplication.instance().mainWindow, self._errorTitle, self._errorMessage)

        return False

class QListWidget_NotEmpty_Validator(QWidget_Abstract_Validator):
    """ A validator for a QListWidget field that must not be empty.
    """

    __DEFAULT_MESSAGE = 'The highlighted list may not be empty.'

    def __init__(self, widget, title=_DEFAULT_TITLE, message=__DEFAULT_MESSAGE):
        super(QListWidget_NotEmpty_Validator, self).__init__(widget, title, message)

    def connect(self, widget):
        """ Connect the QListWidget widget to the validator.
        """
        assert(isinstance(widget, QListWidget))

        super(QListWidget_NotEmpty_Validator, self).connect(widget)

    def isValid(self):
        """ The field is valid if:
                1) The field is not blank.

            If the field is not valid:
                1) Highlight the field.
                2) Display an error message
                3) Return False
        """

        if (self._flags & self.FLAG_CLEAR_HIGHLIGHT_BEFORE_VALIDATING):
            self.clearHighlight()

        if ((self._flags & self.FLAG_DISABLED_WIDGET_ALWAYS_VALID)
            and (not self._widget.isEnabled())):
            return True

        if (self._widget.count()):
            return True

        if (self._flags & self.FLAG_HIGHLIGHT_WIDGETS_WITH_ERRORS):
            self.setHighlight()

        if (self._flags & self.FLAG_SHOW_ERROR_MESSAGE):
            QMessageBox.critical(QApplication.instance().mainWindow, self._errorTitle, self._errorMessage)

        return False

class QComboBox_NotEmpty_Validator(QWidget_Abstract_Validator):
    """ A validator for a QComboBox field that must not be empty/must have
        something selected.
    """

    __DEFAULT_MESSAGE = 'The list must have something selected.'

    def __init__(self, widget, title=_DEFAULT_TITLE, message=__DEFAULT_MESSAGE):
        super(QComboBox_NotEmpty_Validator, self).__init__(widget, title, message)

    def connect(self, widget):
        """ Connect the QLineEdit widget to the validator.
        """
        assert(isinstance(widget,  QComboBox))

        super(QComboBox_NotEmpty_Validator, self).connect(widget)

    def isValid(self):
        """ The field is valid if:
                1) Something in the combobox is selected.

            If the field is not valid:
                1) Highlight the field.
                2) Display an error message
                3) Return False
        """

        if (self._flags & self.FLAG_CLEAR_HIGHLIGHT_BEFORE_VALIDATING):
            self.clearHighlight()

        if ((self._flags & self.FLAG_DISABLED_WIDGET_ALWAYS_VALID)
            and (not self._widget.isEnabled())):
            return True

        if (self._widget.count()):
            if (self._widget.currentText()):
                return True

        if (self._flags & self.FLAG_HIGHLIGHT_WIDGETS_WITH_ERRORS):
            self.setHighlight()

        if (self._flags & self.FLAG_SHOW_ERROR_MESSAGE):
            QMessageBox.critical(QApplication.instance().mainWindow, self._errorTitle, self._errorMessage)

        return False

class WidgetValidators(MutableSequence):
    """ Contains a list widget validators.
    """

    def __init__(self):
        super(WidgetValidators, self).__init__()

        self.validators = []

    def __str__(self):
        return 'WidgetValidators: len: {}'.format(len(self.validators))

    # MutableSequence abstract methods
    # ==========================================================================
    def __getitem__(self, idx):
        return self.validators[idx]

    def __setitem__(self, idx, obj):
        assert(isinstance(obj, AbstractWidgetValidator))

        self.validators[idx] = obj

    def __delitem__(self, idx):
        del self.validators[idx]

    def __len__(self):
        return len(self.validators)

    def insert(self, idx, obj):
        assert(isinstance(obj, AbstractWidgetValidator))

        self.validators.insert(idx, obj)
    # ==========================================================================

    def clear(self):
        """ Remove all connectors from the list.
        """

        del self.validators[:]

    def clearHighlights(self):
        """ Clear the error indicators in the member validators.
        """
        for validator in self.validators:
            validator.clearHighlight()
