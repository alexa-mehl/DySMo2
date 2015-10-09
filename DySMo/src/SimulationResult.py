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

"""
This class holds the values that a simulation generates.
The values in the object are stored in a dictionary that maps each variable to a vector of values of this variable.
The following should illustrate that:
values = 
{
	"x" : [t1(x), t2(x)....],
	"y" : [t1(y), t2(y)....],
	"time" : [t1(time), t2(time)...],
	...
}

Note: Also the simulation time should be present with the name "time" (CASE SENSITIVE).
"""
class SimulationResult:
	#Constructor
	#Args:
	# values - Simulation result values in a form as illustrated above
	def __init__(this, values):
		this.__values = values;
		
	#Public methods
	#Returns a datapoint of a trace of a variable
	#
	#Args:
	# varName - variable trace to be read
	# nTimesBack - number of time steps to move backwards in time (defaults to 0 meaning last available value)
	def get_value(this, varName, nTimestepsBack = 0):
		datapoints = this.__values[varName];
		
		return datapoints[len(datapoints) - 1 - nTimestepsBack];
		
	#Returns the result dictionary		
	def get_values(this):
		return this.__values;
