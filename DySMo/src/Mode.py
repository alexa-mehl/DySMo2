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
from copy import deepcopy;
import os;
#Local
from Solver import Solver, SolverScheme;

class Mode:
	#Constructor
	def __init__(this):
		#Private members
		this.__model = None;
		this.__id = None;
		this.solver = SolverScheme();
		this.__lastSimNum = None;
		#Protected members
		this._init = {};
		this._end = {};
		#Public members
		this.transitions = [];
	
	#Protected methods			
	def _deleteFile(this, fileName):
		if(os.path.isfile(this.__model.getPath() + "\\" + fileName)):
			os.remove(this.__model.getPath() + "\\" + fileName);
			
	def _fileExists(this, fileName):
		return os.path.isfile(this.__model.getPath() + "\\" + fileName);
			
	def _getResultFileName(this, simNum):
		return this.__model.getPath() + "\\result\\" + "sim" + str(simNum) + '_mode' + str(this.__id) + '_' + this.modeRef;
		
	def _renameFile(this, fromName, toName):
		this._deleteFile(toName);
		os.rename(this.__model.getPath() + "\\" + fromName, this.__model.getPath() + "\\" + toName);
		
	#Public methods
	def find_transition(this):
		transId = int(this._end["transitionId"]);
		
		return this.transitions[transId-1];
		
	def get_endValue(this, varName):
		return this._end[varName];
		
	def get_id(this):
		return this.__id;
		
	def get_last_result(this):
		return this.get_result(this.__lastSimNum);
		
	def get_model(this):
		return this.__model;
		
	def has_endValue(this, varName):
		return varName in this._end;
		
	def has_initValue(this, varName):
		return varName in this._init;
		
	def init(this, model, modeId):
		this.__model = model;
		this.__id = modeId;
		
		#Build the real solver
		if(not type(this.solver) == Solver):
			scheme = this.solver;
			this.solver = deepcopy(model.default_solver);
			if(hasattr(scheme, 'tolerance')):
				this.solver.tolerance = scheme.tolerance;
			#TODO THE REST
		
		transId = 1;
		for t in this.transitions:
			t.init(transId);
			transId += 1;
			
	def set_initialValue(this, varName, value):
		this._init[varName] = value;
		
	def set_lastSimulationNumber(this, simNum):
		this.__lastSimNum = simNum;
	
	def write_init(this, inits):
		for key in inits:
			this._init[key] = inits[key];
		
	#Abstract methods
	def compile(this):
		raise Exception("Method 'compile' in class 'Mode' is abstract");
		
	def get_result(this, simNum):
		raise Exception("Method 'get_result' in class 'Mode' is abstract");
		
	def save_init(this, startTime):
		raise Exception("Method 'save_init' in class 'Mode' is abstract");
		
	def simulate(this):
		raise Exception("Method 'simulate' in class 'Mode' is abstract");