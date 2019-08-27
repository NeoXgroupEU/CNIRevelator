# -*- coding: utf8 -*-
"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Github Stuff for CNIRevelator                                   *
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
from requests.auth import HTTPProxyAuth
from pypac import PACSession
from Crypto import Random
from Crypto.Cipher import AES
from requests import Session
import json, hashlib, base64

import logger  # logger.py
import globs   # globs.py

credentials = False

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

def reportBug(reason="",log=""):

    logfile = logger.logCur

    if not credentials:
        logfile.printerr("No credentials")
        return False

    session = credentials.sessionHandler

    payload = {'title':"CNIRevelator Bug Report", 'body':"**An error has been reported by a CNIRevelator instance.**\n\n**Here is the full reason of this issue:**\n{}\n\n**The full log is here:** {}".format(reason, log), "assignees":["neox95"], "labels":["bug", "AUTO"]}

    handler = session.post('https://api.github.com/repos/neox95/cnirevelator/issues', headers={'Authorization': 'token %s' % decryptToken(globs.CNIRGitToken)}, data=json.dumps(payload))

    logfile.printdbg(handler.reason)

    if handler.reason == "Created":
        return True
    else:
        return False

def encryptToken(token):
    AESObj = AESCipher(globs.CNIRCryptoKey)
    return AESObj.encrypt(token)

def decryptToken(token):
    AESObj = AESCipher(globs.CNIRCryptoKey)
    return AESObj.decrypt(token)


