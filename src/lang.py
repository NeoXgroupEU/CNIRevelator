"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application langage file                                        *
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

import globs                        # globs.py

## FRENCH LANGUAGE
french = \
{
"Please type a MRZ or open a scan"  :   "Veuillez taper une MRZ ou ouvrir un scan svp",
"Changelog : update summary"        :   "Changelog : résumé de mise à jour",
"Program version"                   :   "Version du logiciel",
"CNIRevelator Fatal Error"          :   "Erreur fatale de CNIRevelator",
"An error has occured"              :   "Une erreur s'est produite",
"Downloading"                       :   "Téléchargement de",
"Successful retrieved"              :   "Réussite du téléchargement de",
"Choose the identity document"      :   "Choisir le document d'identité",
"OCR Detection Validation"          :   "Validation de la MRZ détectée par OCR",
"Validate"                          :   "Valider",
"Validation Error"                  :   "Erreur de validation",
"The submitted MRZ contains invalid "
 "characters"                       :   "La MRZ soumise contient des caractères invalides",
"Connection"                        :   "Connexion",
"Password"                          :   "Mot de passe",
"Booting up..."                     :   "Démarrage",
"CNIRevelator Fatal Eror"           :   "Erreur Fatale de CNIRevelator",
"CNIRevelator crashed because a "
"fatal error occured. View log for "
"more infos and please open "
"an issue on Github"                :   "CNIRevelator s'est arrêté car une erreur fatale s'est produite. Consultez le journal pour plus d'informations et ouvrez s'il vous plaît un ticket sur Github.",
"Would you like to open an issue "
"on Github to report this bug ?"    :   "Souhaitez-vous ouvrir un ticket sur Github pour signaler ce bogue?",
"Starting..."                       :   "Lancement...",
"Informations about the current "
"document"                          :   "Informations sur la pièce d'identité",
"IDLE"                              :   "EN ATTENTE",
"Status"                            :   "Statut",
"Name"                              :   "Nom",
"Birth date"                        :   "Date de naissance",
"Issue date"                        :   "Date de délivrance",
"Expiration date"                   :   "Date d'expiration",
"Sex"                               :   "Sexe",
"Issuing country"                   :   "Pays émetteur",
"Nationality"                       :   "Nationalité",
"Registration"                      :   "Immatriculation",
"Document number"                   :   "Numéro de document",
"Unknown"                           :   "Inconnu(e)",
"Display and processing of "
"documents"                         :   "Affichage et traitement de documents",
"Complete MRZ capture terminal"     :   "Terminal de saisie de MRZ complète",
"Quick entry terminal (731)"        :   "Terminal de saisie rapide (731)",
"Monitor"                           :   "Moniteur",
"New"                               :   "Nouveau",
"Open scan..."                      :   "Ouvrir scan...",
"Quit"                              :   "Quitter",
"File"                              :   "Fichier",
"Keyboard commands"                 :   "Commandes au clavier",
"Report a bug"                      :   "Signaler un problème",
"About CNIRevelator"                :   "A propos de CNIRevelator",
"Help"                              :   "Aide",
"OCR module error"                  :   "Erreur du module OCR",
"The OCR module located at {} "
"can not be found or corrupted. "
"It will be reinstalled at "
"the next run"                      :   "Le module OCR localisé en {} est introuvable ou corrompu. Il sera réinstallé à la prochaine exécution",
"The Tesseract module "
"encountered a problem: {}"         :   "Le module Tesseract a rencontré un problème : {}",
"Tesseract error : {}. "
"Will be reinstallated"             :   "Erreur de Tesseract : {}. Le module sera réinstallé",
"Document detected: {}\n"           :   "Document detecté : {}\n",
"Document detected again: {}\n"     :   "Document re-detecté : {}\n",
"Character not accepted !\n"        :   "Caractère non accepté !\n",
"Open a scan of document..."        :   "Ouvrir un scan de document...",
"OpenCV error (image processing)"   :   "Erreur OpenCV (traitement d'images)",
"A critical error has occurred in "
"the OpenCV image processing "
"manager used by CNIRevelator, the "
"application will reset itself"     :   "Une erreur critique s'est produite dans le gestionnaire de traitement d'images OpenCV utilisé par CNIRevelator. L'application va se réinitialiser",
"ABOUT"                             :   'Version du logiciel : CNIRevelator ' + globs.verstring_full + '\n\n'
                                        "Copyright © 2018-2019 Adrien Bourmault (neox95)" + "\n\n"
                                        "CNIRevelator est un logiciel libre : vous avez le droit de le modifier et/ou le distribuer "
                                        "dans les termes de la GNU General Public License telle que publiée par "
                                        "la Free Software Foundation, dans sa version 3 ou "
                                        "ultérieure. " + "\n\n"
                                        "CNIRevelator est distribué dans l'espoir d'être utile, sans toutefois "
                                        "impliquer une quelconque garantie de "
                                        "QUALITÉ MARCHANDE ou APTITUDE À UN USAGE PARTICULIER. Référez vous à la "
                                        "GNU General Public License pour plus de détails à ce sujet. "
                                        "\n\n"
                                        "Vous devriez avoir reçu une copie de la GNU General Public License "
                                        "avec CNIRevelator. Si cela n'est pas le cas, jetez un oeil à <https://www.gnu.org/licenses/>. "
                                        "\n\n"
                                        "Le module d'OCR Tesseract 4.0 est soumis à l'Apache License 2004."
                                        "\n\n"
                                        "Les bibliothèques python et l'environnement Anaconda 3 sont soumis à la licence BSD 2018-2019."
                                        "\n\n"
                                        "Le code source de ce programme est disponible sur Github à l'adresse <https://github.com/neox95/CNIRevelator>.\n"
                                        "Son fonctionnement est conforme aux normes et directives du document 9303 de l'OACI régissant les documents de voyages et d'identité." + '\n\n'
                                        " En cas de problèmes ou demande particulière, ouvrez-y une issue ou bien envoyez un mail à neox@os-k.eu !\n\n",

"KEYBHELP"                          :   "Terminal de saisie rapide (731) : \n\n"
                                        "Caractères autorisés : Alphanumériques en majuscule et le caractère '<'. Pas de minuscules ni caractères spéciaux, autrement la somme est mise à zéro \n\n"
                                        "Calculer résultat :\t\t\tTouche Ctrl droite \n"
                                        "Copier :\t\t\t\tCtrl-C \n"
                                        "Coller :\t\t\t\tCtrl-V \n"
                                        "\n\n"
                                        "Terminal de saisie MRZ complète : \n\n"
                                        "Caractères autorisés : Alphanumériques en majuscule et le caractère '<'. Pas de minuscules ni caractères spéciaux, autrement la somme est mise à zéro \n\n"
                                        "Calculer résultat :\t\t\tTouche Ctrl droite \n"
                                        "Compléter champ :\t\t\tTouche Tab \n"
                                        "Copier :\t\t\t\tCtrl-C \n"
                                        "Coller :\t\t\t\tCtrl-V \n"
                                        "Forcer une nouvelle détection du document :\tEchap\n",
"Document Review: {}\n\n"           :   "Examen du document : {}\n\n",
"Check sum position {}: Lu {} VS "
"Calculated {} and {}\n"            :   "Check sum position {}: Lu {} VS Calculated {} and {}\n",
"COMPLIANT"                         :   "CONFORME",
"IMPROPER"                          :   "NON CONFORME",
"Installing the updates"            :   "Installation des mises-à-jour",
"Verifying download..."             :   "Vérification du téléchargement ...",
"Preparing installation..."         :   "Préparation de l'installation",
"Success !"                         :   "Installation terminée !",
"Launching the new version..."      :   "Lancement de la nouvelle version...",
"Credentials Error. No effective "
"update !"                          :   "Identifiants incorrects. Pas de mise-à-jour !",
"Deleting old version"              :   "Suppression de l'ancienne version",
'Software is up-to-date !'          :   "Logiciel à jour !",
"An error occured. "
"No effective update !"             :   "Une erreur s'est produite. Pas de mise-à-jour !",
"Shortcut creation"                 :   "Création de raccourci",
"Would you like to create/update "
"the shortcut for CNIRevelator "
"on your desktop ?"                 : "Souhaitez vous créer/mettre à jour le raccourci pour CNIRevelator sur votre bureau ?",
"The file you provided is "
"not found : {}"                    : "Fichier transmis non trouvé : {}"
}

