"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher graphical interface                        *
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

from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter import ttk

import logger               # logger.py
import globs                # globs.py


controlKeys = ["Escape", "Right", "Left", "Up", "Down", "Home", "End", "BackSpace", "Delete", "Inser", "Shift_L", "Shift_R", "Control_R", "Control_L"]

class DocumentAsk(Toplevel):

    def __init__(self, parent, choices):
        self.choice = 0
        vals = [0, 1]
        super().__init__(parent)
        self.title("Choisir le document d'identité :")

        ttk.Radiobutton(self, text=choices[0], command=self.register0, value=vals[0]).pack()
        ttk.Radiobutton(self, text=choices[1], command=self.register1, value=vals[1]).pack()

        self.button = Button(self, text='OK', command=(self.ok)).pack()
        self.resizable(width=False, height=False)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        w = hs / 3
        h = ws / 20
        self.update()
        if getattr(sys, 'frozen', False):
            self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')
        x = ws / 2 - w / 2
        y = hs / 2 - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def register0(self):
        self.choice = 0
    def register1(self):
        self.choice = 1
    def ok(self):
        self.destroy()

class LoginDialog(Toplevel):

    def __init__(self, parent):
        self.key = ''
        self.login = ''
        super().__init__(parent)
        self.title('Connexion')
        Label(self, text='IPN : ').pack()
        self.entry_login = Entry(self)
        self.entry_login.insert(0, '')
        self.entry_login.pack()
        Label(self, text='Mot de passe : ').pack()
        self.entry_pass = Entry(self, show='*')
        self.entry_pass.insert(0, '')
        self.entry_pass.pack()
        Button(self, text='Connexion', command=(self.connecti)).pack()
        self.resizable(width=False, height=False)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        w = hs / 10
        h = ws / 18
        self.update()
        if getattr(sys, 'frozen', False):
            self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')
        x = ws / 2 - w / 2
        y = hs / 2 - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.bind("<Return>", self.connecti)

    def connecti(self, event=None):
        self.login = self.entry_login.get().strip()
        self.key = self.entry_pass.get().strip()
        self.destroy()

class LauncherWindow(Tk):

    def __init__(self):
        # Initialize the tkinter main class
        Tk.__init__(self)
        self.configure(bg=globs.CNIRLColor)
        self.resizable(width=False, height=False)
        self.queue = []

        # Setting up the geometry
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        wheight = hs /4
        wwidth  = ws /4

        # Creating objects
        self.mainCanvas = Canvas(self, width=wwidth, height=wheight*9/10, bg=globs.CNIRLColor, highlightthickness=0)
        self.pBarZone = Canvas(self, width=wwidth, height=wheight/10, bg=globs.CNIRLColor)

        self.progressBar = ttk.Progressbar(self.pBarZone, orient=HORIZONTAL, length=wwidth-10, mode='determinate')

        self.mainCanvas.create_text((wwidth / 2), (wheight / 3), text=(globs.CNIRName), font='Helvetica 30', fill='white')
        self.msg = self.mainCanvas.create_text((wwidth / 2.05), (wheight / 1.20), text='Booting up...', font='Helvetica 9', fill='white')

        self.wm_title(globs.CNIRName)

        # Centering
        x = ws / 2 - wwidth  / 2
        y = hs / 2 - wheight / 2
        self.geometry('%dx%d+%d+%d' % (wwidth, wheight, x, y))
        self.mainCanvas.grid()
        self.pBarZone.grid()
        self.progressBar.grid()


        if getattr(sys, 'frozen', False):
           self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')
        logfile = logger.logCur
        logfile.printdbg('Launcher IHM successful')
        self.protocol('WM_DELETE_WINDOW', lambda : self.destroy())

        self.update()

    def printmsg(self, msg):
        self.mainCanvas.itemconfigure(self.msg, text=(msg))

class AutoScrollbar(ttk.Scrollbar):

    def set(self, lo, hi):
        if float(lo) <= 0.0:
            if float(hi) >= 1.0:
                self.grid_remove()
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        raise TclError('Cannot use place with the widget ' + self.__class__.__name__)

class OpenPageDialog(Toplevel):

    def __init__(self, parent, number):
        super().__init__(parent)
        self.parent = parent
        self.title("Choisir la page à afficher de l'image selectionnée")
        self.resizable(width=False, height=False)
        self.termtext = Label(self, text='Merci de selectionner un numéro de page dans la liste ci-dessous.')
        self.termtext.grid(column=0, row=0, sticky='N', padx=5, pady=5)
        self.combotry = ttk.Combobox(self)
        self.combotry['values'] = tuple(str(x) for x in range(1, number + 1))
        self.combotry.grid(column=0, row=1, sticky='N', padx=5, pady=5)
        self.button = Button(self, text='Valider', command=(self.valid))
        self.button.grid(column=0, row=2, sticky='S', padx=5, pady=5)
        self.update()
        hs = self.winfo_screenheight()
        w = int(self.winfo_width())
        h = int(self.winfo_height())
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = ws / 2 - w / 2
        y = hs / 2 - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        if getattr(sys, 'frozen', False):
            self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')

    def valid(self):
        self.parent.page = self.combotry.current()
        self.destroy()


class OpenScanWin(Toplevel):

    def __init__(self, parent, file, type, nframe=1):
        super().__init__(parent)
        self.parent = parent
        app = OpenScan(self, file, type, nframe)

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


## Global Handler
launcherWindowCur = LauncherWindow()

