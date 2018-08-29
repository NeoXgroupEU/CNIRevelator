"""
******************************************************************************** 
                ***   Projet  CNI_Revelator   ***
                       
                        GNU GPL * 07/2018

                        Adrien Bourmault
                            
                            CLASSES

********************************************************************************
"""

###IMPORTS GLOBAUX
from CNI_GLOBALVAR import * 



###BEGIN

class App_main(Tk):
    
    def __init__(self, logger):
        
        Tk.__init__(self)
        self.initialize(logger)
        
        
    def initialize(self, logger):
        
        self.logger = logger
        
        #variable mrz
        self.PILE_ETAT = []
        self.MRZCHAR = ""
        self.varnum = 10
        self.Score = []
        for type in MRZCODE.TYPES:
            self.Score += [0]
        
        #taille de l'écran
        
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        
        self.logger.info("App_main() : " + "Launching main window with resolution" +  str(ws) +"x" + str(hs))
        
        self.grid() #init de la grille
        self.grid_columnconfigure(0,weight=1, minsize=(ws/2)* (1/3) )
        self.grid_columnconfigure(1,weight=1, minsize=(ws/2)* (1/3) )
        self.grid_columnconfigure(2,weight=1, minsize=(ws/2)* (1/3) )
        
        self.grid_rowconfigure(0,weight=1, minsize=(hs/2)* (1/2) )
        self.grid_rowconfigure(1,weight=1, minsize=(hs/2)* (1/2) )
        
        # [Zones de travail]
        
        
        
        self.lecteur_ci =  ttk.Labelframe(self, text = "Informations sur la pièce d'identité")
        
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
        
        
        ttk.Label(self.lecteur_ci, text='Nom : ').grid(column = 0, row = 1, padx = 5, pady = 5)
        self.nom = ttk.Label(self.lecteur_ci,text=' ')
        self.nom.grid(column = 1, row = 1, padx = 5, pady = 5)
        
        ttk.Label(self.lecteur_ci, text='Nom (2) : ').grid(column = 0, row = 2, padx = 5, pady = 5)
        self.prenom = ttk.Label(self.lecteur_ci,text=' ')
        self.prenom.grid(column = 1, row = 2, padx = 5, pady = 5)
        
        ttk.Label(self.lecteur_ci, text='Date de naissance : ').grid(column = 0, row = 3, padx = 5, pady = 5)
        self.bdate = ttk.Label(self.lecteur_ci,text=' ')
        self.bdate.grid(column = 1, row = 3, padx = 5, pady = 5)
        
        ttk.Label(self.lecteur_ci, text='Date de délivrance : ').grid(column = 0, row = 4, padx = 5, pady = 5)
        self.ddate = ttk.Label(self.lecteur_ci,text=' ')
        self.ddate.grid(column = 1, row = 4, padx = 5, pady = 5)
        
        ttk.Label(self.lecteur_ci, text="Date d'expiration : ").grid(column = 0, row = 5, padx = 5, pady = 5)
        self.edate = ttk.Label(self.lecteur_ci,text=' ')
        self.edate.grid(column = 1, row = 5, padx = 5, pady = 5)
        
        ttk.Label(self.lecteur_ci, text='Sexe du porteur : ').grid(column = 4, row = 1, padx = 5, pady = 5)
        self.sex = ttk.Label(self.lecteur_ci,text=' ')
        self.sex.grid(column = 5, row = 1, padx = 5, pady = 5)
        
        ttk.Label(self.lecteur_ci, text='Pays de délivrance : ').grid(column = 4, row = 2, padx = 5, pady = 5)
        self.pays = ttk.Label(self.lecteur_ci,text=' ')
        self.pays.grid(column = 5, row = 2, padx = 5, pady = 5)
        
        
        ttk.Label(self.lecteur_ci, text='Nationalité du porteur : ').grid(column = 4, row = 3, padx = 5, pady = 5)
        self.nat = ttk.Label(self.lecteur_ci,text=' ')
        self.nat.grid(column = 5, row = 3, padx = 5, pady = 5)
        
        ttk.Label(self.lecteur_ci, text='Immatriculation : ').grid(column = 4, row = 4, padx = 5, pady = 5)
        self.indic = ttk.Label(self.lecteur_ci,text=' ')
        self.indic.grid(column = 5, row = 4, padx = 5, pady = 5)
        
        ttk.Label(self.lecteur_ci, text='Numéro de document : ').grid(column = 4, row = 5, padx = 5, pady = 5)
        self.no = ttk.Label(self.lecteur_ci,text=' ')
        self.no.grid(column = 5, row = 5, padx = 5, pady = 5)
        
        
        self.nom['text'] = "Inconnu(e)"
        self.prenom['text'] = "Inconnu(e)"
        self.bdate['text'] = "Inconnu(e)"
        self.ddate['text'] = "Inconnu(e)"
        self.edate['text'] = "Inconnu(e)"
        self.no['text'] = "Inconnu(e)"
        self.sex['text'] = "Inconnu(e)"
        self.nat['text'] = "Inconnu(e)"
        self.pays['text'] = "Inconnu(e)"
        self.indic['text'] = "Inconnu(e)"
        
        self.STATUT =  ttk.Labelframe(self, text = "Statut")
        self.STATUT.grid_columnconfigure(0, weight=1)
        self.STATUT.grid_rowconfigure(0, weight=1)
        self.STATUStxt = Label(self.STATUT, text = "", font = "Times 24", fg = "#FFBF00")
        self.STATUStxt.grid(column = 0, row = 0, padx = 0, pady = 0, sticky='EWNS')
        self.STATUStxt['text'] = "EN ATTENTE"
        
        
        self.terminal = ttk.Labelframe(self, text = "Terminal de saisie")
        self.terminal.grid_columnconfigure(0, weight=1)
        self.terminal.grid_rowconfigure(0, weight=1)
        self.termframe = Frame(self.terminal)
        self.termframe.grid(column=0,row=0,sticky='EW')
        self.termframe.grid_columnconfigure(0, weight=1)
        self.termframe.grid_rowconfigure(0, weight=1)
        self.termtext = Text(self.termframe, state='disabled', width=60, height=4, wrap='none', font = "Terminal 17", fg = "#121f38")
        self.termtext.grid(column=0,row=0,sticky='NEW', padx=5)
        vcmd = (self.register(self.validate), '%S', '%P', '%d' )
        self.termentry = Entry(self.termframe, font = "Terminal 17", validate = 'all', validatecommand = vcmd, fg = "#121f38", width = 44)
        self.termentry.grid(column=0,row=0,sticky='SEW', padx=5)
        
        self.monitor =  ttk.Labelframe(self, text = "Moniteur")
        self.monlog = Text(self.monitor, state='disabled', width=60, height=10, wrap='word')
        self.monlog.grid(column=0,row=0,sticky='EWNS', padx=5, pady=5)
        self.monitor.grid_columnconfigure(0, weight=1)
        self.monitor.grid_rowconfigure(0, weight=1)
        
        # création du canvas
        self.lecteur_ci.grid(column=0,row=0,sticky='EWNS',columnspan=2, padx=5, pady=5)
        self.STATUT.grid(column=2,row=0,sticky='EWNS',columnspan=1, padx=5, pady=5)
        self.terminal.grid(column=0,row=1,sticky='EWNS',columnspan=2, padx=5, pady=5)
        self.monitor.grid(column=2,row=1,sticky='EWNS',columnspan=1, padx=5, pady=5)
        
        # [barres de menu]
        menubar = Menu(self)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Nouveau", command=self.newbie)
        menu1.add_command(label="Ouvrir scan...", command=self.openingscan)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.destroy)
        menubar.add_cascade(label="Fichier", menu=menu1)
        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label="A propos", command=self.infobox)
        menubar.add_cascade(label="Aide", menu=menu3)
        
        self.config(menu=menubar)    
    
        # Options de la fenêtre principale
        self.wm_title(CST_TITLE)
        
        if getattr( sys, 'frozen', False ) :
            self.iconbitmap(sys._MEIPASS + "\id-card.ico\id-card.ico")
        else:
            self.iconbitmap("id-card.ico")
        
        
        
        self.resizable(width=True, height=True)
        self.update()
        
        self.minsize(self.winfo_width(), self.winfo_height())
        
        w = int(self.winfo_width())  # width for the Tk root
        h = int(self.winfo_height())  # height for the Tk root
        
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
                
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.bind('<Return>', self.returnaj)
        self.bind('<Escape>', self.tabaj)
        
        self.logger.info("App_main() : " + "Initialization successful")
        
    def returnaj(self, event):
        self.logger.debug("returnaj() : " + "Entering Validation")
        if self.PILE_ETAT != [] and len(self.PILE_ETAT)==1 :
            thetext = self.termentry.get()
            self.logger.debug("returnaj() : " + "PILE_ETAT Satisfy the requisites")
        
            n = len(thetext)
            champ = MRZCODE.TYPES[self.PILE_ETAT[0]][0]
            
            if not n%champ.find("|") == 0 :
                self.logger.debug("returnaj() : " + "Line not complete, operation aborted")
                return None
                
            self.MRZCHAR += thetext
            self.termtext['state'] = "normal"
            self.termtext.insert("end", thetext + "\n")
            self.termtext['state'] = "disabled"
            self.termentry.delete(0, "end")
            
            if len(self.MRZCHAR) == champ.find("|"):
                self.montext("Entrez la seconde ligne de la MRZ ou \nappuyez sur Entrée pour terminer.\n")
                self.logger.debug("returnaj() : " + "First line accepted")
                self.MRZCHAR += "|"
            elif len(self.MRZCHAR) == champ.find("|")*2+1 or len(champ)==champ.find("|") +1:
                self.montext("\nCalcul des sommes ...\n")
                self.logger.info("returnaj() : " + "Launching calculsigma() thread")
                threading.Thread(target=self.calculsigma, args=[self.MRZCHAR,self.PILE_ETAT[0]]).start()
            
                
        
    def tabaj(self, event): #fonction de complétion de champ par touche Escape
        
        if self.PILE_ETAT != [] and len(self.PILE_ETAT)==1 :
            thetext = self.termentry.get()
        
            n = len(thetext)
            
            champ = MRZCODE.TYPES[self.PILE_ETAT[0]][0]
            
            
            if len(self.MRZCHAR) <= champ.find("|"):
                
                champ_type = MRZCODE.TYPES[self.PILE_ETAT[0]][1][ champ[n-1] ].split("|")
                self.logger.debug("tabaj() : " + " First line detected")
                self.logger.debug("tabaj() : " + " champ_type[0] : " + str(champ_type[0]))
                self.logger.debug("tabaj() : " + " champ : " + str(champ))
                self.logger.debug("tabaj() : " + " champ[n-1] : " + str(champ[n-1]))
                self.logger.debug("tabaj() : " + " champ.find(champ[n-1]) : " + str(champ.find(champ[n-1])))
                nb = int(champ_type[0]) - (n - champ.find(champ[n-1]))
            
            else:
                
                self.logger.debug("tabaj() : " + " Second line detected")
                champ = champ[champ.find("|")+1:]
                champ_type = MRZCODE.TYPES[self.PILE_ETAT[0]][1][ champ[n-1] ].split("|")
                self.logger.debug("tabaj() : " + " champ_type[0] : " + str(champ_type[0]))
                self.logger.debug("tabaj() : " + " champ : " + str(champ))
                self.logger.debug("tabaj() : " + " champ[n-1] : " + str(champ[n-1]))
                self.logger.debug("tabaj() : " + " champ.find(champ[n-1]) : " + str(champ.find(champ[n-1])))
                self.logger.debug("tabaj() : " + " n : " + str(n))
                nb = int(champ_type[0]) - (n - champ.find(champ[n-1]))
                
            
            self.termentry.insert("end", "<"*nb)
            
            self.logger.debug("tabaj() : " + "Completing entry with " + str(nb) + " characters <")
            
            
            
    
    def validate(self, char, entry_value, typemod):
        set = False
        isValid = True
        
        if typemod == "1":
            
            SUM = 0
            
            for ch in char:
                if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<":
                    
                    None
                    
                else:
                    
                    self.bell()
                    isValid = False
            
        elif typemod == "0":
            
            for ch in char:
                if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<" :
                    None
                else:
                    
                    self.bell()
                    isValid = False
            
        
        #PARSEUR INTERACTIF    
        n = len(entry_value)
        
        if (n%self.varnum == 0 or len(char)>3) and n<45 and self.PILE_ETAT == []:
            
            for i in range(len(self.Score)):    #Reinitialisation des scores
                
                self.Score[i] = 0
                
            
            for type, t in zip(MRZCODE.TYPES, range(len(MRZCODE.TYPES))):      #Test de chaque type
                
                for e in range(len(entry_value)):             #Parcours des caractères de la chaine évaluee
                    
                    
                    try:
                        champchartest   = type[0][:type[0].find("|")][e]
                        champchar       = type[0][e]
                    except IndexError:
                        self.logger.debug("validate() : " + "type : " + str(t))
                        self.logger.debug("validate() : " + "Too short to be ok")
                        self.Score[t] += -5
                        break
                    else:
                            
                        
                        self.logger.debug("validate() : " + "type : " + str(t))
                        
                        if len(entry_value) <= type[0].find("|"): #test ligne 1 mrz
                            champ_type  = type[1][str(champchar)].split("|")
                        
                            pos = e - type[0].find(champchar) 
                            
                            self.logger.debug("validate() : " + "champ_type[2][pos] : " + str(champ_type[2][pos]))
                            self.logger.debug("validate() : " + "champ_type[1] : " + str(champ_type[1]))
                            
                            if champ_type[1] == "CODE":
                                
                                if champ_type[2][pos] == "*":
                                    self.Score[t] += 0
                                elif champ_type[2][pos] == entry_value[e]:
                                    self.Score[t] += 1
                                    self.logger.debug("validate() : " + "+1")
                                else:
                                    self.Score[t] += -50
                                
                            else:
                                
                                if champ_type[2][pos] == "*":
                                    self.Score[t] += 1
                                    self.logger.debug("validate() : " + "+1")
                                    
                                elif champ_type[2][pos] == "A" and entry_value[e].isalpha():
                                    self.Score[t] += 1
                                    self.logger.debug("validate() : " + "+1")
                                elif champ_type[2][pos] == "0" and entry_value[e].isnumeric():
                                    self.Score[t] += 1
                                    self.logger.debug("validate() : " + "+1")
                                elif champ_type[1] == "CTRL" and entry_value[e].isnumeric():
                                    self.Score[t] += 1
                                    self.logger.debug("validate() : " + "+1")
                                elif champ_type[2][pos] == "&" and (entry_value[e].isalpha() or entry_value[e]=="<"):
                                    self.Score[t] += 1
                                    self.logger.debug("validate() : " + "+1")
                                    
                                else:
                                    self.Score[t] += -1
                                    
                            
                        else:
                            None #bah on fait rien parcequ'on a atteint le bout de la ligne dans le type donné.    
                        
                        
            self.logger.debug("validate() : " + "self.Score : " + str(self.Score))
            
            m     =  max(self.Score)
            typem =  [i for i, j in enumerate(self.Score) if j == m and m > 5]
            
            for h in typem:
                self.PILE_ETAT += [ h ]
            
            if len(self.PILE_ETAT) > 1:
                self.varnum += 3
                self.PILE_ETAT = []
            elif len(self.PILE_ETAT) == 1:
                TOPOS = MRZCODE.TYPES[ self.PILE_ETAT[0] ][2]
                
                self.montext(TOPOS + " détectée !\nAppuyez sur Echap pour compléter les champs avec des '<'\nAppuyez sur Entrée pour terminer.\n")
                self.logger.debug("validate() : " + "Detection : " + str(TOPOS))
                
            
            
        elif len(self.PILE_ETAT) == 1 and len(entry_value) > len(MRZCODE.TYPES[self.PILE_ETAT[0]][0].split("|")[0]):
            isValid = False
        
        return isValid
    
    def montext(self,text):
        
        self.monlog['state'] = "normal"
        self.monlog.insert("end",text)
        self.monlog['state'] = "disabled"
        
    def openingscan(self):
        
        self.initialize(self.logger)
        self.update()
        
        path = ""
        path = filedialog.askopenfilename(parent=self, title = "Ouvrir un scan de CNI...",filetypes = (("TIF files","*.tif"),("TIF files","*.tiff"), ("JPEG files","*.jpg"), ("JPEG files","*.jpeg"))) #dialog
        
        
        if path != "":
            self.logger.info("openingscan() : " + "Opening file with path " + str(path))
            
            im = Image.open(path)
        
            try:
                nframe = im.n_frames 
            except AttributeError:
                nframe = 1
            
            if nframe == 1: 
                
                self.mrzdetected = ""
                self.mrzdict = {}
                opening = OpenScanWin(self, path, 0)
                opening.transient(self)
                opening.grab_set()
                self.wait_window(opening)
                
                self.logger.debug("openingscan() : " + str(self.mrzdetected))
                
            elif nframe > 1: #If multi framed tiff
                
                # self.page = 1
                
                # opening = OpenPageDialog(self, nframe)
                # opening.transient(self)
                # opening.grab_set()
                # self.wait_window(opening)
                # 
                # im.seek(self.page)
                # im.save(CST_FOLDER + '\\temp.tif')
                # 
                # 
                # self.mrzdetected = ""
                # self.mrzdict = {}
                # opening = OpenScanWin(self, CST_FOLDER + '\\temp.tif', 1)
                # opening.transient(self)
                # opening.grab_set()
                # self.wait_window(opening)
                
                self.mrzdetected = ""
                self.mrzdict = {}
                opening = OpenScanWin(self, path, 1, nframe)
                opening.transient(self)
                opening.grab_set()
                self.wait_window(opening)
                
                self.logger.debug("openingscan() : " + str(self.mrzdetected))
                
                
                
                try:
                    os.remove(CST_FOLDER + '\\temp.tif')
                except IOError:
                    pass
                
            else:
                raise(Exception)
                
            mrzsoumisetab = self.mrzdetected.replace(" ", "").split("\n")
            
            #Sending the mrz to the core system
            
            for chain in mrzsoumisetab:
                
                self.termentry.insert("end", chain)
                
                if len(chain)>=5 : self.returnaj("<Return>")
                
        
        
        
        
        return None
        
            
    def newbie(self):
        self.initialize(self.logger)
        self.montext("\n\nEntrez la première ligne de MRZ svp \n")
        
    def infobox(self):
        
        Tk().withdraw()
        showinfo("A propos du logiciel", "Version du logiciel : \n" +CST_NAME + " " + CST_VER + " " + CST_TYPE + " Revision " + CST_REV +"\nLicence GNU/GPL 2018\n\nAuteur : NeoX_ ; devadmin@neoxgroup.eu\n\nTesseract 4.0 est soumis à l'Apache License 2004\n\n N'hésitez pas à faire part de vos commentaires !")
    
    def calculsigma(self, MRZtxt, numtype):   #Calcul des sommes
        
        #récupération des index des CTRL
        CTRList = [c for c,v in MRZCODE.TYPES[numtype][1].items() if "CTRL" in v]
        self.logger.info("[calculsigma() thread] : " + "Sigma calculation launched!")
        self.logger.debug("[calculsigma() thread] : " + "CTRList = " + str(CTRList))
        self.Falsitude = 0
        self.montext("\n")
        
        for i in CTRList:
            
            
            sumtxt = MRZCODE.TYPES[numtype][1][i]           #Récupération du descriptif de la somme
            length = MRZCODE.TYPES[numtype][0].find("|")    # Récupération de la longueur de ligne du code MRZ
            index = MRZCODE.TYPES[numtype][0].find(i)       # Récupération de l'index de la somme 
            
            
            sum_read = MRZtxt[index] #lecture de la somme donnée par la carte

            if len(sumtxt.split("|")[2])==1:    #Cas d'une somme de champ
                
                debut = MRZCODE.TYPES[numtype][0].find(sumtxt.split("|")[2][0]) 
                sum_calc = MRZCODE.MRZ(MRZtxt[ int(debut) : index ])
                
            else:       #Cas d'une somme composite
                
                transm_chain = ""
                for y in sumtxt.split("|")[2]:                                  
                    
                    debut = MRZCODE.TYPES[numtype][0].find(y)
                    fin = debut + int(MRZCODE.TYPES[numtype][1][y].split("|")[0])
                    transm_chain += MRZtxt[ int(debut) : int(fin) ]
                
                sum_calc = MRZCODE.MRZ(transm_chain)
                
                
                
            
            if str(sum_read)[0] != str(sum_calc)[0] and not(sumtxt.split("|")[1] == "CTRLF" and str(sum_read)[0]=="<"):
                
                self.Falsitude += 1
                self.logger.debug("[calculsigma() thread] : " + "Falsitude +1, sum errored : " + str(i))
                self.termtext.tag_add('highLOW', '1.0+'+ str(index) + 'c', '1.0+'+ str(index+1) + 'c')
                self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground = 'white')
                
            else:
                self.termtext.tag_add('highLOWB', '1.0+'+ str(index) + 'c', '1.0+'+ str(index+1) + 'c')
                self.termtext.tag_configure('highLOWB', background='#04B404', relief='raised', foreground = 'white')
            
            self.montext("Somme : Lu " + str(sum_read) + " VS calculé  " + str(sum_calc) + "\n")
            
            
        #Retriving infos
        NameList        = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "|NOM" in v    ]
        SurnameList     = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "PRENOM" in v  ]
        DDateList       = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "DDATE" in v   ]
        BDateList       = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "BDATE" in v   ]
        EDateList       = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "EDATE" in v   ]    
        PAYSList        = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "PAYS" in v    ]
        NATList         = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "NAT" in v     ]
        SEXList         = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "SEX" in v     ]
        NOINTList       = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "NOINT" in v   ]
        NOList          = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "NO|" in v     ]
        FACULTList      = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "FACULT" in v  ]
        INDICList       = [     c for c,v in MRZCODE.TYPES[numtype][1].items() if "INDIC" in v   ]
        
        BIGList = [ NameList, SurnameList, DDateList, BDateList, EDateList, PAYSList, NATList, SEXList, NOList, INDICList, NOINTList]
        
        BIGObj = [ self.nom, self.prenom, self.ddate, self.bdate, self.edate, self.pays, self.nat, self.sex, self.no, self.indic, self.no]
        
        for i in range(len(BIGList)):
            
            for (champ, champnum) in zip(BIGList[i], range(len(BIGList[i]))):
                
                debut = MRZCODE.TYPES[numtype][0].find(champ)
                fin = debut + int(MRZCODE.TYPES[numtype][1][champ].split("|")[0])   #Récupération des coordonnées de champs utiles
                
                
                if BIGObj[i] == self.pays or BIGObj[i] == self.nat:
                    
                    try:
                    
                        BIGObj[i]["text"] = MRZCODE.landcode[ MRZtxt[ int(debut) : int(fin) ] ]           #Si c'est un pays on traduit
                    
                    except KeyError:
                        
                        self.Falsitude += 1
                        self.montext("Code pays : " + str(MRZtxt[ int(debut) : int(fin) ]) + " est inconnu \n")
                        self.logger.debug("[calculsigma() thread] : " + "Falsitude +1, unknown state")
                        self.termtext.tag_add('highLOW', '1.0+'+ str(debut) + 'c', '1.0+'+ str(fin) + 'c')
                        self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground = 'white')
                        BIGObj[i]["background"] = "#760808"
                        BIGObj[i]["foreground"] = "white"
                        
                elif BIGObj[i] == self.sex:
                    
                    try:
                    
                        BIGObj[i]["text"] = MRZCODE.sexcode[ MRZtxt[ int(debut) : int(fin) ] ]
                    
                    except KeyError:
                        
                        self.Falsitude += 1
                        self.montext("Sexe : " + str(MRZtxt[ int(debut) : int(fin) ]) + " est inconnu \n")
                        self.logger.debug("[calculsigma() thread] : " + "Falsitude +1, unknown state")
                        self.termtext.tag_add('highLOW', '1.0+'+ str(debut) + 'c', '1.0+'+ str(fin) + 'c')
                        self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground = 'white')
                        BIGObj[i]["background"] = "#760808"
                        BIGObj[i]["foreground"] = "white"
                     
                elif BIGObj[i] == self.edate or BIGObj[i] == self.ddate or BIGObj[i] == self.bdate:
                    
                    txtl = MRZtxt[ int(debut) : int(fin) ].replace("<<<","").replace("<"," ")
                    
                    if len(txtl) < 6 : txtl += "0" * (6 - len(txtl))
                    
                    BIGObj[i]["text"] = "{0}/{1}/{2}".format(txtl[4:], txtl[2:4], txtl[:2])
                    
                    if BIGObj[i] == self.edate:
                        present = datetime.now()
                        
                        try:
                        
                            expiration = datetime(2000 + int(txtl[:2]), int(txtl[2:4]), int(txtl[4:]) )
                        
                        except ValueError:
                            
                            BIGObj[i]["background"] = "#760808"
                            BIGObj[i]["foreground"] = "white"
                            self.Falsitude += 1
                            self.montext("Date : " + str(BIGObj[i]["text"]) + " est invalide \n")
                            self.logger.debug("[calculsigma() thread] : " + "Falsitude +1, invalid expiration date")
                            self.termtext.tag_add('highLOW', '1.0+'+ str(debut) + 'c', '1.0+'+ str(fin) + 'c')
                            self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground = 'white')
                        
                        else:
                            
                            if expiration < present:
                                
                                BIGObj[i]["background"] = "#e67300"
                                BIGObj[i]["foreground"] = "white"
                    else:
                        
                        try:
                        
                            if int(txtl[4:]) == 0:
                                verif = datetime(2000 + int(txtl[:2]), int(txtl[2:4]), 1 )
                            else:
                                verif = datetime(2000 + int(txtl[:2]), int(txtl[2:4]), int(txtl[4:]) )
                            
                        
                        except ValueError:
                        
                            BIGObj[i]["background"] = "#760808"
                            BIGObj[i]["foreground"] = "white"
                            self.Falsitude += 1
                            self.montext("Date : " + str(BIGObj[i]["text"]) + " est invalide \n")
                            self.logger.debug("[calculsigma() thread] : " + "Falsitude +1, invalid datetime")
                            self.termtext.tag_add('highLOW', '1.0+'+ str(debut) + 'c', '1.0+'+ str(fin) + 'c')
                            self.termtext.tag_configure('highLOW', background='#760808', relief='raised', foreground = 'white')
                    
                else:
                    
                    if champnum == 0:
                        BIGObj[i]["text"] = MRZtxt[ int(debut) : int(fin) ].replace("<<<","").replace("<"," ")
                    else:
                        BIGObj[i]["text"] += MRZtxt[ int(debut) : int(fin) ].replace("<<<","").replace("<"," ")#Sinon on indique juste
                
        if self.Falsitude == 0 :
            
            self.STATUStxt['text'] = "CONFORME"
            self.STATUStxt['fg']   = "#04B404"
            self.logger.debug("[calculsigma() thread] : " + "Conforme !")
            
        else:
            
            self.STATUStxt['text'] = "NON CONFORME"
            self.STATUStxt['fg']   = "#760808"
            self.logger.debug("[calculsigma() thread] : " + "Non conforme !")
            
            self.montext("** Score de non conformité : " + str(self.Falsitude) + "**\n")
            
        return None
 
 
