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

import datetime, os, subprocess, sys

class SingletonLog(object):
    """Write log messages to a file.  This is implements the singlton pattern
    so only one log exists in the application."""

    __instance = None

    def __new__(cls, logFilename=None):
        if SingletonLog.__instance is None:
            SingletonLog.__instance = object.__new__(cls)

            SingletonLog.__instance.logFilename = logFilename
            if (SingletonLog.__instance.logFilename is None):
                SingletonLog.__instance.logFile = None
            else:
                SingletonLog.__instance.logFile = open(SingletonLog.__instance.logFilename, 'a')

        return SingletonLog.__instance

    def __init__(self, logFilename=None):
        if (logFilename is not None):
            self.__open(logFilename)

    def __del__(self):
        self.__close()

    def __close(self):
        """ Flush and close the log file.
        """
        # If the log file exists then it's open.
        if (self.logFile is not None):
            self.logFile.flush()
            self.logFile.close()
            self.logFile = None

    def __open(self, logFilename):
        """ Only open (or re-open) the log file if the name changes.

            If the logFilename parameter is None any existing log file will be
            closed.
        """
        if (logFilename != self.logFilename):
            self.__close()
            self.logFilename = logFilename

        if (self.logFilename is not None):
            self.logFile = open(self.logFilename, 'a')

    def clear(self):
        """ Empty the log file.
        """
        assert(self.logFilename is not None)

        self.logFile.close()
        self.logFile = open(self.logFilename, 'w')
        self.logFile.close()
        self.logFile = open(self.logFilename, 'a')

    def close(self):
        """ Close a log file.
        """
        self.__close()

    def open(self, logFilename):
        """ Open a log file.

            This will close the old log file (if present) and open the new log
            file. Nothing will happen if the file name dosen't change.
        """
        self.__open(logFilename)

    def view(self):
        """ Open the log file in the default text file viewer.
        """
        assert(self.logFilename is not None)

        if (sys.platform == 'linux'):
            subprocess.call(('xdg-open', self.logFilename))
        elif (sys.platform == 'win32'):
            os.startfile(self.logFilename, 'open')
        else:
            raise RuntimeError('Unknown platform "{}" found in SingletonLog.view().'.format(sys.platform))

    def write(self, someText):
        """ Write something to the log file.

            A log file might not exist.  It depends on the user preferences.
        """
        if (self.logFile is not None):
            self.logFile.write(someText)
            self.logFile.flush()

    def writeline(self, someText, timestamp=True):
        """ Write a line of text to the log file.

            A log file might not exist.  It depends on the user preferences.
        """
        if (self.logFile is not None):
            if (timestamp):
                self.write('{}:  '.format(str(datetime.datetime.now())))
            self.write(someText)
            self.write('\n')
            self.logFile.flush()

if __name__ == '__main__':

    x = SingletonLog('TestFiles/x.log')
    x.writeline('first test file')
    print()

    y = SingletonLog()
    y.writeline('first test file again')
    y.writeline('')
    print()

    z = SingletonLog('TestFiles/z.log')
    z.writeline('second test file')
    y.writeline('second test file again')
    z.writeline('')
    print()
