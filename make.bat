@echo off

title Compilation de CNIRevelator



call pyinstaller -c -D --exclude-module PyQt5 --bootloader-ignore-signals --add-data "C:\Users\pf04950\AppData\Local\Continuum\anaconda3\Lib\site-packages\tld\res\effective_tld_names.dat.txt";"tld\res" --add-data "id-card.ico";"id-card.ico" -i "id-card.ico" -n CNIRevelator src\CNIRevelator.py 



copy LICENSE dist\CNIRevelator\LICENSE
copy src\id-card.ico dist\CNIRevelator\id-card.ico
copy src\background.png dist\CNIRevelator\background.png

D:\Public\CNIRevelator-master\CNIRevelator-master\signtool_8.1\signtool\signtool.exe  sign /n "CNIRevelator by Adrien Bourmault (neox95)" dist\CNIRevelator\CNIRevelator.exe

pause

