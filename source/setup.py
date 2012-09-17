#!/usr/bin/env python
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

from distutils.core import setup
import os
import sys
import userSettings as us


# Recognize build in user input and create the global header file
if "build" in sys.argv:
    # 1. generate a extern header file
    header = open(us.scriptFolderName + os.sep +"globalHeader.py", 'w')
    header.write('''########This Headerfile is gerneated automatically 
      # by setup.py! DON'T CHANGE THIS FILE MANUALLY!########\n\n''')
    header.write("PP_HEADER_EXISTS = True\n\n")

## Set package information and write them to global header
if us.INSTALL_DYMOLA_OPT:
    # Dymola is required 
    header.write("PP_USE_DYMOLA = True\n")
    header.write("PP_DYMOLAPATH = "'r'+ '"'+ us.dymolaPath + '"\n')
    header.write("PP_ALISTDIR = r"+ '"' + us.alistDir + '"\n\n')
else:
    header.write("PP_USE_DYMOLA = False\n")

if us.INSTALL_OM_OPT:
    # Open Modelica is required
    header.write("PP_USE_OMODELICA = True\n")
    header.write("PP_OMPATH = r"+ '"' + us.OMPath + '"\n\n')
else:
    header.write("PP_USE_OMODELICA = False\n")

if us.INSTALL_SIMULINK_OPT:
    header.write("PP_USE_SIMULINK = True\n")
else:
    header.write("PP_USE_SIMULINK = False\n")

header.close()
## setup routine    
setup(name='StructDynamicFramework',
      version='0.8',
      description='''Framework to simulate Models with structural Dynamic using
                   different Simulationtools''',
      author='Alexandra Mehlhase',
      author_email='a.mehlhase@tu-berlin.de',
      maintainer = 'Tommy Beckmann',
      maintainer_email = 'tommy.beckmann@campus.tu-berlin.de',
     )
