# -*- coding: utf-8 -*-
"""
This file is part of OpenSesame Toolbox

OpenSesame Toolbox is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame Experiment Manager is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Refer to <http://www.gnu.org/licenses/> for a copy of the GNU General Public License.

@author Bob Rosbag
"""

import codecs
import os


def cleanUpString(string, delimiter):
    """
    Remove spaces and tabs from strings around the delimiter
    """
    stringList = string.split(delimiter)
    stringList = removeJunk(stringList)
    string = ';'.join(stringList)
    return string

def cleanUpStringList(stringList, delimiter):
    """
    Remove spaces and tabs from strings in a list around the delimiter
    """
    for index in range(len(stringList)):
        stringList[index] = cleanUpString(stringList[index],delimiter)

    stringList = stringList[:-1] if stringList[-1] == '' else stringList
    return stringList

def removeJunk(stringList):
    """
    Remove trailing white space from the values in a list
    """
    stringList = list(map(lambda it: it.strip(), stringList))
    stringList = stringList[:-1] if stringList[-1] == '' else stringList
    return stringList

def lowercaseList(stringList):
    """
    Convert strings in a list to lowercase
    """
    for index in range(len(stringList)):
        stringList[index] = stringList[index].lower()
    return stringList

def stringToBool(string):
    if string == 'true' or string == 'True' or string == '1':
        return True
    elif string == 'false' or string == 'False' or string =='0':
        return False
    else:
        raise ValueError

def usanitize(string):
    """
    Convert unicode to ascii plus opensame-style replacement of unicode
    """
    _s = codecs.encode(string, 'ascii', 'osreplace')
    _s = codecs.decode(_s, 'ascii')
    return _s.replace(os.linesep, '\n')

def osreplace(exc):

    """
    desc:
        A replacement function to allow opensame-style replacement of unicode
        characters.

    arguments:
        exc:
        type:	UnicodeEncodeError

    returns:
        desc:	A (replacement, end) tuple.
        type:	tuple
    """

    _s = ''
    for ch in exc.object[exc.start:exc.end]:
        _s += 'U+%.4X' % ord(ch)
    return _s, exc.end

codecs.register_error('osreplace', osreplace)

