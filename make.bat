@echo off

title Compilation de CNIRevelator



call pyinstaller -w -D --exclude-module PyQt5 --bootloader-ignore-signals --add-data "C:\Users\adrie\Anaconda3\Lib\site-packages\tld\res\effective_tld_names.dat.txt";"tld\res" --add-data "src\id-card.ico";"id-card.ico" -i "src\id-card.ico" -n CNIRevelator src\CNIRevelator.py 



copy LICENSE dist\CNIRevelator\LICENSE
copy src\id-card.ico dist\CNIRevelator\id-card.ico
copy src\*.png dist\CNIRevelator\*.png

signtool_8.1\signtool\signtool.exe  sign /n "CNIRevelator by Adrien Bourmault (neox95)" dist\CNIRevelator\CNIRevelator.exe

pause

