"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher updating system                            *
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

from win32com.client import Dispatch
import traceback
import sys
import time

import logger   # logger.py
import globs    # globs.py
import ihm      # ihm.py

def createShortcut(path, target='', wDir='', icon=''):
    ext = path[-3:]
    if ext == 'url':
        shortcut = file(path, 'w')
        shortcut.write('[InternetShortcut]\n')
        shortcut.write('URL=%s' % target)
        shortcut.close()
    else:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        if icon == '':
            pass
        else:
            shortcut.IconLocation = icon
        shortcut.save()

## Main Batch Function
def batch():

    # Global Handlers
    logfile = logger.logCur
    launcherWindow = ihm.launcherWindowCur

    for i in range(0,10000):
        if i % 1000 : launcherWindow.mainCanvas.itemconfigure(launcherWindow.msg, text=('Starting... ' + str(i)))
    return

## Main Function
def umain():
    try:
        # Global Handlers
        logfile = logger.logCur
        launcherWindow = ihm.launcherWindowCur

        try:
            batch()
        except Exception as e:
            logfile.printerr("An error occured on the thread : " + str(traceback.format_exc()))
            launcherWindow.mainCanvas.itemconfigure(launcherWindow.msg, text=('ERROR : ' + str(e)))
            time.sleep(3)
            launcherWindow.destroy()
            return 1

        launcherWindow.mainCanvas.itemconfigure(launcherWindow.msg, text='Software is up-to-date !')
        time.sleep(2)
        launcherWindow.destroy()
        return 0

    except:
        logfile.printerr("A FATAL ERROR OCCURED : " + str(traceback.format_exc()))
        launcherWindow.destroy()
        sys.exit(2)
        return 2


