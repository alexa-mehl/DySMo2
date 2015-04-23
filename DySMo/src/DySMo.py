"""
  Copyright (C) 2014-2015  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
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

#Lib
import imp;
import os;
import os.path;
import sys;
#Local
from __modes__ import *;
from __plots__ import *;
from Config import Config;
from Definitions import *;
from Solver import Solver;
from Transition import Transition;
import VSM;
from exceptions.ModeException import ModeException;
from Log import *;

def ExecPythonFile(fileName):
	file = open(fileName);
	content = file.read();
	code = compile(content, fileName, 'exec');
	exec(code);
	
#Load modes
files = os.listdir("modes");
#for x in files:
#	if os.path.isfile("modes/" + x):
#		ExecPythonFile("modes/" + x);
#		__import__("modes." + x);

modelPath = os.path.abspath(os.path.join(sys.argv[1], os.pardir));
configPath = os.path.abspath(sys.argv[1]);

Log_Init(configPath + ".log");
model = VSM.VSM(modelPath); #The global model instance

ExecPythonFile(sys.argv[1]); #Load config file
os.chdir(modelPath); #switch to model path
try:
	model.simulate(); #Simprocess
except ModeException as e:
	print("ERROR: ", e);
	print("See Log file for details.");