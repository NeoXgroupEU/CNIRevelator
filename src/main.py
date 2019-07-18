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

        # Get the screen size
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        logfile.printdbg('mainWindow() : Launching main window with resolution' + str(ws) + 'x' + str(hs))
        self.grid()

        # Configuring the size of each part of the window
        self.grid_columnconfigure(0, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_columnconfigure(1, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_columnconfigure(2, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_rowconfigure(0, weight=1, minsize=(hs / 2 * 0.5))
        self.grid_rowconfigure(1, weight=1, minsize=(hs / 2 * 0.5))

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
        self.terminal = ttk.Labelframe(self, text='Terminal de saisie')
        self.terminal.grid_columnconfigure(0, weight=1)
        self.terminal.grid_rowconfigure(0, weight=1)
        self.termframe = Frame(self.terminal)
        self.termframe.grid(column=0, row=0, sticky='EW')
        self.termframe.grid_columnconfigure(0, weight=1)
        self.termframe.grid_rowconfigure(0, weight=1)
        self.termtext = Text((self.termframe), state='normal', width=60, height=4, wrap='none', font='Terminal 17', fg='#121f38')
        self.termtext.grid(column=0, row=0, sticky='NEW', padx=5)

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
        self.terminal.grid(column=0, row=1, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.monitor.grid(column=2, row=1, sticky='EWNS', columnspan=1, padx=5, pady=5)
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
        menu3.add_command(label='A propos', command=(self.infobox))
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
        self.update()
        logfile.printdbg('Initialization successful')

    def onTabPressed(self, event):

        return 'break'

    def entryValidation(self, event):
        """
        On the fly validation with regex
        """
        controlled = False

        # verifying that there is no Ctrl-C/Ctrl-V and others
        if event.state & 0x0004 and (   event.keysym == "c" or
                                        event.keysym == "v" or
                                        event.keysym == "a" or
                                        event.keysym == "z" or
                                        event.keysym == "y"  ):
            controlled = True

        # If not a control char
        if not controlled and not event.keysym in ["Return", "Right", "Left", "Home", "End", "Delete", "BackSpace", "Inser", "Shift", "Control"]:
            # the regex
            regex = re.compile("[A-Z]|<|[0-9]")
            # match !
            if not regex.fullmatch(event.char):
                self.logOnTerm("Caractère non accepté !\n")
                return "break"

            # analysis
            self.mrzChar = self.termtext.get("1.0", "end")[:-1] + event.char + '\n'

            # If we must decide the type of the document
            if not self.mrzDecided:
                # Get the candidates
                candidates = mrz.allDocMatch(self.mrzChar.split("\n"))

                if len(candidates) == 2:
                    # XXX demander !
                elif len(candidates) == 1:
                    self.logOnTerm("Document detecté : {}".format(candidates[0]))
                    self.mrzDecided = candidates[0]
            else:
                # Work with the document decided


    def pasteValidation(self, event):
        """
        On the fly validation of pasted text
        """
        # cleanup
        self.termtext.delete("1.0","end")

        # get the clipboard content
        lines = self.clipboard_get()

        # the regex
        regex = re.compile("[^A-Z0-9<]")

        lines = re.sub(regex, '', lines)

        # breaking the lines
        self.termtext.insert("1.0", lines[:mrz.longest] + '\n' + lines[mrz.longest:mrz.longest*2] )
        return "break"


    def logOnTerm(self, text):
        self.monlog['state'] = 'normal'
        self.monlog.insert('end', text)
        self.monlog['state'] = 'disabled'
        self.monlog.yview(END)

    def openingScan(self):
        pass
        # OPEN A SCAN

    def newEntry(self):
        self.initialize()
        self.logOnTerm('\n\nEntrez la première ligne de MRZ svp \n')

    def infobox(self):
        Tk().withdraw()

        showinfo('A propos du logiciel',
        (   'Version du logiciel : CNIRevelator ' + globs.verstring_full + '\n\n' +
            "CNIRevelator is free software: you can redistribute it and/or modify " +
            "it under the terms of the GNU General Public License as published by " +
            "the Free Software Foundation, either version 3 of the License, or " +
            "any later version. " + "\n\n" +
            "CNIRevelator is distributed in the hope that it will be useful, " +
            "but without even the implied warranty of " +
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the " +
            "GNU General Public License for more details. " +
            "\n\n" +
            "You should have received a copy of the GNU General Public License " +
            "along with CNIRevelator. If not, see <https://www.gnu.org/licenses/>. " +
            "\n\n" +
            "Tesseract 4.0 est soumis à l'Apache License 2004" +
            "\n\n" +
            "Anaconda 3 est soumis à la licence BSD 2018-2019" +
            "\n\n" +
            "En cas de problèmes, ouvrez une issue sur le github de CNIRevelator " +
            "<https://github.com/neox95/CNIRevelator>, ou bien envoyez un mail à neox@os-k.eu!"
        ),

        parent=self)

    def calculSigma(self, MRZtxt, numtype):
        pass
        # CALCUL DE TOUTES LES SOMMES DE LA CARTE CONFORMEMENT A SON TYPE


class OpenScan(ttk.Frame):
    def __init__(self, mainframe, fileorig, type, nframe=1, pagenum=0, file=None):
        """ Initialize the main Frame """
        if file == None:
            file = fileorig
        self.file = file
        self.fileorig = fileorig
        self.nframe = nframe
        self.pagenum = pagenum
        self.parent = mainframe.parent
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('Ouvrir un scan... (Utilisez la roulette pour zoomer, clic gauche pour déplacer et clic droit pour sélectionner la MRZ)')
        self.master.resizable(width=False, height=False)
        hs = self.winfo_screenheight()
        w = int(self.winfo_screenheight() / 1.5)
        h = int(self.winfo_screenheight() / 2)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = ws / 2 - w / 2
        y = hs / 2 - h / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        if getattr(sys, 'frozen', False):
            self.master.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.master.iconbitmap('id-card.ico')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.cadre = CanvasImage(self.master, self.file, type)
        self.cadre.grid(row=0, column=0)
        self.master.menubar = Menu(self.master)
        if type == 1:
            self.master.menubar.add_command(label='Page précédente', command=(self.pagep))
        self.master.menubar.add_command(label='Pivoter -90°', command=(self.cadre.rotatemm))
        self.master.menubar.add_command(label='Pivoter -1°', command=(self.cadre.rotatem))
        self.master.menubar.add_command(label='Pivoter +1°', command=(self.cadre.rotatep))
        self.master.menubar.add_command(label='Pivoter +90°', command=(self.cadre.rotatepp))
        if type == 1:
            self.master.menubar.add_command(label='Page suivante', command=(self.pages))
        self.master.config(menu=(self.master.menubar))
        self.cadre.canvas.bind('<ButtonPress-3>', self.motionprep)
        self.cadre.canvas.bind('<B3-Motion>', self.motionize)
        self.cadre.canvas.bind('<ButtonRelease-3>', self.motionend)

    def pages(self):
        if self.pagenum + 1 < self.nframe:
            im = Image.open(self.fileorig)
            im.seek(self.pagenum + 1)
            newpath = globs.CNIREnv + '\\temp' + str(random.randint(11111, 99999)) + '.tif'
            im.save(newpath)
            im.close()
            self.cadre.destroy()
            self.__init__(self.master, self.fileorig, 1, self.nframe, self.pagenum + 1, newpath)

    def pagep(self):
        if self.pagenum - 1 >= 0:
            im = Image.open(self.fileorig)
            im.seek(self.pagenum - 1)
            newpath = globs.CNIREnv + '\\temp' + str(random.randint(11111, 99999)) + '.tif'
            im.save(newpath)
            im.close()
            self.cadre.destroy()
            self.__init__(self.master, self.fileorig, 1, self.nframe, self.pagenum - 1, newpath)

    def motionprep(self, event):
        if hasattr(self, 'rect'):
            self.begx = event.x
            self.begy = event.y
            self.ix = self.cadre.canvas.canvasx(event.x)
            self.iy = self.cadre.canvas.canvasy(event.y)
            self.cadre.canvas.coords(self.rect, self.cadre.canvas.canvasx(event.x), self.cadre.canvas.canvasy(event.y), self.ix, self.iy)
        else:
            self.begx = event.x
            self.begy = event.y
            self.ix = self.cadre.canvas.canvasx(event.x)
            self.iy = self.cadre.canvas.canvasy(event.y)
            self.rect = self.cadre.canvas.create_rectangle((self.cadre.canvas.canvasx(event.x)), (self.cadre.canvas.canvasy(event.y)), (self.ix), (self.iy), outline='red')

    def motionize(self, event):
        event.x
        event.y
        self.cadre.canvas.coords(self.rect, self.ix, self.iy, self.cadre.canvas.canvasx(event.x), self.cadre.canvas.canvasy(event.y))

    def motionend(self, event):
        self.endx = event.x
        self.endy = event.y
        self.imtotreat = self.cadre.resizedim.crop((min(self.begx, self.endx), min(self.begy, self.endy), max(self.endx, self.begx), max(self.endy, self.begy)))
        im = self.imtotreat
        import CNI_pytesseract as pytesseract
        try:
            os.environ['PATH'] = globs.CNIREnv + '\\Tesseract-OCR4\\'
            os.environ['TESSDATA_PREFIX'] = globs.CNIREnv + '\\Tesseract-OCR4\\tessdata'
            self.text = pytesseract.image_to_string(im, lang='ocrb', boxes=False, config='--psm 6 --oem 0 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890<')
        except pytesseract.TesseractNotFoundError as e:
            try:
                os.remove(globs.CNIREnv + '\\Tesseract-OCR4\\*.*')
            except Exception:
                pass

            showerror('Erreur de module OCR', ('Le module OCR localisé en ' + str(os.environ['PATH']) + 'est introuvable. Il sera réinstallé à la prochaine exécution'), parent=self)
        except pytesseract.TesseractError as e:
            pass

        self.master.success = False
        dialogconf = OpenScanDialog(self.master, self.text)
        dialogconf.transient(self)
        dialogconf.grab_set()
        self.wait_window(dialogconf)
        if self.master.success:
            self.master.destroy()

