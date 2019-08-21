# -*- coding: utf8 -*-
"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher & updater                                  *
*                                                                              *
*  Copyright © 2018-2019 Adrien Bourmault (neox95)                             *
*                                                                              *
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
# Import critical files
import os
import threading

import lang         # lang.py
import logger       # logger.py
import globs        # globs.py
import critical     # critical.py

# Import all other files and crash if necessary
try:

    import launcher     # launcher.py"
    import updater      # updater.py
    import pytesseract  # pytesseract.py
    import ihm          # ihm.py
    from tkinter.messagebox import *
    from tkinter import *
except:
    critical.crashCNIR()

# Global handler
logfile = logger.logCur

## MAIN FUNCTION OF CNIREVELATOR
def main():
    logfile.printdbg('*** CNIRevelator LOGFILE. Hello World ! ***')

    mainw = mainWindow()

    try:
        os.environ['PATH'] = globs.CNIRFolder + '\\Tesseract-OCR5\\'
        os.environ['TESSDATA_PREFIX'] = globs.CNIRFolder + '\\Tesseract-OCR5\\tessdata'
        tesser_version = pytesseract.get_tesseract_version()
    except Exception as e:
        logfile.printerr('ERROR WITH TESSERACT MODULE ' + str(e))
    else:
        text = 'Tesseract version ' + str(tesser_version) + ' Licensed Apache 2004 successfully initiated\n'
        mainw.logOnTerm(text)

    mainw.logOnTerm('\n\n{} \n'.format(lang.all[globs.CNIRlang]["Please type a MRZ or open a scan"]))

    # changelog
    if globs.CNIRNewVersion:
        mainw.after_idle(mainw.showChangeLog)

    logfile.printdbg('main() : **** Launching App_main() ****')
    try:
        mainw.mainloop()
    except Exception as e:
        showerror(lang.all[globs.CNIRlang]["CNIRevelator Fatal Error"], "{} : {}".format(lang.all[globs.CNIRlang]["An error has occured"],e), parent=mainw)
    logfile.printdbg('main() : **** Ending App_main() ****')

    logfile.printdbg('*** CNIRevelator LOGFILE. Goodbye World ! ***')
    logfile.close()


## BOOTSTRAP OF CNIREVELATOR
try:

    try:
        # LANGUAGE
        lang.readLang()
    except:
        critical.crashCNIR()
        updater.exitProcess(1)

    from main import *  # main.py
    # GO
    try:
        launcherThread = threading.Thread(target=updater.umain, daemon=False)
        launcher.lmain(launcherThread)
    except Exception:
        critical.crashCNIR(False)

    if updater.UPDATE_IS_MADE:
        # Launch app !
        args = updater.UPATH + '\\CNIRevelator.exe' + " DELETE " + globs.CNIRFolder
        cd = updater.UPATH
        for i in range(0,3):
            try:
                updater.spawnProcess(args, cd)
            except:
                time.sleep(3)
                continue
            break
        updater.exitProcess(0)

    # Here we go !
    try:
        main()
    except Exception as e:
        critical.crashCNIR()
        updater.exitProcess(1)

except:
    critical.crashCNIR()

updater.exitProcess(0)