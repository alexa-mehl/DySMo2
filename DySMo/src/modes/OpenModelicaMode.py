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
import xml;
import xml.dom;
import xml.dom.minidom;
import os;
import shutil;
from subprocess import call;
#Local
from Mat.Mat import Mat;
from globals import *;
from modes.ModelicaMode import ModelicaMode;
from exceptions.UncompiledModeException import UncompiledModeException;

#The name of the .mos script generated during the translation
SCRIPTNAME = "oMScript"

class OpenModelicaMode(ModelicaMode):
	#Constructor
	def __init__(this):
		ModelicaMode.__init__(this);
		
	#Public methods
	def compile(this):
		#write a mos file to be executed by openmodelica
		mosfile = open(SCRIPTNAME + '.mos', 'w', 1);
		mosfile.write("loadModel(Modelica);\r\n")
		
		for item in this.files:
			mosfile.write("loadFile(\"" + item + "\");\r\n");
			
		# do a dummy simulation since it is not yet possible to do a translation only
		mosfile.write("simulate(" + this._getModelicaClassString() + ", startTime = " + str(this.get_model().startTime) + ", stopTime = " + str(this.get_model().stopTime) + ", method = \"" + this.solver.name + "\", outputFormat=\"mat\");\r\n");
		mosfile.close();
		
		#suppress output
		fnull = open(os.devnull, 'w');
		
		#call the open modelica compiler
		ret = call(g_cfg.GetValue("OpenModelica", "PathExe") + ' ' + this.get_model().getPath() + os.sep + SCRIPTNAME + '.mos' + ' Modelica', shell = True, stdout=fnull);
		
		#Remove unnecessary files
		this._deleteFile(this.modeRef + ".c");
		this._deleteFile(this.modeRef + ".libs");
		this._deleteFile(this.modeRef + ".log");
		this._deleteFile(this.modeRef + ".makefile");
		this._deleteFile(this.modeRef + ".o");
		this._deleteFile(this.modeRef + "_01exo.c");
		this._deleteFile(this.modeRef + "_01exo.o");
		this._deleteFile(this.modeRef + "_02nls.c");
		this._deleteFile(this.modeRef + "_02nls.o");
		this._deleteFile(this.modeRef + "_03lsy.c");
		this._deleteFile(this.modeRef + "_03lsy.o");
		this._deleteFile(this.modeRef + "_04set.c");
		this._deleteFile(this.modeRef + "_04set.o");
		this._deleteFile(this.modeRef + "_05evt.c");
		this._deleteFile(this.modeRef + "_05evt.o");
		this._deleteFile(this.modeRef + "_06inz.c");
		this._deleteFile(this.modeRef + "_06inz.o");
		this._deleteFile(this.modeRef + "_07dly.c");
		this._deleteFile(this.modeRef + "_07dly.o");
		this._deleteFile(this.modeRef + "_08bnd.c");
		this._deleteFile(this.modeRef + "_08bnd.o");
		this._deleteFile(this.modeRef + "_09alg.c");
		this._deleteFile(this.modeRef + "_09alg.o");
		this._deleteFile(this.modeRef + "_10asr.c");
		this._deleteFile(this.modeRef + "_10asr.o");
		this._deleteFile(this.modeRef + "_11mix.c");
		this._deleteFile(this.modeRef + "_11mix.o");
		this._deleteFile(this.modeRef + "_11mix.h");
		this._deleteFile(this.modeRef + "_12jac.c");
		this._deleteFile(this.modeRef + "_12jac.h");
		this._deleteFile(this.modeRef + "_12jac.o");
		this._deleteFile(this.modeRef + "_13opt.c");
		this._deleteFile(this.modeRef + "_13opt.o");
		this._deleteFile(this.modeRef + "_13opt.h");
		this._deleteFile(this.modeRef + "_14lnz.c");
		this._deleteFile(this.modeRef + "_14lnz.o");
		this._deleteFile(this.modeRef + "_functions.c");
		this._deleteFile(this.modeRef + "_functions.h");
		this._deleteFile(this.modeRef + "_functions.o");
		this._deleteFile(this.modeRef + "_includes.h");
		this._deleteFile(this.modeRef + "_literals.h");
		this._deleteFile(this.modeRef + "_model.h");
		this._deleteFile(this.modeRef + "_records.c");
		this._deleteFile(this.modeRef + "_records.o");
		this._deleteFile(this.modeRef + "_res.mat");
		this._deleteFile(SCRIPTNAME + ".mos"); #we also don't need the mos script anymore
		
		#Rename important files
		this._renameFile(this.modeRef + ".exe", "m" + str(this.get_id()) + ".exe");
		this._renameFile(this.modeRef + "_init.xml", "m" + str(this.get_id()) + "_init.xml");
		this._renameFile(this.modeRef + "_info.xml", "m" + str(this.get_id()) + "_info.xml");
			
	def read_init(this):
		store = False;
		
		if(not this._fileExists("m" + str(this.get_id()) + "_init.xml")):
			raise UncompiledModeException(this);		
		
		initDom = xml.dom.minidom.parse("m" + str(this.get_id()) + "_init.xml");
		mv = initDom.getElementsByTagName("ModelVariables")[0];
		
		for var in mv.childNodes:
			if(var.nodeType == xml.dom.Node.ELEMENT_NODE):
				if(var.getAttribute("classType").find("Par") == -1): #we want everything that is not a parameter
					varName = var.getAttribute("name");
					
					store = False;
					for node in var.childNodes: #find the value
						if(node.nodeType == xml.dom.Node.ELEMENT_NODE):
							if(node.getAttribute("useStart") == "false"):
								store = False;
								break;
							
							start = node.getAttribute("start");
							store = True;
							if(start == ""):
								value = 0;
							else:
								value = float(start);
							break;
					
					if(store):
						this._init[varName] = value;
						
	def save_init(this, startTime):
		initDom = xml.dom.minidom.parse("m" + str(this.get_id()) + "_init.xml");
		mv = initDom.getElementsByTagName("ModelVariables")[0];
		de = initDom.getElementsByTagName("DefaultExperiment")[0];
		
		if(this.solver.stepSize == 0):
			this.solver.stepSize = 1e-3; #this is bad... but else OM simulates endlessly
		
		#Set experiment values
		de.setAttribute("startTime", str(startTime));
		de.setAttribute("stepSize", str(this.solver.stepSize));
		de.setAttribute("tolerance", str(this.solver.tolerance));
		de.setAttribute("solver", this.solver.name);
		
		#Set initial variables		
		for var in mv.childNodes:
			if(var.nodeType == xml.dom.Node.ELEMENT_NODE):
				varName = var.getAttribute("name");
				
				if(varName not in this._init):
					continue;
					
				for node in var.childNodes: #find the value
					if(node.nodeType == xml.dom.Node.ELEMENT_NODE):
						#node.setAttribute("useStart", "true");
						#node.setAttribute("fixed", "true");
						node.setAttribute("start", str(this._init[varName]));
						break;
						
		this._deleteFile("m" + str(this.get_id()) + "_init_sim.xml");
		file = open("m" + str(this.get_id()) + "_init_sim.xml", "w");
		initDom.writexml(file);
		file.close();
		
	def simulate(this):
		#suppress output
		fnull = open(os.devnull, 'w');
		
		#info file can't be specified as arg to openmodelica
		shutil.copyfile("m" + str(this.get_id()) + "_info.xml", this.modeRef + "_info.xml");
		
		ret = call("m" + str(this.get_id()) + ".exe -f m" + str(this.get_id()) + "_init_sim.xml", shell = True, stdout=fnull);
		
		#keep things clean
		this._deleteFile(this.modeRef + "_info.xml");
		#this._deleteFile("m" + str(this.get_id()) + "_init_sim.xml");
		
		#move results to result path
		shutil.move(this.modeRef + "_res.mat", this._getResultFileName(this.get_model().getCurrentSimulationNumber()) + ".mat");