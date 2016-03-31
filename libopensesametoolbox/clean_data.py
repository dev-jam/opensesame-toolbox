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
    __string = ';'.join(stringList)
    return __string

def cleanUpStringList(stringList, delimiter):
    """
    Remove spaces and tabs from strings in a list around the delimiter
    """
    __stringList = list(stringList)
    for index in range(len(__stringList)):
        __stringList[index] = cleanUpString(__stringList[index],delimiter)

    __stringList = __stringList[:-1] if __stringList[-1] == '' else __stringList
    return __stringList

def removeJunk(stringList):
    """
    Remove trailing white space from the values in a list
    """
    __stringList = list(stringList)   
    __stringList = list(map(lambda it: it.strip(), __stringList))
    __stringList = __stringList[:-1] if __stringList[-1] == '' else __stringList
    return __stringList

def lowercaseList(stringList):
    """
    Convert strings in a list to lowercase
    """
    __stringList = list(stringList)
    for index in range(len(__stringList)):
        __stringList[index] = __stringList[index].lower()
    return __stringList

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
    __s = codecs.encode(string, 'ascii', 'osreplace')
    __s = codecs.decode(__s, 'ascii')
    return __s.replace(os.linesep, '\n')

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

    __s = ''
    for ch in exc.object[exc.start:exc.end]:
        __s += 'U+%.4X' % ord(ch)
    return __s, exc.end

codecs.register_error('osreplace', osreplace)

