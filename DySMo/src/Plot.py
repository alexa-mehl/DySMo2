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

from Definitions import *;

class Plot:
	#Constructor
	def __init__(this):
		this.xAxisVar = 'time';
		
	#Public methods
	def colorToColorString(this, color):
		if(color == Color.BLACK):
			return 'k';
		if(color == Color.BLUE):
			return 'b';
		if(color == Color.CYAN):
			return 'c';
		if(color == Color.GREEN):
			return 'g';
		if(color == Color.MAGENTA):
			return 'm';
		if(color == Color.RED):
			return 'r';
		#if(color == Color.WHITE):
			#return 'w';
		if(color == Color.YELLOW):
			return 'y';
		
		raise Exception("illegal color");
		
	#Abstract methods
	def getColor(this, modeId, simId, varName):
		raise NotImplementedError("Method 'getColor' of Class 'Plot' is abstract.");
