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

from libopensesametoolbox.clean_data import usanitize


def QuestionnaireCreator(infile, fileName, nameString, resolutionHorizontal, resolutionVertical, bgcolorString,
                         fgcolorString, backendString, instructionTitleString, instructionString, questionnaireTitleString,
                         orderString, questionList, idList, answerString, categoryList, scoreList, type_):
    """
    Create questionnaire
    """

    nrcycles = str(len(questionList))

    stringList = []

    ## 0
    stringList.append(bgcolorString)

    ## 1
    stringList.append(fgcolorString)

    ## 2
    stringList.append(backendString)

    ## 3
    stringList.append('custom')

    ## 4
    stringList.append(resolutionHorizontal)

    ## 5
    stringList.append(resolutionVertical)

    ## 6
    stringList.append(nrcycles)

    ## 7
    stringList.append(orderString)

    ## 8
    stringList.append(instructionTitleString)

    ## 9
    stringList.append('\t' +instructionString.replace('\n','\n\t'))

    ## 10
    stringList.append(questionnaireTitleString)

    ## 11 keyboard backend
    if backendString in ['psycho', 'legacy']:
        stringList.append(backendString)
    elif backendString == 'xpyriment':
        stringList.append('legacy')
    else:
        stringList.append('legacy')

    if type_ == 'mc':

        tableString = ''
        for index in range(len(questionList)):
            tableString = tableString + '\tsetcycle '+str(index)+' category \"'+categoryList[index]+'\"\n' \
                '\tsetcycle '+str(index)+' answer_options_scores "'+scoreList[index]+'\"\n' \
                '\tsetcycle '+str(index)+' answer_options \"'+answerString+'\"\n' \
                '\tsetcycle '+str(index)+' id \"'+idList[index]+'\"\n' \
                '\tsetcycle '+str(index)+' question_text "'+questionList[index]+'\"'

            if index < len(questionList)-1:
                tableString = tableString +'\n'
            else:
                pass
        ## 12
        stringList.append(tableString)

        ## 13
        stringList.append('\t' +answerString.replace(';','\n\t'))

    else:
        pass

    if type_ == 'open':

        tableString = ''
        for index in range(len(questionList)):
            tableString = tableString + '\tsetcycle '+str(index)+' id \"'+idList[index]+'\"\n' \
                '\tsetcycle '+str(index)+' question_text "'+questionList[index]+'\"'

            if index < len(questionList)-1:
                tableString = tableString +'\n'
            else:
                pass
        ## 12
        stringList.append(tableString)
    else:
        pass

    replacementDict = {}
    for index in range(len(stringList)):
        replacementDict['@@'+str(index)+'@@'] = stringList[index]

    with open(infile, "r") as myfile:
        data=myfile.read()

    for src, target in replacementDict.items():
         data = data.replace(src, target)

    ## convert all unicode characters not present in ascii to unicode string
    cleanData = usanitize(data)

    with open(fileName, 'w') as out:
        out.write(cleanData)

    return True