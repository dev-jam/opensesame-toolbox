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
import sys
import subprocess
from configobj import ConfigObj

from libopensesametoolbox.io_tools import getResourceLoc
from libopensesametoolbox.clean_data import stringToBool

config = ConfigObj(getResourceLoc('opensesame-toolbox.conf'))

conf_experimentmanager_ui = config['experimentmanager_ui']
debug       = stringToBool(conf_experimentmanager_ui['debug'])


def ExperimentManager(pythonCommand, command, expFolder, logDestinationFileList,
                      subjectNr, languageString, experimentList, fullscreen,
                      customResolution,resolutionHorizontal, resolutionVertical):
        """
        Initialize Experiment Manager UI
        """

        conf_experimentmanager = config['experimentmanager']
        
        subjectParameter              = conf_experimentmanager['subjectParameter']
        logParameter                  = conf_experimentmanager['logParameter']
        resolutionHorizontalParameter = conf_experimentmanager['resolutionHorizontalParameter']
        resolutionVerticalParameter   = conf_experimentmanager['resolutionVerticalParameter']
        fullscreenParameter           = conf_experimentmanager['fullscreenParameter']
        debugParameter                = conf_experimentmanager['debugParameter']

        noErrors = True

        for index in range(len(experimentList)):

            fileName      = os.path.join(expFolder,languageString,experimentList[index])
            subjectArg    = subjectParameter + subjectNr
            logArg        = logParameter + logDestinationFileList[index]

            args = []

            if pythonCommand:
                args.append(pythonCommand)
            else:
                pass

            ## main args
            args += [command, fileName, subjectArg, logArg]

            if customResolution:
                args.append(resolutionHorizontalParameter + resolutionHorizontal)
                args.append(resolutionVerticalParameter + resolutionVertical)
            else:
                pass

            if fullscreen:
                args.append(fullscreenParameter)
            else:
                pass

            if debug:
                args.append(debugParameter)
                print(args)
            else:
                pass


            try:
                subprocess.call(args)
                #output = subprocess.check_output(args)
                #output = subprocess.check_output(' '.join(args), stderr=subprocess.STDOUT, shell=True)
                #print('Got stdout: ', output)

            except:
                noErrors=False


        sys.stdout.write('\nTotal process done!\n')
        return noErrors
