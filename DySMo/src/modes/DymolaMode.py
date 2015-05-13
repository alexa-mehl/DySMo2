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
import subprocess;
import time;
import win32ui;
import dde;
import os;
import os.path;
import shutil;
#Local
from globals import *;
from Log import *;
from Mat.Mat import *;
from Mat.OutputStream import *;
from modes.ModelicaMode import ModelicaMode;
from exceptions.SimulationFailedException import SimulationFailedException;
from exceptions.UncompiledModeException import UncompiledModeException;

g_dymolaOpen = False;
g_ddeServ = None;
g_ddeConv = None;
g_openFiles = {};

class DymolaMode(ModelicaMode):
	#Constructor
	def __init__(this):
		ModelicaMode.__init__(this);
		
		this.intervalLength = 0;		
		this.numberOfIntervals = 500;
		
	#Private methods	
	def __ensureDymolaOpen(this):
		global g_dymolaOpen;
		global g_ddeConv;
		global g_cfg;
		
		if(not g_dymolaOpen):
			g_dymolaOpen = True;
			g_ddeServ = dde.CreateServer();
			g_ddeServ.Create("TestClient");
			g_ddeConv = dde.CreateConversation(g_ddeServ);
			
			subprocess.Popen([g_cfg.GetValue("Dymola", "PathExe")], stdin=subprocess.PIPE);
			time.sleep(5);
			g_ddeConv.ConnectTo("dymola", " ");
			g_ddeConv.Exec("OutputCPUtime:=true;");
			
	def __MapSolver(this, method):
		if(method == "deabm"):
			return 1;
		elif(method == "lsode1"):
			return 2;
		elif(method == "lsode2"):
			return 3;
		elif(method == "lsodar"):
			return 4;
		elif(method == "dopri5"):
			return 5;
		elif(method == "dopri8"):
			return 6;
		elif(method == "grk4t"):
			return 7;
		elif(method == "dassl"):
			return 8;
		elif(method == "odassl"):
			return 9;
		elif(method == "mexx"):
			return 10;
		elif(method == "euler"):
			return 11;
		elif(method == "rkfix2"):
			return 12;
		elif(method == "rkfix3"):
			return 13;
		elif(method == "rkfix4"):
			return 14;
		elif(method == "cvode"):
			return 29;
		return 15;
			
	def __openFile(this, fileName):
		global g_ddeConv;
		global g_openFiles;
		
		if(fileName not in g_openFiles):
			g_ddeConv.Exec("openModel(\"" + this.get_model().getPath().replace('\\', '/') + "/" + fileName + "\")");
			g_openFiles[fileName] = True;
			
	#Public methods
	def compile(this):
		global g_ddeConv;
		
		this.__ensureDymolaOpen();
		
		#open all needed mo files
		for x in this.files:
			this.__openFile(x);
			
		g_ddeConv.Exec("cd(\"" + this.get_model().getPath().replace('\\', '/') + "\")");
		g_ddeConv.Exec("simulateModel(\"" + this._getModelicaClassString() + "\", stopTime=0, method=\"" + this.solver.name + "\" )");
		
		#Delete unnecessary files
		this._deleteFile("buildlog.txt");
		this._deleteFile("dsfinal.txt");
		this._deleteFile("dslog.txt");
		this._deleteFile("dsmodel.c");
		this._deleteFile("dsres.mat");
		this._deleteFile("dymosim.exp");
		this._deleteFile("dymosim.lib");
		
		#Rename important files
		if(os.path.isfile(this.get_model().getPath() + "\\m" + str(this.get_id()) + ".exe")):
			os.remove(this.get_model().getPath() + "\\m" + str(this.get_id()) + ".exe");
		os.rename(this.get_model().getPath() + "\\dymosim.exe", this.get_model().getPath() + "\\m" + str(this.get_id()) + ".exe");
		if(os.path.isfile(this.get_model().getPath() + "\\m" + str(this.get_id()) + "_in.txt")):
			os.remove(this.get_model().getPath() + "\\m" + str(this.get_id()) + "_in.txt");
		os.rename(this.get_model().getPath() + "\\dsin.txt", this.get_model().getPath() + "\\m" + str(this.get_id()) + "_in.txt");
	
	def read_init(this):
		global g_cfg;
		
		currentDir = os.getcwd();
		
		
		if(not this._fileExists("m" + str(this.get_id()) + "_in.txt")):
			raise UncompiledModeException(this);
			
		inPath = this.get_model().getPath() + "\\m" + str(this.get_id()) + "_in.mat";
		if(os.path.isfile(inPath)):
			os.remove(inPath);
			
		os.chdir(g_cfg.GetValue("Dymola", "AlistDir"));
		ret = subprocess.call("alist.exe -b \"" + this.get_model().getPath() + '\m' + str(this.get_id()) + '_in.txt" "' + inPath + "\"", shell = True, stdout = Log_GetFile(), stderr = Log_GetFile());
		
		initMat = Mat();
		initMat.Load(inPath);
		names = initMat.GetMatrix("initialName");
		values = initMat.GetMatrix("initialValue");
		for i in range(0, names.GetNumberOfStrings()):
			this._init[names.GetString(i)] = values.GetValue(1, i);
			
		os.chdir(currentDir);
			
	def save_init(this, startTime):
		inPath = this.get_model().getPath() + "\\m" + str(this.get_id()) + "_in.mat";
			
		outMat = Mat();
		outMat.Load(inPath);
		if(os.path.isfile(inPath)):
			os.remove(inPath);
			
		names = outMat.GetMatrix("initialName");
		values = outMat.GetMatrix("initialValue");
		experiment = outMat.GetMatrix("experiment");
		
		#Set experiment values
		experiment.SetValue(0, 0, startTime);
		experiment.SetValue(0, 1, this.get_model().stopTime);
		experiment.SetValue(0, 2, this.intervalLength);
		experiment.SetValue(0, 3, this.numberOfIntervals);
		experiment.SetValue(0, 4, this.solver.tolerance);
		experiment.SetValue(0, 5, this.solver.stepSize);
		experiment.SetValue(0, 6, this.__MapSolver(this.solver.name));
		
		Log_LogLine("\n \n \n Simulation Settings:\n    StartTime:" + str(startTime) + ",\n    Tolerance:" + str(this.solver.tolerance) + ",\n    Solver: " + str(this.solver.name));
		
		for i in range(0, names.GetNumberOfStrings()):
			varName = names.GetString(i);
			
			if varName in this._init:				
				values.SetValue(1, i, this._init[varName])
			
		#Set correct types, else Dymola won't read the file			
		outMat.GetMatrix("settings").SetDesiredOutputPrecision(2);
		outMat.GetMatrix("initialValue").SetDesiredOutputPrecision(0);
		
		file = open(inPath, "wb");
		stream = OutputStream(file);
		
		#we need to write the matrices in the exact order or dymola can't read the file
		outMat.GetMatrix("Aclass").Write("Aclass", stream);
		outMat.GetMatrix("experiment").Write("experiment", stream);
		outMat.GetMatrix("method").Write("method", stream);
		outMat.GetMatrix("settings").Write("settings", stream);
		outMat.GetMatrix("initialName").Write("initialName", stream);
		outMat.GetMatrix("initialValue").Write("initialValue", stream);
		outMat.GetMatrix("initialDescription").Write("initialDescription", stream);
		
		
		file.close();
		
		
	def simulate(this):
		ret = subprocess.call("m" + str(this.get_id()) + ".exe m" + str(this.get_id()) + "_in.mat", shell = True, stdout = Log_GetFile());
		
		failed = False;		
		if(this._fileExists("failure")):
			failed = True;
		
		#keep things clean
		this._deleteFile("dsfinal.txt");
		this._deleteFile("dslog.txt");
		this._deleteFile("status");
		this._deleteFile("success");
		this._deleteFile("failure");
		
		if(failed):
			this._deleteFile("dsres.mat");
			raise SimulationFailedException();
		
		#move results to result path
		shutil.move("dsres.mat", this._getResultFileName(this.get_model().getCurrentSimulationNumber()) + ".mat");