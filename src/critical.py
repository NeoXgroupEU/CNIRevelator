"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Critical Stuff for CNIRevelator                                 *
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
from tkinter.messagebox import *
from tkinter import *
import webbrowser
import traceback
import psutil
import os

import lang         # lang.py
import logger       # logger.py
import globs        # globs.py

def LASTCHANCECRASH():
    """
    very last solution
    """
    root = Tk()
    root.withdraw()
    logfile = logger.logCur
    logfile.printerr("FATAL ERROR : see traceback below.\n{}".format(traceback.format_exc()))
    showerror(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["CNIRevelator crashed because a fatal error occured. View log for more infos and please open an issue on Github"])
    res = askquestion(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["Would you like to open the log file ?"])
    if res == "yes":
        webbrowser.open_new(globs.CNIRErrLog)
    res = askquestion(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["Would you like to open an issue on Github to report this bug ?"])
    if res == "yes":
        webbrowser.open_new("https://github.com/neox95/CNIRevelator/issues")
    root.destroy()
    # Quit totally without remain in memory
    for process in psutil.process_iter():
        if process.pid == os.getpid():
            process.terminate()
    sys.exit(arg)