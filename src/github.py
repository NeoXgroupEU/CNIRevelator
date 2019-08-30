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

def reportBug(reason="",log="", isVoluntary=False):

    logfile = logger.logCur

    if not credentials:
        logfile.printerr("No credentials")
        return False

    session = credentials.sessionHandler

    if not isVoluntary:
        payload = {
                    'title':"CNIRevelator App Bug Report",
                    'body': (
                        "**An error has been reported by a CNIRevelator instance.**\n\n"

                        "**Global informations:**\n"
                        "verType = {}\n"
                        "version= {}\n"
                        "verstring_full = {}\n"
                        "CNIRTesserHash = {}\n"
                        "CNIRGitToken = {}\n"
                        "CNIRName = {}\n"
                        "CNIRCryptoKey = {}\n"
                        "CNIRlang = {}\n"
                        "CNIRVerStock = {}\n"
                        "CNIREnv = {}\n"
                        "CNIRBetaURL = {}\n"
                        "CNIRDefaultURL = {}\n"
                        "CNIRNewVersion = {}\n"
                        "CNIROpenFile = {}\n"
                        "debug = {}\n"
                        "\n\n"

                        "**Full reason of the crash:**\n{}\n\n"

                        "**Full log:** {}"

                        ).format(
                                globs.verType,
                                globs.version,
                                globs.verstring_full,
                                globs.CNIRTesserHash,
                                globs.CNIRGitToken,
                                globs.CNIRName,
                                globs.CNIRCryptoKey,
                                globs.CNIRlang,
                                globs.CNIRVerStock,
                                globs.CNIREnv,
                                globs.CNIRBetaURL,
                                globs.CNIRDefaultURL,
                                globs.CNIRNewVersion,
                                globs.CNIROpenFile,
                                globs.debug,
                                reason,
                                log
                                ),
                    "assignees":["neox95"], "labels":["bug", "AUTO"]
                  }
    else:
        payload = {
                    'title':"CNIRevelator User Bug Report",
                    'body': (
                        "**An error has been reported by a CNIRevelator user.**\n\n"

                        "**Global informations:**\n"
                        "verType = {}\n"
                        "version= {}\n"
                        "verstring_full = {}\n"
                        "CNIRTesserHash = {}\n"
                        "CNIRGitToken = {}\n"
                        "CNIRName = {}\n"
                        "CNIRCryptoKey = {}\n"
                        "CNIRlang = {}\n"
                        "CNIRVerStock = {}\n"
                        "CNIREnv = {}\n"
                        "CNIRBetaURL = {}\n"
                        "CNIRDefaultURL = {}\n"
                        "CNIRNewVersion = {}\n"
                        "CNIROpenFile = {}\n"
                        "debug = {}\n"
                        "\n\n"

                        "**Possible reason:**\n{}\n\n"

                        "**Full log:** {}"

                        ).format(
                                globs.verType,
                                globs.version,
                                globs.verstring_full,
                                globs.CNIRTesserHash,
                                globs.CNIRGitToken,
                                globs.CNIRName,
                                globs.CNIRCryptoKey,
                                globs.CNIRlang,
                                globs.CNIRVerStock,
                                globs.CNIREnv,
                                globs.CNIRBetaURL,
                                globs.CNIRDefaultURL,
                                globs.CNIRNewVersion,
                                globs.CNIROpenFile,
                                globs.debug,
                                reason,
                                log
                                ),
                    "assignees":["neox95"], "labels":["bug", "AUTO"]
                  }

    handler = session.post('https://api.github.com/repos/neox95/cnirevelator/issues', headers={'Authorization': 'token %s' % decryptToken(globs.CNIRGitToken)}, data=json.dumps(payload))

    logfile.printdbg("Issue is " + handler.reason)

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


