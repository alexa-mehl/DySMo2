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

"""
This class is the base for any class that communicates with a simulation tool.
A simulation tool communication class must subclass from this class and implement their abstract methods.
"""
class Mode:
	#Constructor
	def __init__(this):
		#Private members
		this.__model = None;
		this.__id = None;
		this.__lastSimNum = None;
		#Protected members
		this._init = {};
		this._end = {};
		#Public members
		this.modeRef = ""; #Identifier of the mode
		this.solver = SolverScheme(); #Solver settings for this mode
		this.transitions = []; #Transitions that lead out of this mode
	
	#Protected methods
	#Deletes file in model folder if it exists
	#
	#Args:
	#fileName - file, relative to model folder
	#
	#Returns: Nothing
	def _deleteFile(this, fileName):
		if(os.path.isfile(this.__model.getPath() + "\\" + fileName)):
			os.remove(this.__model.getPath() + "\\" + fileName);
			
	#Checks whether a file in model folder exists
	#
	#Args:
	#fileName - file, relative to model folder
	#
	#Returns: True, if file exists in model folder, else False			
	def _fileExists(this, fileName):
		return os.path.isfile(this.__model.getPath() + "\\" + fileName);
		
	#Proposes a filename (including correct path) for storing a simulation result file for a specific simulation.
	#Does not append a file extension (this must be appended manually).
	#
	#Args:
	# simNum - Simulation number for the current simulation
	#
	#Returns: Path prefix (without file extension) for the result file name
	def _getResultFileName(this, simNum):
		return this.__model.getPath() + "\\result\\" + "sim" + str(simNum) + '_mode' + str(this.__id) + '_' + this.modeRef;
		
	#Renames a file in model folder
	#If the target file exists, it is deleted before the operation.
	#
	#Args:
	# fromName - Source file name
	# toName - Target file name
	#
	#Returns: Nothing
	def _renameFile(this, fromName, toName):
		this._deleteFile(toName);
		os.rename(this.__model.getPath() + "\\" + fromName, this.__model.getPath() + "\\" + toName);
		
	#Public methods
	
	#Finds the transition object based on the transition id in the end values of this mode.
	#
	#Args: None
	#
	#Returns: Outgoing transition object
	def find_transition(this):
		transId = int(this._end["transitionId"]);
		
		return this.transitions[transId-1];
	
	def get_endValue(this, varName):
		return this._end[varName];
		
	#Args: None
	#
	#Returns: The id of this mode
	def get_id(this):
		return this.__id;
		
	#Args: None
	#
	#Returns: The simulation result of the last simulation on this mode.
	def get_last_result(this):
		return this.get_result(this.__lastSimNum);
		
	#Args: None
	#
	#Returns: The model object, that this mode belongs to.
	def get_model(this):
		return this.__model;
		
	def has_endValue(this, varName):
		return varName in this._end;
		
	def has_initValue(this, varName):
		return varName in this._init;
		
	#Initializes this mode.
	#Initializes all transition objects in this mode.
	#
	#Args:
	# model - The model that this mode attaches to
	# modeId - Id of this mode
	#
	#Returns: Nothing
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
		
	#Args:
	# simNum - Simulation number that identifies the last simulation on this mode.
	#
	#Returns: Nothing		
	def set_lastSimulationNumber(this, simNum):
		this.__lastSimNum = simNum;
		
	#Sets initial values in this mode.
	#
	#Args:
	# inits - Dictionary of (String, Double) that contains variables and their initial values
	#
	#Returns: Nothing
	def write_init(this, inits):
		for key in inits:
			this._init[key] = inits[key];
		
	#Abstract methods
	#Called by the framework when this mode should compile itself.
	#Note that this is called only once when the mode gets used the first time.
	#
	#Args: None
	#
	#Returns: Nothing
	def compile(this):
		raise Exception("Method 'compile' in class 'Mode' is abstract");
		
	#Reads and loads a simulation result, based on a simulation number, that this mode produced.
	#The result has to be of type SimulationResult or a subclass of it.
	#
	#Args:
	# simNum - Simulation number
	#
	#Returns: SimulationResult object
	def get_result(this, simNum):
		raise Exception("Method 'get_result' in class 'Mode' is abstract");
		
	#Saves the simulation settings to a file that is later readable by a call to "simulate".
	#
	#Args:
	# startTime - The time at which the mode should start to simulate
	#
	#Returns: Nothing
	def save_init(this, startTime):
		raise Exception("Method 'save_init' in class 'Mode' is abstract");
		
	#Should simulate the mode and move the result file to the result folder.
	#
	#Args: None
	#
	#Returns: Nothing
	def simulate(this):
		raise Exception("Method 'simulate' in class 'Mode' is abstract");
