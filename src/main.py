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

import mrz                      # mrz.py
from image import CanvasImage   # image.py
import globs                    # globs.py

class mainWindow(Tk):

    def __init__(self, logger):
        Tk.__init__(self)
        self.initialize(logger)

    def initialize(self, logger):
        self.logger = logger
        self.PILE_ETAT = []
        self.MRZCHAR = ''
        self.varnum = 10
        self.Score = []
        for type in mrz.TYPES:
            self.Score += [0]

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.logger.info('mainWindow() : Launching main window with resolution' + str(ws) + 'x' + str(hs))
        self.grid()
        self.grid_columnconfigure(0, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_columnconfigure(1, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_columnconfigure(2, weight=1, minsize=(ws / 2 * 0.3333333333333333))
        self.grid_rowconfigure(0, weight=1, minsize=(hs / 2 * 0.5))
        self.grid_rowconfigure(1, weight=1, minsize=(hs / 2 * 0.5))
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
        self.STATUT = ttk.Labelframe(self, text='Statut')
        self.STATUT.grid_columnconfigure(0, weight=1)
        self.STATUT.grid_rowconfigure(0, weight=1)
        self.STATUStxt = Label((self.STATUT), text='', font='Times 24', fg='#FFBF00')
        self.STATUStxt.grid(column=0, row=0, padx=0, pady=0, sticky='EWNS')
        self.STATUStxt['text'] = 'EN ATTENTE'
        self.terminal = ttk.Labelframe(self, text='Terminal de saisie')
        self.terminal.grid_columnconfigure(0, weight=1)
        self.terminal.grid_rowconfigure(0, weight=1)
        self.termframe = Frame(self.terminal)
        self.termframe.grid(column=0, row=0, sticky='EW')
        self.termframe.grid_columnconfigure(0, weight=1)
        self.termframe.grid_rowconfigure(0, weight=1)
        self.termtext = Text((self.termframe), state='disabled', width=60, height=4, wrap='none', font='Terminal 17', fg='#121f38')
        self.termtext.grid(column=0, row=0, sticky='NEW', padx=5)
        vcmd = (self.register(self.entryValidation), '%S', '%P', '%d')
        self.termentry = Entry((self.termframe), font='Terminal 17', validate='all', validatecommand=vcmd, fg='#121f38', width=44)
        self.termentry.grid(column=0, row=0, sticky='SEW', padx=5)
        self.monitor = ttk.Labelframe(self, text='Moniteur')
        self.monlog = Text((self.monitor), state='disabled', width=60, height=10, wrap='word')
        self.monlog.grid(column=0, row=0, sticky='EWNS', padx=5, pady=5)
        self.scrollb = ttk.Scrollbar((self.monitor), command=(self.monlog.yview))
        self.scrollb.grid(column=1, row=0, sticky='EWNS', padx=5, pady=5)
        self.monlog['yscrollcommand'] = self.scrollb.set
        self.monitor.grid_columnconfigure(0, weight=1)
        self.monitor.grid_rowconfigure(0, weight=1)
        self.lecteur_ci.grid(column=0, row=0, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.STATUT.grid(column=2, row=0, sticky='EWNS', columnspan=1, padx=5, pady=5)
        self.terminal.grid(column=0, row=1, sticky='EWNS', columnspan=2, padx=5, pady=5)
        self.monitor.grid(column=2, row=1, sticky='EWNS', columnspan=1, padx=5, pady=5)
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
        self.wm_title(globs.CNIRName)
        if getattr(sys, 'frozen', False):
            self.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
        else:
            self.iconbitmap('id-card.ico')
        self.resizable(width=True, height=True)
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        w = int(self.winfo_width())
        h = int(self.winfo_height())
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = ws / 2 - w / 2
        y = hs / 2 - h / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.termentry.bind('<Return>', self.preentryValidation)
        self.termtext.bind('<Return>', self.preentryValidation)
        self.termentry.bind('<Escape>', self.onTabPressed)
        self.update()
        self.logger.info('mainWindow() : Initialization successful')

    def preentryValidation(self, event):
        self.logger.debug('preentryValidation() : Entering Validation')
        if self.PILE_ETAT != [] and len(self.PILE_ETAT) == 1:
            thetext = self.termentry.get()
            self.logger.debug('preentryValidation() : PILE_ETAT Satisfy the requisites : ' + str(self.PILE_ETAT))
            n = len(thetext)
            champ = mrz.TYPES[self.PILE_ETAT[0]][0]
            if not n % champ.find('|') == 0:
                self.logger.debug('preentryValidation() : Line not complete, operation aborted')
                return 'break'
            self.MRZCHAR += thetext
            self.termtext['state'] = 'normal'
            self.termtext.insert('end', thetext + '\n')
            self.termtext['state'] = 'disabled'
            self.termentry.delete(0, 'end')
            if len(self.MRZCHAR) == champ.find('|'):
                self.logOnTerm('Entrez la seconde ligne de la MRZ ou \nappuyez sur Entrée pour terminer.\n')
                self.logger.debug('preentryValidation() : First line accepted')
                self.MRZCHAR += '|'
            else:
                if len(self.MRZCHAR) == champ.find('|') * 2 + 1 or len(champ) == champ.find('|') + 1:
                    self.logOnTerm('\nCalcul des sommes ...\n')
                    self.logger.info('preentryValidation() : Launching calculSigma() thread')
                    threading.Thread(target=(self.calculSigma), args=[self.MRZCHAR, self.PILE_ETAT[0]]).start()
        else:
            if self.PILE_ETAT != []:
                if len(self.PILE_ETAT) == 2:
                    self.MRZCHAR = self.termtext.get('1.0', 'end').replace('\n', '|')
                    temp = self.termtext.get('1.0', 'end')
                    self.termtext.delete('1.0', 'end')
                    self.termtext.insert('1.0', temp)
                    self.logger.debug('preentryValidation() : PILE_ETAT Satisfy the requisites : ' + str(self.PILE_ETAT))
                    n = len(self.MRZCHAR)
                    champ = mrz.TYPES[self.PILE_ETAT[1]][0]
                    for char in self.MRZCHAR:
                        if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<|':
                            self.logOnTerm('\nSyntaxe erronée, caractère incompatible')
                            return 'break'
                        if self.MRZCHAR[(-1)] == '|':
                            self.MRZCHAR = self.MRZCHAR[:-1]

                    if len(self.MRZCHAR) == champ.find('|') * 2 + 1 or len(champ) == champ.find('|') + 1:
                        self.logger.debug('preentryValidation() :  : ' + str(self.PILE_ETAT))
                        self.logOnTerm('\nCalcul des sommes ...\n')
                        self.logger.info('preentryValidation() : Launching calculSigma() thread')
                        threading.Thread(target=(self.calculSigma), args=[self.MRZCHAR, self.PILE_ETAT[1]]).start()
        return 'break'

    def onTabPressed(self, event):
        if self.PILE_ETAT != [] and len(self.PILE_ETAT) == 1:
            thetext = self.termentry.get()
            n = len(thetext)
            champ = mrz.TYPES[self.PILE_ETAT[0]][0]
            if len(self.MRZCHAR) <= champ.find('|'):
                champ_type = mrz.TYPES[self.PILE_ETAT[0]][1][champ[(n - 1)]].split('|')
                self.logger.debug('onTabPressed() :  First line detected')
                self.logger.debug('onTabPressed() :  champ_type[0] : ' + str(champ_type[0]))
                self.logger.debug('onTabPressed() :  champ : ' + str(champ))
                self.logger.debug('onTabPressed() :  champ[n-1] : ' + str(champ[(n - 1)]))
                self.logger.debug('onTabPressed() :  champ.find(champ[n-1]) : ' + str(champ.find(champ[(n - 1)])))
                nb = int(champ_type[0]) - (n - champ.find(champ[(n - 1)]))
            else:
                self.logger.debug('onTabPressed() :  Second line detected')
                champ = champ[champ.find('|') + 1:]
                champ_type = mrz.TYPES[self.PILE_ETAT[0]][1][champ[(n - 1)]].split('|')
                self.logger.debug('onTabPressed() :  champ_type[0] : ' + str(champ_type[0]))
                self.logger.debug('onTabPressed() :  champ : ' + str(champ))
                self.logger.debug('onTabPressed() :  champ[n-1] : ' + str(champ[(n - 1)]))
                self.logger.debug('onTabPressed() :  champ.find(champ[n-1]) : ' + str(champ.find(champ[(n - 1)])))
                self.logger.debug('onTabPressed() :  n : ' + str(n))
                nb = int(champ_type[0]) - (n - champ.find(champ[(n - 1)]))
            self.termentry.insert('end', '<' * nb)
            self.logger.debug('onTabPressed() : Completing entry with ' + str(nb) + ' characters <')
        return 'break'

    def entryValidation(self, char, entry_value, typemod):
        set = False
        isValid = True
        if typemod == '1':
            SUM = 0
            for ch in char:
                if ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<':
                    continue
                self.bell()
                isValid = False

        else:
            if typemod == '0':
                for ch in char:
                    if ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<':
                        continue
                    self.bell()
                    isValid = False

        n = len(entry_value)
        if (n % self.varnum == 0 or len(char) > 3) and n < 45 and self.PILE_ETAT == []:
            for i in range(len(self.Score)):
                self.Score[i] = 0

            for type, t in zip(mrz.TYPES, range(len(mrz.TYPES))):
                for e in range(len(entry_value)):
                    try:
                        champchartest = type[0][:type[0].find('|')][e]
                        champchar = type[0][e]
                    except IndexError:
                        self.logger.debug('entryValidation() : type : ' + str(t))
                        self.logger.debug('entryValidation() : Too short to be ok')
                        self.Score[t] += -5
                        break
                    else:
                        self.logger.debug('entryValidation() : type : ' + str(t))
                        if len(entry_value) <= type[0].find('|'):
                            champ_type = type[1][str(champchar)].split('|')
                            pos = e - type[0].find(champchar)
                            self.logger.debug('entryValidation() : champ_type[2][pos] : ' + str(champ_type[2][pos]))
                            self.logger.debug('entryValidation() : champ_type[1] : ' + str(champ_type[1]))
                            if champ_type[1] == 'CODE':
                                if champ_type[2][pos] == '*':
                                    self.Score[t] += 0
                                else:
                                    if champ_type[2][pos] == entry_value[e]:
                                        self.Score[t] += 1
                                        self.logger.debug('entryValidation() : +1')
                                    else:
                                        self.Score[t] += -50
                            elif champ_type[2][pos] == '*':
                                self.Score[t] += 1
                                self.logger.debug('entryValidation() : +1')
                            else:
                                if champ_type[2][pos] == 'A':
                                    if entry_value[e].isalpha():
                                        self.Score[t] += 1
                                        self.logger.debug('entryValidation() : +1')
                                    if champ_type[2][pos] == '0':
                                        if entry_value[e].isnumeric():
                                            self.Score[t] += 1
                                            self.logger.debug('entryValidation() : +1')
                                        if champ_type[1] == 'CTRL':
                                            if entry_value[e].isnumeric():
                                                self.Score[t] += 1
                                                self.logger.debug('entryValidation() : +1')
                                            if champ_type[2][pos] == '&':
                                                if entry_value[e].isalpha() or entry_value[e] == '<':
                                                    self.Score[t] += 1
                                                    self.logger.debug('entryValidation() : +1')
                                                self.Score[t] += -1
                                continue

            self.logger.debug('entryValidation() : self.Score : ' + str(self.Score))
            m = max(self.Score)
            typem = [i for i, j in enumerate(self.Score) if j == m if m > 5]
            for h in typem:
                self.PILE_ETAT += [h]

            if len(self.PILE_ETAT) > 1:
                self.varnum += 3
                self.PILE_ETAT = []
            else:
                if len(self.PILE_ETAT) == 1:
                    TOPOS = mrz.TYPES[self.PILE_ETAT[0]][2]
                    self.logOnTerm(TOPOS + " détectée !\nAppuyez sur Echap pour compléter les champs avec des '<'\nAppuyez sur Entrée pour terminer.\n")
                    self.logger.debug('entryValidation() : Detection : ' + str(TOPOS))
        else:
            if len(self.PILE_ETAT) == 1:
                if len(entry_value) > len(mrz.TYPES[self.PILE_ETAT[0]][0].split('|')[0]):
                    isValid = False
        return isValid

    def logOnTerm(self, text):
        self.monlog['state'] = 'normal'
        self.monlog.insert('end', text)
        self.monlog['state'] = 'disabled'
        self.monlog.yview(END)

    def openingScan(self):
        self.initialize(self.logger)
        self.update()
        path = ''
        path = filedialog.askopenfilename(parent=self, title='Ouvrir un scan de CNI...', filetypes=(('TIF files', '*.tif'),
                                                                                                    ('TIF files', '*.tiff'),
                                                                                                    ('JPEG files', '*.jpg'),
                                                                                                    ('JPEG files', '*.jpeg')))
        self.openerrored = False
        if path != '':
            self.logger.info('openingScan() : Opening file with path ' + str(path))
            im = Image.open(path)
        try:
            nframe = im.n_frames
        except AttributeError:
            nframe = 1

        if nframe == 1:
            self.mrzdetected = ''
            self.mrzdict = {}
            try:
                opening = OpenScanWin(self, path, 0)
                opening.transient(self)
                opening.grab_set()
                self.wait_window(opening)
            except TclError:
                pass
            except Exception as e:
                self.logger.critical('openingScan() : ' + str(e))

            if self.openerrored == True:
                self.logger.error('openingScan() : Incompatible file with path ' + str(path))
                return
            self.logger.debug('openingScan() : ' + str(self.mrzdetected))
        else:
            if nframe > 1:
                self.mrzdetected = ''
                self.mrzdict = {}
                try:
                    opening = OpenScanWin(self, path, 1, nframe)
                    opening.transient(self)
                    opening.grab_set()
                    self.wait_window(opening)
                except TclError:
                    pass
                except Exception as e:
                    self.logger.critical('openingScan() : ' + str(e))

                if self.openerrored == True:
                    self.logger.critical('openingScan() : Incompatible file with path ' + str(path))
                    return
                self.logger.debug('openingScan() : ' + str(self.mrzdetected))
                try:
                    os.remove(globs.CNIREnv + '\\temp.tif')
                except IOError:
                    pass

            else:
                raise Exception
            mrzsoumisetab = self.mrzdetected.replace(' ', '').split('\n')
            for chain in mrzsoumisetab:
                self.termentry.insert('end', chain)
                if len(chain) >= 5:
                    self.preentryValidation('<Return>')

    def newEntry(self):
        self.initialize(self.logger)
        self.logOnTerm('\n\nEntrez la première ligne de MRZ svp \n')

    def infobox(self):
        Tk().withdraw()
        showinfo('A propos du logiciel', ('Version du logiciel : \n' + globs.verstring_full + ' ' + "\nLicence GNU/GPL 2018\n\nAuteur : NeoX_ ; devadmin@neoxgroup.eu\n\nTesseract 4.0 est soumis à l'Apache License 2004\n\n N'hésitez pas à faire part de vos commentaires !"), parent=self)

    def calculSigma(self, MRZtxt, numtype):
        CST_BACKGROUND = self['background']
        CTRList = [c for c, v in mrz.TYPES[numtype][1].items() if 'CTRL' in v]
        self.logger.info('[calculSigma() thread] : Sigma calculation launched!')
        self.logger.debug('[calculSigma() thread] : CTRList = ' + str(CTRList))
        self.Falsitude = 0
        self.logOnTerm('\n')
        for i in CTRList:
            sumtxt = mrz.TYPES[numtype][1][i]
            length = mrz.TYPES[numtype][0].find('|')
            index = mrz.TYPES[numtype][0].find(i)
            sum_read = MRZtxt[index]
            if len(sumtxt.split('|')[2]) == 1:
                debut = mrz.TYPES[numtype][0].find(sumtxt.split('|')[2][0])
                sum_calc = mrz.MRZ(MRZtxt[int(debut):index])
            else:
                transm_chain = ''
                for y in sumtxt.split('|')[2]:
                    debut = mrz.TYPES[numtype][0].find(y)
                    fin = debut + int(mrz.TYPES[numtype][1][y].split('|')[0])
                    transm_chain += MRZtxt[int(debut):int(fin)]

                sum_calc = mrz.MRZ(transm_chain)
            if str(sum_read)[0] != str(sum_calc)[0]:
                if not (sumtxt.split('|')[1] == 'CTRLF' and str(sum_read)[0] == '<'):
                    self.Falsitude += 1
                    self.logger.debug('[calculSigma() thread] : Falsitude +1, sum errored : ' + str(i))
                    self.termtext.tag_add('highLOW', '1.0+' + str(index) + 'c', '1.0+' + str(index + 1) + 'c')
                    self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground='white')
                self.termtext.tag_add('highLOWB', '1.0+' + str(index) + 'c', '1.0+' + str(index + 1) + 'c')
                self.termtext.tag_configure('highLOWB', background='#04B404', relief='raised', foreground='white')
            self.logOnTerm('Somme : Lu ' + str(sum_read) + ' VS calculé  ' + str(sum_calc) + '\n')

        NameList = [c for c, v in mrz.TYPES[numtype][1].items() if '|NOM' in v]
        SurnameList = [c for c, v in mrz.TYPES[numtype][1].items() if 'PRENOM' in v]
        DDateList = [c for c, v in mrz.TYPES[numtype][1].items() if 'DDATE' in v]
        BDateList = [c for c, v in mrz.TYPES[numtype][1].items() if 'BDATE' in v]
        EDateList = [c for c, v in mrz.TYPES[numtype][1].items() if 'EDATE' in v]
        PAYSList = [c for c, v in mrz.TYPES[numtype][1].items() if 'PAYS' in v]
        NATList = [c for c, v in mrz.TYPES[numtype][1].items() if 'NAT' in v]
        SEXList = [c for c, v in mrz.TYPES[numtype][1].items() if 'SEX' in v]
        NOINTList = [c for c, v in mrz.TYPES[numtype][1].items() if 'NOINT' in v]
        NOList = [c for c, v in mrz.TYPES[numtype][1].items() if 'NO|' in v]
        FACULTList = [c for c, v in mrz.TYPES[numtype][1].items() if 'FACULT' in v]
        INDICList = [c for c, v in mrz.TYPES[numtype][1].items() if 'INDIC' in v]
        BIGList = [
         NameList, SurnameList, DDateList, BDateList, EDateList, PAYSList, NATList, SEXList, NOList, INDICList, NOINTList]
        BIGObj = [
         self.nom, self.prenom, self.ddate, self.bdate, self.edate, self.pays, self.nat, self.sex, self.no, self.indic, self.no]
        for i in range(len(BIGList)):
            for champ, champnum in zip(BIGList[i], range(len(BIGList[i]))):
                debut = mrz.TYPES[numtype][0].find(champ)
                fin = debut + int(mrz.TYPES[numtype][1][champ].split('|')[0])
                if BIGObj[i] == self.pays or BIGObj[i] == self.nat:
                    try:
                        BIGObj[i]['text'] = mrz.landcode[MRZtxt[int(debut):int(fin)].replace('<', '')]
                    except KeyError:
                        self.Falsitude += 1
                        self.logOnTerm('Code pays : ' + str(MRZtxt[int(debut):int(fin)]) + ' est inconnu \n')
                        self.logger.debug('[calculSigma() thread] : Falsitude +1, unknown state')
                        self.termtext.tag_add('highLOW', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                        self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground='white')
                        BIGObj[i]['background'] = '#760808'
                        BIGObj[i]['foreground'] = 'white'
                    else:
                        BIGObj[i]['background'] = CST_BACKGROUND
                        BIGObj[i]['foreground'] = 'black'
                        self.termtext.tag_add('highLOWN', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                        self.termtext.tag_configure('highLOWN', background='white', relief='raised', foreground='#121f38')
                elif BIGObj[i] == self.sex:
                    try:
                        BIGObj[i]['text'] = mrz.sexcode[MRZtxt[int(debut):int(fin)]]
                    except KeyError:
                        self.Falsitude += 1
                        self.logOnTerm('Sexe : ' + str(MRZtxt[int(debut):int(fin)]) + ' est inconnu \n')
                        self.logger.debug('[calculSigma() thread] : Falsitude +1, unknown state')
                        self.termtext.tag_add('highLOW', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                        self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground='white')
                        BIGObj[i]['background'] = '#760808'
                        BIGObj[i]['foreground'] = 'white'
                    else:
                        BIGObj[i]['background'] = CST_BACKGROUND
                        BIGObj[i]['foreground'] = 'black'
                        self.termtext.tag_add('highLOWN', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                        self.termtext.tag_configure('highLOWN', background='white', relief='raised', foreground='#121f38')
                else:
                    if BIGObj[i] == self.edate or BIGObj[i] == self.ddate or BIGObj[i] == self.bdate:
                        txtl = MRZtxt[int(debut):int(fin)].replace('<<<', '').replace('<', ' ')
                        if len(txtl) < 6:
                            txtl += '0' * (6 - len(txtl))
                        BIGObj[i]['text'] = '{0}/{1}/{2}'.format(txtl[4:], txtl[2:4], txtl[:2])
                        if BIGObj[i] == self.edate:
                            present = datetime.now()
                            try:
                                expiration = datetime(2000 + int(txtl[:2]), int(txtl[2:4]), int(txtl[4:]))
                            except ValueError:
                                BIGObj[i]['background'] = '#760808'
                                BIGObj[i]['foreground'] = 'white'
                                self.Falsitude += 1
                                self.logOnTerm('Date : ' + str(BIGObj[i]['text']) + ' est invalide \n')
                                self.logger.debug('[calculSigma() thread] : Falsitude +1, invalid expiration date')
                                self.termtext.tag_add('highLOW', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                                self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground='white')
                            else:
                                BIGObj[i]['background'] = CST_BACKGROUND
                                BIGObj[i]['foreground'] = 'black'
                                self.termtext.tag_add('highLOWN', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                                self.termtext.tag_configure('highLOWN', background='white', relief='raised', foreground='#121f38')
                                if expiration < present:
                                    BIGObj[i]['background'] = '#e67300'
                                    BIGObj[i]['foreground'] = 'white'
                                    self.termtext.tag_add('highLOWN', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                                    self.termtext.tag_configure('highLOWN', background='white', relief='raised', foreground='#121f38')
                                else:
                                    BIGObj[i]['background'] = CST_BACKGROUND
                                    BIGObj[i]['foreground'] = 'black'
                        else:
                            try:
                                if int(txtl[4:]) == 0:
                                    verif = datetime(2000 + int(txtl[:2]), int(txtl[2:4]), 1)
                                else:
                                    verif = datetime(2000 + int(txtl[:2]), int(txtl[2:4]), int(txtl[4:]))
                            except ValueError:
                                BIGObj[i]['background'] = '#760808'
                                BIGObj[i]['foreground'] = 'white'
                                self.Falsitude += 1
                                self.logOnTerm('Date : ' + str(BIGObj[i]['text']) + ' est invalide \n')
                                self.logger.debug('[calculSigma() thread] : Falsitude +1, invalid datetime')
                                self.termtext.tag_add('highLOW', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                                self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground='white')
                            else:
                                BIGObj[i]['background'] = CST_BACKGROUND
                                BIGObj[i]['foreground'] = 'black'
                                self.termtext.tag_add('highLOWN', '1.0+' + str(debut) + 'c', '1.0+' + str(fin) + 'c')
                                self.termtext.tag_configure('highLOWN', background=CST_BACKGROUND, relief='raised', foreground='#121f38')
                    else:
                        if champnum == 0:
                            BIGObj[i]['text'] = MRZtxt[int(debut):int(fin)].replace('<<<', '').replace('<', ' ')
                        else:
                            BIGObj[i]['text'] += MRZtxt[int(debut):int(fin)].replace('<<<', '').replace('<', ' ')

        if self.Falsitude == 0:
            self.STATUStxt['text'] = 'CONFORME'
            self.STATUStxt['fg'] = '#04B404'
            self.logger.debug('[calculSigma() thread] : Conforme !')
        else:
            self.STATUStxt['text'] = 'NON CONFORME'
            self.STATUStxt['fg'] = '#760808'
            self.logger.debug('[calculSigma() thread] : Non conforme !')
            self.logOnTerm('** Score de non conformité : ' + str(self.Falsitude) + '**\n')
        self.termtext['state'] = 'normal'
        self.PILE_ETAT = [self.Falsitude, numtype]


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

