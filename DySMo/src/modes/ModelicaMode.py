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

from Mat.Mat import *;
from Mode import Mode;
from SimulationResult import *;

#This should be an abstract class that all modelica modes should derive from
class ModelicaMode(Mode):
	#Constructor
	def __init__(this):
		Mode.__init__(this);
		
		#Public members
		this.files = {}; #modelica modes have a set of files
		this.params = {}; #modelica models can have parameters
		
	#Protected Methods
	def _getModelicaClassString(this):
		cmd = this.modeRef;
		if(this.params):
			cmd = cmd + "(";
			for key in this.params:
				cmd = cmd + key + "=" + str(this.params[key]) + ",";
			cmd = cmd[:-1]; #remove last comma
			cmd = cmd + ")";
		
		return cmd;
		
	#Public methods
	def get_result(this, simNum):
		result = {};
		m_res = Mat();
		m_res.Load(this._getResultFileName(simNum) + ".mat");
		
		#dsres matrices are all transposed-.-
		names = m_res.GetMatrix("name");
		names.Transpose();
		dataInfo = m_res.GetMatrix("dataInfo");
		dataInfo.Transpose();
		
		for i in range(0, names.GetNumberOfStrings()):
			if(i == 0 and dataInfo.GetValue(0, i) == 0):
				dataMatrixIndex = 2; #hm... this is not necessarily the case... we need the biggest abscissa
			else:
				dataMatrixIndex = dataInfo.GetValue(0, i);
			dataMatrix = m_res.GetMatrix("data_" + str(dataMatrixIndex));
			k = dataInfo.GetValue(1, i);
			col = abs(k)-1;
			if(k > 0):
				sign = 1;
			else:
				sign = -1;
				
			currentVar = [];				
			for j in range(0, dataMatrix.GetNumberOfColumns()):
				currentVar.append(sign * dataMatrix.GetValue(j, col));
				
			if(names.GetString(i) == "Time"):
				result["time"] = currentVar;
			else:
				result[names.GetString(i)] = currentVar;
			this._end[names.GetString(i)] = sign * dataMatrix.GetValue(dataMatrix.GetNumberOfColumns()-1, col);
			
		return SimulationResult(result);
		
	def set_parameter(this, key, value):
		this.params[key] = value;
		
	def set_parameters(this, params):
		for key in params:
			this.set_parameter(key, params[key]);