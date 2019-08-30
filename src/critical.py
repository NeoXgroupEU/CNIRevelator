# -*- coding: utf8 -*-
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
from importlib import reload
from tkinter import *
import webbrowser
import traceback
import psutil
import os

import lang                     # lang.py
import logger                   # logger.py
import globs                    # globs.py
import github                   # github.py

def crashCNIR(shutdown=True, option="", isVoluntary=False):
    """
    very last solution
    """

    try:
        root = Tk()
        root.withdraw()
        logfile = logger.logCur
        logfile.printerr("FATAL ERROR : see traceback below.\n{}".format(traceback.format_exc()))

        if not isVoluntary:
            showerror(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["CNIRevelator crashed because a fatal error occured. View log for more infos and please open an issue on Github"] + "\n\n{}\n{}".format(option, traceback.format_exc()))

            # Force new update
            try:
                os.remove(globs.CNIRLastUpdate)
            except:
                pass

        res = askquestion(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["Would you like to report this bug ?"])
        if res == "yes":
            # read the log
            data = "No log."
            try:
                with open(globs.CNIRMainLog, 'r') as file:
                    data = file.read()
            except:
                logfile.printerr("Can't read the log file.")

            # send it
            success = github.reportBug(traceback.format_exc(), data, isVoluntary)

            if not success:
                logfile.printerr("Can't send to Github.")
                res = askquestion(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["Would you like to open the log file ?"])
                if res == "yes":
                    webbrowser.open_new(globs.CNIRErrLog)
            else:
                showinfo(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["Bug reported successfully. Thanks."])

        root.destroy()

        # Quit ?
        if not shutdown:
            return

        # Quit totally without remain in memory
        for process in psutil.process_iter():
            if process.pid == os.getpid():
                process.terminate()
        sys.exit(arg)
    except:
        traceback.print_exc()