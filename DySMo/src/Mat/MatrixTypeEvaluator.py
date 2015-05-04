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

TYPE_FLOAT64 = 0;
TYPE_FLOAT32 = 1;
TYPE_INT32 = 2;
TYPE_INT16 = 3;
TYPE_UINT16 = 4;
TYPE_UINT8 = 5;

class MatrixTypeEvaluator:
	#Constructor
	def __init__(this, rows):
		this.__type = TYPE_UINT8;
		this.__min = 0;
		this.__max = 255;
		
		for row in rows:
			for col in row:
				if(this.__type == TYPE_FLOAT64):
					return; #max precision, no need to continue
				this.__NextValue(col);
					
	#Private methods
	def __NextValue(this, value):
		if(isinstance(value, float) and (not value.is_integer())): #any float that can't be an int... 
			this.__type = TYPE_FLOAT64;
			return;
			
		#value is not float from here
		
		if(this.__type == TYPE_FLOAT32): #we came here because of a very large integer
			return; #already highest precision for non float matrix
			
		#The internal type is some int type
		
		if(value < this.__min):
			this.__min = value;
		elif(value > this.__max):
			this.__max = value;
			
		if(this.__min >= 0 and this.__max <= 255):
			this.__type = TYPE_UINT8;
			return;
		if(this.__min >= -32768 and this.__max <= 0x7FFF):
			this.__type = TYPE_INT16;
			return;
		if(this.__min >= 0 and this.__max <= 0xFFFF):
			this.__type = TYPE_UINT16;
			return;
		if(this.__min >= -2147483648 and this.__max <= 0x7FFFFFFF):
			this.__type = TYPE_INT32;
			return;
			
		this.__type = TYPE_FLOAT32; #we have only ints but we can't put them in int32
	
	#Public methods
	def GetType(this):
		return this.__type;