## ENGLISH LANGUAGE

english = \
{
"Please type a MRZ or open a scan"  :   "Please type a MRZ or open a scan",
"Changelog : update summary"        :   "Changelog : update summary",
"Program version"                   :   "Program version",
"CNIRevelator Fatal Error"          :   "CNIRevelator Fatal Error" ,
"An error has occured"              :   "An error has occured",
"Downloading"                       :   "Downloading",
"Successful retrieved"              :   "Successful retrieved",
"Choose the identity document"      :   "Choose the identity document" ,
"OCR Detection Validation"          :   "OCR Detection Validation",
"Validate"                          :   "Validate",
"Validation Error"                  :   "Validation Error",
"The submitted MRZ contains invalid "
 "characters"                       :   "The submitted MRZ contains invalid characters",
"Connection"                        :   "Connection",
"Password"                          :   "Password",
"Booting up..."                     :   "Booting up...",
"CNIRevelator Fatal Eror"           :   "CNIRevelator Fatal Eror",
"CNIRevelator crashed because a "
"fatal error occured. View log for "
"more infos and please open "
"an issue on Github"                :   "CNIRevelator crashed because a fatal error occured. View log for more infos and please open an issue on Github",
"Would you like to open an issue "
"on Github to report this bug ?"    :   "Would you like to open an issue on Github to report this bug ?",
"Starting..."                       :   "Starting...",
"Informations about the current "
"document"                          :   "Informations about the current document",
"IDLE"                              :   "IDLE",
"Status"                            :   "Status",
"Name"                              :   "Name",
"Birth date"                        :   "Birth date",
"Issue date"                        :   "Date de délivrance",
"Expiration date"                   :   "Issue date",
"Sex"                               :   "Sex",
"Issuing country"                   :   "Issuing country",
"Nationality"                       :   "Nationality",
"Registration"                      :   "Registration",
"Document number"                   :   "Document number",
"Unknown"                           :   "Unknown",
"Display and processing of "
"documents"                         :   "Display and processing of documents",
"Complete MRZ capture terminal"     :   "Complete MRZ capture terminal",
"Quick entry terminal (731)"        :   "Quick entry terminal (731)",
"Monitor"                           :   "Monitor",
"New"                               :   "New",
"Open scan..."                      :   "Open scan...",
"Quit"                              :   "Quit",
"File"                              :   "File",
"Keyboard commands"                 :   "Keyboard commands",
"Report a bug"                      :   "Report a bug",
"About CNIRevelator"                :   "About CNIRevelator",
"Help"                              :   "Help",
"OCR module error"                  :   "OCR module error",
"The OCR module located at {} "
"can not be found or corrupted. "
"It will be reinstalled at "
"the next run"                      :   "The OCR module located at {} can not be found or corrupted. It will be reinstalled at the next run",
"The Tesseract module "
"encountered a problem: {}"         :   "The Tesseract module encountered a problem: {}",
"Tesseract error : {}. "
"Will be reinstallated"             :   "Tesseract error : {}. Will be reinstallated",
"Document detected: {}\n"           :   "Document detected : {}\n",
"Document detected again: {}\n"     :   "Document detected again : {}\n",
"Character not accepted !\n"        :   "Character not accepted !\n",
"Open a scan of document..."        :   "Open a scan of document...",
"OpenCV error (image processing)"   :   "OpenCV error (image processing)",
"A critical error has occurred in "
"the OpenCV image processing "
"manager used by CNIRevelator, the "
"application will reset itself"     :   "A critical error has occurred in the OpenCV image processing manager used by CNIRevelator, the application will reset itself",

"ABOUT"                             :   'Software Version: CNIRevelator' + globs.verstring_full + '\n\n'
                                        "Copyright © 2018-2019 Adrien Bourmault (neox95)" + "\n\n"
                                        "CNIRevelator is free software: you have the right to modify and / or distribute it"
                                        "in the terms of the GNU General Public License as published by"
                                        "Free Software Foundation, version 3 or"
                                        "later." + "\n\n"
                                        "CNIRevelator is distributed in the hope of being useful, without however"
                                        "imply any guarantee of"
                                        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE Refer to the"
                                        "GNU General Public License for more details about this."
                                        "\n\n"
                                        "You should have received a copy of the GNU General Public License"
                                        "with CNIRevelator, if this is not the case, take a look at <https://www.gnu.org/licenses/>."
                                        "\n\n"
                                        "The Tesseract 4.0 OCR module is subject to the 2004 Apache License."
                                        "\n\n"
                                        "Python libraries and the Anaconda 3 environment are subject to the BSD 2018-2019 license."
                                        "\n\n"
                                        "The source code for this program is available on Github at <https://github.com/neox95/CNIRevelator>. \n"
                                        "Its operation is in accordance with the standards and guidelines of ICAO document 9303 governing travel and identity documents." + '\n\n'
                                        "In case of problems or special request, open an issue or send an email to neox@os-k.eu! \n\n",


"KEYBHELP"                          :   "Fast entry terminal (731): \n\n"
                                        "Allowed characters: Alphanumeric uppercase and the character '<' No lowercase or special characters, otherwise the sum is set to zero \n\n"
                                        "Calculate Result:\t\t\tControl Right\n"
                                        "Copy:\t\t\t\tCtrl-C\n"
                                        "Paste:\t\t\t\tCtrl-V\n"
                                        "\n\n"
                                        "MRZ input terminal complete: \n\n"
                                        "Allowed characters: Alphanumeric uppercase and the character '<' No lowercase or special characters, otherwise the sum is set to zero \n\n"
                                        "Calculate Result:\t\t\tControl Right\n"
                                        "Complete field:\t\t\tTab button\n"
                                        "Copy:\t\t\t\tCtrl-C\n"
                                        "Paste:\t\t\t\tCtrl-V\n"
                                        "Force a new document detection:\tEchap\n",

"Document Review: {}\n\n"           :   "Document Review: {}\n\n",
"Check sum position {}: Lu {} VS "
"Calculated {} and {}\n"            :   "Check sum position {}: Lu {} VS Calculated {} and {}\n",
"COMPLIANT"                         :   "COMPLIANT",
"IMPROPER"                          :   "IMPROPER",
"Installing the updates"            :   "Installing the updates",
"Verifying download..."             :   "Verifying download...",
"Preparing installation..."         :   "Preparing installation...",
"Success !"                         :   "Success !",
"Launching the new version..."      :   "Launching the new version...",
"Credentials Error. No effective "
"update !"                          :   "Credentials Error. No effective update !",
"Deleting old version"              :   "Deleting old version",
'Software is up-to-date !'          :   "Software is up-to-date !",
"An error occured. "
"No effective update !"             :   "An error occured. No effective update !",
"Shortcut creation"                 :   "Shortcut creation",
"Would you like to create/update "
"the shortcut for CNIRevelator on "
"your desktop ?"                    : "Would you like to create/update the shortcut for CNIRevelator on your desktop ?",
"The file you provided is not "
"found : {}"                        : "The file you provided is not found : {}"
}

## MAIN DICT
all = \
{
"fr" : french,
"en" : english
}