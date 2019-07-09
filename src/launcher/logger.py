"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher logging stuff                              *
*                                                                              *
*  Copyright © 2018-2019 Adrien Bourmault (neox95)                             *
*                                                                              *
*  This file is part of CNIRevelator.                                          *
*                                                                              *
*  CNIRevelator is free software: you can redistribute it and/or modify        *
*  it under the terms of the GNU General Public License as published by        *
*  the Free Software Foundation, either version 3 of the License, or           *
*  any later version.                                                          *
*                                                                              *
*  CNIRevelator is distributed in the hope that it will be useful,             *
*  but WITHOUT ANY WARRANTY*without even the implied warranty of               *
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               *
*  GNU General Public License for more details.                                *
*                                                                              *
*  You should have received a copy of the GNU General Public License           *
* along with CNIRevelator. If not, see <https:*www.gnu.org/licenses/>.         *
********************************************************************************
"""

import logging
import os

import globs    # globs.py

## The logging class
class NewLoggingSystem:

    def __init__(self):

        # Deleting the error log
        try:
            os.remove(globs.CNIRFolder + '\\error.log')
        except Exception as e:
            #print(str(e) + " : " + str(globs.CNIRFolder + '\\error.log'))
            pass

        # Create new logging handle
        logger = logging.getLogger()
        logger.setLevel(logging.INFO) # To make sure we can have a debug channel

        # Create channels
        formatter = logging.Formatter("\n[ %(module)s/%(funcName)s ] %(asctime)s :: %(levelname)s :: %(message)s")
        error_handler = logging.FileHandler((globs.CNIRFolder + '\\error.log'), mode='w', encoding='utf-8', delay=True)
        info_handler = logging.FileHandler((globs.CNIRFolder + '\\launcher.log'), mode='w', encoding='utf-8')

        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

        info_handler.setLevel(logging.DEBUG)
        info_handler.setFormatter(formatter)
        logger.addHandler(info_handler)

        self.logger = logger
        self.printerr = logger.error
        self.printdbg = logger.info

## Global Handler
logCur = NewLoggingSystem()
