"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Application launcher & updater main file                        *
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

import sys
import os

import logger   # logger.py
import ihm      # ihm.py

## Main function 
def main():
    # Creating a log file and removing the old
    logfile = logger.NewLoggingSystem()
    
    # Hello world
    logfile.printdbg('*** CNIRLauncher LOGFILE. Hello World ! ***')
    
    launcherWindow = ihm.LauncherWindow()
    launcherWindow.mainloop()
    
    
    
    
    
    
    
    
## Bootstrap    
main()
sys.exit(0)
