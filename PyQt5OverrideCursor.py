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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class QOverrideCursor(object):
    """ The base class for QWaitCursor and QBusyCursor.
    """

    # The __needCleanup attribute and the __cleanup() method are necessary because:
    #
    #   Using QOverrideCursor() in a 'with' statement causes these method calls:
    #       with QWaitCursor():
    #           do something
    #
    #       __init__()
    #       __enter__()
    #       __exit__()
    #       __del__()
    #
    #   but just creating the object causes fewer calls:
    #       x = QWaitCursor()
    #       do something
    #
    #       __init__()
    #       __del__()
    #
    #   So, the cursor should be restored in the __exit__() method in the first
    #   example and in the __del__() method in the second example.  The __needCleanup
    #   attribute prevents restoreOverrideCursor() from being called twice when
    #   QOverrideCursor is used in a 'with' statement.

    def __init__(self, cursor):
        QApplication.instance().setOverrideCursor(cursor)
        self.__needCleanup = True

    def __del__(self):
        self.__cleanup()

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        self.__cleanup()

    def __cleanup(self):
        if (self.__needCleanup):
            QApplication.instance().restoreOverrideCursor()
            self.__needCleanup = False

class QBusyCursor(QOverrideCursor):
    def __init__(self):
        super().__init__(Qt.BusyCursor)

class QWaitCursor(QOverrideCursor):
    def __init__(self):
        super().__init__(Qt.WaitCursor)
