"""
******************************************************************************** 
                ***   Projet  CNI_Revelator   ***
                       
                        GNU GPL * 07/2018

                        Adrien Bourmault
                            
                            VARIABLES 

********************************************************************************
"""

class changelog:

    def __init__(self):
        self.isOn = False
        self.text = "Mise-à-jour de sécurité avec corrections suivantes :\n- ajout de la signature numérique de l'exécutable\n- ajout d'une clé de cryptage plus performante pour le stockage des identifiants\n- passage à la méthode de cryptage AES256\n\nAjout/correction des fonctionnalités suivantes :\n- somme de contrôle des téléchargements pour une meilleure fiabilité\n- amélioration de présentation du log en cas d'erreur\n- correction d'un bug affectant l'analyse des MRZ après la correction manuelle\n\nEt un petit bonjour à tout le monde! ;)"


CST_REV = '0'
CST_VERTITLE = '2.2'
CST_TAB_VER = ['2', '2', '5']
CST_VER = '{0}.{1}.{2}'.format(CST_TAB_VER[0], CST_TAB_VER[1], CST_TAB_VER[2])
CST_TYPE = 'Final Release'
CST_NAME = 'CNIRevelator'
CST_TITLE = CST_NAME + ' ' + CST_VER + ' - GNU/GPL Licensing 2018'
CST_MARK = CST_NAME + ' ' + CST_TYPE + ' ' + CST_VER + ' - by NeoX, GNU/GPL Licensing 2018'
CST_SUM_VER = int(CST_TAB_VER[0]) * 100 + int(CST_TAB_VER[1]) * 10 + int(CST_TAB_VER[2])
CST_LINK = 'http://neoxgroup.eu/ftpaccess/Applicatifs/CNIRevelator/'
CST_COLOR = '#003380'
CST_TesserHash = '5b58db27f7bc08c58a2cb33d01533b034b067cf8'


import base64, hashlib
from Crypto import Random
from Crypto.Cipher import AES
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter import ttk
import os, time, threading, sys, urllib.request as urllib2, urllib.error as URLExcept, random
from datetime import datetime

CST_FOLDER = os.getenv('APPDATA') + '/CNIRevelator/'
CST_CRYPTOKEY = '82Xh!efX3#@P~2eG'
CST_CHANGELOG = changelog()