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
version             = [3, 0, 0]
verstring_full      = "{}.{}.{}".format(version[0], version[1], version[2])
verstring           = "{}.{}".format(version[0], version[1])

changelog           = "Mise-à-jour majeure avec corrections suivantes :\n- Renouvellement de la signature numérique de l'exécutable\n- Amélioration de présentation du log en cas d'erreur\n- Refonte totale du code source et désobfuscation\n- Téléchargements en HTTPS fiables avec somme de contrôle"

CNIRTesserHash      = '5b58db27f7bc08c58a2cb33d01533b034b067cf8'
CNIRFolder          = os.getcwd()
CNIRLColor          = "#006699"
CNIRName            = "CNIRevelator {}".format(verstring)
CNIRCryptoKey       = '82Xh!efX3#@P~2eG'
CNIRNewVersion      = False

CNIRConfig          = CNIRFolder + '\\config\\conf.ig'
CNIRErrLog          = CNIRFolder + '\\logs\\error.log'
CNIRLauncherLog     = CNIRFolder + '\\logs\\launcher.log'
CNIRMainLog         = CNIRFolder + '\\logs\\main.log'
CNIRUrlConfig       = CNIRFolder + '\\config\\urlconf.ig'
CNIRVerStock        = CNIRFolder + '\\downloads\\versions.lst'
CNIREnv             = os.getenv('APPDATA') + '/CNIRevelator/'