class MRZCODE:
    
    #Fonction de calcul
    def MRZ(code):
        """
        Calcul sommes de contrôle de la chaîne transmise
        """
        resultat = 0                          #init de la somme avant calcul
        i = -1                                #init du pas de somme avant calcul
        facteur = [7, 3, 1]                   #facteurs magiques 
        
        for car in code:                      #Traitement selon le type de caractère
            if car == "<" or car == "|":
                valeur = 0
                i += 1
            elif car in "0123456789":
                valeur = int(car)
                i += 1
            elif car in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                valeur = ord(car)-55
                i += 1
            else:
                self.logger.error("MRZ() : " + "Erreur de calcul : caractère non conforme")
                showerror("Erreur du module de calcul",Exception("Caractère non conforme dans la MRZ"))
                break
                
            resultat += valeur * facteur[i%3]  #Rajout de la valeur du caractère dans la somme et itération suivante
            
        return (resultat % 10) #Fin de la fonction, application du mod 10
  
    #Dictionnaire des sexes
    sexcode = { 'M' : 'Homme' , 'F' : 'Femme', 'X' : 'Non spécifié'}
    
    #Dictionnaire des pays
    landcode2 = {'AW': 'Aruba', 'AF': 'Afghanistan', 'AO': 'Angola', 'AI': 'Anguilla', 'AL': 'Albanie', 'AD': 'Andorre', 'AE': 'Emirats arabes unis', 'AR': 'Argentine', 'AM': 'Arménie', 'AS': 'Samoa américaines', 'AQ': 'Antarctique', 'TF': 'Terres australes et antarctiques françaises', 'AG': 'Antigua-et-Barbuda', 'AU': 'Australie', 'AT': 'Autriche', 'AZ': 'Azerbaidjan', 'BI': 'Burundi', 'BE': 'Belgique', 'BJ': 'Benin', 'BQ': 'Pays-Bas caribéens', 'BF': 'Burkina Faso', 'BD': 'Bangladesh', 'BG': 'Bulgarie', 'BH': 'Bahrein', 'BS': 'Bahamas', 'BA': 'Bosnie-Herzegovine', 'BL': 'Saint-Barthélemy', 'BY': 'Bielorussie', 'BZ': 'Belize', 'BM': 'Bermudes', 'BO': 'Bolivie', 'BR': 'Brésil', 'BB': 'Barbade', 'BN': 'Brunei', 'BT': 'Bhoutan', 'BW': 'Botswana', 'CF': 'République Centrafricaine', 'CA': 'Canada', 'CC': 'Îles Cocos', 'CH': 'Suisse', 'CL': 'Chili', 'CN': 'Chine', 'CI': "Côte d'Ivoire", 'CM': 'Cameroun', 'CD': 'Congo (République démocratique)', 'CG': 'Congo (République)', 'CK': 'Îles Cook', 'CO': 'Colombie', 'KM': 'Comores', 'CV': 'Cap-Vert', 'CR': 'Costa Rica', 'CU': 'Cuba', 'CW': 'Curaçao', 'CX': 'Île Christmas', 'KY': 'Caimans', 'CY': 'Chypre', 'CZ': 'Tchéquie', 'DE': 'Allemagne', 'DJ': 'Djibouti', 'DM': 'Dominique', 'DK': 'Danemark', 'DO': 'République dominicaine', 'DZ': 'Algérie', 'EC': 'Equateur', 'EG': 'Egypte', 'ER': 'Erythrée', 'EH': 'Sahara occidental', 'ES': 'Espagne', 'EE': 'Estonie', 'ET': 'Ethiopie', 'FI': 'Finlande', 'FJ': 'Fidji', 'FK': 'Îles Malouines', 'FR': 'France', 'FO': 'Féroé', 'FM': 'Micronésie', 'GA': 'Gabon', 'GB': 'Royaume-Uni', 'GE': 'Géorgie', 'GG': 'Guernesey', 'GH': 'Ghana', 'GI': 'Gibraltar', 'GN': 'Guinée', 'GP': 'Guadeloupe', 'GM': 'Gambie', 'GW': 'Guinée-Bissau', 'GQ': 'Guinée équatoriale', 'GR': 'Grèce', 'GD': 'Grenade', 'GL': 'Groenland', 'GT': 'Guatemala', 'GF': 'Guyane', 'GU': 'Guam', 'GY': 'Guyana', 'HK': 'Hong Kong', 'HN': 'Honduras', 'HR': 'Croatie', 'HT': 'Haïti', 'HU': 'Hongrie', 'ID': 'Indonésie', 'IM': 'Île de Man', 'IN': 'Inde', 'IO': "Territoire britannique de l'océan Indien", 'IE': 'Irlande', 'IR': 'Irak', 'IQ': 'Iran', 'IS': 'Islande', 'IL': 'Israël', 'IT': 'Italie', 'JM': 'Jamaïque', 'JE': 'Jersey', 'JO': 'Jordanie', 'JP': 'Japon', 'KZ': 'Kazakhstan', 'KE': 'Kenya', 'KG': 'Kirghizistan', 'KH': 'Cambodge', 'KI': 'Kiribati', 'KN': 'Saint-Christophe-et-Niévès', 'KR': 'Corée du Sud', 'KW': 'Koweït', 'LA': 'Laos', 'LB': 'Liban', 'LR': 'Liberia', 'LY': 'Libye', 'LC': 'Sainte-Lucie', 'LI': 'Liechtenstein', 'LK': 'Sri Lanka', 'LS': 'Lesotho', 'LT': 'Lituanie', 'LU': 'Luxembourg', 'LV': 'Lettonie', 'MO': 'Macao', 'MF': 'Sint-Maarten', 'MA': 'Maroc', 'MC': 'Monaco', 'MD': 'Moldavie', 'MG': 'Madagascar', 'MV': 'Maldives', 'MX': 'Mexique', 'MH': 'Marshall', 'MK': 'Macedoine', 'ML': 'Mali', 'MT': 'Malte', 'MM': 'Birmanie', 'ME': 'Monténégro', 'MN': 'Mongolie', 'MP': 'Îles Mariannes du Nord', 'MZ': 'Mozambique', 'MR': 'Mauritanie', 'MS': 'Montserrat', 'MQ': 'Martinique', 'MU': 'Maurice', 'MW': 'Malawi', 'MY': 'Malaisie', 'YT': 'Mayotte', 'NA': 'Namibie', 'NC': 'Nouvelle-Calédonie', 'NE': 'Niger', 'NF': 'Île Norfolk', 'NG': 'Nigeria', 'NI': 'Nicaragua', 'NU': 'Niue', 'NL': 'Pays-Bas', 'NO': 'Norvège', 'NP': 'Nepal', 'NR': 'Nauru', 'NZ': 'Nouvelle-Zélande', 'OM': 'Oman', 'PK': 'Pakistan', 'PA': 'Panama', 'PN': 'Îles Pitcairn', 'PE': 'Pérou', 'PH': 'Philippines', 'PW': 'Palaos', 'PG': 'Papouasie-Nouvelle-Guinée', 'PL': 'Pologne', 'PR': 'Porto Rico', 'KP': 'Corée du Nord', 'PT': 'Portugal', 'PY': 'Paraguay', 'PS': 'Palestine', 'PF': 'Polynésie française', 'QA': 'Qatar', 'RE': 'Réunion', 'RO': 'Roumanie', 'RU': 'Russie', 'RW': 'Rwanda', 'SA': 'Arabie saoudite', 'SD': 'Soudan', 'SN': 'Sénégal', 'SG': 'Singapour', 'GS': 'Georgie du Sud-et-les iles Sandwich du Sud', 'SH': 'Sainte-Hélène, Ascension et Tristan da Cunha', 'SJ': 'Svalbard et île Jan Mayen', 'SB': 'Salomon', 'SL': 'Sierra Leone', 'SV': 'Salvador', 'SM': 'Saint-Marin', 'SO': 'Somalie', 'PM': 'Saint-Pierre-et-Miquelon', 'RS': 'Serbie', 'SS': 'Soudan du Sud', 'ST': 'Sao Tomé-et-Principe', 'SR': 'Suriname', 'SK': 'Slovaquie', 'SI': 'Slovénie', 'SE': 'Suède', 'SZ': 'eSwatani', 'SX': 'Saint-Martin ', 'SC': 'Seychelles', 'SY': 'Syrie', 'TC': 'Îles Turques-et-Caïques', 'TD': 'Tchad', 'TG': 'Togo', 'TH': 'Thaïlande', 'TJ': 'Tadjikistan', 'TK': 'Tokelau', 'TM': 'Turkmenistan', 'TL': 'Timor oriental', 'TO': 'Tonga', 'TT': 'Trinité-et-Tobago', 'TN': 'Tunisie', 'TR': 'Turquie', 'TV': 'Tuvalu', 'TW': 'Taiwan', 'TZ': 'Tanzanie', 'UG': 'Ouganda', 'UA': 'Ukraine', 'UY': 'Uruguay', 'US': 'Etats-Unis', 'UZ': 'Ouzbékistan', 'VA': 'Saint-Siège (État de la Cité du Vatican)', 'VC': 'Saint-Vincent-et-les-Grenadines', 'VE': 'Venezuela', 'VG': 'Îles Vierges britanniques', 'VI': 'Îles Vierges des États-Unis', 'VN': 'Viêt Nam', 'VU': 'Vanuatu', 'WF': 'Wallis-et-Futuna', 'WS': 'Samoa', 'XK': 'Kosovo', 'YE': 'Yémen', 'ZA': 'Afrique du Sud', 'ZM': 'Zambie', 'ZW': 'Zimbabwe'}
    
    landcode = {'ABW': 'Aruba', 'AFG': 'Afghanistan', 'AGO': 'Angola', 'AIA': 'Anguilla', 'ALB': 'Albanie', 'AND': 'Andorre', 'ARE': 'Emirats arabes unis', 'ARG': 'Argentine', 'ARM': 'Arménie', 'ASM': 'Samoa américaines', 'ATA': 'Antarctique', 'ATF': 'Terres australes et antarctiques françaises', 'ATG': 'Antigua-et-Barbuda', 'AUS': 'Australie', 'AUT': 'Autriche', 'AZE': 'Azerbaidjan', 'BDI': 'Burundi', 'BEL': 'Belgique', 'BEN': 'Benin', 'BES': 'Pays-Bas caribéens', 'BFA': 'Burkina Faso', 'BGD': 'Bangladesh', 'BGR': 'Bulgarie', 'BHR': 'Bahrein', 'BHS': 'Bahamas', 'BIH': 'Bosnie-Herzegovine', 'BLM': 'Saint-Barthélemy', 'BLR': 'Bielorussie', 'BLZ': 'Belize', 'BMU': 'Bermudes', 'BOL': 'Bolivie', 'BRA': 'Brésil', 'BRB': 'Barbade', 'BRN': 'Brunei', 'BTN': 'Bhoutan', 'BWA': 'Botswana', 'CAF': 'République Centrafricaine', 'CAN': 'Canada', 'CCK': 'Îles Cocos', 'CHE': 'Suisse', 'CHL': 'Chili', 'CHN': 'Chine', 'CIV': "Côte d'Ivoire", 'CMR': 'Cameroun', 'COD': 'Congo (République démocratique)', 'COG': 'Congo (République)', 'COK': 'Îles Cook', 'COL': 'Colombie', 'COM': 'Comores', 'CPV': 'Cap-Vert', 'CRI': 'Costa Rica', 'CUB': 'Cuba', 'CUW': 'Curaçao', 'CXR': 'Île Christmas', 'CYM': 'Caimans', 'CYP': 'Chypre', 'CZE': 'Tchéquie', 'DEU': 'Allemagne', 'DJI': 'Djibouti', 'DMA': 'Dominique', 'DNK': 'Danemark', 'DOM': 'République dominicaine', 'DZA': 'Algérie', 'ECU': 'Equateur', 'EGY': 'Egypte', 'ERI': 'Erythrée', 'ESH': 'Sahara occidental', 'ESP': 'Espagne', 'EST': 'Estonie', 'ETH': 'Ethiopie', 'FIN': 'Finlande', 'FJI': 'Fidji', 'FLK': 'Îles Malouines', 'FRA': 'France', 'FRO': 'Féroé', 'FSM': 'Micronésie', 'GAB': 'Gabon', 'GBR': 'Royaume-Uni', 'GEO': 'Géorgie', 'GGY': 'Guernesey', 'GHA': 'Ghana', 'GIB': 'Gibraltar', 'GIN': 'Guinée', 'GLP': 'Guadeloupe', 'GMB': 'Gambie', 'GNB': 'Guinée-Bissau', 'GNQ': 'Guinée équatoriale', 'GRC': 'Grèce', 'GRD': 'Grenade', 'GRL': 'Groenland', 'GTM': 'Guatemala', 'GUF': 'Guyane', 'GUM': 'Guam', 'GUY': 'Guyana', 'HKG': 'Hong Kong', 'HND': 'Honduras', 'HRV': 'Croatie', 'HTI': 'Haïti', 'HUN': 'Hongrie', 'IDN': 'Indonésie', 'IMN': 'Île de Man', 'IND': 'Inde', 'IOT': "Territoire britannique de l'océan Indien", 'IRL': 'Irlande', 'IRN': 'Irak', 'IRQ': 'Iran', 'ISL': 'Islande', 'ISR': 'Israël', 'ITA': 'Italie', 'JAM': 'Jamaïque', 'JEY': 'Jersey', 'JOR': 'Jordanie', 'JPN': 'Japon', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya', 'KGZ': 'Kirghizistan', 'KHM': 'Cambodge', 'KIR': 'Kiribati', 'KNA': 'Saint-Christophe-et-Niévès', 'KOR': 'Corée du Sud', 'KWT': 'Koweït', 'LAO': 'Laos', 'LBN': 'Liban', 'LBR': 'Liberia', 'LBY': 'Libye', 'LCA': 'Sainte-Lucie', 'LIE': 'Liechtenstein', 'LKA': 'Sri Lanka', 'LSO': 'Lesotho', 'LTU': 'Lituanie', 'LUX': 'Luxembourg', 'LVA': 'Lettonie', 'MAC': 'Macao', 'MAF': 'Sint-Maarten', 'MAR': 'Maroc', 'MCO': 'Monaco', 'MDA': 'Moldavie', 'MDG': 'Madagascar', 'MDV': 'Maldives', 'MEX': 'Mexique', 'MHL': 'Marshall', 'MKD': 'Macedoine', 'MLI': 'Mali', 'MLT': 'Malte', 'MMR': 'Birmanie', 'MNE': 'Monténégro', 'MNG': 'Mongolie', 'MNP': 'Îles Mariannes du Nord', 'MOZ': 'Mozambique', 'MRT': 'Mauritanie', 'MSR': 'Montserrat', 'MTQ': 'Martinique', 'MUS': 'Maurice', 'MWI': 'Malawi', 'MYS': 'Malaisie', 'MYT': 'Mayotte', 'NAM': 'Namibie', 'NCL': 'Nouvelle-Calédonie', 'NER': 'Niger', 'NFK': 'Île Norfolk', 'NGA': 'Nigeria', 'NIC': 'Nicaragua', 'NIU': 'Niue', 'NLD': 'Pays-Bas', 'NOR': 'Norvège', 'NPL': 'Nepal', 'NRU': 'Nauru', 'NZL': 'Nouvelle-Zélande', 'OMN': 'Oman', 'PAK': 'Pakistan', 'PAN': 'Panama', 'PCN': 'Îles Pitcairn', 'PER': 'Pérou', 'PHL': 'Philippines', 'PLW': 'Palaos', 'PNG': 'Papouasie-Nouvelle-Guinée', 'POL': 'Pologne', 'PRI': 'Porto Rico', 'PRK': 'Corée du Nord', 'PRT': 'Portugal', 'PRY': 'Paraguay', 'PSE': 'Palestine', 'PYF': 'Polynésie française', 'QAT': 'Qatar', 'REU': 'Réunion', 'ROU': 'Roumanie', 'RUS': 'Russie', 'RWA': 'Rwanda', 'SAU': 'Arabie saoudite', 'SDN': 'Soudan', 'SEN': 'Sénégal', 'SGP': 'Singapour', 'SGS': 'Georgie du Sud-et-les iles Sandwich du Sud', 'SHN': 'Sainte-Hélène, Ascension et Tristan da Cunha', 'SJM': 'Svalbard et île Jan Mayen', 'SLB': 'Salomon', 'SLE': 'Sierra Leone', 'SLV': 'Salvador', 'SMR': 'Saint-Marin', 'SOM': 'Somalie', 'SPM': 'Saint-Pierre-et-Miquelon', 'SRB': 'Serbie', 'SSD': 'Soudan du Sud', 'STP': 'Sao Tomé-et-Principe', 'SUR': 'Suriname', 'SVK': 'Slovaquie', 'SVN': 'Slovénie', 'SWE': 'Suède', 'SWZ': 'eSwatani', 'SXM': 'Saint-Martin ', 'SYC': 'Seychelles', 'SYR': 'Syrie', 'TCA': 'Îles Turques-et-Caïques', 'TCD': 'Tchad', 'TGO': 'Togo', 'THA': 'Thaïlande', 'TJK': 'Tadjikistan', 'TKL': 'Tokelau', 'TKM': 'Turkmenistan', 'TLS': 'Timor oriental', 'TON': 'Tonga', 'TTO': 'Trinité-et-Tobago', 'TUN': 'Tunisie', 'TUR': 'Turquie', 'TUV': 'Tuvalu', 'TWN': 'Taiwan', 'TZA': 'Tanzanie', 'UGA': 'Ouganda', 'UKR': 'Ukraine', 'URY': 'Uruguay', 'USA': 'Etats-Unis', 'UZB': 'Ouzbékistan', 'VAT': 'Saint-Siège (État de la Cité du Vatican)', 'VCT': 'Saint-Vincent-et-les-Grenadines', 'VEN': 'Venezuela', 'VGB': 'Îles Vierges britanniques', 'VIR': 'Îles Vierges des États-Unis', 'VNM': 'Viêt Nam', 'VUT': 'Vanuatu', 'WLF': 'Wallis-et-Futuna', 'WSM': 'Samoa', 'XKX': 'Kosovo', 'YEM': 'Yémen', 'ZAF': 'Afrique du Sud', 'ZMB': 'Zambie', 'ZWE': 'Zimbabwe', 'NTZ': 'Zone neutre', 'UNO': 'Fonctionnaire des Nations Unies', 'UNA': "Fonctionnaire d'une organisation affiliée aux Nations Unies", 'UNK': 'Représentant des Nations Unies au Kosovo', 'XXA': 'Apatride Convention 1954', 'XXB': 'Réfugié Convention 1954', 'XXC': 'Réfugié autre', 'XXX': 'Résident Légal de Nationalité Inconnue', 'D': 'Allemagne' , 'EUE': 'Union Européenne', 'GBD': "Citoyen Britannique d'Outre-mer (BOTC)", 'GBN': 'British National (Overseas)', 'GBO': 'British Overseas Citizen', 'GBP': 'British Protected Person', 'GBS': 'British Subject', 'XBA': 'Banque Africaine de Développement', "XIM": "Banque Africaine d'Export–Import", 'XCC': 'Caribbean Community or one of its emissaries', 'XCO': 'Common Market for Eastern and Southern Africa', 'XEC': 'Economic Community of West African States', 'XPO' : 'International Criminal Police Organization', 'XOM': 'Sovereign Military Order of Malta', 'RKS': 'Kosovo', 'WSA' : 'World Service Authority World Passport'}
    
    #Passeport
    P =   ["11222333333333333333333333333333333333333333|444444444566677777789AAAAAABCCCCCCCCCCCCCCDE" , {  
                                                                                                                     "1" : "2|CODE|P*"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "39|NOM|&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
                                                                                                                     "4" : "9|NO|*********",
                                                                                                                     "5" : "1|CTRL|4",
                                                                                                                     "6" : "3|NAT|AAA",
                                                                                                                     "7" : "6|BDATE|000000",
                                                                                                                     "8" : "1|CTRL|7",
                                                                                                                     "9" : "1|SEX|A",
                                                                                                                     "A" : "6|EDATE|000000",
                                                                                                                     "B" : "1|CTRL|A",
                                                                                                                     "C" : "14|FACULT|**************",
                                                                                                                     "D" : "1|CTRLF|C",
                                                                                                                     "E" : "1|CTRL|4578ABCD" 
                                                                                                                                                                                
                                                                                                                                                                                }, "Passeport"]
    #Carte passeport
    IP     =   ["112223333333334555555555555555|66666678999999ABBBCCCCCCCCCCCD" , {  
                                                                                                                     "1" : "2|CODE|IP"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "9|NO|*********",
                                                                                                                     "4" : "1|CTRL|3",
                                                                                                                     "5" : "15|FACULT|***************",
                                                                                                                     "6" : "6|BDATE|000000",
                                                                                                                     "7" : "1|CTRL|6",
                                                                                                                     "8" : "1|SEX|A",
                                                                                                                     "9" : "6|EDATE|000000",
                                                                                                                     "A" : "1|CTRL|9",
                                                                                                                     "B" : "3|NAT|AAA",
                                                                                                                     "C" : "11|FACULT|***********",
                                                                                                                     "D" : "1|CTRL|345679AC"
                                                                                                                                                                                }, "Carte-passeport"]
    #ID dv1
    I_     =   ["112223333333334555555555555555|66666678999999ABBBCCCCCCCCCCCD" , {  
                                                                                                                     "1" : "2|CODE|I*"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "9|NO|*********",
                                                                                                                     "4" : "1|CTRL|3",
                                                                                                                     "5" : "15|FACULT|***************",
                                                                                                                     "6" : "6|BDATE|000000",
                                                                                                                     "7" : "1|CTRL|6",
                                                                                                                     "8" : "1|SEX|A",
                                                                                                                     "9" : "6|EDATE|000000",
                                                                                                                     "A" : "1|CTRL|9",
                                                                                                                     "B" : "3|NAT|AAA",
                                                                                                                     "C" : "11|FACULT|***********",
                                                                                                                     "D" : "1|CTRL|345679AC"
                                                                                                                                                                             }, "Titre d'identité/de voyage"]
     #Certificat de membre dequipaj  
    AC     =   ["112223333333334EEE555555555555|66666678999999ABBBCCCCCCCCCCCD" , {  
                                                                                                                     "1" : "2|CODE|AC"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "9|NO|*********",
                                                                                                                     "4" : "1|CTRL|3",
                                                                                                                     "5" : "15|FACULT|***************",
                                                                                                                     "6" : "6|BDATE|000000",
                                                                                                                     "7" : "1|CTRL|6",
                                                                                                                     "8" : "1|SEX|A",
                                                                                                                     "9" : "6|EDATE|000000",
                                                                                                                     "A" : "1|CTRL|9",
                                                                                                                     "B" : "3|NAT|AAA",
                                                                                                                     "C" : "11|FACULT|***********",
                                                                                                                     "D" : "1|CTRL|345679AC",
                                                                                                                     "E" : "3|INDIC|AA&" #ATTENTION : Doc 8585 (3 lettres) + Airline  Coding  Directory de  l’IATA
                                                                                                                                                                                }, "Certificat de membre d'équipage"]                                                                                                                                                                            
                                                                                                                                                                                
    #Visa de type A
    VA     =   ["11222333333333333333333333333333333333333333|444444444566677777789AAAAAABCCCCCCCCCCCCCCDE" , {  
                                                                                                                     "1" : "2|CODE|V*"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "39|NOM|&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
                                                                                                                     "4" : "9|NO|*********",
                                                                                                                     "5" : "1|CTRL|4",
                                                                                                                     "6" : "3|NAT|AAA",
                                                                                                                     "7" : "6|BDATE|000000",
                                                                                                                     "8" : "1|CTRL|7",
                                                                                                                     "9" : "1|SEX|A",
                                                                                                                     "A" : "6|EDATE|000000",
                                                                                                                     "B" : "1|CTRL|A",
                                                                                                                     "C" : "14|FACULT|**************",
                                                                                                                     
                                                                                                                                                                                }, "Visa de type A"]
    #Visa de type B
    VB     =   ["112223333333333333333333333333333333|444444444566677777789AAAAAABCCCCCC" , {  
                                                                                                                     "1" : "2|CODE|V*"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "31|NOM|&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
                                                                                                                     "4" : "9|NO|*********",
                                                                                                                     "5" : "1|CTRL|4",
                                                                                                                     "6" : "3|NAT|AAA",
                                                                                                                     "7" : "6|BDATE|000000",
                                                                                                                     "8" : "1|CTRL|7",
                                                                                                                     "9" : "1|SEX|A",
                                                                                                                     "A" : "6|EDATE|000000",
                                                                                                                     "B" : "1|CTRL|A",
                                                                                                                     "C" : "8|FACULT|********"
                                                                                                                     
                                                                                                                     
                                                                                                                                                                                }, "Visa de type B"]
    #ID dv2
    I__     =   ["112223333333333333333333333333333333|444444444566677777789AAAAAABCCCCCCCD" , {  
                                                                                                                     "1" : "2|CODE|I*"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "31|NOM|&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
                                                                                                                     "4" : "9|NO|*********",
                                                                                                                     "5" : "1|CTRL|4",
                                                                                                                     "6" : "3|NAT|AAA",
                                                                                                                     "7" : "6|BDATE|000000",
                                                                                                                     "8" : "1|CTRL|7",
                                                                                                                     "9" : "1|SEX|A",
                                                                                                                     "A" : "6|EDATE|000000",
                                                                                                                     "B" : "1|CTRL|A",
                                                                                                                     "C" : "7|FACULT|*******",
                                                                                                                     "D" : "1|CTRL|4578ABC"
                                                                                                                                                                                }, "Pièce d'identité/de voyage"]
    #ID2
    ID      =   ["112223333333333333333333333333444444|555566677777899999999999999AAAAAABCD" , {  
                                                                                                                     "1" : "2|CODE|ID"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "25|NOM|&&&&&&&&&&&&&&&&&&&&&&&&&",
                                                                                                                     "4" : "6|NOINT|000***", #000 pour le département avec prefixe 0 et poste agent ***
                                                                                                                     "5" : "4|DDATE|0000", #AAMM 
                                                                                                                     "6" : "3|NOINT2|000", #departement et pref
                                                                                                                     "7" : "5|NOINT3|00000", #No arbitraire
                                                                                                                     "8" : "1|CTRL|567",
                                                                                                                     "9" : "14|PRENOM|A",
                                                                                                                     "A" : "6|BDATE|000000",
                                                                                                                     "B" : "1|CTRL|A",
                                                                                                                     "C" : "1|SEX|A",
                                                                                                                     "D" : "1|CTRL|123456789ABC"
                                                                                                                                                                                },"Pièce d'identité FR"]                                                                                                                                                                    
    DL      =   ["112223333333334555555666666667|" , {  
                                                                                                                     "1" : "2|CODE|D1"      ,
                                                                                                                     "2" : "3|PAYS|AAA"     , 
                                                                                                                     "3" : "9|NO|00AA00000",
                                                                                                                     "4" : "1|CTRL|123", 
                                                                                                                     "5" : "6|EDATE|000000", 
                                                                                                                     "6" : "8|NOM|&&&&&&&&", 
                                                                                                                     "7" : "1|CTRL|123456",
                                                                                                                     
                                                                                                                                                                                },"Permis de conduire"]                                                                                                                                                                            
    
    
    TYPES = [ ID, I__, VB, VA, AC, I_, IP, P, DL ]                                                  
    
    
    
    
class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class Download: #Gestionnaire de DL
    
    def __init__(self, url, localfile, namefile, opener, p, canvas, message, logger): #p is the progress bar, canvas and message are using to display text
        
        from socket import timeout
        
        self.retry = 6
        self.logger = logger
        self.opener = opener
        self.url = url
        self.localfile = localfile
        self.success = False
        self.time = 5
        
        self.count = 0 # Counts downloaded size.
        self.success = False
        self.downloading = True
        
        self.logger.error("[Download() class] : " + "Initialization ok")
         
        while (not(self.success) and self.downloading):
            try:
                self.Err = ""
                self._netfile = self.opener.open(self.url, timeout=self.time)
                self.filesize = float(self._netfile.info()['Content-Length'])
        
                if (os.path.exists(self.localfile) and os.path.isfile(self.localfile)):
                    self.count = os.path.getsize(self.localfile)
               
                if self.count >= self.filesize:
                    #already downloaded
                    self.downloading = False
                    self.success = True
                    self._netfile.close()
                    return
        
                if (os.path.exists(self.localfile) and os.path.isfile(self.localfile)):
                    #File already exists, start where it left off:
                    self._netfile.close()
                    req = urllib2.Request(self.url)
                   
                    req.add_header("Range","bytes=%s-" % (self.count))
                    self._netfile = self.opener.open(req, timeout=self.time)
                
                if (self.downloading): #Don't do it if cancelled, downloading=false.
                    self._outfile = open(self.localfile,"ab") #to append binary
                    
                    next = self._netfile.read(1024)
                    p.stop()
                    p.configure(mode = "determinate", value = 0, maximum = 100)
                    while (len(next)>0 and self.downloading):
                        self._outfile.write(next)
                        self.count += len(next)
                        next = self._netfile.read(1024)
                        
                        Percent = int(((self.count)/self.filesize*100))
                        p.configure(mode = "determinate", value = int(Percent))
                        canvas.itemconfigure(message, text="Téléchargement de " + str(namefile) + " de taille " + str(int(self.filesize/1024/1024)) + " Mo : " + str(Percent) + " %")
                        
                    self._netfile.close()
                    self._outfile.close()
                    self.success = True
                    
            except urllib2.HTTPError as e:
                
                self.logger.error("[Download() class] : " + "HTTP ERROR " + str(e.code))
                
                try:
                    self._netfile.close()
                    self._outfile.close()
                except Exception as err:
                    self.logger.critical("[Download() class] : " + "FILE I/O ERROR : " + str(err))
                
                self.retry += -1
                canvas.itemconfigure(message, text="Erreur HTTP " + str(e.code) +". Nouvelles tentatives : " +str(self.retry))
                
                if self.retry <= 0:
                    self.downloading = False
                    
            except timeout as e:
                
                self.logger.error("[Download() class] : " + "TIMEOUT ERROR : " + str(e))
                try:
                    self._netfile.close()
                    self._outfile.close()
                except Exception as err:
                    self.logger.critical("[Download() class] : " + "FILE I/O ERROR : " + str(err))    
                
                self.retry += -1
                self.time *= 2
                canvas.itemconfigure(message, text="Connexion expirée. Nouvelles tentatives : " + str(self.retry) + ", " + str(self.time) + " s")
                
                if self.retry <= 0:
                    self.downloading = False
                    
                    
            except IOError as e:
               
                self.logger.error("[Download() class] : " + "I/O ERROR :" + str(e))
                try:
                    self._netfile.close()
                    self._outfile.close()
                except Exception as err:
                    self.logger.critical("[Download() class] : " + "FILE I/O ERROR : " + str(err))
                
                self.retry += -1
                self.time *= 2
                canvas.itemconfigure(message, text="Connexion expirée. Nouvelles tentatives : " + str(self.retry) + ", " + str(self.time) + " s")
                
                if self.retry <= 0:
                    self.downloading = False
                    
            except Exception as e:
                
                self.logger.error("[Download() class] : " + "UNKNOWN ERROR : " + str(e))
                
                try:
                    self._netfile.close()
                    self._outfile.close()
                except Exception as err:
                    self.logger.critical("[Download() class] : " + "FILE I/O ERROR : " + str(err))  
                
                self.retry += -1
                canvas.itemconfigure(message, text="Erreur inconnue. Nouvelles tentatives : " + str(self.retry))
                
                if self.retry <= 0:
                    self.downloading = False
            

class AutoScrollbar(ttk.Scrollbar):
    """ A scrollbar that hides itself if it's not needed. Works only for grid geometry manager """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        raise TclError('Cannot use place with the widget ' + self.__class__.__name__)

class CanvasImage:
    """ Display and zoom image """
    def __init__(self, placeholder, file, type):
        """ Initialize the ImageFrame """
        self.type = type #1 for multipage, 0 for normal
        self.angle = 0
        self.imscale = 1.0  # scale for the canvas image zoom, public for outer classes
        self.__delta = 1.3  # zoom magnitude
        self.__filter = Image.ANTIALIAS  # could be: NEAREST, BILINEAR, BICUBIC and ANTIALIAS
        self.__previous_state = 0  # previous state of the keyboard
        self.path = file  # path to the image, should be public for outer classes
        # Create ImageFrame in placeholder widget
        self.__imframe = ttk.Frame(placeholder)
        self.placeholder = placeholder  # placeholder of the ImageFrame object
        # Vertical and horizontal scrollbars for canvas
        hbar = AutoScrollbar(self.__imframe, orient='horizontal')
        vbar = AutoScrollbar(self.__imframe, orient='vertical')
        hbar.grid(row=1, column=0, sticky='we')
        vbar.grid(row=0, column=1, sticky='ns')
        # Create canvas and bind it with scrollbars. Public for outer classes
        self.canvas = Canvas(self.__imframe, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        hbar.configure(command=self.__scroll_x)  # bind scrollbars to the canvas
        vbar.configure(command=self.__scroll_y)
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda event: self.__show_image())  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.__move_from)  # remember canvas position
        self.canvas.bind('<B1-Motion>',     self.__move_to)  # move canvas to the new position
        self.canvas.bind('<MouseWheel>', self.__wheel)  # zoom 
        # Decide if this image huge or not
        self.__huge = False  # huge or not
        self.__huge_size = 14000  # define size of the huge image
        self.__band_width = 1024  # width of the tile band
        Image.MAX_IMAGE_PIXELS = 1000000000  # suppress DecompressionBombError for the big image
        with warnings.catch_warnings():  # suppress DecompressionBombWarning
            warnings.simplefilter('ignore')
            self.__image = Image.open(self.path)  # open image, but down't load it
        self.imwidth, self.imheight = self.__image.size  # public for outer classes
        if self.imwidth * self.imheight > self.__huge_size * self.__huge_size and \
           self.__image.tile[0][0] == 'raw':  # only raw images could be tiled
            self.__huge = True  # image is huge
            self.__offset = self.__image.tile[0][2]  # initial tile offset
            self.__tile = [self.__image.tile[0][0],  # it have to be 'raw'
                           [0, 0, self.imwidth, 0],  # tile extent (a rectangle)
                           self.__offset,
                           self.__image.tile[0][3]]  # list of arguments to the decoder
        self.__min_side = min(self.imwidth, self.imheight)  # get the smaller image side
        # Create image pyramid
        self.__pyramid = [self.smaller()] if self.__huge else [Image.open(self.path)]
        # Set ratio coefficient for image pyramid
        self.__ratio = max(self.imwidth, self.imheight) / self.__huge_size if self.__huge else 1.0
        self.__curr_img = 0  # current image from the pyramid
        self.__scale = self.imscale * self.__ratio  # image pyramide scale
        self.__reduction = 2  # reduction degree of image pyramid
        w, h = self.__pyramid[-1].size
        while w > 512 and h > 512:  # top pyramid image is around 512 pixels in size
            w /= self.__reduction  # divide on reduction degree
            h /= self.__reduction  # divide on reduction degree
            try:
                self.__pyramid.append(self.__pyramid[-1].resize((int(w), int(h)), self.__filter))
            except TypeError:
                showerror(title="Erreur de fichier", message="Image incompatible. Merci d'utiliser une autre image ou de la convertir", parent = self.placeholder)
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle((0, 0, self.imwidth, self.imheight), width=0)
        self.__show_image()  # show image on the canvas
        self.canvas.focus_set()  # set focus on the canvas
        
    def rotatem(self):
        self.angle += 1
        self.__show_image()
        
    def rotatep(self):
        self.angle -= 1
        self.__show_image()
        
    def rotatemm(self):
        self.angle += 90
        self.__show_image()
        
    def rotatepp(self):
        self.angle -= 90
        self.__show_image()

    def smaller(self):
        """ Resize image proportionally and return smaller image """
        w1, h1 = float(self.imwidth), float(self.imheight)
        w2, h2 = float(self.__huge_size), float(self.__huge_size)
        aspect_ratio1 = w1 / h1
        aspect_ratio2 = w2 / h2  # it equals to 1.0
        if aspect_ratio1 == aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(h2)))
            k = h2 / h1  # compression ratio
            w = int(w2)  # band length
        elif aspect_ratio1 > aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(w2 / aspect_ratio1)))
            k = h2 / w1  # compression ratio
            w = int(w2)  # band length
        else:  # aspect_ratio1 < aspect_ration2
            image = Image.new('RGB', (int(h2 * aspect_ratio1), int(h2)))
            k = h2 / h1  # compression ratio
            w = int(h2 * aspect_ratio1)  # band length
        i, j, n = 0, 1, round(0.5 + self.imheight / self.__band_width)
        while i < self.imheight:
            
            band = min(self.__band_width, self.imheight - i)  # width of the tile band
            self.__tile[1][3] = band  # set band width
            self.__tile[2] = self.__offset + self.imwidth * i * 3  # tile offset (3 bytes per pixel)
            self.__image.close()
            self.__image = Image.open(self.path)  # reopen / reset image
            self.__image.size = (self.imwidth, band)  # set size of the tile band
            self.__image.tile = [self.__tile]  # set tile
            cropped = self.__image.crop((0, 0, self.imwidth, band))  # crop tile band
            image.paste(cropped.resize((w, int(band * k)+1), self.__filter), (0, int(i * k)))
            i += band
            j += 1
        
        return image

    def redraw_figures(self):
        """ Dummy function to redraw figures in the children classes """
        pass

    def grid(self, **kw):
        """ Put CanvasImage widget on the parent widget """
        self.__imframe.grid(**kw)  # place CanvasImage widget on the grid
        self.__imframe.grid(sticky='nswe')  # make frame container sticky
        self.__imframe.rowconfigure(0, weight=1)  # make canvas expandable
        self.__imframe.columnconfigure(0, weight=1)

    # noinspection PyUnusedLocal
    def __scroll_x(self, *args, **kwargs):
        """ Scroll canvas horizontally and redraw the image """
        self.canvas.xview(*args)  # scroll horizontally
        self.__show_image()  # redraw the image

    # noinspection PyUnusedLocal
    def __scroll_y(self, *args, **kwargs):
        """ Scroll canvas vertically and redraw the image """
        self.canvas.yview(*args)  # scroll vertically
        self.__show_image()  # redraw the image

    def __show_image(self):
        """ Show image on the Canvas. Implements correct image zoom almost like in Google Maps """
        box_image = self.canvas.coords(self.container)  # get image area
        box_canvas = (self.canvas.canvasx(0),  # get visible area of the canvas
                      self.canvas.canvasy(0),
                      self.canvas.canvasx(self.canvas.winfo_width()),
                      self.canvas.canvasy(self.canvas.winfo_height()))
        box_img_int = tuple(map(int, box_image))  # convert to integer or it will not work properly
        # Get scroll region box
        box_scroll = [min(box_img_int[0], box_canvas[0]), min(box_img_int[1], box_canvas[1]),
                      max(box_img_int[2], box_canvas[2]), max(box_img_int[3], box_canvas[3])]
        # Horizontal part of the image is in the visible area
        if  box_scroll[0] == box_canvas[0] and box_scroll[2] == box_canvas[2]:
            box_scroll[0]  = box_img_int[0]
            box_scroll[2]  = box_img_int[2]
        # Vertical part of the image is in the visible area
        if  box_scroll[1] == box_canvas[1] and box_scroll[3] == box_canvas[3]:
            box_scroll[1]  = box_img_int[1]
            box_scroll[3]  = box_img_int[3]
        # Convert scroll region to tuple and to integer
        self.canvas.configure(scrollregion=tuple(map(int, box_scroll)))  # set scroll region
        x1 = max(box_canvas[0] - box_image[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(box_canvas[1] - box_image[1], 0)
        x2 = min(box_canvas[2], box_image[2]) - box_image[0]
        y2 = min(box_canvas[3], box_image[3]) - box_image[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            if self.__huge and self.__curr_img < 0:  # show huge image
                h = int((y2 - y1) / self.imscale)  # height of the tile band
                self.__tile[1][3] = h  # set the tile band height
                self.__tile[2] = self.__offset + self.imwidth * int(y1 / self.imscale) * 3
                self.__image.close()
                self.__image = Image.open(self.path)  # reopen / reset image
                self.__image.size = (self.imwidth, h)  # set size of the tile band
                self.__image.tile = [self.__tile]
                image = self.__image.crop((int(x1 / self.imscale), 0, int(x2 / self.imscale), h))
            else:  # show normal image
                image = self.__pyramid[max(0, self.__curr_img)].crop(  # crop current img from pyramid
                                    (int(x1 / self.__scale), int(y1 / self.__scale),
                                     int(x2 / self.__scale), int(y2 / self.__scale)))
            #
            
            self.resizedim = image.resize((int(x2 - x1), int(y2 - y1)), self.__filter).rotate(self.angle, expand = 1)
            imagetk = ImageTk.PhotoImage(self.resizedim, master = self.placeholder)
            imageid = self.canvas.create_image(max(box_canvas[0], box_img_int[0]),
                                               max(box_canvas[1], box_img_int[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def __move_from(self, event):
        """ Remember previous coordinates for scrolling with the mouse """
        self.canvas.scan_mark(event.x, event.y)

    def __move_to(self, event):
        """ Drag (move) canvas to the new position """
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.__show_image()  # zoom tile and show it on the canvas

    def outside(self, x, y):
        """ Checks if the point (x,y) is outside the image area """
        bbox = self.canvas.coords(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            return False  # point (x,y) is inside the image area
        else:
            return True  # point (x,y) is outside the image area

    def __wheel(self, event):
        """ Zoom with mouse wheel """
        x = self.canvas.canvasx(event.x)  # get coordinates of the event on the canvas
        y = self.canvas.canvasy(event.y)
        if self.outside(x, y): return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.delta == -120:  # scroll down, smaller
            if round(self.__min_side * self.imscale) < int(self.placeholder.winfo_screenheight()): return  # image is less than the number of window pixels
            self.imscale /= self.__delta
            scale        /= self.__delta
        if event.delta == 120:  # scroll up, bigger
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height()) >> 1
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.__delta
            scale        *= self.__delta
        # Take appropriate image from the pyramid
        k = self.imscale * self.__ratio  # temporary coefficient
        self.__curr_img = min((-1) * int(math.log(k, self.__reduction)), len(self.__pyramid) - 1)
        self.__scale = k * math.pow(self.__reduction, max(0, self.__curr_img))
        #
        self.canvas.scale('all', x, y, scale, scale)  # rescale all objects
        # Redraw some figures before showing image on the screen
        self.redraw_figures()  # method for child classes
        self.__show_image()

    def crop(self, bbox):
        """ Crop rectangle from the image and return it """
        if self.__huge:  # image is huge and not totally in RAM
            band = bbox[3] - bbox[1]  # width of the tile band
            self.__tile[1][3] = band  # set the tile height
            self.__tile[2] = self.__offset + self.imwidth * bbox[1] * 3  # set offset of the band
            self.__image.close()
            self.__image = Image.open(self.path)  # reopen / reset image
            self.__image.size = (self.imwidth, band)  # set size of the tile band
            self.__image.tile = [self.__tile]
            return self.__image.crop((bbox[0], 0, bbox[2], band))
        else:  # image is totally in RAM
            return self.__pyramid[0].crop(bbox)

    def destroy(self):
        """ ImageFrame destructor """
        self.__image.close()
        map(lambda i: i.close, self.__pyramid)  # close all pyramid images
        del self.__pyramid[:]  # delete pyramid list
        del self.__pyramid  # delete pyramid variable
        self.canvas.destroy()
       

class OpenScan(ttk.Frame):
    """ Main window class """
    def __init__(self, mainframe, fileorig, type, nframe = 1, pagenum = 0, file = None):
        """ Initialize the main Frame """
        if file == None : file = fileorig
        self.file = file
        self.fileorig = fileorig
        self.nframe = nframe
        self.pagenum = pagenum
        self.parent = mainframe.parent
        ttk.Frame.__init__(self, master=mainframe)
        
        self.master.title('Ouvrir un scan... (Utilisez la roulette pour zoomer, clic gauche pour déplacer et clic droit pour sélectionner la MRZ)')
        
        self.master.resizable(width=False, height=False)
        hs = self.winfo_screenheight()
                
        w = int(self.winfo_screenheight()/1.5)  # width for the Tk root
        h = int(self.winfo_screenheight()/2)    # height for the Tk root
        
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
                
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        if getattr( sys, 'frozen', False ) :
            self.master.iconbitmap(sys._MEIPASS + "\id-card.ico\id-card.ico")
        else:
            self.master.iconbitmap("id-card.ico")  
        self.master.rowconfigure(0, weight=1)  
        self.master.columnconfigure(0, weight=1)
        self.cadre = CanvasImage(self.master, self.file, type)  
        self.cadre.grid(row=0, column=0)
        
        self.master.menubar = Menu(self.master)
        if type==1 : self.master.menubar.add_command(label="Page précédente", command= self.pagep)
        self.master.menubar.add_command(label="Pivoter -90°", command= self.cadre.rotatemm)
        self.master.menubar.add_command(label="Pivoter -1°", command= self.cadre.rotatem)
        self.master.menubar.add_command(label="Pivoter +1°", command= self.cadre.rotatep)
        self.master.menubar.add_command(label="Pivoter +90°", command= self.cadre.rotatepp)
        if type==1 : self.master.menubar.add_command(label="Page suivante", command= self.pages) 
        
        self.master.config(menu=self.master.menubar)
        
        self.cadre.canvas.bind('<ButtonPress-3>', self.motionprep)
        self.cadre.canvas.bind('<B3-Motion>', self.motionize)
        self.cadre.canvas.bind('<ButtonRelease-3>', self.motionend)
        
    def pages(self):
        
        if self.pagenum +1 < self.nframe:
            # self.destroy()
            im = Image.open(self.fileorig)
            im.seek(self.pagenum +1)
            newpath = CST_FOLDER + '\\temp' + str(random.randint(11111,99999)) +'.tif'
            im.save(newpath)
            im.close()
            self.cadre.destroy()
            self.__init__(self.master, self.fileorig, 1, self.nframe, self.pagenum +1, newpath)
        
    def pagep(self):
        
        if self.pagenum - 1 >= 0:
            # self.destroy()
            im = Image.open(self.fileorig)
            im.seek(self.pagenum - 1)
            newpath = CST_FOLDER + '\\temp' + str(random.randint(11111,99999)) +'.tif'
            im.save(newpath)
            im.close()
            self.cadre.destroy()
            self.__init__(self.master, self.fileorig, 1, self.nframe, self.pagenum -1, newpath)
        
    def motionprep(self,event):
        
        if hasattr(self,"rect"):
            
            self.begx = event.x
            self.begy = event.y
            
            
            self.ix = self.cadre.canvas.canvasx(event.x)
            self.iy = self.cadre.canvas.canvasy(event.y)
            
            self.cadre.canvas.coords(self.rect, self.cadre.canvas.canvasx(event.x), self.cadre.canvas.canvasy(event.y),self.ix,self.iy)
            
        else:
            self.begx = event.x
            self.begy = event.y
            
            self.ix = self.cadre.canvas.canvasx(event.x)
            self.iy = self.cadre.canvas.canvasy(event.y)
            self.rect = self.cadre.canvas.create_rectangle(self.cadre.canvas.canvasx(event.x), self.cadre.canvas.canvasy(event.y),self.ix,self.iy, outline='red')
        
    def motionize(self,event):
        
        event.x
        event.y
        
        self.cadre.canvas.coords(self.rect, self.ix,self.iy,self.cadre.canvas.canvasx(event.x),self.cadre.canvas.canvasy(event.y)) 
        
    def motionend(self,event):
        
        self.endx = event.x
        self.endy = event.y
       
        
        self.imtotreat = self.cadre.resizedim.crop((min(self.begx,self.endx), min(self.begy, self.endy), max(self.endx, self.begx), max(self.endy, self.begy)))
        
        im = self.imtotreat
        
        import CNI_pytesseract as pytesseract
            
        try:
            os.environ["PATH"] = CST_FOLDER + "\\Tesseract-OCR4\\" 
            os.environ["TESSDATA_PREFIX"] = CST_FOLDER + "\\Tesseract-OCR4\\tessdata"
            self.text = pytesseract.image_to_string(im, lang="ocrb",boxes=False,config="--psm 6 --oem 0 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890<")
            
            
        except pytesseract.TesseractNotFoundError as e:
            
            try:
                os.remove(CST_FOLDER + "\\Tesseract-OCR4\\*.*")
            except Exception:
                pass
                
            showerror("Erreur de module OCR", "Le module OCR localisé en " + str(os.environ["PATH"]) + "est introuvable. Il sera réinstallé à la prochaine exécution", parent = self)
            
        
        except pytesseract.TesseractError as e:
            
            pass
        
        self.master.success = False
        dialogconf = OpenScanDialog(self.master, self.text)
        dialogconf.transient(self)
        dialogconf.grab_set()
        self.wait_window(dialogconf)
        
        if self.master.success:
            self.master.destroy()
        
        
        
class OpenScanWin(Toplevel):
    
    def __init__(self, parent, file, type, nframe = 1):
        
        super().__init__(parent)
        self.parent = parent
        app = OpenScan(self, file, type, nframe)
        
class OpenScanDialog(Toplevel):
    
    def __init__(self, parent, text):
        
        super().__init__(parent)
        self.parent = parent
        
        self.title('Validation de la MRZ détectée')
        
        self.resizable(width=False, height=False)
        self.termtext = Text(self, state='normal', width=45, height=2, wrap='none', font = "Terminal 17", fg = "#121f38")
        self.termtext.grid(column=0,row=0,sticky='NEW', padx=5, pady = 5)
        self.termtext.insert("end", text + "\n")
        
        self.button = Button(self, text="Valider", command=self.valid)
        self.button.grid(column=0,row=1,sticky='S', padx=5, pady = 5)
        
        self.update()
        hs = self.winfo_screenheight()
                
        w = int(self.winfo_width())  # width for the Tk root
        h = int(self.winfo_height())  # height for the Tk root
        
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
                
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        if getattr( sys, 'frozen', False ) :
            self.iconbitmap(sys._MEIPASS + "\id-card.ico\id-card.ico")
        else:
            self.iconbitmap("id-card.ico")
            
    def valid(self):
        
        self.parent.parent.mrzdetected = self.termtext.get('1.0', 'end')
        
        texting = self.parent.parent.mrzdetected.replace(" ","").replace("\r","").split("\n")
        
        for i in range(len(texting)):
            for char in texting[i]:
                if not char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<":
                    showerror("Erreur de validation", "La MRZ soumise contient des caractères invalides", parent = self)
                    self.parent.parent.mrzdetected = ""
                    return
                    
        self.parent.success = True
        
        self.destroy()
        
        
class OpenPageDialog(Toplevel):
    
    def __init__(self, parent, number):
        
        super().__init__(parent)
        self.parent = parent
        
        self.title("Choisir la page à afficher de l'image selectionnée")
        
        self.resizable(width=False, height=False)
        self.termtext = Label(self, text = "Merci de selectionner un numéro de page dans la liste ci-dessous.")
        self.termtext.grid(column=0,row=0,sticky='N', padx=5, pady = 5)
        
        self.combotry = ttk.Combobox(self)
        self.combotry['values'] = tuple(str(x) for x in range(1,number+1) )
        self.combotry.grid(column=0,row=1,sticky='N', padx=5, pady = 5)
        
        self.button = Button(self, text="Valider", command=self.valid)
        self.button.grid(column=0,row=2,sticky='S', padx=5, pady = 5)
        
        self.update()
        hs = self.winfo_screenheight()
                
        w = int(self.winfo_width())  # width for the Tk root
        h = int(self.winfo_height())  # height for the Tk root
        
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
                
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        if getattr( sys, 'frozen', False ) :
            self.iconbitmap(sys._MEIPASS + "\id-card.ico\id-card.ico")
        else:
            self.iconbitmap("id-card.ico")
            
    def valid(self):
        
        self.parent.page = self.combotry.current()
        
        self.destroy()