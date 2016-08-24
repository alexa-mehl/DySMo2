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

#Lib
import os;
import PySimLib;
import time;

class Mode:
	#Constructor
	def __init__(this):
		#Private members
		this.__vsmModel = None;
		this.__id = None;
		this.__mdlObj = None; #the PySimLib model object
		this.__lastSimNum = None;
		this.__simObjs = {}; #dict containing all simulation objects for this mode
		
		#Public members
		this.files = [];
		this.modeRef = None; #Identifier of the mode
		this.solver = None; #Solver settings for this mode
		this.synonym = {};
		this.tool = None; #PySimLib tool object for simulating this mode
		this.transitions = []; #Transitions that lead out of this mode
		
	#Magic methods
	def __str__(this):
		return "Mode " + str(this.__id);
		
	#Public methods
	#Called by the framework when this mode should compile itself.
	#Note that this is called only once when the mode gets used the first time.
	#
	#Args: None
	#
	#Returns: Nothing
	def compile(this):
		print("Compiling mode", this.get_id(), "...");
		
		this.tool.Compile(this.__mdlObj);
		
	#Finds the transition object based on the transition id in the end values of this mode.
	#
	#Args: None
	#
	#Returns: Outgoing transition object
	def find_transition(this):
		transId = int(this.get_endValue("transitionId"));
		
		if(transId > len(this.transitions)):
			from exceptions.InvalidTransitionException import InvalidTransitionException;
			raise InvalidTransitionException(this, transId);
		
		return this.transitions[transId-1];
		
	def get_endValue(this, varName):
		return this.__mdlObj.variables[varName].final;
		
	#Args: None
	#
	#Returns: The id of this mode
	def get_id(this):
		return this.__id;
		
	def get_model(this):
		return this.__vsmModel;
		
	def get_parameter(this, key):
		return this.__mdlObj.parameters[key];
		
	def has_endValue(this, varName):
		return varName in this.__mdlObj.variables;
		
	#Initializes this mode.
	#Initializes all transition objects in this mode.
	#
	#Args:
	# model - The model that this mode attaches to
	# modeId - Id of this mode
	#
	#Returns: Nothing
	def init(this, model, modeId):
		from exceptions.InvalidModeModelException import InvalidModeModelException;
		
		this.__vsmModel = model;
		this.__id = modeId;
		
		if(this.solver is None):
			this.solver = model.default_solver;
			
		#acquire PySimLib model object
		if(this.modeRef is None):
			raise InvalidModeModelException(this);
			
		this.__mdlObj = PySimLib.Model(this.modeRef, this.files);
		
		if(this.__mdlObj is None):
			raise InvalidModeModelException(this);
			
		#set settings on model object
		this.__mdlObj.outputName = 'm' + str(this.get_id());
		this.__mdlObj.outputDir = model.getPath() + os.sep + "output";
		this.__mdlObj.resultDir = model.getPath() + os.sep + "result";
		this.__mdlObj.simDir = model.getPath();
		
		#check tool
		if(not (this.tool is None)):
			this.tool = PySimLib.FindTool(this.tool);
			if(this.tool is None):
				print("The desired tool for mode " + str(this.__id) + " is not available.");
				
		if(this.tool is None): #we dont have a tool
			if(not(this.__vsmModel.default_tool is None)): #try the default tool
				if(this.__vsmModel.default_tool.Accepts(this.__mdlObj)): #if is compatible
					this.tool = this.__vsmModel.default_tool; #silent using, as the user specified the default_tool
			else: #last try to get some compatible tool
				compatibleTools = this.__mdlObj.GetCompatibleTools();
					
				if(compatibleTools): #there is at least one simulator
					this.tool = compatibleTools[0];
					print("Choosing tool '" + str(this.tool) + "' for mode " + str(this.__id) + "."); #inform which one we use
				else:
					print("No simulator is available for mode " + str(this.__id) + ". Exiting...");
					exit(1);
			
		#init transitions
		transId = 1;
		for t in this.transitions:
			t.init(transId);
			transId += 1;
			
	def read_init(this):
		from exceptions.MissingTransitionIdException import MissingTransitionIdException;
		
		this.tool.ReadInit(this.__mdlObj);
		
		if(not('transitionId' in this.__mdlObj.variables)):
			raise MissingTransitionIdException(this);
		
	#Args: None
	#
	#Returns: The simulation result of the last simulation on this mode.
	def read_last_result(this):
		return this.read_result(this.__lastSimNum);
		
	#Reads and loads a simulation result, based on a simulation number, that this mode produced.
	#The result has to be of type SimulationResult or a subclass of it.
	#
	#Args:
	# simNum - Simulation number
	#
	#Returns: SimulationResult object
	def read_result(this, simNum):
		return this.tool.ReadResult(this.__simObjs[simNum]);
		
	def set_initialValue(this, varName, value):
		this.__mdlObj.variables[varName].start = value;
		
	def set_parameter(this, name, value):
		this.__mdlObj.parameters[name] = value;
		
	def set_parameters(this, params):
		for key in params:
			this.set_parameter(key, params[key]);
		
	#Simulates the mode and moves the result file to the result folder.
	#
	#Args: None
	#
	#Returns: Nothing
	def simulate(this):
		simObj = PySimLib.Simulation(this.__mdlObj, this.__vsmModel.getCurrentSimulationNumber());
		
		simObj.startTime = this.__vsmModel.currentTime;
		simObj.stopTime = this.__vsmModel.stopTime;
		
		print("Running simulation", simObj.GetSimNumber(), "ModeID:", this.get_id(), "Time:", this.__vsmModel.currentTime);
		t1 = time.clock();
		this.tool.Simulate(simObj);
		t2 = time.clock();
		
		
		string = "Simulation " + str(simObj.GetSimNumber()) + " of mode " + str(this.get_id()) + " took " + str(t2 - t1) + " seconds";
		PySimLib.Log.Line(string);
		
		this.__lastSimNum = simObj.GetSimNumber();
		this.__simObjs[this.__lastSimNum] = simObj;
		
		return t2 - t1;
		
	#Sets initial values in this mode.
	#
	#Args:
	# inits - Dictionary of (String, Double) that contains variables and their initial values
	#
	#Returns: Nothing
	def write_init(this, inits):
		for key in inits:
			this.__mdlObj.variables[key].start = inits[key];
