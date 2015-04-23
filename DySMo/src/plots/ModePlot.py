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

from Definitions import Color;
from Plot import Plot;

class ModePlot(Plot):
	#Constructor
	def __init__(this):
		Plot.__init__(this);
		this.__counter = 0;
		this.__vars = {};
		
	#Private methods
	def getVarCounter(this, varName):
		if(varName not in this.__vars):
			this.__vars[varName] = this.__counter;
			this.__counter -= 1;
			
		return this.__vars[varName];
		
	#Public methods
	def getColor(this, modeId, simId, varName):
		colId = ((this.getVarCounter(varName)+ modeId - 1) % 7)+1;
		if(varName in this.vars):
			return Color(colId);
		return None;