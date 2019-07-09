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

import launcher # launcher.py
import ihm      # ihm.py
import logger   # logger.py
import updater  # updater.py

## Global Handlers
logfile = logger.logCur
launcherWindow = ihm.launcherWindowCur

## MAIN FUNCTION OF CNIREVELATOR
def main():
    
    import CNI_pytesseract as pytesseract
    try:
        os.environ['PATH'] = CST_FOLDER + 'Tesseract-OCR4\\'
        os.environ['TESSDATA_PREFIX'] = CST_FOLDER + 'Tesseract-OCR4\\tessdata'
        tesser_version = pytesseract.get_tesseract_version()
    except Exception as e:
        logger.error('main() : **** ERROR WITH TESSERACT MODULE ' + str(e) + ' ****')
    else:
        text = 'Tesseract version ' + str(tesser_version) + ' Licensed Apache 2004 successfully initiated\n'
        main_w.montext(text)
    main_w.montext('\n\nEntrez la première ligne de MRZ svp \n')
    
    if CST_CHANGELOG.isOn:
        showinfo('Changelog : résumé de mise à jour', ('Version du logiciel : ' + CST_VER + ' ' + CST_TYPE + ' Revision ' + CST_REV + '\n\n' + CST_CHANGELOG.text), parent=main_w)
    logger.info('main() : **** Launching App_main() ****')
    main_w.mainloop()
    logger.info('main() : **** Ending App_main() ****')


## BOOTSTRAP OF CNIREVELATOR

try:
    launcherThread = threading.Thread(target=updater.umain, daemon=False)
    launcher.lmain(launcherThread)
except Exception:
    logfile.printerr("A FATAL ERROR OCCURED : " + str(traceback.format_exc()))
    sys.exit(1)

main()
sys.exit(0)
