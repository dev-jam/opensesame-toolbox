OpenSesame Toolbox
==========
Copyright Bob Rosbag (2015)

ABOUT
-----
Current version: 1.9.2

OpenSesame Toolbox offers two applications to supplement OpenSesame.  
  
OpenSesame Experiment Manager can manage, order and execute OpenSesame Experiments and create OpenSesame questionnaires.

OpenSesame Questionnaire Processor can process OpenSesame multiple choice questionnaires by giving a summary of the scores.


DOCUMENTATION AND INSTALLATION INSTRUCTIONS
-------------------------------------------
This is a standalone program that does not need to be installed. Make sure your 
python environment meets all dependencies specified below and that all files in
this repository are located in the same folder. This program only works in Python3.

If you want to use the GUI simply run the program by

    python3 opensesame-experiment-manager
    and/or
    python3 opensesame-questionnaire-processor

It is also possible to use OpenSesame Questionnaire Processor from CLI:

    python3 opensesame-questionnaire-processor <source_folder> [<target_folder>]

To use the CLI method it is required the questionnaires originate from the OpenSesame Questionnaire Manager or contain the same column names in the log files.


DEPENDENCIES
------------
- Python3 (> 3.4) <https://www.python.org>
- PyQt5 (QtGui, QtCore, uic) <http://www.riverbankcomputing.com/software/pyqt/download>
- NumPy <http://http://www.numpy.org>
- ConfigObj <http://www.voidspace.org.uk/python/configobj.html>
