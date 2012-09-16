############User input, change your path settings and options here#############
import os
# The folder where the main scripts are located
scriptFolderName = 'scripts'

# DYMOLA settings, if you don t want to use dymola, set to False
INSTALL_DYMOLA_OPT = True
# Set path to your dymola.exe
dymolaPath = os.path.join('C:\\','Program Files (x86)','Dymola 2012', 'bin', 'dymola.exe')
# Set path to the folder where your alist.exe is located
alistDir = os.path.join('C:\\','Program Files (x86)','Dymola 2012','Mfiles')

# OpenModelica settings, if you don t want to use OM, set to False
INSTALL_OM_OPT = True
OMPath = os.path.join('C:\\', 'OpenModelica1.8.1', 'bin', 'omc')

# Simulink settings (TODO)
INSTALL_SIMULINK_OPT = False
