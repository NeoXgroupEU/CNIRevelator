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

import ihm                      # ihm.py
import logger                   # logger.py
import mrz                      # mrz.py
import globs                    # globs.py
import pytesseract              # pytesseract.py
from image import *             # image.py

# Global handler
logfile = logger.logCur

class mainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.initialize()

    def initialize(self):
        self.mrzChar = ''
        self.mrzDecided = False
        self.Tags = []

        # Get the screen size
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        logfile.printdbg('Launching main window with resolution' + str(ws) + 'x' + str(hs))
        self.grid()

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

        # The STATUS indicator
        self.STATUT = ttk.Labelframe(self, text='Statut')
        self.STATUT.grid_columnconfigure(0, weight=1)
        self.STATUT.grid_rowconfigure(0, weight=1)
        self.STATUStxt = Label((self.STATUT), text='', font='Times 24', fg='#FFBF00')
        self.STATUStxt.grid(column=0, row=0, padx=0, pady=0, sticky='EWNS')
        self.STATUStxt['text'] = 'EN ATTENTE'

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
        self.speed731text.grid(column=0, row=0, sticky='NEW', padx=5)
        self.speedResult = Text((self.speed731), state='disabled', width=1, height=1, wrap='none', font='Terminal 14')
        self.speedResult.grid(column=2, row=0, sticky='NEW')

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
        self.lecteur_ci.grid(column=0, row=0, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.STATUT.grid(column=2, row=0, sticky='EWNS', columnspan=1, padx=5, pady=5)
        self.terminal.grid(column=0, row=2, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.terminal2.grid(column=0, row=1, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.monitor.grid(column=2, row=1, sticky='EWNS', columnspan=1, rowspan=2, padx=5, pady=5)
        self.update()

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
        self.minsize(self.winfo_width(), self.winfo_height())
        w = int(self.winfo_width())
        h = int(self.winfo_height())
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = ws / 2 - w / 2
        y = hs / 2 - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Some bindings
        self.termtext.bind('<Key>', self.entryValidation)
        self.termtext.bind('<<Paste>>', self.pasteValidation)
        self.speed731text.bind('<Return>', self.speedValidation)
        self.update()
        logfile.printdbg('Initialization successful')

    def stringValidation(self):
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

                self.logOnTerm("Document detecté : {}".format(candidates[invite.choice][2]))
                self.mrzDecided = candidates[invite.choice]

            elif len(candidates) == 1:
                self.logOnTerm("Document detecté : {}".format(candidates[0][2]))
                self.mrzDecided = candidates[0]
        else:
            # break the line
            if (len(self.mrzChar) - 2 >= len(self.mrzDecided[0][0])) and ("\n" not in self.mrzChar[:-1]):
                # In case of there is no second line
                if len(self.mrzDecided[0][1]) == 0:
                    self.mrzChar = self.termtext.get("1.0", "end")[:-2]
                    self.termtext.delete("1.0","end")
                    self.termtext.insert("1.0", self.mrzChar)
                    self.nope = True
                else:
                    # In case of there is a second line
                    self.mrzChar = self.termtext.get("1.0", "end")[:-1] + '\n'
                    self.termtext.delete("1.0","end")
                    self.termtext.insert("1.0", self.mrzChar)
                    self.nope = True
            # stop when limit reached
            elif (len(self.mrzChar) - 3 >= 2 * len(self.mrzDecided[0][0])):
                self.mrzChar = self.termtext.get("1.0", "end")[:-2]
                self.termtext.delete("1.0","end")
                self.termtext.insert("1.0", self.mrzChar)

            # compute the control sum if needed
            self.computeSigma()

    def entryValidation(self, event):
        """
        On the fly validation with regex
        """
        print("go")

        controlled = False

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

                position = self.termtext.index(INSERT).split(".")
                pos = (int(position[0]) - 1) * len(self.mrzDecided[0][0]) + (int(position[1]) - 1)

                number = mrz.completeDocField(self.mrzDecided, code, pos) - 1

                if number == 0:
                    return "break"

                self.mrzChar = self.termtext.get("1.0", "end")[:-1] + "<"*number
                self.termtext.delete("1.0","end")
                self.termtext.insert("1.0", self.mrzChar)
                self.termtext.mark_set("insert", "%d.%d" % (int(position[0]), int(position[1]) + number))
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
            self.mrzChar = self.termtext.get("1.0", "end")[:-1] + event.char + '\n'

        # validation of the mrz string
        self.stringValidation()

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
            self.termtext.insert("1.0", self.mrzChar)
            self.mrzChar = self.mrzChar + char
            self.stringValidation()

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

    def speedResultPrint(self, text):
        self.speedResult['state'] = 'normal'
        self.speedResult.delete("1.0", 'end')
        self.speedResult.insert('end', text)
        self.speedResult['state'] = 'disabled'


    def openingScan(self):
        pass
        # OPEN A SCAN

    def newEntry(self):
        self.initialize()
        self.logOnTerm('\n\nEntrez la première ligne de MRZ svp \n')

    def infobox(self):
        Tk().withdraw()

        showinfo('A propos de CNIRevelator',
        (   'Version du logiciel : CNIRevelator ' + globs.verstring_full + '\n\n' +
            "CNIRevelator est un logiciel libre : vous avez le droit de le modifier et/ou le distribuer " +
            "dans les termes de la GNU General Public License telle que publiée par " +
            "la Free Software Foundation, dans sa version 3 ou " +
            "ultérieure. " + "\n\n" +
            "CNIRevelator est distribué dans l'espoir d'être utile, sans toutefois " +
            "impliquer une quelconque garantie de " +
            "QUALITÉ MARCHANDE ou APTITUDE À UN USAGE PARTICULIER. Référez vous à la " +
            "GNU General Public License pour plus de détails à ce sujet. " +
            "\n\n" +
            "Vous devriez avoir reçu une copie de la GNU General Public License " +
            "avec CNIRevelator. Si cela n'est pas le cas, jetez un oeil à '<https://www.gnu.org/licenses/>. " +
            "\n\n" +
            "Le module d'OCR Tesseract 4.0 est soumis à l'Apache License 2004" +
            "\n\n" +
            "Les bibliothèques python et l'environnement Anaconda 3 sont soumis à la licence BSD 2018-2019" +
            "\n\n" +
            "Le code source de ce programme est disponible sur Github à l'adresse <https://github.com/neox95/CNIRevelator>.\n" +
            " En cas de problèmes ou demande particulière, ouvrez-y une issue ou bien envoyez un mail à neox@os-k.eu !"
        ),

        parent=self)

    def helpbox(self):
        Tk().withdraw()

        showinfo('Aide sur les contrôles au clavier',
        (   '' + '\n\n' +
            "In construction"
        ),

        parent=self)

    # XXX
    def computeSigma(self):
        # the regex
        regex = re.compile("[^A-Z0-9<]")
        code = re.sub(regex, '', self.mrzChar)

        allSums = mrz.computeAllControlSum(self.mrzDecided, code)
        print("Code : {} | Sums : {}".format(code, allSums))



































