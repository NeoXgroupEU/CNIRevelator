import globs
import psutil
import os

for process in psutil.process_iter():
    if process.name() == 'CNIRevelator.exe':
        print('Process found. Command line: {}'.format(process.cmdline()))
        if True:
            print(process.pid)

            continue
        else:
            print('Terminating process !')
            #process.terminate()
        break