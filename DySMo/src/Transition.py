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

from exceptions.IllegalMappingException import IllegalMappingException;

class Transition:
	#Constructor
	def __init__(this):
		this.__id = None;
		
	#Private methods
	def __mapStar(this, oldMode, newMode, valuesToSet):
		for key in oldMode._end:
			if(newMode.has_initValue(key)):
				valuesToSet[key] = oldMode.get_endValue(key);
		
	#Public methods
	def get_id(this):
		return this.__id;
		
	def init(this, id):
		this.__id = id;
		
	def mapping(this, oldMode, newMode):
		valuesToSet = {};
		mapping = this.mapping;
		
		for key in mapping:
			if(key == "*" and mapping[key] == "*"):
				this.__mapStar(oldMode, newMode, valuesToSet);
				continue;
				
			if(not oldMode.has_endValue(mapping[key])):
				raise IllegalMappingException(oldMode, key, this, mapping[key]);
				
			valuesToSet[key] = oldMode.get_endValue(mapping[key]);
			
		return valuesToSet;