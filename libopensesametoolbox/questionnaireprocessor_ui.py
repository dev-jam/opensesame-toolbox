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

import sys
import os
import logging

from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWebKitWidgets import QWebView
from configobj import ConfigObj

from libopensesametoolbox.logger import configureLogging
from libopensesametoolbox.questionnaireprocessor import QuestionnaireProcessor
from libopensesametoolbox.io_tools import OutLog, getResourceLoc
from libopensesametoolbox.clean_data import cleanUpString, cleanUpStringList, removeJunk, stringToBool

version = "2.6"
author = "Bob Rosbag"
email = "b.rosbag@let.ru.nl"

config = ConfigObj(getResourceLoc('opensesame-toolbox.conf'))

conf_questionnaireprocessor_ui = config['questionnaireprocessor_ui']

verbose     = stringToBool(conf_questionnaireprocessor_ui['verbose'])
debug       = stringToBool(conf_questionnaireprocessor_ui['debug'])
windowTitle = conf_questionnaireprocessor_ui['windowTitle']


aboutString = windowTitle + """
v{0}

Copyright 2015
{1}
{2}
""".format(version,author,email)


class QuestionnaireProcessorUI(QtWidgets.QMainWindow):
    """
    QT User interface
    """
    def __init__(self):
        """
        Initialize Questionnaire Processor UI
        """

        super(QuestionnaireProcessorUI, self).__init__()

        self._initConf()
        self._initHomeApp()
        self._initLogging()
        self._initDefaultValues()
        self._initUI()

    def _initConf(self):
        """
        Initialize config file
        """

        self.conf_default_io                = config['default_io']
        self.conf_questionnaireprocessor_ui = config['questionnaireprocessor_ui']
        self.conf_ui                        = config['ui']
        self.conf_default_input             = config['default_input']
        self.conf_format                    = config['format']

    def _initHomeApp(self):
        """
        Initializes paths of the application
        """

        self.homeFolder = os.path.expanduser("~")

        homeAppFolderName         = self.conf_default_io['homeAppFolderName']
        homeAppLogFolder          = self.conf_default_io['homeAppLogFolder']

        self.homeAppFolder        = os.path.join(self.homeFolder, homeAppFolderName)
        self.homeAppLogFolder     = os.path.join(self.homeAppFolder, homeAppLogFolder)

        if not os.path.exists(self.homeAppFolder):
            os.mkdir(self.homeAppFolder)
        if not os.path.exists(self.homeAppLogFolder):
            os.mkdir(self.homeAppLogFolder)

    def _initLogging(self):
        """
        Initializes paths of the application
        """
        fileName = 'errors_' + windowTitle.replace(' ', '-').lower() + '.log'
        errorLogPath = os.path.join(self.homeAppLogFolder, fileName)
        if debug:
            level = logging.DEBUG
        else:
            level = logging.ERROR
        configureLogging(errorLogPath, level)

    def _initDefaultValues(self):
        """
        Initializes default values
        """

        # Load resources
        self.idKey                   = self.conf_default_input['idKey']
        self.responseKey             = self.conf_default_input['responseKey']
        self.categoryKey             = self.conf_default_input['categoryKey']
        self.answerKey               = self.conf_default_input['answerKey']
        self.scoreKey                = self.conf_default_input['scoreKey']

        ## remove illegal characters
        self.illegalCharacterList = self.conf_format['illegalCharacterList']

        self.defaultIdentityList  = self.conf_default_input['defaultIdList']
        self.defaultCategoryList  = self.conf_default_input['defaultCategoryList']
        self.defaultAnswerString  = self.conf_default_input['defaultAnswerString']
        self.defaultScoreList     = self.conf_default_input['defaultScoreList']

        # Load resource paths
        self.uiPath       = getResourceLoc(self.conf_questionnaireprocessor_ui['uiPath'])
        self.icoPath      = getResourceLoc(self.conf_questionnaireprocessor_ui['icoPath'])
        self.helpimgPath  = getResourceLoc(self.conf_ui['helpimgPath'])
        self.aboutimgPath = getResourceLoc(self.conf_ui['aboutimgPath'])
        self.labelimgPath = getResourceLoc(self.conf_questionnaireprocessor_ui['labelimgPath'])

        # default folders
        self.sourceFolder = ""
        self.destinationFolder = ""
        self._lastSelectedDestDir = ""
        self._lastSelectedSourceDir = ""

        # default text
        self.windowTitle = self.conf_questionnaireprocessor_ui['windowTitle']
        self.StatusBoxHeight = int(self.conf_questionnaireprocessor_ui['StatusBoxHeight'])



    def _initUI(self):
        """
        Initializes the UI, sets button actions and default values
        """

        # icons
        self.helpIcon  = QtGui.QIcon(self.helpimgPath)
        self.aboutIcon = QtGui.QIcon(self.aboutimgPath)
        self.windowIcon = QtGui.QIcon(self.icoPath)

        # images
        self.pixmap = QtGui.QPixmap(self.labelimgPath)

        # Load and setup UI
        uic.loadUi(self.uiPath, self)

        self.windowHorizontalResolution = self.width()

        if verbose:
            self.windowVerticalResolution  = self.height()
        else:
            self.windowVerticalResolution  = self.height() - self.StatusBoxHeight

        # set default window values
        self.setWindowIcon(self.windowIcon)
        self.setFixedSize(self.windowHorizontalResolution,self.windowVerticalResolution)
        self.setWindowTitle(self.windowTitle)
        self.center()

        # set icons
        self.docButton.setIcon(self.helpIcon)
        self.aboutButton.setIcon(self.aboutIcon)

        # set default values
        self.idColumnLineEdit.setText(self.idKey)
        self.responseColumnLineEdit.setText(self.responseKey)
        self.categoryColumnLineEdit.setText(self.categoryKey)
        self.answerOptionColumnLineEdit.setText(self.answerKey)
        self.answerScoreColumnLineEdit.setText(self.scoreKey)
        self.idCustomPlainTextEdit.setPlainText('\n'.join(self.defaultIdentityList))
        self.categoryCustomPlainTextEdit.setPlainText('\n'.join(self.defaultCategoryList))
        self.answerCustomLineEdit.setText(self.defaultAnswerString)
        self.scoreCustomPlainTextEdit.setPlainText('\n'.join(self.defaultScoreList))
        self.caseInsensitiveCheckBox.setChecked(True)

        # set statusbox
        self.statusBox.setReadOnly(True)
        self.statusBox.hide()

        # set GUI image
        self.image.setPixmap(self.pixmap)

        ## hide custom column elements
        self.idColumnLabel.hide()
        self.idColumnLineEdit.hide()
        self.responseColumnLabel.hide()
        self.responseColumnLineEdit.hide()
        self.categoryColumnLabel.hide()
        self.categoryColumnLineEdit.hide()
        self.answerOptionColumnLabel.hide()
        self.answerOptionColumnLineEdit.hide()
        self.answerScoreColumnLabel.hide()
        self.answerScoreColumnLineEdit.hide()
        #self.line_2.hide()

        ## hide custom score elements
        self.idCustomLabel.hide()
        self.idCustomPlainTextEdit.hide()
        self.categoryCustomLabel.hide()
        self.categoryCustomPlainTextEdit.hide()
        self.answerCustomLabel.hide()
        self.answerCustomLineEdit.hide()
        self.scoreCustomLabel.hide()
        self.scoreCustomPlainTextEdit.hide()
        self.customExperimentCheckBox.hide()

        # Set button actions
        self.inputFolderButton.clicked.connect(self.selectInputFolderLocation)
        self.outputFolderButton.clicked.connect(self.selectOutputFolderDestination)
        self.processButton.clicked.connect(self.startAnalysis)
        self.docButton.clicked.connect(self.showDocWindow)
        self.aboutButton.clicked.connect(self.showAboutWindow)

        # Set checkbox actions
        self.customColumnCheckBox.stateChanged.connect(self.updateCustomColumnWidgets)
        self.customExperimentCheckBox.stateChanged.connect(self.updateCustomExperimentWidgets)

        if verbose:
            self.statusBox.show()
            self.label.hide()
        else:
            pass

        if verbose and not debug:

            # Redirect console output to textbox in UI, printing stdout in black
            # and stderr in red
            sys.stdout = OutLog(self.statusBox, sys.stdout, QtGui.QColor(0,0,0))
            if not hasattr(sys,'frozen'):
                sys.stderr = OutLog(self.statusBox, sys.stderr, QtGui.QColor(255,0,0))
            else:
                sys.stderr = OutLog(self.statusBox, None, QtGui.QColor(255,0,0))
            print("")
        else:
            pass

    def startAnalysis(self):
        """
        Starts sanity checks and if passed starts the analyze operation.
        """

        # check if sourceFolder is selected
        if self.sourceFolder == "":
            errorMessage = "Please select a source folder containing the data files to merge."
            print(errorMessage, file=sys.stderr)
            self.showErrorMessage(errorMessage)
            return
        # check if destinationFolder is selected
        elif self.destinationFolder == "":

            errorMessage = "Please specify a folder to save the results."
            print(errorMessage, file=sys.stderr)
            self.showErrorMessage(errorMessage)
            return

        else:
            print("Starting Analyze operation...")

            # set the default keys
            responseKey  = self.responseKey
            idKey        = self.idKey
            categoryKey  = self.categoryKey
            answerKey    = self.answerKey
            scoreKey     = self.scoreKey

            idList       = None
            categoryList = None
            answerList   = None
            scoreList    = None

            caseInsensitiveComparison = self.caseInsensitiveCheckBox.isChecked()

            if not self.customColumnCheckBox.isChecked():

                # calculate score automatically
                custom = False
                analyzedDataset = QuestionnaireProcessor(self.sourceFolder, self.destinationFolder, responseKey, idKey, categoryKey, 
                                                         answerKey, scoreKey, idList, categoryList, answerList, scoreList, custom, 
                                                         caseInsensitiveComparison, self)

                if analyzedDataset:
                    print("Output saved to " + self.destinationFolder)
                    print("Ready.")
                else:
                    pass


            elif self.customColumnCheckBox.isChecked() and not self.customExperimentCheckBox.isChecked():

                # calculate score with the given column keys
                responseKey = self.responseColumnLineEdit.text()
                idKey       = self.idColumnLineEdit.text()
                categoryKey = self.categoryColumnLineEdit.text()
                answerKey   = self.answerOptionColumnLineEdit.text()
                scoreKey    = self.answerScoreColumnLineEdit.text()

                custom = False

                ## check for illegal character
                stringCheck = None

                checkStringList = [responseKey, idKey, categoryKey, answerKey, scoreKey]

                for index in range(len(checkStringList)):
                    for illegalCharacter in self.illegalCharacterList:
                        if illegalCharacter in checkStringList[index]:
                            checkStringList[index] = checkStringList[index].replace(illegalCharacter, '')
                            stringCheck = True
                        else:
                            pass

                if stringCheck:

                    errorMessage = "The following characters are not allowed and have been stripped: double-quote (\") and backslash (\\)"
                    print(errorMessage, file=sys.stderr)
                    self.showErrorMessage(errorMessage)

                    self.responseColumnLineEdit.setText(checkStringList[0])
                    self.idColumnLineEdit.setText(checkStringList[1])
                    self.categoryColumnLineEdit.setText(checkStringList[2])
                    self.answerOptionColumnLineEdit.setText(checkStringList[3])
                    self.answerScoreColumnLineEdit.setText(checkStringList[4])

                    return

                else:
                    pass

                if responseKey != "" and idKey != "" and categoryKey != "" and answerKey != "" and scoreKey != "":

                    analyzedDataset = QuestionnaireProcessor(self.sourceFolder, self.destinationFolder, responseKey, idKey, categoryKey, 
                                                             answerKey, scoreKey, idList, categoryList, answerList, scoreList, custom, 
                                                             caseInsensitiveComparison, self)

                    if analyzedDataset:
                        print("Output saved to " + self.destinationFolder)
                        print("Ready.")
                    else:
                        pass
                else:
                    ## show error message if checks failed
                    errorMessage = "Not all column names are defined."
                    print(errorMessage, file=sys.stderr)
                    self.showErrorMessage(errorMessage)
                    return

            # calculate score with the custom given experiment data
            elif self.customColumnCheckBox.isChecked() and self.customExperimentCheckBox.isChecked():

                # set custom bool
                custom = True

                # get values from the widgets
                responseKey    = self.responseColumnLineEdit.text()
                idKey          = self.idColumnLineEdit.text()
                idString       = self.idCustomPlainTextEdit.toPlainText()
                answerString   = self.answerCustomLineEdit.text()
                categoryString = self.categoryCustomPlainTextEdit.toPlainText()
                scoreString    = self.scoreCustomPlainTextEdit.toPlainText()

                ## String Checks
                stringCheck = None

                checkStringList = [responseKey,idKey,idString, answerString, categoryString, scoreString]

                for index in range(len(checkStringList)):
                    for illegalCharacter in self.illegalCharacterList:
                        if illegalCharacter in checkStringList[index]:
                            checkStringList[index] = checkStringList[index].replace(illegalCharacter, '')
                            stringCheck = True
                        else:
                            pass

                if stringCheck:

                    errorMessage = "The following characters are not allowed and have been stripped: double-quote (\"), backslash (\\) and tab"
                    print(errorMessage, file=sys.stderr)
                    self.showErrorMessage(errorMessage)

                    self.responseColumnLineEdit.setText(checkStringList[0])
                    self.idColumnLineEdit.setText(checkStringList[1])
                    self.idCustomPlainTextEdit.setPlainText(checkStringList[2])
                    self.answerCustomLineEdit.setText(checkStringList[3])
                    self.categoryCustomPlainTextEdit.setPlainText(checkStringList[4])
                    self.scoreCustomPlainTextEdit.setPlainText(checkStringList[5])

                    return

                else:
                    pass


                ## split string to list and remove last enter
                idList       = (idString[:-1] if idString.endswith('\n') else idString).split('\n')
                categoryList = (categoryString[:-1] if categoryString.endswith('\n') else categoryString).split('\n')
                scoreList    = (scoreString[:-1] if scoreString.endswith('\n') else scoreString).split('\n')

                ## clean up items
                idList       = removeJunk(idList)
                categoryList = cleanUpStringList(categoryList,';')
                scoreList    = cleanUpStringList(scoreList,';')
                answerString = cleanUpString(answerString,';')

                ## make answer list for counting
                answerItemList = answerString.split(';')

                ## determine number of elements
                ncategory = len(categoryList)
                nscore    = len(scoreList)
                nid       = len(idList)
                nanswers  = len(answerItemList)

                ## replicate answer option to a list with length ntrials
                answerList = []
                for index in range(len(idList)):
                    answerList.append(answerString)

                ## number check
                nScoreItemList = []
                checkList = []
                for item in scoreList:
                    scoreItemList = item.split(';')
                    nScoreItemList.append(len(scoreItemList))
                    checkList.append(all(element.isdigit()==True for element in scoreItemList))

                numberCheck = all(item==True for item in checkList)

                ## check if all score lines have equal number of elements (seperated by ;) and is equal to
                ## the number of elements of answers
                uniqueScoreItemList = list(set(nScoreItemList))
                if len(uniqueScoreItemList)==1:

                    uniqueItems = uniqueScoreItemList[0]
                    if uniqueItems == nanswers:
                        scoreCheck = True
                    else:
                        scoreCheck = False
                else:
                    scoreCheck = False

                ## combine checks and show error if applicable
                if nid == ncategory == nscore and scoreCheck and numberCheck:
                    analyzedDataset = QuestionnaireProcessor(self.sourceFolder, self.destinationFolder, responseKey, idKey, categoryKey,
                                                             answerKey, scoreKey, idList, categoryList, answerList, scoreList, custom,
                                                             caseInsensitiveComparison, self)

                    if analyzedDataset:
                        print("Output saved to " + self.destinationFolder)
                        print("Ready.")
                    else:
                        pass
                else:
                    ## show error messages if checks failed
                    errorMessageList = []

                    if not (nid == ncategory == nscore and scoreCheck):
                        errorMessageList.append('- Not all fields have the correct number of elements\n')
                    if not numberCheck:
                        errorMessageList.append('- Field \"score\" should contain only integers seperated by \";\", found other characters\n')

                    self.showErrorMessage(''.join(errorMessageList))
                    return
            else:
                pass

    def updateCustomColumnWidgets(self):
        """
        Show custom column widgets when checkbox is checked else hide
        """
        if self.customColumnCheckBox.isChecked() :
            self.idColumnLabel.show()
            self.idColumnLineEdit.show()
            self.responseColumnLabel.show()
            self.responseColumnLineEdit.show()
            self.categoryColumnLabel.show()
            self.categoryColumnLineEdit.show()
            self.answerOptionColumnLabel.show()
            self.answerOptionColumnLineEdit.show()
            self.answerScoreColumnLabel.show()
            self.answerScoreColumnLineEdit.show()
            #self.line_2.show()

            self.customExperimentCheckBox.show()

            self.updateCustomExperimentWidgets()

        else:
            self.idColumnLabel.hide()
            self.idColumnLineEdit.hide()
            self.responseColumnLabel.hide()
            self.responseColumnLineEdit.hide()
            self.categoryColumnLabel.hide()
            self.categoryColumnLineEdit.hide()
            self.answerOptionColumnLabel.hide()
            self.answerOptionColumnLineEdit.hide()
            self.answerScoreColumnLabel.hide()
            self.answerScoreColumnLineEdit.hide()
            #self.line_2.hide()

            self.customExperimentCheckBox.hide()
            self.idCustomLabel.hide()
            self.idCustomPlainTextEdit.hide()
            self.categoryCustomLabel.hide()
            self.categoryCustomPlainTextEdit.hide()
            self.answerCustomLabel.hide()
            self.answerCustomLineEdit.hide()
            self.scoreCustomLabel.hide()
            self.scoreCustomPlainTextEdit.hide()
            self.customExperimentCheckBox.hide()

    def updateCustomExperimentWidgets(self):
        """
        Show custom experiment widgets (and hide some column widget elements)
        when checkbox is checked else hide
        """
        if self.customExperimentCheckBox.isChecked():
            self.idCustomLabel.show()
            self.idCustomPlainTextEdit.show()
            self.categoryCustomLabel.show()
            self.categoryCustomPlainTextEdit.show()
            self.answerCustomLabel.show()
            self.answerCustomLineEdit.show()
            self.scoreCustomLabel.show()
            self.scoreCustomPlainTextEdit.show()

            self.categoryColumnLabel.hide()
            self.categoryColumnLineEdit.hide()
            self.answerOptionColumnLabel.hide()
            self.answerOptionColumnLineEdit.hide()
            self.answerScoreColumnLabel.hide()
            self.answerScoreColumnLineEdit.hide()

        else:
            self.idCustomLabel.hide()
            self.idCustomPlainTextEdit.hide()
            self.categoryCustomLabel.hide()
            self.categoryCustomPlainTextEdit.hide()
            self.answerCustomLabel.hide()
            self.answerCustomLineEdit.hide()
            self.scoreCustomLabel.hide()
            self.scoreCustomPlainTextEdit.hide()

            self.categoryColumnLabel.show()
            self.categoryColumnLineEdit.show()
            self.answerOptionColumnLabel.show()
            self.answerOptionColumnLineEdit.show()
            self.answerScoreColumnLabel.show()
            self.answerScoreColumnLineEdit.show()

    def selectInputFolderLocation(self):
        """
        Select folder to read csv files from
        """
        selectedFolder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.inputFolderLocation.text())
        # Prevent erasing previous entry on cancel press
        if selectedFolder:
            self.sourceFolder = selectedFolder
            self.inputFolderLocation.setText(os.path.normpath(self.sourceFolder))
            self.progressBar.setValue(0)

    def selectOutputFolderDestination(self):
        """
        Set folder to write output to
        """
        selectedDest = QtWidgets.QFileDialog.getExistingDirectory(self,"Save output in..", directory=self.outputFolderDestination.text())
        # Prevent erasing previous entry on cancel press
        if selectedDest:
            self.destinationFolder = selectedDest
            self.outputFolderDestination.setText(os.path.normpath(self.destinationFolder))
            self.progressBar.setValue(0)

    def center(self):
        """
        Centers the main app window on the screen
        """
        qr = self.frameGeometry()
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDocWindow(self):
        """
        Shows documentation window (with help and licensing info)
        """

        title = "Documentation"
        htmlFile = "helpfile.html"

        self.docWindow = QWebView()
        self.docWindow.closeEvent = self.closeDocWindow
        self.docWindow.setWindowTitle(title)
        self.docWindow.setWindowIcon(self.helpIcon)
        self.docWindow.load(QtCore.QUrl.fromLocalFile(getResourceLoc(htmlFile)))
        self.docWindow.show()

    def closeDocWindow(self,source):
        """
        Callback function of the docWindow QWebView item.
        Destroys reference to doc window after its closed
        """
        del(self.docWindow)

    def showAboutWindow(self):
        """
        Shows about window
        """
        about ="About"

        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowIcon(self.aboutIcon)
        msgBox.about(self, about, aboutString)

    def showErrorMessage(self, message):
        """
        Shows error message
        """
        error ="Error"

        msgBox = QtWidgets.QMessageBox(self)
        msgBox.about(self, error, message)

    def confirmEvent(self, message):
        """
        Confirm box
        """
        reply = QtWidgets.QMessageBox.question(self, 'Message',
            message, QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            reply = True
        else:
            reply = False
        return reply

    def closeEvent(self, event):
        """
        Confirm closing the main window
        """
        message = "Are you sure to quit?"

        reply = self.confirmEvent(message)

        if reply:
            event.accept()
        else:
            event.ignore()
