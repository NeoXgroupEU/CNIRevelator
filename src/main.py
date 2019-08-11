"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application IHM & work main class                               *
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

from PIL import Image, ImageFont, ImageDraw, ImageTk, ImageEnhance, ImageFilter
import math, warnings, string
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter import ttk
import threading
from datetime import datetime
import re
import traceback
import cv2
import PIL.Image, PIL.ImageTk
import os, shutil
import webbrowser

import ihm                      # ihm.py
import logger                   # logger.py
import mrz                      # mrz.py
import globs                    # globs.py
import pytesseract              # pytesseract.py

# Global handler
logfile = logger.logCur

class mainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.initialize()

    def initialize(self):
        self.mrzChar = ""
        self.mrzDecided = False
        self.Tags = []
        self.compliance = True
        self.corners = []
        self.validatedtext = ""

        # Hide during construction
        self.withdraw()

        # Get the screen size and center
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        logfile.printdbg('Launching main window with resolution' + str(ws) + 'x' + str(hs))

        # Configuring the size of each part of the window
        self.grid_columnconfigure(0, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_columnconfigure(1, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_columnconfigure(2, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_rowconfigure(0, weight=1, minsize=(hs / 2 * 0.5))
        self.grid_rowconfigure(1, weight=1, minsize=(hs / 2 * 0.10))
        self.grid_rowconfigure(2, weight=1, minsize=(hs / 2 * 0.35))

        # Prepare the data sections
        self.lecteur_ci = ttk.Labelframe(self, text="Informations sur la pièce d'identité")
        self.lecteur_ci.grid_columnconfigure(0, weight=1)
        self.lecteur_ci.grid_columnconfigure(1, weight=1)
        self.lecteur_ci.grid_columnconfigure(2, weight=1)
        self.lecteur_ci.grid_columnconfigure(3, weight=1)
        self.lecteur_ci.grid_columnconfigure(4, weight=1)
        self.lecteur_ci.grid_columnconfigure(5, weight=1)
        self.lecteur_ci.grid_rowconfigure(1, weight=1)
        self.lecteur_ci.grid_rowconfigure(2, weight=1)
        self.lecteur_ci.grid_rowconfigure(3, weight=1)
        self.lecteur_ci.grid_rowconfigure(4, weight=1)
        self.lecteur_ci.grid_rowconfigure(5, weight=1)

        # Fill the data sections
        ttk.Label((self.lecteur_ci), text='Statut : ').grid(column=0, row=0, padx=5, pady=5)
        self.STATUStxt = ttk.Label((self.lecteur_ci), text='EN ATTENTE', font=("TkDefaultFont", 13, "bold"), foreground="orange", anchor=CENTER)
        self.STATUStxt.grid(column=1, row=0, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Nom : ').grid(column=0, row=1, padx=5, pady=5)
        self.nom = ttk.Label((self.lecteur_ci), text=' ')
        self.nom.grid(column=1, row=1, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Nom (2) : ').grid(column=0, row=2, padx=5, pady=5)
        self.prenom = ttk.Label((self.lecteur_ci), text=' ')
        self.prenom.grid(column=1, row=2, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Date de naissance : ').grid(column=0, row=3, padx=5, pady=5)
        self.bdate = ttk.Label((self.lecteur_ci), text=' ')
        self.bdate.grid(column=1, row=3, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Date de délivrance : ').grid(column=0, row=4, padx=5, pady=5)
        self.ddate = ttk.Label((self.lecteur_ci), text=' ')
        self.ddate.grid(column=1, row=4, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text="Date d'expiration : ").grid(column=0, row=5, padx=5, pady=5)
        self.edate = ttk.Label((self.lecteur_ci), text=' ')
        self.edate.grid(column=1, row=5, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Sexe du porteur : ').grid(column=4, row=1, padx=5, pady=5)
        self.sex = ttk.Label((self.lecteur_ci), text=' ')
        self.sex.grid(column=5, row=1, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Pays de délivrance : ').grid(column=4, row=2, padx=5, pady=5)
        self.pays = ttk.Label((self.lecteur_ci), text=' ')
        self.pays.grid(column=5, row=2, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Nationalité du porteur : ').grid(column=4, row=3, padx=5, pady=5)
        self.nat = ttk.Label((self.lecteur_ci), text=' ')
        self.nat.grid(column=5, row=3, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Immatriculation : ').grid(column=4, row=4, padx=5, pady=5)
        self.indic = ttk.Label((self.lecteur_ci), text=' ')
        self.indic.grid(column=5, row=4, padx=5, pady=5)
        ttk.Label((self.lecteur_ci), text='Numéro de document : ').grid(column=4, row=5, padx=5, pady=5)
        self.no = ttk.Label((self.lecteur_ci), text=' ')
        self.no.grid(column=5, row=5, padx=5, pady=5)

        self.nom['text'] = 'Inconnu(e)'
        self.prenom['text'] = 'Inconnu(e)'
        self.bdate['text'] = 'Inconnu(e)'
        self.ddate['text'] = 'Inconnu(e)'
        self.edate['text'] = 'Inconnu(e)'
        self.no['text'] = 'Inconnu(e)'
        self.sex['text'] = 'Inconnu(e)'
        self.nat['text'] = 'Inconnu(e)'
        self.pays['text'] = 'Inconnu(e)'
        self.indic['text'] = 'Inconnu(e)'


        self.infoList = \
        {
            "NOM"    : self.nom,
            "PRENOM" : self.prenom,
            "BDATE"  : self.bdate,
            "DDATE"  : self.ddate,
            "EDATE"  : self.edate,
            "NO"     : self.no,
            "SEX"    : self.sex,
            "NAT"    : self.nat,
            "PAYS"   : self.pays,
            "INDIC"  : self.indic,
        }

        # The the image viewer
        self.imageViewer = ttk.Labelframe(self, text='Affichage et traitement de documents')
        self.imageViewer.grid_columnconfigure(0, weight=1)
        self.imageViewer.grid_columnconfigure(1, weight=0)
        self.imageViewer.grid_rowconfigure(0, weight=1)
        self.imageViewer.grid_rowconfigure(1, weight=1)
        self.imageViewer.grid_rowconfigure(2, weight=1)
        self.imageViewer.frame = Frame(self.imageViewer)
        self.imageViewer.frame.grid(column=0, row=0, sticky='NSEW')
        self.imageViewer.frame.grid_columnconfigure(0, weight=1)
        self.imageViewer.frame.grid_rowconfigure(0, weight=1)
        # + toolbar
        self.toolbar = ttk.Frame(self.imageViewer)
        self.toolbar.grid_columnconfigure(0, weight=1)
        self.toolbar.grid_columnconfigure(1, weight=1)
        self.toolbar.grid_columnconfigure(2, weight=1)
        self.toolbar.grid_columnconfigure(3, weight=1)
        self.toolbar.grid_columnconfigure(4, weight=1)
        self.toolbar.grid_columnconfigure(5, weight=1)
        self.toolbar.grid_columnconfigure(6, weight=1, minsize=10)
        self.toolbar.grid_columnconfigure(7, weight=1)
        self.toolbar.grid_columnconfigure(8, weight=1, minsize=10)
        self.toolbar.grid_columnconfigure(9, weight=1)
        self.toolbar.grid_columnconfigure(10, weight=1)
        self.toolbar.grid_columnconfigure(11, weight=1)
        self.toolbar.grid_columnconfigure(12, weight=1)
        self.toolbar.grid_columnconfigure(13, weight=1, minsize=10)
        self.toolbar.grid_columnconfigure(14, weight=1)
        self.toolbar.grid_columnconfigure(15, weight=1, minsize=10)
        self.toolbar.grid_columnconfigure(16, weight=1)
        self.toolbar.grid_rowconfigure(0, weight=1)

        self.toolbar.zoomIn50Img = ImageTk.PhotoImage(PIL.Image.open("zoomIn50.png"))
        self.toolbar.zoomIn50 = ttk.Button(self.toolbar, image=self.toolbar.zoomIn50Img, command=self.zoomInScan50)
        self.toolbar.zoomIn50.grid(column=0, row=0)

        self.toolbar.zoomIn20Img = ImageTk.PhotoImage(PIL.Image.open("zoomIn20.png"))
        self.toolbar.zoomIn20 = ttk.Button(self.toolbar, image=self.toolbar.zoomIn20Img, command=self.zoomInScan20)
        self.toolbar.zoomIn20.grid(column=1, row=0)

        self.toolbar.zoomInImg = ImageTk.PhotoImage(PIL.Image.open("zoomIn.png"))
        self.toolbar.zoomIn = ttk.Button(self.toolbar, image=self.toolbar.zoomInImg, command=self.zoomInScan)
        self.toolbar.zoomIn.grid(column=2, row=0)

        self.toolbar.zoomOutImg = ImageTk.PhotoImage(PIL.Image.open("zoomOut.png"))
        self.toolbar.zoomOut = ttk.Button(self.toolbar, image=self.toolbar.zoomOutImg, command=self.zoomOutScan)
        self.toolbar.zoomOut.grid(column=3, row=0)

        self.toolbar.zoomOut20Img = ImageTk.PhotoImage(PIL.Image.open("zoomOut20.png"))
        self.toolbar.zoomOut20 = ttk.Button(self.toolbar, image=self.toolbar.zoomOut20Img, command=self.zoomOutScan20)
        self.toolbar.zoomOut20.grid(column=4, row=0)

        self.toolbar.zoomOut50Img = ImageTk.PhotoImage(PIL.Image.open("zoomOut50.png"))
        self.toolbar.zoomOut50 = ttk.Button(self.toolbar, image=self.toolbar.zoomOut50Img, command=self.zoomOutScan50)
        self.toolbar.zoomOut50.grid(column=5, row=0)

        self.toolbar.invertImg = ImageTk.PhotoImage(PIL.Image.open("invert.png"))
        self.toolbar.invert = ttk.Button(self.toolbar, image=self.toolbar.invertImg, command=self.negativeScan)
        self.toolbar.invert.grid(column=7, row=0)

        self.toolbar.rotateLeftImg = ImageTk.PhotoImage(PIL.Image.open("rotateLeft.png"))
        self.toolbar.rotateLeft = ttk.Button(self.toolbar, image=self.toolbar.rotateLeftImg, command=self.rotateLeft)
        self.toolbar.rotateLeft.grid(column=9, row=0)

        self.toolbar.rotateLeft1Img = ImageTk.PhotoImage(PIL.Image.open("rotateLeft1.png"))
        self.toolbar.rotateLeft1 = ttk.Button(self.toolbar, image=self.toolbar.rotateLeft1Img, command=self.rotateLeft1)
        self.toolbar.rotateLeft1.grid(column=10, row=0)

        self.toolbar.rotateRight1Img = ImageTk.PhotoImage(PIL.Image.open("rotateRight1.png"))
        self.toolbar.rotateRight1 = ttk.Button(self.toolbar, image=self.toolbar.rotateRight1Img, command=self.rotateRight1)
        self.toolbar.rotateRight1.grid(column=11, row=0)

        self.toolbar.rotateRightImg = ImageTk.PhotoImage(PIL.Image.open("rotateRight.png"))
        self.toolbar.rotateRight = ttk.Button(self.toolbar, image=self.toolbar.rotateRightImg, command=self.rotateRight)
        self.toolbar.rotateRight.grid(column=12, row=0)
        
        self.toolbar.goOCRImg = ImageTk.PhotoImage(PIL.Image.open("OCR.png"))
        self.toolbar.goOCR = ttk.Button(self.toolbar, image=self.toolbar.goOCRImg, command=self.goOCRDetection)
        self.toolbar.goOCR.grid(column=14, row=0)
        
        self.toolbar.pagenumber = StringVar()
        self.toolbar.pageChooser = ttk.Combobox(self.toolbar, textvariable=self.toolbar.pagenumber)
        self.toolbar.pageChooser.bind("<<ComboboxSelected>>", self.goPageChoice)
        self.toolbar.pageChooser['values'] = ('1')
        self.toolbar.pageChooser.current(0)
        self.toolbar.pageChooser.grid(column=16, row=0)

        self.toolbar.grid(column=0, row=2, padx=0, pady=0)

        # + image with scrollbars
        self.imageViewer.hbar = ttk.Scrollbar(self.imageViewer, orient='horizontal')
        self.imageViewer.vbar = ttk.Scrollbar(self.imageViewer, orient='vertical')
        self.imageViewer.hbar.grid(row=1, column=0, sticky="NSEW")
        self.imageViewer.vbar.grid(row=0, column=1, sticky="NSEW")

        self.imageViewer.ZONE = ihm.ResizeableCanvas(self.imageViewer.frame, bg=self["background"], xscrollcommand=(self.imageViewer.hbar.set),
          yscrollcommand=(self.imageViewer.vbar.set))
        self.imageViewer.ZONE.grid(sticky="NSEW")

        self.imageViewer.hbar.config(command=self.imageViewer.ZONE.xview)
        self.imageViewer.vbar.config(command=self.imageViewer.ZONE.yview)

        self.STATUSimg = self.imageViewer.ZONE.create_image(0,0, image=None, anchor="nw")
        

        # The terminal to enter the MRZ
        self.terminal = ttk.Labelframe(self, text='Terminal de saisie de MRZ complète')
        self.terminal.grid_columnconfigure(0, weight=1)
        self.terminal.grid_rowconfigure(0, weight=1)
        self.termframe = Frame(self.terminal)
        self.termframe.grid(column=0, row=0, sticky='EW')
        self.termframe.grid_columnconfigure(0, weight=1)
        self.termframe.grid_rowconfigure(0, weight=1)
        self.termguide = Label((self.termframe), text='', font='Terminal 17', fg='#006699')
        self.termguide.grid(column=0, row=0, padx=5, pady=0, sticky='NW')
        self.termguide['text'] = '0   |5   |10  |15  |20  |25  |30  |35  |40  |45'
        self.termtext = Text((self.termframe), state='normal', width=60, height=4, wrap='none', font='Terminal 17', fg='#121f38')
        self.termtext.grid(column=0, row=0, sticky='SW', padx=5, pady=25)

        # Speed Entry Zone for 731
        self.terminal2 = ttk.Labelframe(self, text='Terminal de saisie rapide (731)')
        self.terminal2.grid_columnconfigure(0, weight=1)
        self.terminal2.grid_rowconfigure(0, weight=1)
        self.speed731 = Frame(self.terminal2)
        self.speed731.grid(column=0, row=0, sticky='EW')
        self.speed731.grid_columnconfigure(0, weight=1)
        self.speed731.grid_columnconfigure(1, weight=1)
        self.speed731.grid_columnconfigure(2, weight=1)
        self.speed731.grid_columnconfigure(3, weight=1)
        self.speed731.grid_columnconfigure(4, weight=1)
        self.speed731.grid_columnconfigure(5, weight=1)
        self.speed731.grid_columnconfigure(6, weight=1)
        self.speed731.grid_columnconfigure(7, weight=1)
        self.speed731.grid_columnconfigure(8, weight=1)
        self.speed731.grid_columnconfigure(9, weight=1)
        self.speed731.grid_rowconfigure(0, weight=1)
        self.speed731text = Entry(self.speed731, font='Terminal 14')
        self.speed731text.grid(column=0, row=0, sticky='NEW', padx=5, pady=5)
        self.speedResult = Text((self.speed731), state='disabled', width=1, height=1, wrap='none', font='Terminal 14')
        self.speedResult.grid(column=2, row=0, sticky='NEW', padx=5, pady=5)

        # The monitor that indicates some useful infos
        self.monitor = ttk.Labelframe(self, text='Moniteur')
        self.monlog = Text((self.monitor), state='disabled', width=60, height=10, wrap='word')
        self.monlog.grid(column=0, row=0, sticky='EWNS', padx=5, pady=5)
        self.scrollb = ttk.Scrollbar((self.monitor), command=(self.monlog.yview))
        self.scrollb.grid(column=1, row=0, sticky='EWNS', padx=5, pady=5)
        self.monlog['yscrollcommand'] = self.scrollb.set
        self.monitor.grid_columnconfigure(0, weight=1)
        self.monitor.grid_rowconfigure(0, weight=1)

        # All the items griding
        self.lecteur_ci.grid(column=2, row=0, sticky='EWNS', columnspan=1, padx=5, pady=5)
        self.imageViewer.grid(column=0, row=0, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.terminal.grid(column=0, row=2, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.terminal2.grid(column=0, row=1, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.monitor.grid(column=2, row=1, sticky='EWNS', columnspan=1, rowspan=2, padx=5, pady=5)

        # What is a window without a menu bar ?
        menubar = Menu(self)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label='Nouveau', command=(self.newEntry))
        menu1.add_command(label='Ouvrir scan...', command=(self.openingScan))
        menu1.add_separator()
        menu1.add_command(label='Quitter', command=(self.destroy))
        menubar.add_cascade(label='Fichier', menu=menu1)
        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label='Commandes au clavier', command=(self.helpbox))
        menu3.add_command(label='Signaler un problème', command=(self.openIssuePage))
        menu3.add_separator()
        menu3.add_command(label='A propos de CNIRevelator', command=(self.infobox))
        menubar.add_cascade(label='Aide', menu=menu3)
        self.config(menu=menubar)

        # The title
        self.wm_title(globs.CNIRName)

        # The icon
        if getattr(sys, 'frozen', False):
            self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')

        # Make this window resizable and set her size
        self.resizable(width=True, height=True)
        self.update()
        w = int(self.winfo_reqwidth())
        h = int(self.winfo_reqheight())
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws - w)/2
        y = (hs - h)/2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.update()
        self.deiconify()
        self.minsize(self.winfo_width(), self.winfo_height())
        
        # Set image
        self.imageViewer.image = None
        self.imageViewer.imagePath = None
        self.imageViewer.imgZoom = 1
        self.imageViewer.rotateCount = 0
        self.imageViewer.blackhat = False
        self.imageViewer.pagenumber = 0

        # Some bindings
        self.termtext.bind('<Key>', self.entryValidation)
        self.termtext.bind('<<Paste>>', self.pasteValidation)
        self.speed731text.bind('<Control_R>', self.speedValidation)
        self.imageViewer.ZONE.bind("<Button-1>", self.rectangleSelectScan)

        logfile.printdbg('Initialization successful')

    def statusUpdate(self, image=None, setplace=False):
        if image:
            self.imageViewer.image = image
            self.imageViewer.ZONE.itemconfigure(self.STATUSimg, image=(self.imageViewer.image))
            self.imageViewer.ZONE.configure(scrollregion=self.imageViewer.ZONE.bbox("all"))
        
    def rectangleSelectScan(self, event):
        if self.imageViewer.image:
            canvas = event.widget
            print("Get coordinates : [{}, {}], for [{}, {}]".format(canvas.canvasx(event.x), canvas.canvasy(event.y), event.x, event.y))
            
            self.corners.append([canvas.canvasx(event.x), canvas.canvasy(event.y)])
            if len(self.corners) == 2:
                self.select = self.imageViewer.ZONE.create_rectangle(self.corners[0][0], self.corners[0][1], self.corners[1][0], self.corners[1][1], outline ='cyan', width = 2)
                print("Get rectangle : [{}, {}], for [{}, {}]".format(self.corners[0][0], self.corners[0][1], self.corners[1][0], self.corners[1][1]))
            if len(self.corners) > 2:
                self.corners = []
                self.imageViewer.ZONE.delete(self.select)

    def goOCRDetection(self):
        if self.imageViewer.image:
            cv_img = cv2.imreadmulti(self.imageViewer.imagePath)[1][self.imageViewer.pagenumber]
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            if self.imageViewer.blackhat:
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                cv_img = cv2.GaussianBlur(cv_img, (3, 3), 0)
                cv_img = cv2.bitwise_not(cv_img)
            try:
                # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                height, width, channels_no = cv_img.shape
                # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                height, width, channels_no = cv_img.shape
            except ValueError:
                # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                height, width  = cv_img.shape
                # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                height, width  = cv_img.shape
            # Rotate
            rotationMatrix=cv2.getRotationMatrix2D((width/2, height/2),int(self.imageViewer.rotateCount*90),1)
            cv_img=cv2.warpAffine(cv_img,rotationMatrix,(width,height))
            # Resize
            dim = (int(width * (self.imageViewer.imgZoom + 100) / 100), int(height * (self.imageViewer.imgZoom + 100) / 100))
            cv_img = cv2.resize(cv_img, dim, interpolation = cv2.INTER_AREA)
    
            x0 = int(self.corners[0][0])
            y0 = int(self.corners[0][1])
            x1 = int(self.corners[1][0])
            y1 = int(self.corners[1][1])
            
            crop_img = cv_img[y0:y1, x0:x1]
    
            # Get the text by OCR
            try:
                os.environ['PATH'] = globs.CNIRTesser
                os.environ['TESSDATA_PREFIX'] =  globs.CNIRTesser + '\\tessdata'
                
                text = pytesseract.image_to_string(crop_img, lang='ocrb', boxes=False, config='--psm 6 --oem 0 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890<')
                
                # manual validation
                # the regex
                regex = re.compile("[^A-Z0-9<\n]")
                text = re.sub(regex, '', text)
                self.validatedtext = ''
                invite = ihm.OpenScanDialog(self, text)
                invite.transient(self)
                invite.grab_set()
                invite.focus_force()
                self.wait_window(invite)
                
                print("text : {}".format(self.validatedtext))
                
                self.mrzChar = ""
                
                # Get that
                for char in self.validatedtext:
                    self.termtext.delete("1.0","end")
                    self.termtext.insert("1.0", self.mrzChar)
                    self.mrzChar = self.mrzChar + char
                
                self.stringValidation("")
                print(self.mrzChar)
            
            # Reinstall tesseract 
            except pytesseract.TesseractNotFoundError as e:
                try:
                    shutil.rmtree(globs.CNIRTesser)
                except Exception:
                    pass
                showerror('Erreur de module OCR', ('Le module OCR localisé en ' + str(os.environ['PATH']) + 'est introuvable ou corrompu. Il sera réinstallé à la prochaine exécution'), parent=self)
                logfile.printerr("Tesseract error : {}. Will be reinstallated".format(e))
                
            # Tesseract error
            except pytesseract.TesseractError as e:
                logfile.printerr("Tesseract error : {}".format(e))
                showerror('Erreur de module OCR', ("Le module Tesseract a rencontré un problème : {}".format(e)), parent=self)


    def stringValidation(self, keysym):
        # analysis
        # If we must decide the type of the document
        if not self.mrzDecided:
            # Get the candidates
            candidates = mrz.allDocMatch(self.mrzChar.split("\n"))

            if len(candidates) == 2 and len(self.mrzChar) >= 8:
                # Parameters for the choice invite
                invite = ihm.DocumentAsk(self, [candidates[0][2], candidates[1][2]])
                invite.transient(self)
                invite.grab_set()
                invite.focus_force()

                self.wait_window(invite)

                self.logOnTerm("Document detecté : {}\n".format(candidates[invite.choice][2]))
                self.mrzDecided = candidates[invite.choice]

            elif len(candidates) == 1:
                self.logOnTerm("Document detecté : {}\n".format(candidates[0][2]))
                self.mrzDecided = candidates[0]
        else:
            # corrects some problems
            if keysym in ["BackSpace", "Delete"]:
                return
            # get the cursor position
            curPos = self.termtext.index(INSERT)
            # break the line
            if (len(self.mrzChar) - 2 >= len(self.mrzDecided[0][0])) and ("\n" not in self.mrzChar[:-1]):
                # In case of there is no second line
                if len(self.mrzDecided[0][1]) == 0:
                    self.mrzChar = self.termtext.get("1.0", "end")[:-1]
                    self.termtext.delete("1.0","end")
                    self.termtext.insert("1.0", self.mrzChar[:-1])
                    self.termtext.mark_set(INSERT, curPos)
                else:
                    # In case of there is a second line
                    self.mrzChar = self.termtext.get("1.0", "end")[:-1] + '\n'
                    self.termtext.delete("1.0","end")
                    self.termtext.insert("1.0", self.mrzChar)
            # stop when limit reached
            elif (len(self.mrzChar) - 3 >= 2 * len(self.mrzDecided[0][0])):
                self.mrzChar = self.termtext.get("1.0", "end")[:-1]
                self.termtext.delete("1.0","end")
                self.termtext.insert("1.0", self.mrzChar[:-1])
                self.termtext.mark_set(INSERT, curPos)
            # compute the control sum if needed
            self.computeSigma()

    def entryValidation(self, event):
        """
        On the fly validation with regex
        """
        controlled = False

        # get the cursor
        if self.mrzDecided:
            curPosition = self.termtext.index(INSERT)
            position = curPosition.split(".")
            pos = (int(position[0]) - 1) * len(self.mrzDecided[0][0]) + (int(position[1]) - 1)
        else:
            curPosition = self.termtext.index(INSERT)
            position = curPosition.split(".")
            pos = (int(position[1]) - 1)

        # verifying that there is no Ctrl-C/Ctrl-V and others
        if event.state & 0x0004 and (   event.keysym == "c" or
                                        event.keysym == "v" or
                                        event.keysym == "a" or
                                        event.keysym == "z" or
                                        event.keysym == "y"  ):
            controlled = True

        if event.keysym == "Tab":
            if self.mrzDecided:
                controlled = True
                self.mrzChar = self.termtext.get("1.0", "end")[:-1]
                # the regex
                regex = re.compile("[^A-Z0-9<]")
                code = re.sub(regex, '', self.mrzChar)

                number = mrz.completeDocField(self.mrzDecided, code, pos) - 1

                if number == 0:
                    return "break"

                mrzChar = self.termtext.get(curPosition, "end")[:-1]
                self.termtext.delete(curPosition,"end")
                self.termtext.insert(curPosition, "<"*number + mrzChar)
                self.termtext.mark_set("insert", "%d.%d" % (int(position[0]), int(position[1]) + number))
            return "break"

        if event.keysym == "Escape":
            if self.mrzDecided:
                # Get the candidates
                candidates = mrz.allDocMatch(self.mrzChar.split("\n"))

                if len(candidates) == 2 and len(self.mrzChar) >= 8:
                    # Parameters for the choice invite
                    invite = ihm.DocumentAsk(self, [candidates[0][2], candidates[1][2]])
                    invite.transient(self)
                    invite.grab_set()
                    invite.focus_force()

                    self.wait_window(invite)

                    self.logOnTerm("Document re-detecté : {}\n".format(candidates[invite.choice][2]))
                    self.mrzDecided = candidates[invite.choice]

                elif len(candidates) == 1:
                    self.logOnTerm("Document re-detecté : {}\n".format(candidates[0][2]))
                    self.mrzDecided = candidates[0]
            return "break"

        # If not a control char
        if not controlled and not event.keysym in ihm.controlKeys:
            # the regex
            regex = re.compile("[A-Z]|<|[0-9]")
            # match !
            if not regex.fullmatch(event.char):
                self.logOnTerm("Caractère non accepté !\n")
                return "break"
        # Adds the entry
        tempChar = self.termtext.get("1.0", "end")[:-1]
        self.mrzChar =  tempChar[:pos+1] + event.char + tempChar[pos+1:] + '\n'

        # validation of the mrz string
        self.stringValidation(event.keysym)

    def pasteValidation(self, event):
        """
        On the fly validation of pasted text
        """
        # cleanup
        self.termtext.delete("1.0","end")

        # get the clipboard content
        lines = self.clipboard_get()
        self.mrzChar = ""

        # the regex
        regex = re.compile("[^A-Z0-9<]")

        lines = re.sub(regex, '', lines)

        # Get that
        for char in lines:
            self.termtext.delete("1.0","end")
            self.termtext.insert("1.0", self.mrzChar)
            self.mrzChar = self.mrzChar + char
            self.stringValidation("")
        self.termtext.insert("1.0", self.mrzChar)

        return "break"

    def speedValidation(self, event):
        """
        Computation of the speed entry
        """
        char = self.speed731text.get()
        self.speedResultPrint(str(mrz.computeControlSum(char)))
        return "break"

    def logOnTerm(self, text):
        self.monlog['state'] = 'normal'
        self.monlog.insert('end', text)
        self.monlog['state'] = 'disabled'
        self.monlog.yview(END)

    def clearTerm(self):
        self.monlog['state'] = 'normal'
        self.monlog.delete('1.0', 'end')
        self.monlog['state'] = 'disabled'
        self.monlog.yview(END)

    def speedResultPrint(self, text):
        self.speedResult['state'] = 'normal'
        self.speedResult.delete("1.0", 'end')
        self.speedResult.insert('end', text)
        self.speedResult['state'] = 'disabled'

    def goPageChoice(self, event):
        self.imageViewer.pagenumber = int(self.toolbar.pageChooser.get()) - 1
        self.resizeScan()
        
    def openingScan(self):
        path = ''
        path = filedialog.askopenfilename(parent=self, title='Ouvrir un scan de CNI...', filetypes=(('TIF files', '*.tif'),
                                                                                                    ('TIF files', '*.tiff'),
                                                                                                    ('JPEG files', '*.jpg'),
                                                                                                    ('JPEG files', '*.jpeg')))
        # Load an image using OpenCV
        self.imageViewer.imagePath = path
        self.imageViewer.imgZoom = 1
        self.imageViewer.blackhat = False
        self.imageViewer.rotateCount = 0
        self.imageViewer.pagenumber = 0
        
        # Determine how many pages
        self.toolbar.pageChooser['values'] = ('1')
        total = len(cv2.imreadmulti(self.imageViewer.imagePath)[1])
        
        for i in range(2, total + 1):
             self.toolbar.pageChooser['values'] += tuple(str(i))
        
        # Open the first page
        cv_img = cv2.imreadmulti(self.imageViewer.imagePath)[1][self.imageViewer.pagenumber]
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        
        try:
            # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
            height, width, channels_no = cv_img.shape
            # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
            height, width, channels_no = cv_img.shape
        except ValueError:
            # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
            height, width  = cv_img.shape
            # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
            height, width  = cv_img.shape
            
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
        self.statusUpdate(photo)

    def zoomInScan50(self, quantity = 50):
        if self.imageViewer.image:
            self.imageViewer.imgZoom += quantity
            self.resizeScan()

    def zoomOutScan50(self, quantity = 50):
        if self.imageViewer.image:
            self.imageViewer.imgZoom -= quantity
            self.resizeScan()

    def zoomInScan20(self, quantity = 20):
        if self.imageViewer.image:
            self.imageViewer.imgZoom += quantity
            self.resizeScan()

    def zoomOutScan20(self, quantity = 20):
        if self.imageViewer.image:
            self.imageViewer.imgZoom -= quantity
            self.resizeScan()

    def zoomInScan(self, quantity = 1):
        if self.imageViewer.image:
            self.imageViewer.imgZoom += quantity
            self.resizeScan()

    def zoomOutScan(self, quantity = 1):
        if self.imageViewer.image:
            self.imageViewer.imgZoom -= quantity
            self.resizeScan()

    def rotateRight(self):
        if self.imageViewer.image:
            self.imageViewer.rotateCount -= 1
            if self.imageViewer.rotateCount < 0:
                self.imageViewer.rotateCount = 4
            self.resizeScan()

    def rotateLeft(self):
        if self.imageViewer.image:
            self.imageViewer.rotateCount += 1
            if self.imageViewer.rotateCount > 4:
                self.imageViewer.rotateCount = 0
            self.resizeScan()

    def rotateLeft1(self):
        if self.imageViewer.image:
            self.imageViewer.rotateCount += 0.01
            if self.imageViewer.rotateCount > 4:
                self.imageViewer.rotateCount = 0
            self.resizeScan()

    def rotateRight1(self):
        if self.imageViewer.image:
            self.imageViewer.rotateCount -= 0.01
            if self.imageViewer.rotateCount < 0:
                self.imageViewer.rotateCount = 4
            self.resizeScan()

    def negativeScan(self):
        if self.imageViewer.image:
            # Load an image using OpenCV
            cv_img = cv2.imreadmulti(self.imageViewer.imagePath)[1][self.imageViewer.pagenumber]
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            if not self.imageViewer.blackhat:
                self.imageViewer.blackhat = True
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                cv_img = cv2.GaussianBlur(cv_img, (3, 3), 0)
                cv_img = cv2.bitwise_not(cv_img)
            else:
                self.imageViewer.blackhat = False
            self.resizeScan(cv_img)

    def resizeScan(self, cv_img = None):
        if self.imageViewer.image:
            try:
                if not hasattr(cv_img, 'shape'):
                    # Load an image using OpenCV
                    cv_img = cv2.imreadmulti(self.imageViewer.imagePath)[1][self.imageViewer.pagenumber]
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                    if self.imageViewer.blackhat:
                        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                        cv_img = cv2.GaussianBlur(cv_img, (3, 3), 0)
                        cv_img = cv2.bitwise_not(cv_img)
    
                try:
                    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                    height, width, channels_no = cv_img.shape
                    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                    height, width, channels_no = cv_img.shape
                except ValueError:
                    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                    height, width  = cv_img.shape
                    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                    height, width  = cv_img.shape
                # Rotate
                rotationMatrix=cv2.getRotationMatrix2D((width/2, height/2),int(self.imageViewer.rotateCount*90),1)
                cv_img=cv2.warpAffine(cv_img,rotationMatrix,(width,height))
                # Resize
                dim = (int(width * (self.imageViewer.imgZoom + 100) / 100), int(height * (self.imageViewer.imgZoom + 100) / 100))
                cv_img = cv2.resize(cv_img, dim, interpolation = cv2.INTER_AREA)
                # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
                photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
                self.statusUpdate( photo)
            except Exception as e:
                logfile.printerr("Error with opencv : {}".format(e))
                traceback.print_exc(file=sys.stdout)
                try:
                    # Reload an image using OpenCV
                    path = self.imageViewer.imagePath
                    self.imageViewer.imgZoom = 1
                    self.imageViewer.blackhat = False
                    self.imageViewer.rotateCount = 0
                    cv_img = cv2.imreadmulti(path)
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                    height, width, channels_no = cv_img.shape
                    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
                    height, width, channels_no = cv_img.shape
                    # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
                    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
                    self.statusUpdate(photo)
                except Exception as e:
                    logfile.printerr("Critical error with opencv : ".format(e))
                    traceback.print_exc(file=sys.stdout)
                    showerror("Erreur OpenCV (traitement d'images)", "Une erreur critique s'est produite dans le gestionnaire de traitement d'images OpenCV utilisé par CNIRevelator. L'application va se réinitialiser")
                    self.initialize()

    def newEntry(self):
        self.initialize()
        self.logOnTerm('\n\nEntrez la première ligne de MRZ svp \n')

    def infobox(self):
        Tk().withdraw()

        showinfo('A propos de CNIRevelator',
        (   'Version du logiciel : CNIRevelator ' + globs.verstring_full + '\n\n'
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
            " En cas de problèmes ou demande particulière, ouvrez-y une issue ou bien envoyez un mail à neox@os-k.eu !\n\n"
        ),

        parent=self)

    def helpbox(self):
        Tk().withdraw()

        showinfo('Aide sur les contrôles au clavier',
        (   "Terminal de saisie rapide (731) : \n\n"
            "       Caractères autorisés : Alphanumériques en majuscule et le caractère '<'. Pas de minuscules ni caractères spéciaux, autrement la somme est mise à zéro \n\n"
            "       Calculer résultat :\t\t\tTouche Ctrl droite \n"
            "       Copier :\t\t\t\tCtrl-C \n"
            "       Coller :\t\t\t\tCtrl-V \n"
            "\n\n"
            "Terminal de saisie MRZ complète : \n\n"
            "       Caractères autorisés : Alphanumériques en majuscule et le caractère '<'. Pas de minuscules ni caractères spéciaux, autrement la somme est mise à zéro \n\n"
            "       Calculer résultat :\t\t\tTouche Ctrl droite \n"
            "       Compléter champ :\t\t\tTouche Tab \n"
            "       Copier :\t\t\t\tCtrl-C \n"
            "       Coller :\t\t\t\tCtrl-V \n"
            "       Forcer une nouvelle détection du document :\tEchap\n"
        ),

        parent=self)
        
    def openIssuePage(self):
        self.openBrowser("https://github.com/neox95/CNIRevelator/issues")
        
    def openBrowser(self, url):
        webbrowser.open_new(url)

    def computeSigma(self):
        """
        Launch the checksum computation, infos validation and display the results
        """
        # the regex
        regex = re.compile("[^A-Z0-9<]")
        code = re.sub(regex, '', self.mrzChar)
        self.compliance = True

        allSums = mrz.computeAllControlSum(self.mrzDecided, code)["ctrlSumList"]
        #print("Code : _{}_ | Sums : {}".format(code, allSums))

        self.termtext.tag_remove("conforme",  "1.0", "end")
        self.termtext.tag_remove("nonconforme",  "1.0", "end")

        self.clearTerm()
        self.logOnTerm("Examen du document : {}\n\n".format(self.mrzDecided[2]))

        for sum in allSums:
            x = sum[1] // len(self.mrzDecided[0][0]) +1
            y = sum[1] %  len(self.mrzDecided[0][0])
            #print("index : {}.{}".format(x,y))
            #print("{} == {}".format(code[sum[1]], sum[2]))

            self.logOnTerm("Somme de contrôle position {} : Lu {} VS Calculé {}\n".format(sum[1], code[sum[1]], sum[2]))

            # if sum is facultative or if sum is ok
            try:
                if sum[3] or int(code[sum[1]]) == int(sum[2]):
                    self.termtext.tag_add("conforme", "{}.{}".format(x,y), "{}.{}".format(x,y+1))
                    self.termtext.tag_configure("conforme", background="green", foreground="white")
                else:
                    self.termtext.tag_add("nonconforme", "{}.{}".format(x,y), "{}.{}".format(x,y+1))
                    self.termtext.tag_configure("nonconforme", background="red", relief='raised', foreground="white")
                    self.compliance = False
            except ValueError:
                self.termtext.tag_add("nonconforme", "{}.{}".format(x,y), "{}.{}".format(x,y+1))
                self.termtext.tag_configure("nonconforme", background="red", relief='raised', foreground="white")
                self.compliance = False

        # get the infos
        docInfos = mrz.getDocInfos(self.mrzDecided, code)
        #print(docInfos)
        # display the infos
        for key in [ e for e in docInfos ]:
            #print(docInfos[key])
            if key in ["CODE", "CTRL"]:
                continue
            if not docInfos[key] == False:
                self.infoList[key]['text'] = docInfos[key]
                self.infoList[key]['background'] = self['background']
                self.infoList[key]['foreground'] = "black"
            else:
                self.infoList[key]['background'] = "red"
                self.infoList[key]['foreground'] = "white"
                self.infoList[key]['text'] = "NC"
                self.compliance = False

        if self.compliance == True:
            self.STATUStxt["text"] = "CONFORME"
            self.STATUStxt["foreground"] = "green"
        else:
            self.STATUStxt["text"] = "NON CONFORME"
            self.STATUStxt["foreground"] = "red"

        return

























