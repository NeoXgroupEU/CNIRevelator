# -*- coding: utf8 -*-
"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher & updater main file                        *
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

import sys
import os
import threading

import critical # critical.py
import updater  # updater.py
import ihm      # ihm.py
import globs    # globs.py
import logger   # logger.py
import lang     # lang.py

## Main function
def lmain(mainThread):
    logfile = logger.logCur
    launcherWindow = ihm.launcherWindowCur

    # Hello world
    logfile.printdbg('*** CNIRLauncher LOGFILE. Hello World ! ***')
    #logfile.printdbg('Files in directory : ' + str(os.listdir(globs.CNIRFolder)))

    # Hello user
    launcherWindow.progressBar.configure(mode='indeterminate', value=0, maximum=20)
    launcherWindow.printmsg(lang.all[globs.CNIRlang]["Starting..."])
    launcherWindow.progressBar.start()

    # Starting the main update thread
    mainThread.start()

    launcherWindow.mainloop()

    logfile.printdbg('*** CNIRLauncher LOGFILE. Goodbye World ! ***')
    return
