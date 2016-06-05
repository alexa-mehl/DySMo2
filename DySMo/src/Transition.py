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

class Transition:
	#Constructor
	def __init__(this):
		this.__id = None;
		
	#Public methods
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
