# -*- coding: utf8 -*-
"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher global variables                           *
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
import os

# CNIRevelator version
verType             = "stable release"
version             = [3, 1, 5]
verstring_full      = "{}.{}.{} {}".format(version[0], version[1], version[2], verType)
verstring           = "{}.{}".format(version[0], version[1])

CNIRTesserHash      = "947224361ffab8c01f05c9394b44b1bd7c8c3d4d"
CNIRGitToken        = "mJHKXqnazO/xZ9Fs18SDMqcGJ15A27OlZyd27cDe5dhHKklO2YShdWwUgEDUZQI02kpgYaLceMidTK37ZqakW+VYgPPuh0e9Ry2IH0KHc3o="
CNIRFolder          = os.path.dirname(os.path.realpath(__file__))
CNIRLColor          = "#006699"
CNIRName            = "CNIRevelator {}".format(verstring)
CNIRCryptoKey       = '82Xh!efX3#@P~2eG'

CNIRLangFile        = CNIRFolder + '\\config\\lang.ig'
CNIRlang            = "fr"

CNIRConfig          = CNIRFolder + '\\config\\conf.ig'
CNIRTesser          = CNIRFolder + '\\Tesseract-OCR5\\'
CNIRErrLog          = CNIRFolder + '\\logs\\error.log'
CNIRMainLog         = CNIRFolder + '\\logs\\main.log'
CNIRUrlConfig       = CNIRFolder + '\\config\\urlconf.ig'
CNIRLastUpdate      = CNIRFolder + '\\config\\lastupdate.ig'
CNIRVerStock        = CNIRFolder + '\\downloads\\versions.lst'
CNIREnv             = CNIRFolder + '\\Data\\'

CNIRBetaURL         = "https://raw.githubusercontent.com/neox95/CNIRevelator/v3.1/VERSIONS.LST"
CNIRDefaultURL      = "https://raw.githubusercontent.com/neox95/CNIRevelator/master/VERSIONS.LST"

CNIRNewVersion      = False
CNIROpenFile        = False
debug               = True