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

import glob

from distutils.core import setup

from libopensesametoolbox import experimentmanager_ui


setup(name="opensesame-toolbox",

	version = str(experimentmanager_ui.version),
	description = "OpenSesame Toolbox can manage/execute all kinds of OpenSesame experiments. Additionally it can create and process scores from OpenSesame Questionnaires",
	author = "Bob Rosbag",
	author_email = "debian@bobrosbag.nl",
	url = "https://github.com/dev-jam/opensesame-toolbox",
	scripts = ["opensesame-experiment-manager","opensesame-questionnaire-processor"],
	packages = [ \
		"libopensesametoolbox", \
		],
	package_dir = { \
		"libopensesametoolbox" : "libopensesametoolbox", \
		},
	data_files=[
		("/usr/share/opensesame-toolbox", ["COPYING"]), \
		("/usr/share/applications", ["data/opensesame-experiment-manager.desktop","data/opensesame-questionnaire-processor.desktop"]), \
		("/usr/share/opensesame-toolbox/resources", glob.glob("resources/*")),
		]
	)
