OpenSesame Toolbox
==========
Copyright Bob Rosbag (2015)

ABOUT
-----
Current version: 2.1

OpenSesame Toolbox offers two applications to supplement OpenSesame.  
  
OpenSesame Experiment Manager can manage, order and execute OpenSesame Experiments and create OpenSesame questionnaires.

OpenSesame Questionnaire Processor can process OpenSesame multiple choice questionnaires by giving a summary of the scores.


DOCUMENTATION AND INSTALLATION INSTRUCTIONS
-------------------------------------------
This is a standalone program that does not need to be installed. Make sure your 
python environment meets all dependencies specified below and that all files in
this repository are located in the same folder. This program only works in Python 3.

If you want to use the GUI simply run the program by

    python opensesame-experiment-manager
    and/or
    python opensesame-questionnaire-processor

It is also possible to use OpenSesame Questionnaire Processor from CLI:

    python opensesame-questionnaire-processor <source_folder> [<target_folder>]

In linux where Python 2 is default, <python3> has to be used as cmd instead of <python>
To use the CLI method it is required the questionnaires originate from the OpenSesame Experiment Manager or contain the same column names in the log files.


DEPENDENCIES
------------
- Python3 (> 3.4) <https://www.python.org>
- PyQt5 (QtGui, QtCore, uic) <http://www.riverbankcomputing.com/software/pyqt/download>
- NumPy <http://http://www.numpy.org>
- ConfigObj <http://www.voidspace.org.uk/python/configobj.html>
