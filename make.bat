@echo off

title Compilation de CNIRevelator



call pyinstaller -w -D --exclude-module PyQt5 --bootloader-ignore-signals --add-data "C:\Users\pf04950\AppData\Local\Continuum\anaconda3\Lib\site-packages\tld\res\effective_tld_names.dat.txt";"tld\res" --add-data "id-card.ico";"id-card.ico" -i "id-card.ico" --add-data "background.png";"background.png" -i "background.png" -n CNIRevelator src\CNIRevelator.py 



copy LICENSE dist\CNIRevelator\

copy src\id-card.ico dist\CNIRevelator\

copy src\background.png dist\CNIRevelator\


D:\Public\CNIRevelator-master\CNIRevelator-master\signtool_8.1\signtool\signtool.exe  sign /n "CNIRevelator by Adrien Bourmault (neox95)" dist\CNIRevelator\CNIRevelator.exe

pause

