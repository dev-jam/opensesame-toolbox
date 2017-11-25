#!/usr/bin/env python3
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

import os
from setuptools import setup
import fnmatch
from libopensesametoolbox import experimentmanager_ui


EXCLUDE = [
    u'[\\/].*',
    u'*~',
    u'*.pyc',
    u'*.pyo',
    u'*__pycache__*'
    ]

def is_excluded(path):

    for m in EXCLUDE:
        if fnmatch.fnmatch(path, m):
            return True
    return False

def resources():

    """
    desc:
        Create a list of all resource files that need to be included

    returns:
        A list of (target folder, filenames) tuples.
    """

    l = []
    for root, dirnames, filenames in os.walk('opensesametoolbox_resources'):
        for f in filenames:
            path = os.path.join(root, f)
            if not is_excluded(path):
                l.append((os.path.join('share', root), [path]))
    return l


def data_files():

    return [
        ("share/icons/hicolor/scalable/apps", ["data/opensesame-toolbox.svg"]),
        ("share/mime/packages", ["data/x-opensesame-experiment-manager.xml"]),
        ("share/applications", ["data/opensesame-experiment-manager.desktop","data/opensesame-questionnaire-processor.desktop"])] + \
        resources()

setup(
    name="opensesame-toolbox",
    version = str(experimentmanager_ui.version),
    description = "OpenSesame Toolbox can manage/execute all kinds of OpenSesame experiments. Additionally it can create and process scores from OpenSesame Questionnaires",
    author = "Bob Rosbag",
    author_email = "debian@bobrosbag.nl",
    url = "https://github.com/dev-jam/opensesame-toolbox",
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    scripts = ['opensesame-experiment-manager','opensesame-questionnaire-processor'],
    packages = [ \
        "libopensesametoolbox", \
        ],
    package_dir = {
        "libopensesametoolbox" : "libopensesametoolbox",
        },
    data_files=data_files(),
    )
