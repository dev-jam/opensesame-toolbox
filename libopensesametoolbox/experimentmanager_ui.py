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
import glob
import errno
import tempfile
import tarfile
import logging

from configobj import ConfigObj
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWebKitWidgets import QWebView

from libopensesametoolbox.logger import configureLogging
from libopensesametoolbox.experimentmanager import ExperimentManager
from libopensesametoolbox.questionnairecreator_ui import QuestionnaireCreatorUI
from libopensesametoolbox.io_tools import OutLog, getResourceLoc, findOpensesamerun
from libopensesametoolbox.clean_data import stringToBool


version = "2.7"
author = "Bob Rosbag"
email = "b.rosbag@let.ru.nl"

config = ConfigObj(getResourceLoc('opensesame-toolbox.conf'))

conf_experimentmanager_ui = config['experimentmanager_ui']

verbose     = stringToBool(conf_experimentmanager_ui['verbose'])
debug       = stringToBool(conf_experimentmanager_ui['debug'])
windowTitle = conf_experimentmanager_ui['windowTitle']

aboutString = windowTitle + """
v{0}

Copyright 2015
{1}
{2}
""".format(version,author,email)


class ExperimentManagerUI(QtWidgets.QMainWindow):
    """
    QT User interface
    """
    def __init__(self):
        """
        Initialize Experiment Manager UI
        """

        super(ExperimentManagerUI, self).__init__()
        self.fs = os.sep
        self._initConf()
        self._initHomeApp()
        self._initLogging()
        self._initDefaultValues()
        self._initUI()
        self._initWidgets()

    def _initConf(self):
        """
        Initialize config file
        """

        self.conf_default_io           = config['default_io']
        self.conf_experimentmanager_ui = config['experimentmanager_ui']
        self.conf_ui                   = config['ui']

    def _initHomeApp(self):
        """
        Initializes paths of the application
        """

        self.homeFolder = os.path.expanduser("~")

        homeAppFolderName         = self.conf_default_io['homeAppFolderName']
        homeAppLogFolder          = self.conf_default_io['homeAppLogFolder']
        homeDataFolderName        = self.conf_default_io['homeDataFolderName']

        homeExperimentFolderName  = self.conf_experimentmanager_ui['homeExperimentFolderName']
        dataTarFileName           = self.conf_experimentmanager_ui['dataTarFileName']

        self.homeAppFolder        = os.path.join(self.homeFolder, homeAppFolderName)
        self.homeAppLogFolder     = os.path.join(self.homeAppFolder, homeAppLogFolder)
        self.homeDataFolder       = os.path.join(self.homeFolder, homeDataFolderName)

        self.homeExperimentFolder = os.path.join(self.homeDataFolder, homeExperimentFolderName)
        self.homeDataLogFolder    = os.path.join(self.homeDataFolder, 'logs')

        self.dataTarFile = getResourceLoc(dataTarFileName)

        if not os.path.exists(self.homeAppFolder):
            os.mkdir(self.homeAppFolder)
        if not os.path.exists(self.homeAppLogFolder):
            os.mkdir(self.homeAppLogFolder)
        if not os.path.exists(self.homeDataFolder):
            os.mkdir(self.homeDataFolder)
        if not os.path.exists(self.homeDataLogFolder):
            os.mkdir(self.homeDataLogFolder)
        if not os.path.exists(self.homeExperimentFolder):
            with tarfile.open(self.dataTarFile, "r:gz") as dataTar:
                dataTar.extractall(path=self.homeDataFolder)

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
        Initialize default values
        """

        # Load resource paths
        self.uiPath       = getResourceLoc(self.conf_experimentmanager_ui['uiPath'])
        self.icoPath      = getResourceLoc(self.conf_experimentmanager_ui['icoPath'])
        self.helpimgPath  = getResourceLoc(self.conf_ui['helpimgPath'])
        self.aboutimgPath = getResourceLoc(self.conf_ui['aboutimgPath'])
        self.labelimgPath = getResourceLoc(self.conf_experimentmanager_ui['labelimgPath'])

        # set commands
        self.opensesamerunCommandAuto = findOpensesamerun()
        self.settingsExtension = self.conf_experimentmanager_ui['settingsExtension']
        self.defaultName       = 'default.' + self.settingsExtension
        self.extFilterSettings = self.settingsExtension + " (*." + self.settingsExtension + ")"
        self.extFilterAll      = "All Files" + " (*)"

        # default folders
        self.destinationFolder          = ""
        self._lastSelectedDestDir       = ""
        self._lastSelectedSourceDir     = ""
        self.pythonCommandManual        = ""
        self.opensesamerunCommandManual = ""

        # default text
        self.windowTitle = self.conf_experimentmanager_ui['windowTitle']
        self.StatusBoxHeight = int(self.conf_experimentmanager_ui['StatusBoxHeight'])

        # default folder
        self.sourceFolder = self.homeExperimentFolder
        print(self.sourceFolder)

        # default widget values
        self.defaultResolutionHorizontalInteger = int(self.conf_experimentmanager_ui['defaultResolutionHorizontalInteger'])
        self.defaultResolutionVerticalInteger   = int(self.conf_experimentmanager_ui['defaultResolutionVerticalInteger'])
        self.extensionList                      = list(self.conf_experimentmanager_ui['extensionList'])


    def _initUI(self):
        """
        Initializes the UI and sets button actions
        """

        # icons
        self.helpIcon   = QtGui.QIcon(self.helpimgPath)
        self.aboutIcon  = QtGui.QIcon(self.aboutimgPath)
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
        self.srcCheckBox.setChecked(False)
        self.inputFolderLocation.setText(self.sourceFolder)
        self.fullscreenCheckBox.setChecked(True)
        self.customResolutionCheckBox.setChecked(False)
        self.resolutionHorizontalSpinBox.setValue(self.defaultResolutionHorizontalInteger)
        self.resolutionVerticalSpinBox.setValue(self.defaultResolutionVerticalInteger)

        # set statusbox
        self.statusBox.setReadOnly(True)
        self.statusBox.hide()

        # show/hide default widgets
        self.pythonLabel.hide()
        self.pythonLineEdit.hide()
        self.pythonButton.hide()
        self.resolutionHorizontalLabel.hide()
        self.resolutionHorizontalSpinBox.hide()
        self.resolutionVerticalLabel.hide()
        self.resolutionVerticalSpinBox.hide()

        # set Gui image
        self.image.setPixmap(self.pixmap)

        # set context menu
        self.experimentListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.experimentListWidget.customContextMenuRequested.connect(self.listItemRightClicked)

        if not self.opensesamerunCommandAuto:
            self.opensesamerunLabel.show()
            self.opensesamerunLineEdit.show()
            self.opensesamerunButton.show()
            self.opensesameNotFoundLabel.show()

        else:
            self.opensesamerunLabel.hide()
            self.opensesamerunLineEdit.hide()
            self.opensesamerunButton.hide()
            self.opensesameNotFoundLabel.hide()

        # Set button actions
        self.inputFolderButton.clicked.connect(self.selectInputFolderLocation)
        self.logFolderButton.clicked.connect(self.selectLogFolderDestination)
        self.startButton.clicked.connect(self.startExperiments)
        self.docButton.clicked.connect(self.showDocWindow)
        self.aboutButton.clicked.connect(self.showAboutWindow)
        self.restoreSettingsButton.clicked.connect(self.selectOpenSettingsFile)
        self.saveSettingsButton.clicked.connect(self.selectSaveSettingsFile)
        self.opensesamerunButton.clicked.connect(self.selectOpensesamerunFile)
        self.pythonButton.clicked.connect(self.selectPythonFile)
        self.createOpenButton.clicked.connect(self.addOpenQuestion)
        self.createMCButton.clicked.connect(self.addMCQuestion)
        self.refreshButton.clicked.connect(self.refreshWidgets)
        self.resetButton.clicked.connect(self.resetButtonClicked)

        # set checkbox actions
        self.srcCheckBox.stateChanged.connect(self.updaterunFromSource)
        self.customResolutionCheckBox.stateChanged.connect(self.updateCustomResolution)

        if verbose:
            self.statusBox.show()
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

    def _initWidgets(self):

        # set empty strings, lists and dicts
        self.currentLangString = ''
        self.langList = []
        self.languageComboBoxItemList = []
        self.experimentFileListDict = {}
        self.widgetItemObjectListDict = {}
        self.widgetItemNameListDict = {}

        self.experimentListWidget.clear()
        self.languageComboBox.clear()
        self.refreshWidgets()

    def startExperiments(self):
        """
        Starts the sanity checks and if passed then the execution of experiments.
        """

        if not self.sourceFolder:
            errorMessage = "Please select a source folder containing the experiment files."
            print(errorMessage, file=sys.stderr)
            self.showErrorMessage(errorMessage)
            return
        elif not self.destinationFolder :
            errorMessage = "Please select a log folder."
            print(errorMessage, file=sys.stderr)
            self.showErrorMessage(errorMessage)
        elif not self.subjectLineEdit.text().strip().isdigit():
            errorMessage = "Please enter an integer as subject number."
            print(errorMessage, file=sys.stderr)
            self.showErrorMessage(errorMessage)
            return
        elif not self.srcCheckBox.isChecked() and not self.opensesamerunCommandAuto and not self.opensesamerunCommandManual:
            error_message = "Please specify the path to the opensesamerun executable."
            print(error_message, file=sys.stderr)
            self.showErrorMessage(error_message)
            return
        elif self.srcCheckBox.isChecked() and not self.opensesamerunCommandManual:
            error_message = "Please specify the path to the opensesamerun source file."
            print(error_message, file=sys.stderr)
            self.showErrorMessage(error_message)
            return
        elif self.srcCheckBox.isChecked() and not self.pythonCommandManual:
            error_message = "Please specify the path to the python 2 executable."
            print(error_message, file=sys.stderr)
            self.showErrorMessage(error_message)
            return

        else:

            selectedSubjectNr = self.subjectLineEdit.displayText().strip()

            if self.srcCheckBox.isChecked():
                self.opensesamerunCommand = self.opensesamerunCommandManual
                self.pythonCommand  = self.pythonCommandManual
            else:
                if self.opensesamerunCommandAuto:
                    self.opensesamerunCommand = self.opensesamerunCommandAuto
                    self.pythonCommand = ''
                else:
                    self.opensesamerunCommand = self.opensesamerunCommandManual
                    self.pythonCommand  = ''

            fullscreen = self.fullscreenCheckBox.isChecked()
            customResolution = self.customResolutionCheckBox.isChecked()

            if customResolution:
                resolutionHorizontal = str(self.resolutionHorizontalSpinBox.value())
                resolutionVertical   = str(self.resolutionVerticalSpinBox.value())
            else:
                resolutionHorizontal = None
                resolutionVertical   = None


            [selectedExperimentList, selectedLanguage] = self.getSelectedExperimentData()

            if not selectedExperimentList:
                errorMessage = "No experiments selected, please select at least one experiment."
                print(errorMessage, file=sys.stderr)
                self.showErrorMessage(errorMessage)
                return
            else:
                pass

            logFileExists = None
            logDestinationFilePathList = []
            for experiment in selectedExperimentList:
                strippedExperiment = experiment
                logDestinationFolder = os.path.join(self.destinationFolder, selectedLanguage, strippedExperiment)
                logDestinationFile = 'subject-' + selectedSubjectNr + '.csv'
                logDestinationFilePath = os.path.join(logDestinationFolder, logDestinationFile)
                logDestinationFilePathList.append(logDestinationFilePath)

                try:
                    os.makedirs(logDestinationFolder)
                except OSError as exc: # Python >2.5
                    if exc.errno == errno.EEXIST and os.path.isdir(logDestinationFolder):
                        pass
                    else: raise

                if  os.path.isfile(logDestinationFilePath):
                    logFileExists = True
                else:
                    pass

            if logFileExists:
                overwriteCheck = self.confirmOverwriteEvent()
                if not overwriteCheck:
                    return
                else:
                    pass
            elif not logFileExists:
                overwriteCheck = True
            else:
                overwriteCheck = False
                return

            if overwriteCheck:
                print("Starting Experiment...")
                finishedExperiment = ExperimentManager(self.pythonCommand, self.opensesamerunCommand,
                                                       self.sourceFolder, logDestinationFilePathList,
                                                       selectedSubjectNr, selectedLanguage, selectedExperimentList,
                                                       fullscreen, customResolution,resolutionHorizontal, resolutionVertical)

                if finishedExperiment:
                    print("Output saved to " + self.destinationFolder)
                    print("Ready.")
                    return
                else:
                    errorMessage = "Error: Could not start the experiments! Did you select the correct opensesamerun and Python File?"
                    print(errorMessage, file=sys.stderr)
                    self.showErrorMessage(errorMessage)
                    return
            else:
                errorMessageList = []
                self.showErrorMessage(''.join(errorMessageList))
                return


    def listItemRightClicked(self, QPos):
        """
        Add right click context menu to the ListWidget
        """
        self.listMenu= QtWidgets.QMenu()
        renameItem = self.listMenu.addAction("Rename Questionnaire on disk")
        removeItem = self.listMenu.addAction("Delete Questionnaire from disk")

        if self.experimentListWidget.count() == 0:
            renameItem.setDisabled(True)
            removeItem.setDisabled(True)

        renameItem.triggered.connect(self.renameItemClicked)
        removeItem.triggered.connect(self.removeItemClicked)

        parentPosition = self.experimentListWidget.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)

        self.listMenu.show()

    def renameItemClicked(self):
        """
        Create right click rename method
        """
        if self.experimentListWidget.count() == 0:
            return

        currentWidget       = self.experimentListWidget.currentItem()
        currentItemName     = self.experimentListWidget.currentItem().text()
        currentItemLanguage = self.languageComboBox.currentText()

        fileExistsCheck = True
        go = True
        noChange = False

        while fileExistsCheck and go and not noChange:

            destItemValueTuple = self.renameEvent(currentItemName)
            go = destItemValueTuple[1]
            destItemName = destItemValueTuple[0]

            srcFilePath  = os.path.join(self.sourceFolder, currentItemLanguage, currentItemName)
            destFilePath = os.path.join(self.sourceFolder, currentItemLanguage, destItemName)

            if srcFilePath ==  destFilePath:
                noChange = True

            fileExistsCheck = os.path.exists(destFilePath)

            if fileExistsCheck and not noChange and go:
                errorMessage = "A questionnaire with that filename already exists, please select another name"
                self.showErrorMessage(errorMessage)

        if go and not fileExistsCheck:

            try:
                self.renameQuestionnaire(srcFilePath, destFilePath)
            except Exception:
                errorMessage = 'Access denied, cannot rename experiment, do you have the correct permissions?'
                self.showErrorMessage(errorMessage)
                return

            currentWidget.setText(destItemName)

            expindex = self.experimentFileListDict[currentItemLanguage].index(currentItemName)
            self.experimentFileListDict[currentItemLanguage][expindex] = destItemName

            nameindex = self.widgetItemNameListDict[currentItemLanguage].index(currentItemName)
            self.widgetItemNameListDict[currentItemLanguage][nameindex] = destItemName

    def removeItemClicked(self):
        """
        Create right click remove item method
        """
        if self.experimentListWidget.count() == 0:
            return

        currentWidget = self.experimentListWidget.currentItem()
        currentItemName = currentWidget.text()
        currentItemLanguage = self.languageComboBox.currentText()

        if self.confirmDeleteEvent():

            try:
                self.removeQuestionnaire(currentItemName, currentItemLanguage)
            except Exception:
                errorMessage = 'Access denied, cannot delete experiment, do you have the correct permissions?'
                self.showErrorMessage(errorMessage)
                return

            widgetIndex = self.experimentListWidget.row(currentWidget)
            self.experimentListWidget.takeItem(widgetIndex)

            self.experimentFileListDict[currentItemLanguage].remove(currentItemName)
            self.widgetItemObjectListDict[currentItemLanguage].remove(currentWidget)
            self.widgetItemNameListDict[currentItemLanguage].remove(currentItemName)

    def renameQuestionnaire(self,srcFilePath,destFilePath):
        """
        Rename item on disk
        """
        if  os.path.isfile(srcFilePath) and not os.path.exists(destFilePath):
            os.rename(srcFilePath, destFilePath)

    def removeQuestionnaire(self,fileName,lang):
        """
        Remove item from disk
        """
        filePath = os.path.join(self.sourceFolder, lang, fileName)
        if  os.path.isfile(filePath):
            os.remove(filePath)

    def isWritable(self, path):
        """
        Check if path is writable by creating a temp file
        """
        try:
            testfile = tempfile.TemporaryFile(dir = path)
            testfile.close()
            return True
        except Exception:
            return False

    def resetButtonClicked(self):
        """
        Reset the listwidget to initial state
        """
        answer = self.confirmResetEvent()
        if answer:
            self._initWidgets()
        else:
            pass

    def renameEvent(self,original):
        """
        Confirm box renaming item on disk
        """
        reply = QtWidgets.QInputDialog.getText(self, "Please enter the new name.", "Filename:", QtWidgets.QLineEdit.Normal, original)
        return reply

    def addMCQuestion(self):
        """
        Start the MC questionnaire creator with write check
        """
        if self.isWritable(self.sourceFolder):
            self.mc = QuestionnaireCreatorUI(self.languageComboBox.currentText(),self.langList,self.sourceFolder,'mc')
            reply = self.mc.exec_()

            if reply:
                [widgetItemName, lang] = self.mc.getValues()
                self.processQuestion(widgetItemName, lang)
            else:
                pass

        else:
            errorMessage = 'Access denied, cannot write in questionnaire folder, please change questionnaire folder.'
            self.showErrorMessage(errorMessage)

    def addOpenQuestion(self):
        """
        Start the open questionnaire creator with write check
        """
        if self.isWritable(self.sourceFolder):
            self.open = QuestionnaireCreatorUI(self.languageComboBox.currentText(),self.langList,self.sourceFolder,'open')
            reply = self.open.exec_()

            if reply:
                [widgetItemName, lang] = self.open.getValues()
                self.processQuestion(widgetItemName, lang)
            else:
                pass
        else:
            errorMessage = 'Access denied, cannot write in questionnaire folder, please change questionnaire folder.'
            self.showErrorMessage(errorMessage)

    def processQuestion(self,widgetItemName, lang):
        """
        Add the questionnaire to the dicts and widgets
        """
        listWidgetItem = self.createListWidgetItem(widgetItemName)

        if lang not in self.widgetItemNameListDict:
            self.widgetItemNameListDict[lang] = []
        if lang not in self.widgetItemObjectListDict:
            self.widgetItemObjectListDict[lang] = []
        if lang not in self.experimentFileListDict:
            self.experimentFileListDict[lang] = []
        else:
            pass

        self.widgetItemNameListDict[lang].append(widgetItemName)
        self.widgetItemObjectListDict[lang].append(listWidgetItem)
        self.experimentFileListDict[lang].append(widgetItemName)

        if lang == self.languageComboBox.currentText():
            self.experimentListWidget.addItem(listWidgetItem)
        else:
            pass

    def startRestoreSettings(self, settingsFilePath):
        """
        Restore settings from ini file
        """
        if os.path.isfile(settingsFilePath):
            self.settingsRestore = QtCore.QSettings(settingsFilePath, QtCore.QSettings.IniFormat)
            self.refreshWidgets()
            self.restoreSettings()
        else:
            errorMessage = "File not found, nothing to restore."
            print(errorMessage, file=sys.stderr)
            self.showErrorMessage(errorMessage)

    def startSaveSettings(self, settingsFilePath):
        """
        Save settings to ini file
        """
        self.settingsSave = QtCore.QSettings(settingsFilePath, QtCore.QSettings.IniFormat)
        self.saveSettings()

    def selectSaveSettingsFile(self):
        """
        Save settings file dialog
        """
        selectedSettingsDest = QtWidgets.QFileDialog.getSaveFileName(self,"Save output as..", self.defaultName, self.extFilterSettings)
        # Prevent erasing previous entry on cancel press
        if selectedSettingsDest[0]:
            self.startSaveSettings(selectedSettingsDest[0])

    def selectOpenSettingsFile(self):
        """
        Open settings file dialog
        """
        selectedSettingsLocation = QtWidgets.QFileDialog.getOpenFileName(self,"Open File..", self.defaultName, self.extFilterSettings)
        # Prevent erasing previous entry on cancel press
        if selectedSettingsLocation[0]:
            self.startRestoreSettings(selectedSettingsLocation[0])

    def selectOpensesamerunFile(self):
        """
        Set file to write output to
        """
        selectedOpensesamerunLocation = QtWidgets.QFileDialog.getOpenFileName(self,"Open File..", self.homeFolder, self.extFilterAll)
        # Prevent erasing previous entry on cancel press
        if selectedOpensesamerunLocation[0]:
            self.opensesamerunCommandManual = selectedOpensesamerunLocation[0]
            self.opensesamerunLineEdit.setText(os.path.normpath(self.opensesamerunCommandManual))

    def selectPythonFile(self):
        """
        Set file to write output to
        """
        selectedPythonLocation = QtWidgets.QFileDialog.getOpenFileName(self,"Open File..", self.homeFolder, self.extFilterAll)
        # Prevent erasing previous entry on cancel press
        if selectedPythonLocation[0]:
            self.pythonCommandManual = selectedPythonLocation[0]
            self.pythonLineEdit.setText(os.path.normpath(self.pythonCommandManual))

    def selectInputFolderLocation(self):
        """
        Select folder to read csv files from
        """
        selectedFolder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.inputFolderLocation.text())
        # Prevent erasing previous entry on cancel press
        if selectedFolder:
            self.sourceFolder = selectedFolder
            self.inputFolderLocation.setText(os.path.normpath(self.sourceFolder))
            self._initWidgets()

    def selectLogFolderDestination(self):
        """
        Set file to write output to
        """
        selectedDest = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.logFolderDestination.text())
        # Prevent erasing previous entry on cancel press
        if selectedDest:
            self.destinationFolder = selectedDest
            self.logFolderDestination.setText(os.path.normpath(self.destinationFolder))

    def refreshWidgets(self):
        """
        Refresh widgets
        """
        try: self.languageComboBox.currentIndexChanged.disconnect(self.updateListWidget)
        except Exception: pass

        self.emptyListWidget()
        self.updateDirs()
        self.updateListWidgetItems()
        self.updateComboBoxItems()
        self.fillListWidget()

        self.languageComboBox.currentIndexChanged.connect(self.updateListWidget)

    def updateDirs(self):
        """
        Process and update directories
        """
        langList = list(self.langList)

        for item in sorted(os.listdir(self.sourceFolder)):
            languageDir = os.path.join(self.sourceFolder, item)
            if os.path.isfile(languageDir):
                pass
            else:
                if item not in langList:
                    self.langList.append(item)
                    self.experimentFileListDict[item] = []
                else:
                    pass

                expFileList = []
                for extension in self.extensionList:
                    expFileList.extend(glob.glob(languageDir + self.fs + '*' + extension))

                expFileList = sorted(expFileList)

                for expFilePath in expFileList:
                    expFile = os.path.basename(expFilePath)
                    if os.path.isfile(expFilePath):
                        if expFile not in self.experimentFileListDict[item]:
                            self.experimentFileListDict[item].append(expFile)
                        else:
                            pass
                    else:
                        pass

        for lang in langList:
            languageDir = os.path.join(self.sourceFolder, lang)

            if not os.path.isdir(languageDir):
                self.langList.remove(lang)
                del self.experimentFileListDict[lang]
            else:
                for expFile in self.experimentFileListDict[lang]:
                    filePath = os.path.join(languageDir, expFile)
                    if not os.path.isfile(filePath):
                        self.experimentFileListDict[lang].remove(expFile)
                    else:
                        pass

    def updateComboBoxItems(self):
        """
        Process and update the languageComboBox
        """
        comboBoxItemList = list(self.languageComboBoxItemList)

        for lang in self.langList:
            if lang not in comboBoxItemList:
                self.languageComboBox.addItem(lang)
                self.languageComboBoxItemList.append(lang)
            else:
                pass

        for lang in comboBoxItemList:
            if lang not in self.langList:

                if self.languageComboBox.currentText() == lang:
                    index1 = self.languageComboBox.findText(self.langList[0],QtCore.Qt.MatchExactly)
                    self.languageComboBox.setCurrentIndex(index1)
                else:
                    pass

                self.languageComboBoxItemList.remove(lang)
                index = self.languageComboBox.findText(lang,QtCore.Qt.MatchExactly)
                self.languageComboBox.removeItem(index)
            else:
                pass

    def updateListWidgetItems(self):
        """
        Process and update the ListWidget items
        """
        widgetItemNameListDictKeys =  list(self.widgetItemNameListDict)

        for lang in self.langList:
            expnameList = self.experimentFileListDict[lang]
            if lang not in widgetItemNameListDictKeys:
                self.widgetItemNameListDict[lang] = []
                self.widgetItemObjectListDict[lang] = []

            else:
                pass

            for index in range(len(expnameList)):
                widgetItemName = expnameList[index]
                if widgetItemName not in self.widgetItemNameListDict[lang]:
                    listWidgetItem = self.createListWidgetItem(widgetItemName)
                    self.widgetItemNameListDict[lang].append(widgetItemName)
                    self.widgetItemObjectListDict[lang].append(listWidgetItem)
                else:
                    pass

        for lang in widgetItemNameListDictKeys:

            if lang not in self.langList:
                del self.widgetItemNameListDict[lang]
                del self.widgetItemObjectListDict[lang]

            else:
                for widgetItemName in self.widgetItemNameListDict[lang]:
                    if widgetItemName not in self.experimentFileListDict[lang]:
                        widgetIndex = self.widgetItemNameListDict[lang].index(widgetItemName)
                        del self.widgetItemObjectListDict[lang][widgetIndex]
                        del self.widgetItemNameListDict[lang][widgetIndex]
                    else:
                        pass

    def createListWidgetItem(self, widgetItem):
        """
        Create a ListWidget item
        """
        listWidgetItem = QtWidgets.QListWidgetItem(widgetItem)
        listWidgetItem.setCheckState(QtCore.Qt.Checked)
        listWidgetItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled)

        return listWidgetItem

    def updateListWidget(self):
        """
        Update the ListWidget
        """
        self.emptyListWidget()
        self.fillListWidget()

    def emptyListWidget(self):
        """
        Empty the ListWidget
        """
        nrListWidgetItems = self.experimentListWidget.count()
        if not self.currentLangString == '' or not nrListWidgetItems  == 0:
            lang = self.currentLangString

            widgetList = list(self.widgetItemObjectListDict[lang])
            widgetNameList = list(self.widgetItemNameListDict[lang])


            self.widgetItemNameListDict[lang] = []
            self.widgetItemObjectListDict[lang] = []

            for index in range(nrListWidgetItems):
                listWidgetItem = self.experimentListWidget.takeItem(0)
                widgetIndex = widgetList.index(listWidgetItem)

                self.widgetItemNameListDict[lang].append(widgetNameList[widgetIndex])
                self.widgetItemObjectListDict[lang].append(listWidgetItem)

    def fillListWidget(self):
        """
        Fill the ListWidget
        """
        lang = self.languageComboBox.currentText()
        if not lang == '':
            listWidgetItemList = list(self.widgetItemObjectListDict[lang])

            for row in range(len(listWidgetItemList)):
                self.experimentListWidget.insertItem(row,listWidgetItemList[row])
                #self.experimentListWidget.item(row).setCheckState(QtCore.Qt.Checked)

        self.currentLangString = self.languageComboBox.currentText()

    def getSelectedExperimentData(self):
        """
        Get the language and experiment list from the widgets
        """
        selectedExperimentList = []
        selectedLanguage = self.languageComboBox.currentText()

        nWidgets = self.experimentListWidget.count()
        for index in range(nWidgets):
            listWidgetItem = self.experimentListWidget.item(index)
            if listWidgetItem.checkState() == 2:
                selectedExperimentList.append(listWidgetItem.text())

        return [selectedExperimentList, selectedLanguage]

    def updaterunFromSource(self):
        """
        Get the language and experiment list from the widgets
        """
        if self.srcCheckBox.isChecked():
            self.pythonLabel.show()
            self.pythonLineEdit.show()
            self.pythonButton.show()
            self.opensesamerunLabel.show()
            self.opensesamerunLineEdit.show()
            self.opensesamerunButton.show()
        else:
            self.pythonLabel.hide()
            self.pythonLineEdit.hide()
            self.pythonButton.hide()
            if not self.opensesamerunCommandAuto:
                self.opensesamerunLabel.show()
                self.opensesamerunLineEdit.show()
                self.opensesamerunButton.show()
            else:
                self.opensesamerunLabel.hide()
                self.opensesamerunLineEdit.hide()
                self.opensesamerunButton.hide()

    def updateCustomResolution(self):
        """
        Get the language and experiment list from the widgets
        """
        if self.customResolutionCheckBox.isChecked():
            self.resolutionHorizontalLabel.show()
            self.resolutionHorizontalSpinBox.show()
            self.resolutionVerticalLabel.show()
            self.resolutionVerticalSpinBox.show()
        else:
            self.resolutionHorizontalLabel.hide()
            self.resolutionHorizontalSpinBox.hide()
            self.resolutionVerticalLabel.hide()
            self.resolutionVerticalSpinBox.hide()

    def saveSettings(self):
        """
        Save GUI values to ini file
        """
        [selectedExperimentList, selectedLanguage] = self.getSelectedExperimentData()

        self.settingsSave.setValue('srcCheckBox', self.srcCheckBox.isChecked())
        self.settingsSave.setValue('customResolutionCheckBox', self.customResolutionCheckBox.isChecked())
        self.settingsSave.setValue('fullscreenCheckBox', self.fullscreenCheckBox.isChecked())
        self.settingsSave.setValue('sourceFolder', self.sourceFolder)
        self.settingsSave.setValue('destinationFolder', self.destinationFolder)
        self.settingsSave.setValue('pythonCommandManual', self.pythonCommandManual)
        self.settingsSave.setValue('opensesamerunCommandManual', self.opensesamerunCommandManual)
        self.settingsSave.setValue('resolutionHorizontalSpinBox', self.resolutionHorizontalSpinBox.value())
        self.settingsSave.setValue('resolutionVerticalSpinBox', self.resolutionVerticalSpinBox.value())
        self.settingsSave.setValue('languageComboBox', selectedLanguage)
        self.settingsSave.setValue('selectedExperimentList', selectedExperimentList)


    def restoreSettings(self):
        """
        Restore GUI values from ini file
        """

        errorMessageList = []
        errorMessageExperimentList = []

        srcCheckBox = self.settingsRestore.value('srcCheckBox')
        self.srcCheckBox.setChecked(stringToBool(srcCheckBox))

        fullscreenCheckBox = self.settingsRestore.value('fullscreenCheckBox')
        self.fullscreenCheckBox.setChecked(stringToBool(fullscreenCheckBox))

        customResolutionCheckBox = self.settingsRestore.value('customResolutionCheckBox')
        self.customResolutionCheckBox.setChecked(stringToBool(customResolutionCheckBox))

        resolutionHorizontalSpinBox = int(self.settingsRestore.value('resolutionHorizontalSpinBox'))
        self.resolutionHorizontalSpinBox.setValue(resolutionHorizontalSpinBox)

        resolutionVerticalSpinBox = int(self.settingsRestore.value('resolutionVerticalSpinBox'))
        self.resolutionVerticalSpinBox.setValue(resolutionVerticalSpinBox)


        sourceFolder = self.settingsRestore.value('sourceFolder')
        if sourceFolder:
            if os.path.isdir(sourceFolder):
                self.sourceFolder = sourceFolder
                self.inputFolderLocation.setText(os.path.normpath(sourceFolder))
                self._initWidgets()
            else:
                errorMessageList.append('- Experiment folder not found! Using current experiment folder\n')
        else:
            pass


        destinationFolder = self.settingsRestore.value('destinationFolder')
        if destinationFolder:
            if os.path.isdir(destinationFolder):
                self.destinationFolder = destinationFolder
                self.logFolderDestination.setText(os.path.normpath(destinationFolder))
            else:
                errorMessageList.append('- Log folder not found! Using current log folder\n')
        else:
            pass


        pythonCommandManual = self.settingsRestore.value('pythonCommandManual')
        if pythonCommandManual:
            if os.path.isfile(pythonCommandManual):
                self.pythonCommandManual = pythonCommandManual
                self.pythonLineEdit.setText(os.path.normpath(pythonCommandManual))
            else:
                errorMessageList.append('- Python file not found! Using current Python file\n')
        else:
            pass


        opensesamerunCommandManual = self.settingsRestore.value('opensesamerunCommandManual')
        if opensesamerunCommandManual:
            if os.path.isfile(opensesamerunCommandManual):
                self.opensesamerunCommandManual = opensesamerunCommandManual
                self.opensesamerunLineEdit.setText(os.path.normpath(opensesamerunCommandManual))
            else:
                errorMessageList.append('- Opensesamerun File not found! Using current Opensesamerun File\n')
        else:
            pass


        languageComboBox = self.settingsRestore.value('languageComboBox')
        if languageComboBox:
            index = self.languageComboBox.findText(languageComboBox)
            if index == -1:
                errorMessageList.append('- Language not found in current language folder! Cannot restore language and experiments.\n')
                self.showErrorMessage(''.join(errorMessageList))
                return
            else:
                self.languageComboBox.setCurrentIndex(index)
        else:
            errorMessageList.append('- No language present in restore file! Cannot restore language and experiments.\n')
            self.showErrorMessage(''.join(errorMessageList))
            return


        selectedExperimentList = self.settingsRestore.value('selectedExperimentList')
        if selectedExperimentList:
            nWidgets = self.experimentListWidget.count()
            for index in range(nWidgets):
                self.experimentListWidget.item(index).setCheckState(QtCore.Qt.Unchecked)

            counter = 0
            for selectedExperiment in selectedExperimentList:
                try:
                    [listWidgetItem] = self.experimentListWidget.findItems(selectedExperiment,QtCore.Qt.MatchExactly)
                    currentIndex = self.experimentListWidget.row(listWidgetItem)
                    targetWidget = self.experimentListWidget.takeItem(currentIndex)
                    targetWidget.setCheckState(QtCore.Qt.Checked)
                    self.experimentListWidget.insertItem(counter,targetWidget)
                    counter += 1
                except Exception:
                    errorMessageExperimentList.append('- ' + selectedExperiment + ' not found in data, not restoring this item.\n')
        else:
            errorMessageList.append('- No experiments present in restore file! Cannot restore experiments.\n')
            self.showErrorMessage(''.join(errorMessageList))
            return

        if errorMessageList:
            self.showErrorMessage(''.join(errorMessageList))
        else:
            pass

        if errorMessageExperimentList:
            self.showErrorMessage(''.join(errorMessageExperimentList))
        else:
            pass

    def center(self):
        """
        Centers the main app window on the screen
        """
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def confirmDeleteEvent(self):
        """
        Confirm box deleting item from disk
        """
        message = "Are you sure to delete this questionnaire from disk?"

        reply = self.confirmEvent(message)
        return reply

    def confirmResetEvent(self):
        """
        Confirm box deleting item from disk
        """
        message = "Are you sure you want to reset the experiment selection and order?"

        reply = self.confirmEvent(message)
        return reply

    def confirmOverwriteEvent(self):
        """
        Confirm box deleting item from disk
        """
        message =  "Log file(s) already exists, do you want to overwrite the log file(s)?"

        reply = self.confirmEvent(message)
        return reply

    def confirmEvent(self, message):
        """
        Confirm box overwriting (log) files
        """
        reply = QtWidgets.QMessageBox.question(self, 'Message',
            message, QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            reply = True
        else:
            reply = False
        return reply

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
