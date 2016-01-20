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

# Run the build process by running the command 'python setup-cxfreeze_win32.py bdist_msi'
#
# If everything works well you should find an installer in the dist directory

import sys

from cx_Freeze import setup, Executable

from libopensesametoolbox import experimentmanager_ui


base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ['atexit', 'PyQt5.QtPrintSupport'], 
        'include_msvcr': True,
        'include_files': [('resources','resources')	]
    }
}

executables = [
    Executable('opensesame-experiment-manager', base=base, shortcutName="OpenSesame Experiment Manager", shortcutDir="StartMenuFolder"),
    Executable('opensesame-questionnaire-processor', base=base, shortcutName="OpenSesame Questionnaire Processor", shortcutDir="StartMenuFolder")
]

setup(name='OpenSesame Toolbox',
      version=str(experimentmanager_ui.version),
      description='OpenSesame Toolbox',
      options=options,
      executables=executables
      )
