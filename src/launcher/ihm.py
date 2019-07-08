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
        w = 150
        h = 110
        self.update()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        if getattr(sys, 'frozen', False):
            self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')
        x = ws / 2 - w / 2
        y = hs / 2 - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def connecti(self):
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
        #self.update()

        # Creating objects
        self.mainCanvas = Canvas(self, width=wwidth, height=wheight*9/10, bg=globs.CNIRLColor, highlightthickness=0)
        self.pBarZone = Canvas(self, width=wwidth, height=wheight/10, bg=globs.CNIRLColor)
        
        self.progressBar = ttk.Progressbar(self.pBarZone, orient=HORIZONTAL, length=wwidth-10, mode='determinate')
        #self.update()
        
        self.mainCanvas.create_text((wwidth / 2), (wheight / 3), text=(globs.CNIRName), font='Helvetica 30', fill='white')
        self.msg = self.mainCanvas.create_text((wwidth / 2.05), (wheight / 1.20), text='', font='Helvetica 9', fill='white')
        #self.update()
        
        self.wm_title(globs.CNIRName)
        
        # Centering
        x = ws / 2 - wwidth  / 2
        y = hs / 2 - wheight / 2
        self.geometry('%dx%d+%d+%d' % (wwidth, wheight, x, y))
        self.mainCanvas.grid()
        self.pBarZone.grid()
        self.progressBar.grid()
        
        #self.after(2000, updating)
        
        if getattr(sys, 'frozen', False):
           self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')
        logfile = logger.logCur
        logfile.printdbg('Launcher IHM successful')
        self.protocol('WM_DELETE_WINDOW', lambda : self.destroy())

## Global Handler
launcherWindowCur = LauncherWindow()
        
