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

import site
import sys
import os

from PyQt5 import QtCore, QtGui


def getResourceLoc(name):

    """
    A hacky way to get a resource using the functionality from openexp

    Arguments:
    name    --    The name of the requested resource. If this is a regular string
                it is assumed to be encoded as utf-8.

    Returns:
    A Unicode string with the full path to the resource.
    """

    for folder in base_folders:
        path = os.path.join(folder, 'opensesametoolbox_resources',name)
        if os.path.exists(path):
            return path
    return None

def findOpensesamerun():

    if os.name == "nt":
        if os.path.isfile('C:\\Program Files (x86)\\OpenSesame\\opensesamerun.exe'):
            command =  os.path.abspath('C:\\Program Files (x86)\\OpenSesame\\opensesamerun.exe')
        elif os.path.isfile('C:\\Program Files\\OpenSesame\\opensesamerun.exe'):
            command = os.path.abspath('C:\\Program Files\\OpenSesame\\opensesamerun.exe')
        else:
            command = ""
    elif os.name == "posix":
        if os.path.isfile('/usr/bin/opensesamerun'):
            command = '/usr/bin/opensesamerun'
        else:
            command = ""
    else:
        command = ""

    return command


def home_folder():

    """
    Determines the home folder.

    Returns:
    A path to the home folder.
    """

    import platform
    if platform.system() == "Windows":
        home_folder = os.environ["APPDATA"]
    elif platform.system() == "Darwin":
        home_folder = os.environ[u"HOME"]
    elif platform.system() == "Linux":
        home_folder = os.environ["HOME"]
    else:
        home_folder = os.environ["HOME"]
    return home_folder


base_folders = []
cwd = os.getcwd()
parent_folder = os.path.dirname(os.path.dirname(__file__))
base_folders = [cwd, parent_folder]
if hasattr(site, 'getuserbase'):
    base_folders.append(os.path.join(site.getuserbase(), 'share'))
if hasattr(site, 'getusersitepackages'):
    base_folders.append(os.path.join(site.getusersitepackages(),'share'))
if hasattr(site, 'getsitepackages'):
    base_folders += \
        [os.path.join(folder, 'share') \
        for folder in site.getsitepackages()]
base_folders += ['/usr/local/share', '/usr/share']
# Locate Anaconda/Miniconda share
base_folders.append(os.path.join(os.path.dirname(os.path.dirname(sys.executable)),"share"))
base_folders = list(filter(os.path.exists, base_folders))



class OutLog(object):
    """
    Class that intercepts stdout and stderr prints, and shows them in te QT
    textarea of the app.
    """
    def __init__(self, statusBox, out=None, color=None):
        """(statusBox, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.statusBox = statusBox
        self.out = out
        self.color = color

    def write(self, m):
        self.statusBox.moveCursor(QtGui.QTextCursor.End)
        if self.color:
            self.statusBox.setTextColor(self.color)

        self.statusBox.insertPlainText( m )
        # Make sure the messages are immediately shown
        QtCore.QCoreApplication.instance().processEvents()

        if self.out:
            self.out.write(m)
