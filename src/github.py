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
from requests import Session
import json

import logger  # logger.py
import globs   # globs.py

credentials = False

def reportBug(reason="",log=""):

    logfile = logger.logCur

    if not credentials:
        logfile.printerr("No credentials")
        return False

    session = credentials.sessionHandler

    payload = {'title':"CNIRevelator Bug Report", 'body':"**An error has been reported by a CNIRevelator instance.**\n\n**Here is the full reason of this issue:**\n{}\n\n**The full log is here:** {}".format(reason, log), "assignees":["neox95"], "labels":["bug", "AUTO"]}

    handler = session.post('https://api.github.com/repos/neox95/cnirevelator/issues', headers={'Authorization': 'token %s' % globs.CNIRGitToken}, data=json.dumps(payload))

    logfile.printdbg(handler.reason)

    if handler.reason == "Created":
        return True
    else:
        return False


