# -*- coding: utf-8 -*-
"""
  Copyright (C) 2012  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
  This file is part of modelica3d 
  (https://mlcontrol.uebb.tu-berlin.de/redmine/projects/modelica3d-public).

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
   
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


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
INSTALL_SIMULINK_OPT = True
