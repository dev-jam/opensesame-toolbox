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
import os
import sys
import csv
import logging

from configobj import ConfigObj
import numpy as np

from libopensesametoolbox.clean_data import cleanUpStringList, removeJunk
from libopensesametoolbox.io_tools import getResourceLoc

config = ConfigObj(getResourceLoc('opensesame-toolbox.conf'))

fs = os.sep

def QuestionnaireProcessor(dataFolder, destinationFolder, responseKey, idKey, categoryKey,
                           answerKey, scoreKey, customId, customCategory, customAnswers,
                           customScore, custom, caseInsensitiveComparison, ui=None):

    conf_questionnaireprocessor = config['questionnaireprocessor']
    dataExtList             = conf_questionnaireprocessor['dataExtList']
    resultExt               = conf_questionnaireprocessor['resultExt']
    resultDelimiter         = conf_questionnaireprocessor['resultDelimiter']
    scoreTypeList           = conf_questionnaireprocessor['scoreTypeList']
    incompleteCheck         = None


    dataFolderList    = listDataFolders(dataFolder)

    if not dataFolderList:
        dataFolderList = [dataFolder]
        singleFolder = True
    else:
        singleFolder = False

    totalFiles = 0

    for dataFolder in dataFolderList:
        nrDataFile    = len(listDataFiles(dataFolder, dataExtList))
        totalFiles += nrDataFile

    counter = 0

    for newDataFolder in dataFolderList:

        ## find data files and put file names in list and array
        dataFileList    = listDataFiles(newDataFolder, dataExtList)

        ## start counter and progressbar
        if ui is not None:
            ui.progressBar.setValue(0)


        subjectResponseDict = {}
        subjectCategoryDict = {}
        fileNameList = []

        for dataFile in dataFileList:
            fileName = os.path.basename(dataFile)
            sys.stdout.write(fileName)

            dataDict = readCsv(dataFile, ui)
            if dataDict == None:
                return

            fileNameList.append(fileName)

            ## make lists with the dependent variables from the dict

            try:
                responseList     = dataDict[responseKey]

            except:
                errorMessage = ("\nError: Column with name: " + responseKey + " is not present in the data file, "
                                "please try custom experiment")
                print(errorMessage, file=sys.stderr)
                if ui is not None:
                    ui.showErrorMessage(errorMessage)
                return

            try:
                responseIdList           = dataDict[idKey]

            except:
                errorMessage = ("\nError: Column with name: " + idKey + " is not present in the data file, "
                                "please try custom experiment")
                print(errorMessage, file=sys.stderr)
                if ui is not None:
                    ui.showErrorMessage(errorMessage)
                return

            if custom:
                keyIdList = customId
                categoryList = customCategory
                answerList = customAnswers
                scoreList = customScore
            else:

                keyIdList = responseIdList

                try:
                    answerList       = dataDict[answerKey]

                except:
                    errorMessage = ("\nError: Column with name: " + answerKey + " is not present in the data file, "
                                    "please try custom experiment")
                    print(errorMessage, file=sys.stderr)
                    if ui is not None:
                        ui.showErrorMessage(errorMessage)
                    return

                try:
                    categoryList     = dataDict[categoryKey]

                except:
                    errorMessage = ("\nError: Column with name: " + categoryKey + " is not present in the data file, "
                                    "please try custom experiment")
                    print(errorMessage, file=sys.stderr)
                    if ui is not None:
                        ui.showErrorMessage(errorMessage)
                    return

                try:
                    scoreList  = dataDict[scoreKey]

                except:
                    errorMessage = ("\nError: Column with name: " + scoreKey + " is not present in the data file, "
                                    "please try custom experiment")
                    print(errorMessage, file=sys.stderr)
                    if ui is not None:
                        ui.showErrorMessage(errorMessage)
                    return

            ## clean up items
            responseList   = removeJunk(responseList)
            responseIdList = removeJunk(responseIdList)

            if not custom:
                categoryList = cleanUpStringList(categoryList,';')
                scoreList    = cleanUpStringList(scoreList,';')
                answerList   = cleanUpStringList(answerList,';')

            else:
                pass

            responseDict = {}
            answerScoreDict = {}
            categoryDict = {}

            if not len(keyIdList) == len(responseIdList):
                incompleteCheck = True
            else:
                pass

            ## make dicts
            for index in range(len(keyIdList)):

                ## make categoryDict
                categoryItemList = categoryList[index].split(';')
                categoryDict[keyIdList[index]] = categoryItemList

                ## make answerScoreDict
                answerItemList = answerList[index].split(';')
                scoreItemList  = scoreList[index].split(';')

                answerDict = {}

                for subindex in range(len(answerItemList)):
                    if caseInsensitiveComparison:
                        answerDict[answerItemList[subindex].lower()] = scoreItemList[subindex]
                    else:
                        answerDict[answerItemList[subindex]] = scoreItemList[subindex]

                answerScoreDict[keyIdList[index]] = answerDict

                ## make reponseDict
            for index in range(len(responseIdList)):

                if caseInsensitiveComparison:
                    responseDict[responseIdList[index]] = responseList[index].lower()
                else:
                    responseDict[responseIdList[index]] = responseList[index]

            individualScoreDict = {}
            categoryScoreDict = {}
            sortedIdList = sorted(keyIdList)

            for index in range(len(sortedIdList)):
                selectedId = sortedIdList[index]

                categoryList = categoryDict[selectedId]
                scoreDict = answerScoreDict[selectedId]

                try:
                    response = responseDict[selectedId]
                except:

                    errorMessage = ("\nResponse with ID: \"" + selectedId + "\" is not found in the log file.\n"
                                    "Log File contains the following ID values:\n\n\"" + '\"\n\"'.join(responseIdList) + "\"\n\n"
                                    "Please input the correct ID values")

                    print(errorMessage, file=sys.stderr)
                    if ui is not None:
                        ui.showErrorMessage(errorMessage)
                    return

                try:
                    score = scoreDict[response]

                except:

                    errorMessage = ("\nResponse: \"" + response + "\" is not defined in the response field\n"
                                    "Given values are: \n\n\"" + '\"\n\"'.join(scoreDict))

                    print(errorMessage, file=sys.stderr)
                    if ui is not None:
                        ui.showErrorMessage(errorMessage)
                    return

                individualScoreDict[selectedId] = score

                for category in categoryList:
                    if category in categoryScoreDict:
                        categoryScoreDict[category].append(score)
                    else:
                        categoryScoreDict[category] = [score]

            subjectResponseDict[fileName] = individualScoreDict
            uniCategoryList = categoryScoreDict.keys()
            uniCategoryScoreDict = {}

            for uniCategory in uniCategoryList:
                uniCategoryScoreList = categoryScoreDict[uniCategory]
                uniCategoryScoreArray = np.array(uniCategoryScoreList, dtype='d')

                sumUniCategoryScoreString = str(np.sum(uniCategoryScoreArray))
                meanUniCategoryScoreString = str(np.mean(uniCategoryScoreArray))

                uniCategoryScoreDict1 = {}
                uniCategoryScoreDict1['Sum'] = sumUniCategoryScoreString
                uniCategoryScoreDict1['Mean'] = meanUniCategoryScoreString
                uniCategoryScoreDict[uniCategory] = uniCategoryScoreDict1

            subjectCategoryDict[fileName] = uniCategoryScoreDict

            sys.stdout.write(' Done!\n')
            counter += 1
            if ui is not None:
                ui.progressBar.setValue(counter / totalFiles * 100)

        if singleFolder:
            destinationFile = 'Cumulative_Score_Results.' + resultExt
        else:
            destinationFile = os.path.basename(os.path.dirname(newDataFolder)) + '_Cumulative_Score_Results.' + resultExt

        destinationFilePath = os.path.join(destinationFolder, destinationFile)

        writeCsv(destinationFilePath, subjectCategoryDict, subjectResponseDict, sorted(fileNameList),
                 sorted(uniCategoryList), sorted(keyIdList),scoreTypeList,resultDelimiter)

        print('Saved file: ' +  destinationFilePath)

    if incompleteCheck     :
        errorMessage = ("Warning:\n\nLog file contains more trials than were defined in the custom "
                        "input fields, only defined trials were processed!")
        print(errorMessage, file=sys.stderr)
        if ui is not None:
            ui.showErrorMessage(errorMessage)
    else:
        pass

    if ui is not None:
        ui.progressBar.setValue(100)
    sys.stdout.write('\nTotal process done!\n')

    succesMessage = ("Total process done!")
    if ui is not None:
        ui.showErrorMessage(succesMessage)

    return True


