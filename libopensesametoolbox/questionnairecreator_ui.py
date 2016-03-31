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
import errno

from PyQt5 import QtWidgets, uic
from configobj import ConfigObj

from libopensesametoolbox.questionnairecreator import QuestionnaireCreator
from libopensesametoolbox.io_tools import getResourceLoc
from libopensesametoolbox.clean_data import cleanUpString, cleanUpStringList, removeJunk

config = ConfigObj(getResourceLoc('opensesame-toolbox.conf'))


class QuestionnaireCreatorUI(QtWidgets.QDialog):

    """GUI Class to create questionnaires"""

    def __init__(self,currentLang,availableLang,sourceFolder,kind):

        """
        Constructor.

        Arguments:
        lang            -- Language
        sourceFolder    -- Folder containing the experiments
        kind            -- type of questionnaire (mc or open)
        """

        # invoke the parents
        super(QuestionnaireCreatorUI, self).__init__()

        self.currentLang   = currentLang
        self.availableLang = availableLang
        self.sourceFolder  = sourceFolder
        self.kind = kind
        self.fs = os.sep

        self._initConf()
        self._initDefaultValues()
        self._initUI()

    def _initConf(self):
        self.conf_questionnairecreator_ui = config['questionnairecreator_ui']
        self.conf_default_input           = config['default_input']
        self.conf_format                  = config['format']

    def _initDefaultValues(self):

        ## get the ui file path
        self.uiPath      = getResourceLoc(self.conf_questionnairecreator_ui['uiPath'])

        ## set file names
        self.mcFile       = getResourceLoc(self.conf_questionnairecreator_ui['mcFile'])
        self.openFile     = getResourceLoc(self.conf_questionnairecreator_ui['openFile'])

        self.mcFilePath   = getResourceLoc(self.mcFile)
        self.openFilePath = getResourceLoc(self.openFile)

        ## replace illegal characters
        self.illegalCharacterList = self.conf_format['illegalCharacterList']


        # set default values
        self.defaultBgcolorString               = self.conf_questionnairecreator_ui['defaultBgcolorString']
        self.defaultFgcolorString               = self.conf_questionnairecreator_ui['defaultFgcolorString']
        self.defaultOrderString                 = self.conf_questionnairecreator_ui['defaultOrderString']
        self.defaultBackendString               = self.conf_questionnairecreator_ui['defaultBackendString']
        self.defaultResolutionHorizontalInteger = int(self.conf_questionnairecreator_ui['defaultResolutionHorizontalInteger'])
        self.defaultResolutionVerticalInteger   = int(self.conf_questionnairecreator_ui['defaultResolutionVerticalInteger'])
        self.defaultInstructionTitleString      = self.conf_questionnairecreator_ui['defaultInstructionTitleString']
        self.defaultInstructionString           = self.conf_questionnairecreator_ui['defaultInstructionString']
        self.defaultQuestionnaireTitleString    = self.conf_questionnairecreator_ui['defaultQuestionnaireTitleString']
        self.defaultQuestionList                = self.conf_questionnairecreator_ui['defaultQuestionList']
        self.defaultIdList                      = self.conf_default_input['defaultIdList']

        if self.kind == 'mc':

            self.defaultAnswerString = self.conf_default_input['defaultAnswerString']
            self.defaultCategoryList = self.conf_default_input['defaultCategoryList']
            self.defaultScoreList    = self.conf_default_input['defaultScoreList']

        else:
            pass

    def _initUI(self):

        """Setup the UI.	"""

        ## load UI
        uic.loadUi(self.uiPath, self)

        ## set connect buttons
        self.addQuestionButton.clicked.connect(self.makeQuestionnaire)
        self.cancelButton.clicked.connect(self.reject)

        ## set values
        self.backendComboBox.insertItems(0,self.defaultBackendString)
        self.bgColorComboBox.insertItems(0,self.defaultBgcolorString)
        self.fgColorComboBox.insertItems(0,self.defaultFgcolorString)
        self.orderComboBox.insertItems(0,self.defaultOrderString)
        self.instructionPlainTextEdit.setPlainText(self.defaultInstructionString)
        self.instructionTitleLineEdit.setText(self.defaultInstructionTitleString)
        self.questionnaireTitleLineEdit.setText(self.defaultQuestionnaireTitleString)
        self.questionPlainTextEdit.setPlainText('\n'.join(self.defaultQuestionList))
        self.idPlainTextEdit.setPlainText('\n'.join(self.defaultIdList))
        self.resolutionHorizontalSpinBox.setValue(self.defaultResolutionHorizontalInteger)
        self.resolutionVerticalSpinBox.setValue(self.defaultResolutionVerticalInteger)
        self.languageLineEdit.setText(self.currentLang)


        if self.kind == 'mc':

            ## set widget values
            self.label.setText('Create MC Questionnaire')
            self.answerLineEdit.setText(self.defaultAnswerString)
            self.categoryPlainTextEdit.setPlainText('\n'.join(self.defaultCategoryList))
            self.scorePlainTextEdit.setPlainText('\n'.join(self.defaultScoreList))

        elif self.kind == 'open':

            ## set widget values
            self.label.setText('Create Open Questionnaire')
            self.answerLineEdit.hide()
            self.categoryPlainTextEdit.hide()
            self.scorePlainTextEdit.hide()
            self.answerLabel.hide()
            self.categoryLabel.hide()
            self.scoreLabel.hide()

        else:
            pass

    def makeQuestionnaire(self):

        """Create the questionnaire.	"""

        ## get values from widgets
        nameString               = self.nameLineEdit.text()
        bgcolorString            = self.bgColorComboBox.currentText()
        fgcolorString            = self.fgColorComboBox.currentText()
        backendString            = self.backendComboBox.currentText()
        orderString              = self.orderComboBox.currentText()
        resolutionHorizontal     = str(self.resolutionHorizontalSpinBox.value())
        resolutionVertical       = str(self.resolutionVerticalSpinBox.value())

        instructionTitleString   = self.instructionTitleLineEdit.text()
        instructionString        = self.instructionPlainTextEdit.toPlainText()
        questionnaireTitleString = self.questionnaireTitleLineEdit.text()
        languageString           = self.languageLineEdit.text()
        questionString           = self.questionPlainTextEdit.toPlainText()
        idString                 = self.idPlainTextEdit.toPlainText()



        if self.kind == 'mc':
            answerString = self.answerLineEdit.text()
            categoryString = self.categoryPlainTextEdit.toPlainText()
            scoreString = self.scorePlainTextEdit.toPlainText()
        elif self.kind == 'open':
            answerString = None
            categoryList = None
            scoreList = None
        else:
            pass

        ## check for illegal characters
        stringCheck = None

        if '/' in nameString:
            nameString = nameString.replace('/','')
            stringCheck = True
        else:
            pass

        checkStringList = [nameString, instructionTitleString, instructionString,
                           questionnaireTitleString, languageString, questionString, idString]

        if self.kind == 'mc':
            checkMCStringList = [answerString, categoryString, scoreString]
            checkStringList = checkStringList + checkMCStringList
        else:
            pass



        for index in range(len(checkStringList)):
            for illegalCharacter in self.illegalCharacterList:
                if illegalCharacter in checkStringList[index]:
                    checkStringList[index] = checkStringList[index].replace(illegalCharacter, '')
                    stringCheck = True
                else:
                    pass

        if stringCheck:

            errorMessage = ("The following characters are not allowed and have been stripped: double-quote (\") and backslash (\\) "
                            "are generally not allowed and slash (/) is not allowed in filename.")
            print(errorMessage, file=sys.stderr)
            self.showErrorMessage(errorMessage)

            self.nameLineEdit.setText(checkStringList[0])
            self.instructionTitleLineEdit.setText(checkStringList[1])
            self.instructionPlainTextEdit.setPlainText(checkStringList[2])
            self.questionnaireTitleLineEdit.setText(checkStringList[3])
            self.languageLineEdit.setText(checkStringList[4])
            self.questionPlainTextEdit.setPlainText(checkStringList[5])
            self.idPlainTextEdit.setPlainText(checkStringList[6])

            if self.kind == 'mc':

                self.answerLineEdit.setText(checkStringList[7])
                self.categoryPlainTextEdit.setPlainText(checkStringList[8])
                self.scorePlainTextEdit.setPlainText(checkStringList[9])
            else:
                pass

            return

        else:
            pass

        ## split string to list and remove last enter
        questionList = (questionString[:-1] if questionString.endswith('\n') else questionString).split('\n')
        idList       = (idString[:-1] if idString.endswith('\n') else idString).split('\n')

        questionList = removeJunk(questionList)
        idList       = removeJunk(idList)

        ## determine number of elements
        nquestions   = len(questionList)
        nidentity    = len(idList)


        ## name check
        if not nameString:
            nameCheck = False
        else:
            nameCheck = True

        ## language check
        if not languageString:
            languageCheck = False
        else:
            if languageString not in self.availableLang:

                availableLangUpperList = [x.upper() for x in self.availableLang]
                if languageString.upper() in availableLangUpperList:
                    index = availableLangUpperList.index(languageString.upper())
                    languageString = self.availableLang[index]
                else:
                    pass
            else:
                pass

            languageCheck = True

        if self.kind == 'mc':

            ## split string to list and remove last enter
            categoryList = (categoryString[:-1] if categoryString.endswith('\n') else categoryString).split('\n')
            scoreList    = (scoreString[:-1] if scoreString.endswith('\n') else scoreString).split('\n')

            ## clean up items
            categoryList   = cleanUpStringList(categoryList,';')
            scoreList      = cleanUpStringList(scoreList,';')
            answerString   = cleanUpString(answerString,';')

            answerItemList = answerString.split(';')

            ## determine number of elements
            ncategory = len(categoryList)
            nscore = len(scoreList)
            nanswers = len(answerItemList)

            ## check if all elements in score input field are numbers and if number of elements match number of elements in answerList
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
        else:
            pass

        self.languageString = languageString

        ## create file name
        self.baseName = nameString + '.osexp'
        folderName    = os.path.join(self.sourceFolder, self.languageString)
        fileNamePath  = os.path.join(folderName, self.baseName)


        ## check if file already exists
        if  os.path.isfile(fileNamePath):
            fileNameCheck = False
        else:
            fileNameCheck = True

        if ((self.kind == 'mc' and nquestions == nidentity == ncategory == nscore and scoreCheck and nameCheck and numberCheck and fileNameCheck and languageCheck) or
            (self.kind == 'open' and nquestions == nidentity and nameCheck and fileNameCheck and languageCheck)):

            ## create folder names if needed
            try:
                os.makedirs(folderName)
            except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(folderName):
                    pass
                else: raise

            if self.kind == 'mc':
                infile = self.mcFilePath
            elif self.kind == 'open':
                infile = self.openFilePath
            else:
                errorMessage = "Type of questionnaire is unclear, this error should not happen!"
                print(errorMessage, file=sys.stderr)
                self.showErrorMessage(errorMessage)

            QuestionnaireCreator(infile, fileNamePath, nameString, resolutionHorizontal, resolutionVertical, bgcolorString,
                                 fgcolorString, backendString, instructionTitleString, instructionString, questionnaireTitleString,
                                 orderString, questionList, idList, answerString, categoryList, scoreList, self.kind)
            self.accept()

        ## show error message if checks fail
        else:
            errorMessageList = []

            if not nameCheck:
                errorMessageList.append('- No questionnaire name specified\n')
            if not fileNameCheck:
                errorMessageList.append('- Filename already exist, please use another name.\n')
            if not languageCheck:
                errorMessageList.append('- No language specified\n')
            if not (self.kind == 'mc' and nquestions == nidentity == ncategory == nscore and scoreCheck) or (self.kind == 'open' and nquestions == nidentity):
                errorMessageList.append('- Not all fields have the correct number of elements\n')
            if not numberCheck:
                errorMessageList.append('- Field \"score\" should contain only numbers, found other characters\n')

            self.showErrorMessage(''.join(errorMessageList))

    def getValues(self):

        return [self.baseName, self.languageString]

    def showErrorMessage(self, message):
        """
        Shows error message
        """
        error ="Error"

        msgBox = QtWidgets.QMessageBox(self)
        msgBox.about(self, error, message)