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

import os.path

from PyQt5.QtCore import (
    QFileInfo,
    QSettings
)
from PyQt5.QtWidgets import (
    QAction,
    QApplication
)

class QRecentFiles(object):
    """ A class to handle selecting/opening recent files on a QMenu.

        This class is designed to be inherited by a main window with a menu.

        QCoreApplication::setOrganizationName(), QCoreApplication::setOrganizationDomain(),
        and/or QCoreApplication::setApplicationName() should be called before
        setupRecentFiles().
    """
    MAX_RECENT_FILES = 10

    def __init__(self, maxRecentFiles=MAX_RECENT_FILES):
        self.windowTitle = None
        self.maxRecentFiles = maxRecentFiles
        self.recentFileActs = []
        self.currentFile = None

    def clearRecentFiles(self):
        """ Remove all files from the recent file list.  Then update the recent
            file menu.
        """
        settings = QSettings()

        settings.setValue('recentFileList', [])

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QRecentFiles):
                widget.updateRecentFileActions()

    def removeDeadRecentFiles(self):
        """ Remove files that no longer exist from the file list.  Then update
            menu.
        """
        settings = QSettings()
        files = settings.value('recentFileList', [])
        filelist = settings.value('recentFileList', [])

        for file in filelist:
            if (not os.path.exists(file)):
                try:
                    files.remove(file)
                except ValueError:
                    pass

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QRecentFiles):
                widget.updateRecentFileActions()

    def setupRecentFiles(self, menu, triggeredMethod, windowTitle=None):
        """ Add the recent files entries to the menu.

            Parameters:
                menu - A QMenu widget; The recent files menu items will be
                    appended to the menu.
                triggeredMethod - This method will be called whenever a recent
                    a recent file is selected.
        """
        self.windowTitle = windowTitle

        for i in range(self.maxRecentFiles):
            self.recentFileActs.append(QAction(self, visible=False,
                    triggered=triggeredMethod))
            menu.addAction(self.recentFileActs[i])

        self.updateRecentFileActions()

    def setCurrentFile(self, fileName):
        """ Make the current file the top item in the list of files.  Then drop
            the last item from the list, if necessary.  Then update the recent
            file list menu.
        """
        self.currentFile = fileName

        if (self.windowTitle):
            if self.currentFile:
                self.setWindowTitle('{} - {}'.format(self.strippedName(self.currentFile),
                    self.windowTitle))
            else:
                self.setWindowTitle(self.windowTitle)
                return

        settings = QSettings()
        files = settings.value('recentFileList', [])

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[self.MAX_RECENT_FILES:]

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QRecentFiles):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        """ Update the menu of recent files.
        """
        settings = QSettings()
        files = settings.value('recentFileList', [])

        numRecentFiles = min(len(files), self.MAX_RECENT_FILES)

        for i in range(numRecentFiles):
            text = '&{} {}'.format(i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, self.MAX_RECENT_FILES):
            self.recentFileActs[j].setVisible(False)

    def strippedName(self, fullFileName):
        """ Returns the file name portion of the path.
        """
        return QFileInfo(fullFileName).fileName()
