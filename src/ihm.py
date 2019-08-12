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
import webbrowser
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
import traceback

import logger               # logger.py
import globs                # globs.py
import lang                 # lang.py


controlKeys = ["Escape", "Right", "Left", "Up", "Down", "Home", "End", "BackSpace", "Delete", "Inser", "Shift_L", "Shift_R", "Control_R", "Control_L"]

class DocumentAsk(Toplevel):

    def __init__(self, parent, choices):
        self.choice = 0
        vals = [0, 1]
        super().__init__(parent)
        self.title("{} :".format(lang.all[globs.CNIRlang]["Choose the identity document"]))

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


class OpenScanDialog(Toplevel):

    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent
        self.title(lang.all[globs.CNIRlang]["OCR Detection Validation"])
        self.resizable(width=False, height=False)
        self.termtext = Text(self, state='normal', width=45, height=2, wrap='none', font='Terminal 17', fg='#121f38')
        self.termtext.grid(column=0, row=0, sticky='NEW', padx=5, pady=5)
        self.termtext.insert('end', text + '\n')
        self.button = Button(self, text=lang.all[globs.CNIRlang]["Validate"], command=(self.valid))
        self.button.grid(column=0, row=1, sticky='S', padx=5, pady=5)
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
        self.parent.validatedtext = self.termtext.get('1.0', 'end')
        texting = self.parent.validatedtext.replace(' ', '').replace('\r', '').split('\n')
        for i in range(len(texting)):
            for char in texting[i]:
                if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<':
                    showerror(lang.all[globs.CNIRlang]["Validation Error"], lang.all[globs.CNIRlang]["The submitted MRZ contains invalid characters"], parent=self)
                    self.parent.validatedtext = ''

        self.destroy()

class LoginDialog(Toplevel):

    def __init__(self, parent):
        self.key = ''
        self.login = ''
        super().__init__(parent)
        self.title(lang.all[globs.CNIRlang]["Connection"])
        Label(self, text='IPN : ').pack()
        self.entry_login = Entry(self)
        self.entry_login.insert(0, '')
        self.entry_login.pack()
        Label(self, text='{} : '.format(lang.all[globs.CNIRlang]["Password"])).pack()
        self.entry_pass = Entry(self, show='*')
        self.entry_pass.insert(0, '')
        self.entry_pass.pack()
        Button(self, text=lang.all[globs.CNIRlang]["Connection"], command=(self.connecti)).pack()
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
        self.resizable(width=False, height=False)

        # Setting up the geometry
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        wheight = 274
        wwidth  = 480
        # Centering
        x = ws / 2 - wwidth  / 2
        y = hs / 2 - wheight / 2
        self.geometry('%dx%d+%d+%d' % (wwidth, wheight, x, y))

        # Creating objects
        # Load an image using OpenCV
        # if getattr(sys, 'frozen', False):
        #    cv_img = cv2.imread(sys._MEIPASS +  r"\background.png\background.png")
        # else:
        cv_img = cv2.imread("background.png")

        cv_img = cv2.imread("background.png")
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        cv_img = cv2.blur(cv_img, (15, 15))
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        height, width, no_channels = cv_img.shape
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        height, width, no_channels = cv_img.shape
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
        self.mainCanvas = Canvas(self, width=wwidth, height=wheight, bg=globs.CNIRLColor, highlightthickness=0)
        self.mainCanvas.create_image(wwidth /2, wheight /2, image=self.photo)

        # Column
        self.mainCanvas.grid_rowconfigure(0, weight=1, minsize=(wheight / 10 * 9))
        self.mainCanvas.grid_rowconfigure(1, weight=1, minsize=(wheight / 10 * 1))

        self.mainCanvas.create_text((wwidth / 2), (wheight / 3), text=(globs.CNIRName), font='Helvetica 30', fill='white')
        self.mainCanvas.create_text((wwidth / 2), (wheight / 2), text="version " + (globs.verstring_full), font='Helvetica 8', fill='white')
        self.msg = self.mainCanvas.create_text((wwidth / 2), (wheight / 1.20), text=lang.all[globs.CNIRlang]["Booting up..."], font='Helvetica 9', fill='white')

        #self.pBarZone = Frame(self.mainCanvas, width=wwidth, height=wheight/10)
        self.update()

        self.progressBar = ttk.Progressbar(self.mainCanvas, orient=HORIZONTAL, length=wwidth, mode='determinate')

        self.wm_title(globs.CNIRName)

        self.mainCanvas.grid(row=0)
        self.update()
        self.progressBar.grid(row=1, sticky='S')


        if getattr(sys, 'frozen', False):
           self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')
        logfile = logger.logCur
        logfile.printdbg('Launcher IHM successful')
        self.protocol('WM_DELETE_WINDOW', lambda : 0)
        self.attributes("-topmost", 1)

        self.update()

    def printmsg(self, msg):
        self.mainCanvas.itemconfigure(self.msg, text=(msg))

    def exit(self):
        self.after(1000, self.destroy)

class ResizeableCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

def crashCNIR():
    """
    last solution
    """
    # Global handler
    logfile = logger.logCur
    # hide main window
    root = Tk()
    root.withdraw()
    logfile.printerr("FATAL ERROR : see traceback below.\n{}".format(traceback.format_exc()))
    showerror(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["CNIRevelator crashed because a fatal error occured. View log for more infos and please open an issue on Github"])
    res = askquestion(lang.all[globs.CNIRlang]["CNIRevelator Fatal Eror"], lang.all[globs.CNIRlang]["Would you like to open an issue on Github to report this bug ?"])
    if res == "yes":
        webbrowser.open_new("https://github.com/neox95/CNIRevelator/issues")
    root.destroy()


## Global Handler
launcherWindowCur = LauncherWindow()

