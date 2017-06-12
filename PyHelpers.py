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

import unicodedata

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