def listDataFolders(folder):

    folderList = sorted(glob.glob(folder + fs + '*/'))

    return folderList

def listDataFiles(dataDir,extensionList):
    """
    List data files
    """

    fileList = []
    for extension in extensionList:
        fileList.extend(glob.glob(dataDir + fs + '*.' + extension))

    fileList = sorted(fileList)

    return fileList

def readCsv(pathToCsv, ui):
    """
    Reads csv file to a dict containing lists, each representing a column.
    The keys of the dictionary represent the column names, and the value contains
    the corresponding list of the column.

    Args:
        pathToCsv (string): a path to the csv file to be parsed
    Returns:
        a dictionary with for every key the corresponding column list of data

    """

    encoding = 'utf-8'
#    delimiter = ','
#    quotechar = '"'


    with open(pathToCsv, 'rt', newline='', encoding=encoding) as fp:

        try:
            dialect = csv.Sniffer().sniff(fp.readline())
        except Exception:
            dialect = csv.get_dialect('excel')
        fp.seek(0)


        try:
            data = csv.reader(fp, dialect=dialect)
        except Exception as e:
            errorMessage = ("Cannot process csv file, unknown format, see the log file for more information")
            if ui is not None:
                logging.exception("Cannot process csv file: %s", e)
                ui.showErrorMessage(errorMessage)
            return None

        rowDataList = list(data)
    headerList = rowDataList[0]
    dataTupleList = list(zip(*rowDataList[1:]))


    dataDict = {}

    try:
        for index in range(len(headerList)):

            headerString = headerList[index]
            dataTuple = dataTupleList[index]

            dataDict[headerString] = list(dataTuple)

    except Exception as e:
            errorMessage = ("Cannot process csv file, unknown format")
            if ui is not None:
                logging.exception("Cannot process csv file: %s", e)
                ui.showErrorMessage(errorMessage)
            return None

    return dataDict


def writeCsv(pathToTsv, subjectCategoryDict, subjectResponseDict, fileNameList,
             uniCategoryList, keyIdList, scoreTypeList, delimiter):
    """
    Write data to tsv
    """
    encoding = 'utf-8'


    with open(pathToTsv, 'wt', newline='', encoding=encoding) as fp:

        writer = csv.writer(fp, delimiter=delimiter)

        catHeader = []
        for cat in uniCategoryList:
            for scoreType in scoreTypeList:
                catHeader = catHeader + [cat + '_' + scoreType]

        responseHeader = []
        for identity in keyIdList:
            responseHeader = responseHeader + [identity]

        header = ['Item'] + catHeader + responseHeader

        writer.writerow(header)

        for dataFile in fileNameList:
            categoryDict = subjectCategoryDict[dataFile]
            score =[]
            for category in uniCategoryList:
                scoreDict = categoryDict[category]

                for scoreType in scoreTypeList:
                    score.append(scoreDict[scoreType])

            responseDict = subjectResponseDict[dataFile]
            responseList = []
            for identity in keyIdList:
                responseList.append(responseDict[identity])

            row = [dataFile]  +  score + responseList
            writer.writerow(row)