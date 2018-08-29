"""
******************************************************************************** 
                ***   Projet  CNI_Revelator   ***
                       
                        GNU GPL * 07/2018

                        Adrien Bourmault
                            
                            main

********************************************************************************
"""

###IMPORTS GLOBAUX
from CNI_GLOBALVAR import * 


##LOGGING

try:
    os.remove("error.log")
    os.remove("conf.ig")
except:
    pass
import logging

CST_NIVEAU_LOG = logging.ERROR

from logging.handlers import RotatingFileHandler

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(CST_NIVEAU_LOG)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('error.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(CST_NIVEAU_LOG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

##History



### IMPORTS LOCAUX       
from CNI_classes import *
from CNI_Update import *  

### FONCTION PRINCIPALE


def main(logger):
    
    logger.info("main() : " +"**** Creating App_main() ****")
    main_w = App_main(logger)
    
    main_w.montext("* " + CST_NAME + " " + CST_VER + " " + CST_TYPE + " Revision " + CST_REV + " *\n")
    
    import CNI_pytesseract as pytesseract
    
    try:
        
        os.environ["PATH"] = CST_FOLDER + "Tesseract-OCR4\\" 
        os.environ["TESSDATA_PREFIX"] = CST_FOLDER + "Tesseract-OCR4\\tessdata"
        tesser_version = pytesseract.get_tesseract_version()
        
    except Exception as e:
        logger.error("main() : " +"**** ERROR WITH TESSERACT MODULE " + str(e) + " ****")
    else:
        text = "Tesseract version " + str(tesser_version) +" Licensed Apache 2004 successfully initiated\n"
        main_w.montext(text)
        
    
    main_w.montext("\n\nEntrez la première ligne de MRZ svp \n")
    
    
    
    logger.info("main() : " +"**** Launching App_main() ****")
    main_w.mainloop()
    logger.info("main() : " +"**** Ending App_main() ****")
    

   
##Launcher

logger.info("launcher : " + CST_NAME +" "+ CST_VER)
logger.info("launcher : " +"*****Hello World*****")

logger.info("launcher : " +"*****Launching SoftUpdate()*****")
try:
    Answer = SoftUpdate(logger)
except Exception as e:
    logger.info("launcher : " +"*****FATAL ERROR*****" + str(e))
    os.abort()
logger.info("launcher : " +"*****Ending SoftUpdate()*****")


try:
    if Answer == True:
        logger.info("launcher : " +"*****Launching main()*****")
        State = main(logger)
except Exception as e:
    logger.info("launcher : " +"*****FATAL ERROR*****" + str(e))
    os.abort()
    
logger.info("launcher : " +"*****Ending main()*****")
logger.info("launcher : " +"*****Goodbye!*****")

handlers = logger.handlers[:]
for handler in handlers:
    handler.close()
    logger.removeHandler(handler)
    
    
if os.path.getsize("error.log") == 0:
    try:
        os.remove("error.log")
    except:
        raise(OSError)
        os.abort()

sys.exit(0)

    