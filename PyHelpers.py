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

import os.path, sys, unicodedata
from collections import MutableSequence
from functools import reduce

if (sys.platform == 'win32'):
    from win32api import GetVolumeInformation

BAD_FILENAME_CHARACTERS = "|^?*<>[]=+\"\\/,:;"

# def ReplaceNone(variable, value):
#     """ The idea is "if variable is None: variable = value".  BUT you can't get
#         there from here. What we want to do is replace is an immutable variable
#         and Python doesn't allow them to be passed by reference.
#     """
#     pass



def NormalizeFileName(filename):
    """Clean up the file name by replacing or deleting bad characters."""

    # On windows, certain device names are reserved.
    # For instance, you can't create a file named "nul", "nul.txt" (or nul.anything in fact) The reserved names are:
    # CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, and LPT9

    # unicodedata.normalize replaces accented characters with the unaccented equivalent
    cleanFilename = unicodedata.normalize('NFKD', filename.strip())
    # cleanFilename = unicodedata.normalize('NFKD', filename.strip()).encode('ASCII', 'ignore')
    cleanFilename = ''.join(c for c in cleanFilename if c not in BAD_FILENAME_CHARACTERS)

    return cleanFilename

def GetVolumeLabel(path):
    """ Returns the volume label for a given path.

        This only works under Windows.  Linux does really have disk volumes, so
        it doesn't have volume labels.  An RuntimeError is raised if this
        function is called and the platform is not 'win32'.
    """
    if (sys.platform != 'win32'):
        raise RuntimeError('Method GetVolueLabel(path) was called but the OS is not Windows.')

    drive, tail = os.path.splitdrive(self.dirpickerctrlSource.GetPath().strip())
    return GetVolumeInformation(drive)[0]

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)

    return reduce(lambda x,y:x+y, lst)

def TimedeltaToString(td, noZeroDays=True):
    """ Based on an answer found ton stackoverflow.
    """
    if (td.days > 0):
        out = str(td).replace(' days, ', ':')
    else:
        if (noZeroDays):
            out = str(td)
        else:
            out = '0:' + str(td)

    outAr = out.split(':')
    outAr = ['%02d' % (int(float(x))) for x in outAr]
    out   = ':'.join(outAr)

    return out

class TemporaryFilesList(MutableSequence):
    """ Contains a list of temporary files.

        The temporary files will be deleted when the unlink() method is called
        or when the object destructor is called.
    """

    def __init__(self):
        super().__init__()
        self.temporaryFilenames = []

    def __del__(self):
        self.unlink()

    # MutableSequence abstract methods
    # ==========================================================================
    def __getitem__(self, idx):
        return self.temporaryFilenames[idx]

    def __setitem__(self, idx, obj):
        self.temporaryFilenames[idx] = obj

    def __delitem__(self, idx):
        del self.temporaryFilenames[idx]

    def __len__(self):
        return len(self.temporaryFilenames)

    def insert(self, idx, obj):
        self.temporaryFilenames.insert(idx, obj)
    # ==========================================================================

    def clear(self):
        """ Remove all the file names from the list.  The files will not be
            deleted.
        """
        del self.temporaryFilenames[:]

    def unlink(self):
        """ Delete all of the temporary files in the list then clear the list.
        """
        for temporaryFilename in self.temporaryFilenames:
            try:
                os.unlink(temporaryFilename)
            except:
                pass

        self.clear()
