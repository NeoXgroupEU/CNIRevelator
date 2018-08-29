"""
******************************************************************************** 
                ***   Projet  CNI_Revelator   ***
                       
                        GNU GPL * 07/2018

                        Adrien Bourmault
                            
                            VARIABLES 

********************************************************************************
"""
CST_REV = "8"
CST_VERTITLE = "2.2"
CST_TAB_VER = ["2","2","1"]
CST_VER = "{0}.{1}.{2}".format(CST_TAB_VER[0], CST_TAB_VER[1], CST_TAB_VER[2])
CST_TYPE = "Final Release"
CST_NAME = "CNIRevelator"
CST_TITLE = CST_NAME + " " +  CST_VER + " - GNU/GPL Licensing 2018"
CST_MARK = CST_NAME + " " + CST_TYPE + " " + CST_VER + " - by NeoX, GNU/GPL Licensing 2018"
CST_SUM_VER = int(CST_TAB_VER[0])*100 + int(CST_TAB_VER[1])*10 + int(CST_TAB_VER[2])
CST_LINK = <lien vers serveur>
CST_COLOR = "#003380"


import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter import ttk as ttk
import os
import time 
import threading
import sys
import urllib.request as urllib2
import urllib.error as URLExcept
import random
from pypac import PACSession
from requests.auth import HTTPProxyAuth
import subprocess
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw, ImageTk, ImageEnhance, ImageFilter
import math
import warnings
import string

CST_FOLDER = os.getenv('APPDATA') + "/CNIRevelator/"