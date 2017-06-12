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

from collections import MutableSequence

def BoolToString(value):
    """Converts a boolean value to an XML valid string."""

    if (value == True):
        return 'true'

    return 'false'

def GetXMLAttribute(element, attribute, defaultValue=""):
    """Returns the attribute value (if present) or the default value."""

    if (element.hasAttribute(attribute)):
        return element.getAttribute(attribute)

    return defaultValue

def GetXMLAttributes(element, attributes, defaultValue=""):
    """Returns the first value found in a list attributes.
    Returns the default value is none of the attributes are found."""

    assert(isinstance(attributes, list))

    for attribute in attributes:
        if (element.hasAttribute(attribute)):
            return element.getAttribute(attribute)

    return defaultValue

def GetXMLAttributeAsBool(element, attribute, defaultValue=False):
    """Returns the attribute value (if present) or the default value."""
        #~ Throws an exception if the string is not true, false, 1, 0
        #~ (per the XML Schema xs:boolean type)."""

    if (element.hasAttribute(attribute)):
        value = element.getAttribute(attribute)

        if (value.isdigit()):
            if (value == '1'):
                return True
            elif (value == '0'):
                return False
        elif(value.isalpha()):
            if (value.lower() == 'true'):
                return True
            elif (value.lower() == 'false'):
                return False

    return defaultValue

def GetXMLAttributeAsFloat(element, attribute, defaultValue=0.0):
    """Returns the attribute value (if present) or the default value."""

    if (element.hasAttribute(attribute)):
        value = element.getAttribute(attribute)

        try:
            return float(value)
        except:
            pass

    return defaultValue

def GetXMLAttributeAsInt(element, attribute, defaultValue=0):
    """Returns the attribute value (if present) or the default value."""

    if (element.hasAttribute(attribute)):
        value = element.getAttribute(attribute)

        try:
            return int(value)
        except:
            pass

    return defaultValue

def GetXMLAttributesAsInt(element, attributes, defaultValue=0):
    """Returns the attribute value (if present) or the default value."""

    assert(isinstance(attributes, list))

    for attribute in attributes:
        if (element.hasAttribute(attribute)):
            value = element.getAttribute(attribute)

            try:
                return int(value)
            except:
                break

    return defaultValue

def GetValidXMLAttribute(element, attribute, defaultValue, validValues):
    """Returns the attribute value (if present) or the default value.

    The value must be in the list of valid values or the default value is returned."""

    if (not (isinstance(validValues, list) or isinstance(validValues, MutableSequence))):
        raise TypeError('Parameter "validValues" is not of type "list".')

    if (element.hasAttribute(attribute)):
        value = element.getAttribute(attribute)
        if (value in validValues):
            return value

    return defaultValue

def GetValidXMLAttributes(element, attributes, defaultValue, validValues):
    """Returns the attribute value (if present) or the default value.

    The value must be in the list of valid values or the default value is returned."""

    if (not isinstance(attributes, list)):
        raise TypeError('Parameter "attributes" is not of type "list".')

    if (not (isinstance(validValues, list) or isinstance(validValues, MutableSequence))):
        raise TypeError('Parameter "validValues" is not of type "list".')

    for attribute in attributes:
        if (element.hasAttribute(attribute)):
            value = element.getAttribute(attribute)
            if (value in validValues):
                return value

    return defaultValue
