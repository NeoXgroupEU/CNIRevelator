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
import os
import shutil
import zipfile
import hashlib
import subprocess
import psutil

import ihm          # ihm.py
import logger       # logger.py
import globs        # globs.py
import downloader   # downloader.py

UPDATE_IS_MADE = False
UPATH = ' '

launcherWindow = ihm.launcherWindowCur

def createShortcut(path, target='', wDir='', icon=''):
    """
    Creates a shortcut for a program or an internet link
    """
    ext = path[-3:]
    if ext == 'url':
        shortcut = file(path, 'w')
        shortcut.write('[InternetShortcut]\n')
        shortcut.write('URL=%s' % target)
        shortcut.close()
    else:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shell.SpecialFolders("Desktop") + r"\{}".format(path))
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        if icon == '':
            pass
        else:
            shortcut.IconLocation = icon
        shortcut.save()

def spawnProcess(args, cd):
    """
    Creates a new independant process. Used to launch a new version after update
    """
    subprocess.Popen(args, close_fds=True, cwd=cd, creationflags=subprocess.DETACHED_PROCESS)

def exitProcess(arg):
    """
    Forcefully quits a process. Used to help deletion of an old version or to quit properly
    """
    # Quit totally without remain in memory
    for process in psutil.process_iter():
        if process.pid == os.getpid():
            process.terminate()
    sys.exit(arg)

def runPowershell(scriptblock, cwd=os.getcwd()):
    """
    Executes a powershell command
    """
    log.debug("Running PowerShell Block:\r\n%s", scriptblock)
    log.debug("Current Directory: %s\r\n" % cwd)
    psProc = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                                '-ExecutionPolicy', 'Bypass',
                                '-noprofile',
                                '-c', '-',],
                                cwd=cwd,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    stdoutdata, stderrdata = psProc.communicate(scriptblock)

    if stdoutdata:
        log.debug("Script Output:\r\n%s" % stdoutdata)
    elif not stderrdata:
        log.debug("Script completed succssfully (no stdout/stderr).")
    if stderrdata:
        log.error("Script Error:\r\n%s" % stderrdata)

    return stdoutdata, stderrdata


def getCertificates(server_list, location="LocalMachine", store="My"):
    """
    Returns the json data of all installed certificates
    """
    cmd = '''
$sb = { ls Cert:\%s\%s | Select Subject,ThumbPrint }
$Servers = '%s' | ConvertFrom-Json

Invoke-Command -ComputerName $Servers -ScriptBlock $sb -Authentication Negotiate | ConvertTo-Json -Depth 999
    ''' % (location, store, json.dumps(server_list))
    stdoutdata, stderrdata = runPowershell(cmd)
    return json.loads(stdoutdata)



def getLatestVersion(credentials):
    """
    Returns the latest version of the software
    """

    # Global Handlers
    logfile = logger.logCur
     

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
            try:
                os.mkdir(globs.CNIRFolder + '\\config')
            except:
                pass
            with open(globs.CNIRUrlConfig, 'w') as (configFile):
                configFile.write("https://raw.githubusercontent.com/neox95/CNIRevelator/master/VERSIONS.LST\n0\n0")

    # Getting the list of versions of the software
    logfile.printdbg('Retrieving the software versions')
    try:
        os.mkdir(globs.CNIRFolder + '\\downloads')
    except:
        pass
    getTheVersions = downloader.newdownload(credentials, urlparsed[0], globs.CNIRVerStock, "the version repository").download()
    
    logfile.printdbg('Parsing the software versions')
    with open(globs.CNIRVerStock) as versionsFile:
        versionsTab = versionsFile.read().split("\n")[1].split("||")
        logfile.printdbg('Versions retrieved : {}'.format(versionsTab))
    # Choose the newer
    finalver = globs.version.copy()
    for entry in versionsTab:
        if not entry:
            continue
        verstr, url, checksum = entry.split("|")
        # Calculating sum considering we can have 99 sub versions
        ver = verstr.split(".")
        ver = [int(i) for i in ver]
        finalsum = finalver[2] + finalver[1]*100 + finalver[0]*100*100
        sum = ver[2] + ver[1]*100 + ver[0]*100*100
        # Make a statement
        if sum >= finalsum:
            finalver = ver.copy()
            finalurl = url
            finalchecksum = checksum
        else:
            finalurl = url
            finalchecksum = None
            
    return (finalver, finalurl, finalchecksum)


