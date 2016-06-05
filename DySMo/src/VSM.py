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
import pylab;
import PySimLib;
import shutil;
import time;

class VSM:
	#Constructor
	def __init__(this, path):
		#Private members
		this.__path = path;
		this.__actMode = None; #current mode
		this.__compiledModes = {};
		this.__currentTime = 0;
		this.__currentNum = 1; #sim counter
		this.__observer = {};
		
		#Public members
		this.translate = True;
		this.default_tool = None;
		
	#Private methods
	def __clearResult(this):
		resultPath = this.__path + os.sep + "result";
		#check whether the sub directory already exists
		if os.path.exists(resultPath):
			#delete all files in resultFolder and create an empty folder
			shutil.rmtree(resultPath);
			time.sleep(2); #ugly... but somehow os.makedirs fails sometimes with permission error when there is not enough time between shutil.rmtree and os.makedirs
			
		os.makedirs(resultPath);
		
		#make sure output dir exists
		outputPath = this.__path + os.sep + "output";
		if not(os.path.exists(outputPath)):
			os.makedirs(outputPath);
		
	def __compileMode(this, mode):
		if(mode not in this.__compiledModes):
			if(this.translate):
				t1 = time.clock();
				mode.compile();
				PySimLib.Log.Line("Compilation of mode " + str(mode.get_id()) + " took " + str(time.clock() - t1) + " seconds.");
			this.__compiledModes[mode] = True;
			mode.read_init();
			
	def __drawPlots(this):
		show = False;
		for p in this.plots:
			figure = pylab.figure(); #new plot
			for var in this.observe:
				for i in range(0, len(this.__observer[var])):
					col = p.getColor(this.__observer["modeID"][i], i, var);
					if((col is not None) and (this.__observer[var][i])):
						#print(this.__observer[var][i]);
						#print(var, len(this.__observer[var]), len(this.__observer["time"][i]));
						#print(this.__observer['y']);
						pylab.plot(this.__observer[p.xAxisVar][i], this.__observer[var][i], p.colorToColorString(col));
			pylab.grid(p.drawGrid);
			pylab.xlabel(p.labelXAxis);
			pylab.ylabel(p.labelYAxis);
			if(hasattr(p, 'fileName')):
				pylab.savefig(this.__path + os.sep + "result" + os.sep + p.fileName);
			if((not hasattr(p, 'fileName')) or hasattr(p, 'show')):
				show = True;
			else:
				pylab.close(figure);
		
		if(show):
			pylab.show();
			
	def __init(this):
		#Init observer
		for k in this.observe:
			this.__observer[k] = [];
		this.__observer["time"] = [];
		this.__observer["modeID"] = [];
		
		#check default_tool
		if(not(this.default_tool is None)):
			name = this.default_tool;
			this.default_tool = PySimLib.FindTool(name);
			if(this.default_tool is None):
				print("The specified default tool '" + name + "' is not available.");
				
	def __observe(this, simResults):
		for k in this.observe:
			if(k in this.__actMode.synonym):
				synonym = this.__actMode.synonym[k];
				this.__observer[k].append(simResults[synonym]);
			else:
				this.__observer[k].append([]);
				
		this.__observer["time"].append(simResults["time"]);		
		this.__observer["modeID"].append(this.__actMode.get_id());
		
	def __preprocess(this):
		#Numerate modes
		modeId = 1;
		for m in this.modes:
			m.init(this, modeId);
			modeId += 1;
			
		#TODO
		#Run initial mode
		this.__actMode = this.modes[0];
		this.__compileMode(this.__actMode);
		this.__actMode.write_init(this.init);
		
	def __save_observer(this):
		from PySimLib.Mat.Mat import Mat;
		from PySimLib.Mat.OutputStream import OutputStream;
		
		nan = float("NaN");
		variables = ["time", "modeID"] + this.observe;
		lastVariable = variables[len(variables)-1];
		
		#get for every simulation the maximum number of datapoints
		nDataPointsPerSim = [];
		for p in this.__observer["modeID"]: #init all sims with datapoints-length of 1
			nDataPointsPerSim.append(1);
			
		for key in variables:
			if(key == "modeID"):
				continue; #unimportant
				
			for i in range(0, len(nDataPointsPerSim)):
				if(len(this.__observer[key][i]) > nDataPointsPerSim[i]):
					nDataPointsPerSim[i] = len(this.__observer[key][i]);
		nDataPointsSum = 0;
		for n in nDataPointsPerSim:
			nDataPointsSum += n;
		
		#write mat
		mat = Mat();
		
		#names matrix
		names = mat.AddTextMatrix("names", len(this.__observer));
		i = 0;
		for key in variables:
			names.SetString(i, key);
			i += 1;
			
		#values matrix
		values = mat.AddMatrix("values", len(this.__observer), nDataPointsSum);
		x = 0;
		for key in variables:
			i = 0;
			y = 0;
			if(key == "modeID"): #modeID is special...
				for p in this.__observer[key]: 
					for j in range(0, nDataPointsPerSim[i]):
						values.SetValue(x, y, p);
						y += 1;
					i += 1;
			else:
				for points in this.__observer[key]:
					for p in points:
						values.SetValue(x, y, p);
						y += 1;
					for j in range(len(points), nDataPointsPerSim[i]):
						values.SetValue(x, y, nan);
						y += 1;
					i += 1;
			x += 1;
			
		file = open("result" + os.sep + "observer_data.mat", "wb");
		stream = OutputStream(file);
		mat.Write(stream);		
		file.close();
		
		#write csv
		file = open("result" + os.sep + "observer_data.csv", "w");
		
		#var names
		for key in variables:
			file.write(key);
			if(key != lastVariable):
				file.write(";");
		file.write("\n");
		
		#var values
		y = 0;
		while(y < nDataPointsSum):
			x = 0;
			for key in variables:
				p = values.GetValue(x, y);
				x += 1;
				file.write(str(p));
				if(key != lastVariable):
					file.write(";");
			file.write("\n");
			y += 1;
		file.close();
		
	def __transitionActive(this, transition):
		from Transition import Transition;
		
		oldMode = this.__actMode;
		this.set_active_mode(transition.post);
		this.__compileMode(this.__actMode);
		
		mappedValues = Transition.mapping(transition, oldMode, this.__actMode); #direct call to class function because the dicts name is also "mapping"
		this.__actMode.write_init(mappedValues);
		
		if(hasattr(transition, "init_function")):
			transition.init_function(this.__actMode, oldMode);
	
	#Public methods
	def getCurrentSimulationNumber(this):
		return this.__currentNum;
		
	def getCurrentTime(this):
		return this.__currentTime;
		
	def getPath(this):
		return this.__path;
		
	def set_active_mode(this, newMode):
		this.__actMode = newMode;
		
	def simulate(this):
		simTime = 0;
		readTime = 0;
		
		this.__init();
		this.__clearResult();
		this.__preprocess();
		
		this.__currentTime = this.startTime;
		
		while(this.__currentTime < this.stopTime):
			#Run sim
			simTime += this.__actMode.simulate();
			result, dt = this.__actMode.read_last_result();
			readTime += dt;
			
			#process results
			this.__observe(result.GetValues());
			
			observTime = this.__observer["time"];
			observTime = observTime[len(observTime)-1];
			lastTimeValue = observTime[len(observTime)-1];
			
			if(lastTimeValue < this.__currentTime):
				raise SimulationRanBackwardsException();
			
			this.__currentTime = lastTimeValue;
			string = "Simulation "+ str(this.__currentNum) + " ended at "+ str(this.__currentTime)
			PySimLib.Log.Line(string+"\n===================================\n\n\n")
			print(string);
			
			if(this.__currentTime >= this.stopTime):
				print("Simulation done");
				break;
				
			#find a transition
			transition = this.__actMode.find_transition();
			if transition is None:
				print("Error, no transition found for mode ", this.__actMode.id);
				return;
			this.__transitionActive(transition);
		
			this.__currentNum += 1; #next sim
			
		PySimLib.Log.Line("");
		PySimLib.Log.Line("Overall timing info");
		PySimLib.Log.Line("Reading simulation results: " + str(readTime) + " seconds.");
		PySimLib.Log.Line("Simulation time: " + str(simTime) + " seconds");
		#TODO compile time
		
		this.__save_observer();
		this.__drawPlots();
