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

import logger       # logger.py
import globs        # globs.py
import ihm          # ihm.py
import downloader   # downloader.py

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

    credentials = downloader.newcredentials()

    if not credentials.valid:
        return False

    # First retrieving the urls !
    while True:
        try:
            # Open the config file
            logfile.printdbg('Reading urlconf.ig')
            with open(globs.CNIRUrlConfig, 'r') as (configFile):
                try:
                    # Reading it
                    reading = configFile.read()
                    # Parsing it
                    urlparsed = reading.split("\n")
                    break

                except Exception as e:
                    raise IOError(str(e))

        except FileNotFoundError:
            logfile.printdbg('Recreate urlconf.ig')
            # Recreating the url file
            with open(globs.CNIRUrlConfig, 'w') as (configFile):
                configFile.write("https://raw.githubusercontent.com/neox95/CNIRevelator/master/VERSIONS.LST\n0\n0") #XXX

    # Getting the list of versions of the software
    logfile.printdbg('Retrieving the software versions')
    getTheVersions = downloader.newdownload(credentials, urlparsed[0], globs.CNIRFolder + '\\versions.lst').download()

    logfile.printdbg('Parsing the software versions')
    with open(globs.CNIRFolder + '\\versions.lst') as versionsFile:
        versionsTab = versionsFile.read().split("\n")[1].split("||")
        logfile.printdbg('Versions retrieved : {}'.format(versionsTab))
    # Choose the newer
    finalver = globs.version.copy()
    for entry in versionsTab:
        verstr, url, checksum = entry.split("|")
        # Calculating sum considering we can have 99 sub versions
        ver = verstr.split(".")
        ver = [int(i) for i in ver]
        finalsum = finalver[2] + finalver[1]*100 + finalver[0]*100*100
        sum = ver[2] + ver[1]*100 + ver[0]*100*100
        # Make a statement
        if sum > finalsum:
            finalver = ver.copy()
            finalurl = url

    if finalver == globs.version:
        logfile.printdbg('The software is already the newer version')
        return True

    logfile.printdbg('Preparing download for the new version')

    getTheUpdate = downloader.newdownload(credentials, finalurl, globs.CNIRFolder + '\\..\\CNIPackage.zip').download()

    return True

## Main Function
def umain():
    try:
        # Global Handlers
        logfile = logger.logCur
        launcherWindow = ihm.launcherWindowCur

        try:
            # EXECUTING THE UPDATE BATCH
            success = batch()
        except Exception as e:
            logfile.printerr("An error occured on the thread : " + str(traceback.format_exc()))
            launcherWindow.mainCanvas.itemconfigure(launcherWindow.msg, text=('ERROR : ' + str(e)))
            time.sleep(3)
            launcherWindow.destroy()
            return 1

        if success:
            logfile.printdbg("Software is up-to-date !")
            launcherWindow.mainCanvas.itemconfigure(launcherWindow.msg, text='Software is up-to-date !')
        else:
            logfile.printerr("An error occured. No effective update !")
            launcherWindow.mainCanvas.itemconfigure(launcherWindow.msg, text='An error occured. No effective update !')
        time.sleep(2)
        launcherWindow.destroy()
        return 0

    except:
        logfile.printerr("A FATAL ERROR OCCURED : " + str(traceback.format_exc()))
        launcherWindow.destroy()
        sys.exit(2)
        return 2

    return