# XXX Warning : when tesseracturl is not found, it seems to hang and freeze
def tessInstall(PATH, credentials):
    # Global Handlers
    logfile = logger.logCur
     
    
    # Verifying that Tesseract is installed
    if not os.path.exists(PATH + '\\Tesseract-OCR4\\'):
        finalver, finalurl, finalchecksum = getLatestVersion(credentials)
        tesseracturl = finalurl.replace("CNIRevelator.zip", "tesseract_4.zip")
        
        # WE ASSUME THAT THE MAIN FILE IS CNIRevelator.zip AND THAT THE TESSERACT PACKAGE IS tesseract_4.zip
        logfile.printdbg('Preparing download of Tesseract OCR 4...')
        getTesseract = downloader.newdownload(credentials, tesseracturl, PATH + '\\downloads\\TsrtPackage.zip', "Tesseract 4 OCR Module").download()
        
        try:
            # Unzip Tesseract   
            logfile.printdbg("Unzipping the package")
            launcherWindow.printmsg('Installing the updates')
            zip_ref = zipfile.ZipFile(PATH + '\\downloads\\TsrtPackage.zip', 'r')
            zip_ref.extractall(PATH)
            zip_ref.close()            
            # Cleanup
            try:
                os.remove(UPATH + '\\downloads\\TsrtPackage.zip')
            except:
                pass                
            return True

        except:
            return False
    else:
        return True

