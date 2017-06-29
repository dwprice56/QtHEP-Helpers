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

# if (sys.platform == 'win32'):
#     import win32api

        # if (sys.platform == 'win32'):
        #     drive, tail = os.path.splitdrive(self.dirpickerctrlSource.GetPath().strip())
        #     return win32api.GetVolumeInformation(drive)[0]


# import wmi
# c = wmi.WMI()
# for pm in c.Win32_PhysicalMedia():
#      print pm.Tag, pm.SerialNumber
#
# or to retrieve the serial number for the installation drive:
#
# serial = c.Win32_PhysicalMedia(["SerialNumber"],
# Tag=r"\\.\PHYSICALDRIVE0")[0].SerialNumber.strip()


# # smartctl -i /dev/sda
# smartctl version 5.38 [i686-pc-linux-gnu] Copyright (C) 2002-8 Bruce Allen
# Home page is http://smartmontools.sourceforge.net/
#
# === START OF INFORMATION SECTION ===
# Model Family: Seagate Momentus 7200.2
# Device Model: ST9200420AS
# Serial Number: 7QW138AK
# Firmware Version: 3.AAA
# User Capacity: 200,049,647,616 bytes
# Device is: In smartctl database [for details use: -P show]
# ATA Version is: 7
# ATA Standard is: Exact ATA specification draft version not indicated
# Local Time is: Thu Jun 4 09:30:23 2009 BST
# SMART support is: Available - device has SMART capability.
# SMART support is: Enabled


# import sys, os, fcntl, struct
#
# if os.geteuid() >  0:
#     print("ERROR: Must be root to use")
#     sys.exit(1)
#
# with open(sys.argv[1], "rb") as fd:
#     # tediously derived from the monster struct defined in <hdreg.h>
#     # see comment at end of file to verify
#     hd_driveid_format_str = "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"
#     # Also from <hdreg.h>
#     HDIO_GET_IDENTITY = 0x030d
#     # How big a buffer do we need?
#     sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)
#
#     # ensure our format string is the correct size
#     # 512 is extracted using sizeof(struct hd_id) in the c code
#     assert sizeof_hd_driveid == 512
#
#     # Call native function
#     buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid)
#     fields = struct.unpack(hd_driveid_format_str, buf)
#     serial_no = fields[10].strip()
#     model = fields[15].strip()
#     print("Hard Disk Model: %s" % model)
#     print("  Serial Number: %s" % serial_no)


#
# import os
#
# def get_mount_point(pathname):
#     "Get the mount point of the filesystem containing pathname"
#     pathname= os.path.normcase(os.path.realpath(pathname))
#     parent_device= path_device= os.stat(pathname).st_dev
#     while parent_device == path_device:
#         mount_point= pathname
#         pathname= os.path.dirname(pathname)
#         if pathname == mount_point: break
#         parent_device= os.stat(pathname).st_dev
#     return mount_point
#
# def get_mounted_device(pathname):
#     "Get the device mounted at pathname"
#     # uses "/proc/mounts"
#     pathname= os.path.normcase(pathname) # might be unnecessary here
#     try:
#         with open("/proc/mounts", "r") as ifp:
#             for line in ifp:
#                 fields= line.rstrip('\n').split()
#                 # note that line above assumes that
#                 # no mount points contain whitespace
#                 if fields[1] == pathname:
#                     return fields[0]
#     except EnvironmentError:
#         pass
#     return None # explicit
#
# def get_fs_freespace(pathname):
#     "Get the free space of the filesystem containing pathname"
#     stat= os.statvfs(pathname)
#     # use f_bfree for superuser, or f_bavail if filesystem
#     # has reserved space for superuser
#     return stat.f_bfree*stat.f_bsize
# Some sample pathnames on my computer:

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
