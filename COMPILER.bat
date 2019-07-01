@echo off
set /p version=Numero de version: 


title Compilation du programme final

call pyinstaller -w -D --exclude-module PyQt5 --bootloader-ignore-signals --add-data "C:\users\adrie\Anaconda3\Lib\site-packages\tld\res\effective_tld_names.dat.txt";"tld\res" --add-data "id-card.ico";"id-card.ico" -i "id-card.ico" -n CNIRevelator_%version%.exe CNI_Revelator.py 

pause