## Main Batch Function
def batch(credentials):
    # Global Handlers
    logfile = logger.logCur
     

    # Get the latest version of CNIRevelator
    finalver, finalurl, finalchecksum = getLatestVersion(credentials)
    
    if finalver == globs.version:
        logfile.printdbg('The software is already the newer version')
        return True

    logfile.printdbg('Preparing download for the new version')

    getTheUpdate = downloader.newdownload(credentials, finalurl, globs.CNIRFolder + '\\downloads\\CNIPackage.zip', "CNIRevelator {}.{}.{}".format(finalver[0], finalver[1], finalver[2])).download()
    
    launcherWindow.printmsg('Verifying download...')
    
    # CHECKSUM
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    
    sha1 = hashlib.sha1()
    
    with open(globs.CNIRFolder + '\\downloads\\CNIPackage.zip', 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
            
    check = sha1.hexdigest()
    logfile.printdbg("SHA1: {0}".format(check))
    
    if not check == finalchecksum:
        logfile.printerr("Checksum error")
        return False

    # And now prepare install
    global UPATH
    UPATH = globs.CNIRFolder + '\\..\\CNIRevelator' + "{}.{}.{}".format(finalver[0], finalver[1], finalver[2])
    logfile.printdbg("Make place")
    launcherWindow.printmsg('Preparing installation...')
    # Cleanup
    try:
        shutil.rmtree(UPATH + 'temp')
    except Exception as e:
        logfile.printdbg('Unable to cleanup : ' +str(e))
    try:
        shutil.rmtree(UPATH)
    except Exception as e:
        logfile.printdbg('Unable to cleanup : ' +str(e))
    # Unzip    
    logfile.printdbg("Unzipping the package")
    launcherWindow.printmsg('Installing the updates')
    zip_ref = zipfile.ZipFile(globs.CNIRFolder + '\\downloads\\CNIPackage.zip', 'r')
    zip_ref.extractall(UPATH + "temp")
    zip_ref.close()
    
    # Move to the right place
    shutil.copytree(UPATH + 'temp\\CNIRevelator', UPATH)
    shutil.rmtree(UPATH + 'temp')
    logfile.printdbg('Extracted :' + UPATH + '\\CNIRevelator.exe')    

    # Make a shortcut
    createShortcut("CNIRevelator.lnk", UPATH + '\\CNIRevelator.exe', UPATH)

    launcherWindow.printmsg('Success !')
    
    # Cleanup
    try:
        os.remove(globs.CNIRFolder + '\\downloads\\CNIPackage.zip')
    except:
        pass
    # Time to quit
    launcherWindow.printmsg('Launched the new process.')
    global UPDATE_IS_MADE
    UPDATE_IS_MADE = True
    return True

## Main Function
def umain():
    
    # Global Handlers
    logfile = logger.logCur
     
    
    credentials = downloader.newcredentials()
    
    if not credentials.valid:
        logfile.printerr("Credentials Error. No effective update !")
        launcherWindow.printmsg('Credentials Error. No effective update !')
        time.sleep(2)
        launcherWindow.exit()
        return 0
    
    # Cleaner for the old version if detected
    if len(sys.argv) > 2:
        globs.CNIRNewVersion = True
        launcherWindow.printmsg('Deleting old version !')
        logfile.printdbg("Old install detected : {}".format(sys.argv[1]))
        while os.path.exists(str(sys.argv[2])):
            try:
                os.remove(str(sys.argv[2]))
            except Exception as e:
                logfile.printerr(str(e))
                logfile.printdbg('Trying stop the process !')
                launcherWindow.printmsg('Fail :{}'.format(e))
                try:
                    for process in psutil.process_iter():
                        if process.name() == 'CNIRevelator.exe':
                            logfile.printdbg('Process found. Command line: {}'.format(process.cmdline()))
                            if process.pid == os.getpid():
                                logfile.printdbg("Don't touch us ! {} = {}".format(process.pid, os.getpid()))
                            else:
                                logfile.printdbg('Terminating process !')
                                process.terminate()
                                os.remove(str(sys.argv[2]))
                                break
                except Exception as e:
                    logfile.printerr(str(e))
                    launcherWindow.printmsg('Fail :{}'.format(e))
        launcherWindow.printmsg('Starting...')
    elif len(sys.argv) > 1:
        globs.CNIRNewVersion = True
        launcherWindow.printmsg('Deleting old version !')
        logfile.printdbg("Old install detected : {}".format(sys.argv[1]))
        while os.path.exists(str(sys.argv[1])):
            try:
                shutil.rmtree(str(sys.argv[1]))
            except Exception as e:
                logfile.printerr(str(e))
                logfile.printdbg('Trying stop the process !')
                launcherWindow.printmsg('Fail :{}'.format(e))
                try:
                    for process in psutil.process_iter():
                        if process.name() == 'CNIRevelator.exe':
                            logfile.printdbg('Process found. Command line: {}'.format(process.cmdline()))
                            if process.pid == os.getpid():
                                logfile.printdbg("Don't touch us ! {} = {}".format(process.pid, os.getpid()))
                            else:
                                logfile.printdbg('Terminating process !')
                                process.terminate()
                                shutil.rmtree(str(sys.argv[1]))
                                break
                except Exception as e:
                    logfile.printerr(str(e))
                    launcherWindow.printmsg('Fail :{}'.format(e))
        launcherWindow.printmsg('Starting...')
    
    try:
        try:
            # EXECUTING THE UPDATE BATCH
            success = batch(credentials)
        except Exception as e:
            logfile.printerr("An error occured on the thread : " + str(traceback.format_exc()))
            launcherWindow.printmsg('ERROR : ' + str(e))
            time.sleep(3)
            launcherWindow.exit()
            return 1

        if success:
            logfile.printdbg("Software is up-to-date !")
            launcherWindow.printmsg('Software is up-to-date !')
        else:
            logfile.printerr("An error occured. No effective update !")
            launcherWindow.printmsg('An error occured. No effective update !')
            time.sleep(2)
            launcherWindow.exit()
            return 0         
               
        if UPDATE_IS_MADE:
            launcherWindow.exit()
            return 0
    except:
        logfile.printerr("A FATAL ERROR OCCURED : " + str(traceback.format_exc()))
        launcherWindow.exit()
        sys.exit(2)
        return 2
        
    try:
        try:
            # INSTALLING TESSERACT OCR
            success = tessInstall(globs.CNIRFolder, credentials)
        except Exception as e:
            logfile.printerr("An error occured on the thread : " + str(traceback.format_exc()))
            launcherWindow.printmsg('ERROR : ' + str(e))
            time.sleep(3)
            launcherWindow.exit()
            return 1

        if success:
            logfile.printdbg("Software is up-to-date !")
            launcherWindow.printmsg('Software is up-to-date !')
        else:
            logfile.printerr("An error occured. No effective update !")
            launcherWindow.printmsg('An error occured. No effective update !')
            time.sleep(2)
            launcherWindow.exit()
            return 0

    except:
        logfile.printerr("A FATAL ERROR OCCURED : " + str(traceback.format_exc()))
        launcherWindow.exit()
        sys.exit(2)
        return 2

    time.sleep(2)
    launcherWindow.exit()
    return 0
