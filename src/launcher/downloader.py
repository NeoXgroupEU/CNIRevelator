"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher download stuff                             *
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

import hashlib
from pypac import PACSession
from requests.auth import HTTPProxyAuth
import base64, hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os

import logger   # logger.py
import globs    # globs.py
import ihm      # ihm.py

class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
        

class newcredentials:
    def __init__(self):
        
        logfile = logger.logCur
        
        self.login = ''
        self.password = ''
        self.valid = False
        self.readInTheBooks = False
        self.trying = 0
        session = PACSession()
        
        while True:
            self.trying += 1
            
            try:
                sessionAnswer = session.get('https://www.google.com')
            except Exception as e:
                logfile.printerr('Network Error : ' + str(e))
                sessionAnswer = '<Response [407]>'# XXX TO DEBUG XXX
                
            logfile.printdbg("Session Answer : " + str(sessionAnswer))
            
            if str(sessionAnswer) == '<Response [200]>':
                logfile.printdbg('Successfully connected to the Internet !')
                self.sessionHandler = session
                self.valid = True
                return
            
            if str(sessionAnswer) != '<Response [407]>':
                logfile.printerr('Network Error!')
                return
            
            if self.trying > 3:
                logfile.printerr('Invalid credentials : access denied, a maximum of 3 trials have been raised !')
                return
            
            logfile.printdbg('Invalid credentials : access denied')
            
            # Deleting the root of Evil if needed
            if self.readInTheBooks:
                os.remove(globs.CNIRFolder + '\\conf.ig')
                logfile.printdbg("Deleting the root of Evil")
            
            try:
                with open(globs.CNIRFolder + '\\conf.ig', 'rb') as (configFile):
                    self.readInTheBooks = True
                    # Decrypt the config file
                    AESObj = AESCipher(globs.CNIRCryptoKey)
                    try:
                        # Reading it
                        reading = AESObj.decrypt(configFile.read())
                        # Parsing it
                        if reading != '||':
                            if reading.find('||') != -1:
                                # TADAAA
                                self.login, self.password = reading.split('||')[0:2]
                            else:
                                # UPS
                                logfile.printerr('Cryptokey is bad !')
                                return

                    except Exception as e:
                        raise IOError(str(e))
                    
            except FileNotFoundError:
                logfile.printdbg('We will ask for credentials then')
                
                launcherWindow = ihm.launcherWindowCur
                
                # Parameters for the password invite
                invite = ihm.LoginDialog(launcherWindow)
                invite.transient(launcherWindow)
                invite.grab_set()
                
                launcherWindow.wait_window(invite)
                
                # Getting the credentials
                self.login = invite.login
                self.password = invite.key
                
                AESObj = AESCipher(globs.CNIRCryptoKey)
                with open(globs.CNIRFolder + '\\conf.ig', 'wb+') as (configFile):
                    logfile.printdbg('Saving credentials in encrypted config file')
                    configFile.write(AESObj.encrypt(self.login + '||' + self.password))
                
            
        return

class newdownload():
    def __init__(self, credentials, urlFile, destinationFile):
        self.urlFile = urlFile
        self.destinationFile = destinationFile
        
        