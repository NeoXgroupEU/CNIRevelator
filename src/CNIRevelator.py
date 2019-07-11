"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher & updater                                  *
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
import subprocess
import threading
import traceback
import psutil

import launcher     # launcher.py
import updater      # updater.py
import globs        # globs.py
import pytesseract  # pytesseract.py

## MAIN FUNCTION OF CNIREVELATOR
def main():
    import logger   # logger.py
    logfile = logger.logMain

    try:
        os.environ['PATH'] = globs.CNIRFolder + '\\Tesseract-OCR4\\'
        os.environ['TESSDATA_PREFIX'] = globs.CNIRFolder + '\\Tesseract-OCR4\\tessdata'
        tesser_version = pytesseract.get_tesseract_version()
    except Exception as e:
        logfile.printerr('ERROR WITH TESSERACT MODULE ' + str(e))
    else:
        text = 'Tesseract version ' + str(tesser_version) + ' Licensed Apache 2004 successfully initiated\n'
        main_w.montext(text)

    main_w.montext('\n\nEntrez la première ligne de MRZ svp \n')

    if globs.CNIRNewVersion:
        showinfo('Changelog : résumé de mise à jour', ('Version du logiciel : CNIRevelator ' + globs.verstring_full + '\n\n' + globs.changelog), parent=main_w)
    logger.info('main() : **** Launching App_main() ****')
    main_w.mainloop()
    logger.info('main() : **** Ending App_main() ****')


## BOOTSTRAP OF CNIREVELATOR

try:
    launcherThread = threading.Thread(target=updater.umain, daemon=False)
    launcher.lmain(launcherThread)
except Exception:
    sys.exit(1)

if updater.UPDATE_IS_MADE:
    # Launch app !
    args = updater.UPATH + '\\CNIRevelator.exe ' + globs.CNIRFolder
    cd = updater.UPATH
    for i in range(0,3):
        try:
            updater.spawnProcess(args, cd)
        except:
            time.sleep(3)
            continue
        break
    sys.exit(0)

# Here we go !
try:
    main()
except Exception:
    sys.exit(1)

# Quit totally without remain in memory
for process in psutil.process_iter():
    if process.pid == os.getpid():
        process.terminate()