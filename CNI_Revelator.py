"""
******************************************************************************** 
                ***   Projet  CNI_Revelator   ***
                       
                        GNU GPL * 07/2018

                        Adrien Bourmault
                            
                            main

********************************************************************************
"""
from CNI_GLOBALVAR import *
try:
    os.remove('error.log')
    os.remove('conf.ig')
except:
    print("pass log deletion")
    pass

if not os.path.exists(CST_FOLDER):
    try:
        os.makedirs(CST_FOLDER)
    except IOError:
        print("pass IO ERROR")
        pass

print("debug")
import logging
from logging import FileHandler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
error_handler = FileHandler((CST_FOLDER + '\\error.log'), mode='w', encoding='utf-8', delay=True)
info_handler = FileHandler((CST_FOLDER + '\\cnirevelator.log'), mode='w', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)
info_handler.setLevel(logging.DEBUG)
info_handler.setFormatter(formatter)
logger.addHandler(info_handler)
from CNI_classes import *
from CNI_Update import *

def main(logger):
    logger.error('')
    logger.info('main() : **** Creating App_main() ****')
    main_w = App_main(logger)
    main_w.montext('* ' + CST_NAME + ' ' + CST_VER + ' ' + CST_TYPE + ' Revision ' + CST_REV + ' *\n')
    import CNI_pytesseract as pytesseract
    try:
        os.environ['PATH'] = CST_FOLDER + 'Tesseract-OCR4\\'
        os.environ['TESSDATA_PREFIX'] = CST_FOLDER + 'Tesseract-OCR4\\tessdata'
        tesser_version = pytesseract.get_tesseract_version()
    except Exception as e:
        logger.error('main() : **** ERROR WITH TESSERACT MODULE ' + str(e) + ' ****')
    else:
        text = 'Tesseract version ' + str(tesser_version) + ' Licensed Apache 2004 successfully initiated\n'
        main_w.montext(text)
    main_w.montext('\n\nEntrez la première ligne de MRZ svp \n')
    if CST_CHANGELOG.isOn:
        showinfo('Changelog : résumé de mise à jour', ('Version du logiciel : ' + CST_VER + ' ' + CST_TYPE + ' Revision ' + CST_REV + '\n\n' + CST_CHANGELOG.text), parent=main_w)
    logger.info('main() : **** Launching App_main() ****')
    main_w.mainloop()
    logger.info('main() : **** Ending App_main() ****')


logger.info('launcher : ' + CST_NAME + ' ' + CST_VER)
logger.info('launcher : *****Hello World*****')
logger.info('launcher : *****Launching SoftUpdate()*****')
try:
    Answer = SoftUpdate(logger)
except Exception as e:
    logger.info('launcher : *****FATAL ERROR*****' + str(e))
    os.abort()

logger.info('launcher : *****Ending SoftUpdate()*****')
try:
    if Answer == True:
        logger.info('launcher : *****Launching main()*****')
        State = main(logger)
except Exception as e:
    logger.info('launcher : *****FATAL ERROR*****' + str(e))
    os.abort()

logger.info('launcher : *****Ending main()*****')
logger.info('launcher : *****Goodbye!*****')
handlers = logger.handlers[:]
for handler in handlers:
    handler.close()
    logger.removeHandler(handler)

try:
    with open(CST_FOLDER + '\\error.log') as (echo):
        try:
            os.remove('error.log')
        except OSError:
            pass

        from shutil import copyfile
        temptwo = str(echo.read())
        if len(temptwo) != 1:
            copyfile(CST_FOLDER + '\\cnirevelator.log', 'error.log')
except IOError:
    pass

print("exit")
#sys.exit(0)