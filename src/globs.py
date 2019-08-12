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
verType             = "final release"
version             = [3, 1, 0]
verstring_full      = "{}.{}.{} {}".format(version[0], version[1], version[2], verType)
verstring           = "{}.{}".format(version[0], version[1])
debug = True

changelog           =   "Version 3.1.0 \nMise-à-jour majeure avec les progressions suivantes :\n- Modifications cosmétiques de l'interface utilisateur\n- Stabilisation des changements effectués sur la version mineure 3.0 : interface utilisateur, OCR, VISA A et B, logging\n- Rationalisation du système de langues"

CNIRTesserHash      = '5b58db27f7bc08c58a2cb33d01533b034b067cf8'
CNIRFolder          = os.getcwd()
CNIRLColor          = "#006699"
CNIRName            = "CNIRevelator {}".format(verstring)
CNIRCryptoKey       = '82Xh!efX3#@P~2eG'
CNIRNewVersion      = False
CNIRLangFile        = CNIRFolder + '\\config\\lang.ig'
CNIRlang            = "fr"

CNIRConfig          = CNIRFolder + '\\config\\conf.ig'
CNIRTesser          = CNIRFolder + '\\Tesseract-OCR4\\'
CNIRErrLog          = CNIRFolder + '\\logs\\error.log'
CNIRMainLog         = CNIRFolder + '\\logs\\main.log'
CNIRUrlConfig       = CNIRFolder + '\\config\\urlconf.ig'
CNIRVerStock        = CNIRFolder + '\\downloads\\versions.lst'
CNIREnv             = CNIRFolder + '\\Data\\'

CNIROpenFile        = False