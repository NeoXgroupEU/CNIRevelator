"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher & updater                                  *
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

from CNI_GLOBALVAR import *
from CNI_classes import *
import hashlib
from pypac import PACSession
from requests.auth import HTTPProxyAuth
import subprocess

def SoftUpdate(logger):
    global ret
    global upwin
    import zipfile
    for f in os.listdir(CST_FOLDER):
        if f[-4:] == '.tif':
            try:
                os.remove(CST_FOLDER + '\\' + f)
            except PermissionError as e:
                logger.info('SoftUpdate() : Failing to purge : ' + str(e))

    logger.info('SoftUpdate() : Looking for older version in dir...')
    list = os.listdir('.')
    for file in list:
        if file.startswith('CNIRevelator_'):
            temp = ['0', '0', '0']
            ver = file[13:].split('.')
            for i in range(len(ver)):
                if ver[i] != 'exe':
                    try:
                        temp[i] = ver[i]
                    except:
                        pass

            ver = temp.copy()
            try:
                sum_ver = int(ver[0]) * 100 + int(ver[1]) * 10 + int(ver[2])
                if sum_ver < CST_SUM_VER:
                    if file[-3:] == 'exe':
                        os.remove(file)
                        logger.info('SoftUpdate() : Removed old version : ' + str(file))
                        CST_CHANGELOG.isOn = True
            except Exception as e:
                logger.error('SoftUpdate() : Failing to remove old version ' + str(file) + ' : ' + str(e))

    def updating():

        def updator():
            global ret
            logger.info('[updator() thread] : Welcome !')
            ret = 11
            canvas.itemconfigure(message, text='Recherche de mises-à-jour...')
            p.configure(mode='indeterminate', value=0, maximum=20)
            p.start()
            upwin.update()
            logger.info('[updator() thread] : Looking for updates...')
            try:

                def download(url, filename):
                    global key
                    global login
                    try:
                        logger.info('[download() thread] : Trying getting credentials in the config file')
                        with open(CST_FOLDER + 'conf.ig', 'rb') as (config):
                            AESObj = AESCipher(CST_CRYPTOKEY)
                            try:
                                tempone = AESObj.decrypt(config.read())
                                if tempone != '||':
                                    if tempone.find('||') != -1:
                                        IPN, IPN_PASS = tempone.split('||')[0:2]
                                    else:
                                        raise ValueError('Cryptokey is bad !')
                                else:
                                    IPN = ''
                                    IPN_PASS = ''
                            except Exception as e:
                                raise IOError(str(e))
                            else:
                                logger.info('[download() thread] : Got credentials !')
                        session = PACSession(proxy_auth=(HTTPProxyAuth(IPN, IPN_PASS)))
                        logger.info('[download() thread] : Authenticated to proxy successfully')
                    except IOError as e:
                        logger.error('[download() thread] : False or absent credentials in the config file : ' + str(e))
                        NoConnect = True
                        while NoConnect:

                            class LoginDialog(Toplevel):

                                def __init__(self, parent):
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
                                    upwin.update()
                                    x = ws / 2 - w / 2
                                    y = hs / 2 - h / 2
                                    self.geometry('%dx%d+%d+%d' % (w, h, x, y))

                                def connecti(self):
                                    global key
                                    global login
                                    login = self.entry_login.get().strip()
                                    key = self.entry_pass.get().strip()
                                    self.destroy()

                            session = PACSession()
                            if session.get_pac() == None:
                                IPN = ''
                                IPN_PASS = ''
                                NoConnect = False
                                break
                            canvas.itemconfigure(message, text='En attente de connexion au serveur proxy...')
                            login = ''
                            key = ''
                            result = LoginDialog(upwin)
                            result.transient(upwin)
                            result.grab_set()
                            upwin.wait_window(result)
                            IPN = login
                            IPN_PASS = key
                            session = PACSession(proxy_auth=(HTTPProxyAuth(IPN, IPN_PASS)))
                            Ans = session.get('http://www.google.com')
                            if str(Ans) == '<Response [407]>':
                                canvas.itemconfigure(message, text='Identifiants erronés, accès refusé')
                                logger.info('[download() thread] : 407 Error')
                                time.sleep(1)
                            else:
                                if str(Ans) == '<Response [200]>':
                                    logger.info('[download() thread] : Connection ok !')
                                    NoConnect = False
                                else:
                                    raise IOError()

                        AESObj = AESCipher(CST_CRYPTOKEY)
                        with open(CST_FOLDER + 'conf.ig', 'wb+') as (f):
                            logger.info('[download() thread] : Saving credentials in encrypted config file')
                            f.write(AESObj.encrypt(IPN + '||' + IPN_PASS))

                    if IPN == 'i005316':
                        canvas.itemconfigure(message, text='Bienvenue Thierry !')
                    else:
                        if IPN == 'i020251':
                            canvas.itemconfigure(message, text='Bienvenue Samia !')
                        else:
                            if IPN == 'i018410':
                                canvas.itemconfigure(message, text='Bienvenue Adrien !')
                            else:
                                if IPN == 'i003067':
                                    canvas.itemconfigure(message, text='Bienvenue Remy !')
                                else:
                                    if IPN == 'i018422':
                                        canvas.itemconfigure(message, text='Bienvenue Eloise !')
                    time.sleep(1)
                    try:
                        Prox_us = session.get_pac().find_proxy_for_url(CST_LINK, 'neoxgroup.eu')
                        PROXY_USABLE = Prox_us[6:-1].split(';')[0]
                        proxy_server_url = IPN + ':' + IPN_PASS + '@' + PROXY_USABLE
                        ph = urllib2.ProxyHandler({'http': proxy_server_url})
                        auth = urllib2.ProxyBasicAuthHandler()
                        server = urllib2.build_opener(ph, auth, urllib2.HTTPHandler)
                        urllib2.install_opener(server)
                        logger.info('[download() thread] : Proxy connection initiated successfully')
                    except:
                        logger.info('[download() thread] : Proxy connection not initiated')

                    try:
                        urllib2.urlretrieve(url, filename)
                        return True
                    except Exception as e:
                        logger.error('[download() thread] : HTTP ERROR ')
                        return e

                logger.info('[updator() thread] : Prepare downloading the version recap file...')
                tempfile = CST_FOLDER + 'temp' + str(random.randint(11111, 99999)) + '.cniu'
                isOk = download(CST_LINK + 'cnir.ver', tempfile)
                if not isOk:
                    raise isOk
                urllib2.urlcleanup()
                logger.info('[updator() thread] : Opening version recap file...')
                file_ver = open(tempfile, 'r')
                logger.info('[updator() thread] : Reading version recap file...')
                version = file_ver.read()
                logger.info('[updator() thread] : Closing version recap file...')
                repert = version.split('|')
                file_ver.close()
                logger.info('[updator() thread] : Deleting version recap file...')
                os.remove(tempfile)
                logger.info('[updator() thread] : Parsing informations about version...')
                final_f = 'CNI_file'
                final_ver = ['0', '0', '0']
                final_hash = ''
                for sentence in repert:
                    try:
                        file, hashref = sentence.split(':')
                    except ValueError:
                        pass
                    else:
                        if str.startswith(file, CST_NAME):
                            ver = file.replace(CST_NAME + '_', '').split('.')
                            temp = [
                             '0', '0', '0']
                            for i in range(len(ver)):
                                temp[i] = ver[i]

                            ver = temp.copy()
                            sum_fver = int(final_ver[0]) * 100 + int(final_ver[1]) * 10 + int(final_ver[2])
                            sum_ver = int(ver[0]) * 100 + int(ver[1]) * 10 + int(ver[2])
                            if sum_ver > sum_fver:
                                final_ver = ver.copy()
                                final_f = file
                                final_hash = hashref

                sum_ver = int(final_ver[0]) * 100 + int(final_ver[1]) * 10 + int(final_ver[2])
                if final_f != 'CNI_file':
                    if sum_ver > CST_SUM_VER:
                        logger.info('[updator() thread] : New version of CNIRevelator found !')
                        canvas.itemconfigure(message, text='Mise à jour disponible ! Préparation du téléchargement...')
                        logger.info('[updator() thread] : Preparing download')
                        with open(CST_FOLDER + 'conf.ig', 'rb') as (config):
                            logger.info('[updator() thread] : Reading credentials for proxy in config file...')
                            AESObj = AESCipher(CST_CRYPTOKEY)
                            IPN, IPN_PASS = AESObj.decrypt(config.read()).split('||')[0:2]
                        session = PACSession(proxy_auth=(HTTPProxyAuth(IPN, IPN_PASS)))
                        try:
                            Prox_us = session.get_pac().find_proxy_for_url(CST_LINK, 'neoxgroup.eu')
                            PROXY_USABLE = Prox_us[6:-1].split(';')[0]
                            proxy_server_url = IPN + ':' + IPN_PASS + '@' + PROXY_USABLE
                            ph = urllib2.ProxyHandler({'http': proxy_server_url})
                            auth = urllib2.ProxyBasicAuthHandler()
                            server = urllib2.build_opener(ph, auth, urllib2.HTTPHandler)
                            logger.info('[updator() thread] : Connection to the proxy initiated successfully !')
                        except:
                            canvas.itemconfigure(message, text='Téléchargement en connexion directe...')
                            server = urllib2.build_opener()
                            logger.info('[updator() thread] : Direct connection initiated successfully')

                        logger.info('[updator() thread] : Launching download of ' + final_f)
                        Statut = Download(CST_LINK + final_f, final_f, final_f, server, p, canvas, message, logger)
                        BLOCKSIZE = 65536
                        hasher = hashlib.sha1()
                        try:
                            with open(final_f, 'rb') as (afile):
                                buf = afile.read(BLOCKSIZE)
                                while len(buf) > 0:
                                    hasher.update(buf)
                                    buf = afile.read(BLOCKSIZE)

                            hashcod = hasher.hexdigest()
                            if hashcod != final_hash:
                                Statut.success = False
                                logger.error('[updator() thread] : Hashcode Error :' + final_f)
                                try:
                                    os.remove(final_f)
                                except IOError:
                                    pass

                            else:
                                logger.info('[updator() thread] : Hashcode pass :' + final_f)
                        except FileNotFoundError as e:
                            logger.error('[updator() thread] : File not found  ' + final_f)

                        if Statut.success:
                            try:
                                os.rename(final_f, final_f + '.exe')
                            except IOError:
                                logger.error('[updator() thread] : Unable to rename the file ! Wait 3 sec and retry')
                                time.sleep(3)
                                try:
                                    os.rename(final_f, final_f + '.exe')
                                except IOError:
                                    logger.critical('[updator() thread] : Unable to rename the file !')

                            else:
                                canvas.itemconfigure(message, text='Téléchargement terminé ! Préparation du lancement...')
                                logger.info('[updator() thread] : Download of ' + final_f + 'finished successfully')
                                p.configure(mode='indeterminate', value=0, maximum=20)
                                p.start()
                                time.sleep(1)
                                logger.info('[updator() thread] : Launching ' + final_f)
                                try:
                                    proc = subprocess.Popen((final_f + '.exe'), shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
                                except:
                                    logger.error('[updator() thread] : Unable to start the new version ! Wait 3 sec and retry')
                                    time.sleep(3)
                                    try:
                                        proc = subprocess.Popen((final_f + '.exe'), shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
                                    except Exception as e:
                                        logger.critical('[updator() thread] : Unable to start the new version ! Stopping : ' + str(e))
                                        showerror("Erreur d'appel de procédure distante", 'Le lancement du nouveau programme a échoué, vous devez le lancer manuellement une fois cette fenêtre fermée', parent=upwin)

                                ret = 12
                        else:
                            canvas.itemconfigure(message, text='Echec de la mise à jour : Erreur HTTP. Préparation du lancement...')
                            logger.error('[updator() thread] : Update has failed with HTTP error')
                            time.sleep(1)
                    canvas.itemconfigure(message, text='Logiciel déjà à jour. Préparation du lancement...')
                    logger.info('[updator() thread] : CNIRevelator is up to date !')
                    time.sleep(1)
                    ret = 11
                if os.path.exists(CST_FOLDER + 'Tesseract-OCR4\\tesseract.exe'):
                    os.environ['PATH'] = CST_FOLDER + 'Tesseract-OCR4\\'
                    os.environ['TESSDATA_PREFIX'] = CST_FOLDER + 'Tesseract-OCR4\\tessdata'
                else:
                    final_f = 'tesseract_4'
                    logger.info('[updator() thread] : Downloading tesseract 4 !')
                    canvas.itemconfigure(message, text='Mise à jour du module OCR ! Préparation du téléchargement...')
                    logger.info('[updator() thread] : Preparing download')
                    with open(CST_FOLDER + 'conf.ig', 'rb') as (config):
                        logger.info('[updator() thread] : Reading credentials for proxy in config file...')
                        AESObj = AESCipher(CST_CRYPTOKEY)
                        IPN, IPN_PASS = AESObj.decrypt(config.read()).split('||')[0:2]
                    session = PACSession(proxy_auth=(HTTPProxyAuth(IPN, IPN_PASS)))
                    try:
                        Prox_us = session.get_pac().find_proxy_for_url(CST_LINK, 'neoxgroup.eu')
                        PROXY_USABLE = Prox_us[6:-1].split(';')[0]
                        proxy_server_url = IPN + ':' + IPN_PASS + '@' + PROXY_USABLE
                        ph = urllib2.ProxyHandler({'http': proxy_server_url})
                        auth = urllib2.ProxyBasicAuthHandler()
                        server = urllib2.build_opener(ph, auth, urllib2.HTTPHandler)
                        logger.info('[updator() thread] : Connection to the proxy initiated successfully !')
                    except:
                        canvas.itemconfigure(message, text='Téléchargement en connexion directe...')
                        server = urllib2.build_opener()
                        logger.info('[updator() thread] : Direct connection initiated successfully')

                    logger.info('[updator() thread] : Launching download of ' + final_f)
                    Statut = Download(CST_LINK + final_f, CST_FOLDER + final_f, final_f, server, p, canvas, message, logger)
                    hashcod = ''
                    logger.info('[updator() thread] : Verifying hashcode of  ' + final_f)
                    BLOCKSIZE = 65536
                    hasher = hashlib.sha1()
                    try:
                        with open(CST_FOLDER + final_f, 'rb') as (afile):
                            buf = afile.read(BLOCKSIZE)
                            while len(buf) > 0:
                                hasher.update(buf)
                                buf = afile.read(BLOCKSIZE)

                        hashcod = hasher.hexdigest()
                        if hashcod != CST_TesserHash:
                            Statut.success = False
                            logger.error('[updator() thread] : Hashcode Error : ' + final_f)
                            try:
                                os.remove(CST_FOLDER + final_f)
                            except IOError:
                                pass

                        else:
                            logger.info('[updator() thread] : Hashcode pass : ' + final_f)
                    except FileNotFoundError as e:
                        logger.error('[updator() thread] : File not found  ' + final_f)

                    if Statut.success:
                        canvas.itemconfigure(message, text='Téléchargement terminé ! Installation...')
                        logger.info('[updator() thread] : Download of ' + final_f + 'finished successfully')
                        p.configure(mode='indeterminate', value=0, maximum=20)
                        p.start()
                        try:
                            zip_ref = zipfile.ZipFile(CST_FOLDER + final_f, 'r')
                            zip_ref.extractall(CST_FOLDER)
                            zip_ref.close()
                            os.environ['PATH'] = CST_FOLDER + 'Tesseract-OCR4\\'
                            os.environ['TESSDATA_PREFIX'] = CST_FOLDER + 'Tesseract-OCR4\\tessdata'
                            canvas.itemconfigure(message, text='Installation terminée !')
                        except:
                            logger.error('[updator() thread] : Unable to install the module. Wait and retry')
                            time.sleep(3)
                            try:
                                zip_ref = zipfile.ZipFile(CST_FOLDER + final_f, 'r')
                                zip_ref.extractall(CST_FOLDER)
                                zip_ref.close()
                                os.environ['PATH'] = CST_FOLDER + 'Tesseract-OCR4\\'
                                os.environ['TESSDATA_PREFIX'] = CST_FOLDER + 'Tesseract-OCR4\\tessdata'
                                canvas.itemconfigure(message, text='Installation terminée !')
                            except Exception as e:
                                logger.critical('[updator() thread] : Unable to install the module ! Stopping : ' + str(e))
                                showerror("Erreur d'appel de procédure distante", "L'installation du module OCR a échoué, contactez le développeur.")

                        ret = 11
                    else:
                        logger.critical('[updator() thread] : Unable to download the module ! ')
                        showerror('Erreur de téléchargement', "L'installation du module OCR a échoué, merci d'indiquer le chemin d'accès au fichier tesseract_4 dans la fenêtre suivante")
                        path = filedialog.askopenfilename(title="Indiquez le chemin d'accès à tesseract_4...", filetypes=(('Tesseract_4', '*.cni4'),
                                                                                                                          ('Tesseract_4', '*.cni4')))
                        if path != '':
                            try:
                                canvas.itemconfigure(message, text='Installation...')
                                zip_ref = zipfile.ZipFile(path, 'r')
                                zip_ref.extractall(CST_FOLDER)
                                zip_ref.close()
                                logger.error('[updator() thread] : Manual installation successed')
                                canvas.itemconfigure(message, text='Installation terminée !')
                                os.environ['PATH'] = CST_FOLDER + 'Tesseract-OCR4\\'
                                os.environ['TESSDATA_PREFIX'] = CST_FOLDER + 'Tesseract-OCR4\\tessdata'
                            except Exception as e:
                                logger.error('[updator() thread] : Manual installation has failed' + str(e))
                                showerror('Erreur de lecture', "Le module OCR n'a pas pu être installé, la saisie automatique de scans ne pourra donc fonctionner")

                        else:
                            showerror('Opération annulée', "Le module OCR n'a été installé, la saisie automatique de scans ne pourra donc fonctionner")
            except URLExcept.HTTPError as e:
                canvas.itemconfigure(message, text=('Echec de la mise à jour : Erreur HTTP ' + str(e.code) + ' . Préparation du lancement...'))
                logger.error('[updator() thread] : Update has failed with HTTP error' + str(e.code))
                if int(e.code) == 407:
                    showerror('Erreur 407', 'Attention : le système de mise à jour automatique a fait face à une erreur 407, signifiant que la connexion au serveur proxy a été refusée. Vos identifiants vous seront redemandés au prochain démarrage. La mise à jour a échoué.')
                    logger.info('[updator() thread] : Credential error. Deleting the config file...')
                    os.remove(CST_FOLDER + 'conf.ig')
                p.configure(mode='indeterminate', value=0, maximum=20)
                p.start()
                time.sleep(3)
            except Exception as e:
                canvas.itemconfigure(message, text='Echec de la mise à jour. Préparation du lancement...')
                logger.error('[updator() thread] : Error from the updating system : ' + str(e))
                p.configure(mode='indeterminate', value=0, maximum=20)
                p.start()
                time.sleep(2)

            p.stop()
            upwin.destroy()
            root.destroy()
            return ret

        logger.info('updating() : Launching updator() thread...')
        threading.Thread(target=updator, daemon=True).start()
        logger.info('updating() [Thread] : Ending updator() thread')

    ret = 11
    root = Tk()
    root.attributes('-alpha', 0.0)
    root.iconify()
    upwin = Toplevel(root)
    upwin.overrideredirect(1)
    upwin.configure(bg=CST_COLOR)
    upwin.resizable(width=False, height=False)
    w = 600
    h = 300
    upwin.update()
    canvas = Canvas(upwin, width=600, height=270, bg=CST_COLOR, highlightthickness=0)
    pbar = Canvas(upwin, width=600, height=30, bg=CST_COLOR)
    p = ttk.Progressbar(pbar, orient=HORIZONTAL, length=590, mode='determinate')
    upwin.update()
    ws = upwin.winfo_screenwidth()
    hs = upwin.winfo_screenheight()
    canvas.create_text((w / 2), (h / 3), text=(CST_NAME + ' ' + CST_VERTITLE), font='Calibri 30 bold', fill='white')
    message = canvas.create_text((w / 2), (h / 1.15), text=' ', font='Calibri 9', fill='white')
    upwin.update()
    x = ws / 2 - w / 2
    y = hs / 2 - h / 2
    upwin.geometry('%dx%d+%d+%d' % (w, h, x, y))
    canvas.grid()
    pbar.grid()
    p.grid()
    upwin.after(2000, updating)
    if getattr(sys, 'frozen', False):
        root.iconbitmap(sys._MEIPASS + '\\id-card.ico\\id-card.ico')
    else:
        root.iconbitmap('id-card.ico')
    logger.info('SoftUpdate() : Entering upwin mainloop()')
    upwin.protocol('WM_DELETE_WINDOW', lambda : root.destroy())
    upwin.mainloop()
    logger.info('SoftUpdate() : Exiting upwin mainloop()')
    if ret == 11:
        logger.info('SoftUpdate() : OK to start to main() normally !')
        return True
    else:
        logger.info('SoftUpdate() : Program will stop !')
        return False