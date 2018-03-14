"""
  Copyright (C) 2014-2016  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
  Implemented by Alexandra Mehlhase, Amir Czwink
  
  This file is part of the AMSUN project
  (https://gitlab.tubit.tu-berlin.de/groups/amsun)

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

# Lib
import os
import sys
import PySimLib
# Local
from Definitions import *
from exceptions.ModeException import ModeException
from Mode import Mode
from Plots import *
from Transition import Transition
from VSM import VSM


# Functions
def ExecPythonFile(fileName):
    file = open(fileName)
    content = file.read()
    code = compile(content, fileName, 'exec')
    exec(code)

# Functions for config script


def Solver(name):
    return PySimLib.FindSolver(name)


func = VSM.simulate

# Checks
if(len(sys.argv) == 1):
    print("Please provide a path to a variable-structure simulatiom description file as argument.")
    print("Exiting...")
    exit()

if(len(sys.argv) == 3):
    if(sys.argv[2] == "clean"):
        func = VSM.clean
    else:
        print("You specified the following unknown argument:", sys.argv[2])
        print("Exiting...")
        exit()


# paths
configPath = os.path.abspath(sys.argv[1])

# instantiate model
model = VSM(configPath)  # The global model instance

# execute config file
ExecPythonFile(sys.argv[1])

# run simulation
os.chdir(model.getPath())  # switch to model path
try:
    func(model)
except ModeException as e:
    print("ERROR: ", e)
    print("See Log file for details.")

model.shutdown()
