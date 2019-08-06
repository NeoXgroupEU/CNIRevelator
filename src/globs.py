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
verType             = "alpha"
version             = [3, 0, 5]
verstring_full      = "{}.{}.{} {}".format(version[0], version[1], version[2], verType)
verstring           = "{}.{}".format(version[0], version[1])
debug = True

changelog           =   "Version 3.0.5 \nMise-à-jour mineure avec les corrections suivantes :\n- Changement de l'icône de l'exécutable afin de refléter le changement de version majeur accompli en 3.0\n\n" + \
"Version 3.0.4 \nMise-à-jour mineure avec les corrections suivantes :\n- Correction d'un bug affectant le système de mise-à-jour\n\n" + \
"Version 3.0.3 \nMise-à-jour mineure avec les corrections suivantes :\n- Correction d'un bug affectant le changelog\n- Correction d'une erreur avec la touche Suppr Arrière et Suppr causant une perte de données\n\n" + \
"Version 3.0.2 \nMise-à-jour mineure avec les corrections suivantes :\n- Changement d'icône de l'exécutable\n- Correction d'un bug affectant le logging\n- Correction d'un bug affectant la détection de documents\n- Et autres modifications mineures\n\n" + \
"Version 3.0.1 \nMise-à-jour majeure avec les corrections suivantes :\n- Renouvellement de la signature numérique de l'exécutable\n- Amélioration de présentation du log en cas d'erreur\n- Refonte totale du code source et désobfuscation\n- Téléchargements en HTTPS fiables avec somme de contrôle\n- Nouveaux terminaux d'entrées : un rapide (731) et un complet\n- Détection des documents améliorée, possibilité de choix plus fin\nEt les regressions suivantes :\n- Suppression temporaire de la fonction de lecture OCR. Retour planifié pour une prochaine version"

CNIRTesserHash      = '5b58db27f7bc08c58a2cb33d01533b034b067cf8'
CNIRFolder          = os.getcwd()
CNIRLColor          = "#006699"
CNIRName            = "CNIRevelator {}".format(verstring)
CNIRCryptoKey       = '82Xh!efX3#@P~2eG'
CNIRNewVersion      = False

CNIRConfig          = CNIRFolder + '\\config\\conf.ig'
CNIRErrLog          = CNIRFolder + '\\logs\\error.log'
CNIRMainLog         = CNIRFolder + '\\logs\\main.log'
CNIRUrlConfig       = CNIRFolder + '\\config\\urlconf.ig'
CNIRVerStock        = CNIRFolder + '\\downloads\\versions.lst'
CNIREnv             = CNIRFolder + '\\Data\\'
