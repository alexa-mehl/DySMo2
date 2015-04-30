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

class TextMatrix:
	#Constructor
	def __init__(this, nStrings):
		this.__strings = [];
		for i in range(0, nStrings):
			this.__strings.append([]);
			
	#Private methods
	def __GetLongestStringLength(this):
		length = 0;
		for x in this.__strings:
			if(len(x) > length):
				length = len(x);
				
		return length;
	
	#Public methods		
	def GetNumberOfStrings(this):
		return len(this.__strings);
		
	def GetString(this, row):
		result = "";
		str = this.__strings[row];
		for i in range(0, len(str)):
			if(str[i] == 0): #end of string
				break;
			result = result + chr(str[i]);
		return result.rstrip();
		
	def SetString(this, y, str):
		for i in range(0, len(str)):
			this.SetValue(i, y, str[i]);
		
	def SetValue(this, x, y, value):
		str = this.__strings[y];
		length = len(str);
		while(length <= x):
			str.append(0);
			length = length + 1;
			
		if(type(value) == int):
			str[x] = value;
		else:
			str[x] = ord(value);
			
	def Transpose(this):
		nCols = this.__GetLongestStringLength();
		nRows = this.GetNumberOfStrings();
		rows = this.__strings;
		
		this.__init__(nCols);
		
		for x in range(0, nCols):
			for y in range(0, nRows):
				this.SetValue(y, x, rows[y][x]);
		
	def Write(this, matrixName, target):
		target.WriteUInt32(51); #type
		target.WriteUInt32(this.GetNumberOfStrings()); #rows
		target.WriteUInt32(this.__GetLongestStringLength()); #cols
		target.WriteUInt32(0); #imagf
		target.WriteUInt32(len(matrixName)+1); #namelen
		target.WriteASCII(matrixName); #name
		target.WriteByte(0); #\0
		
		#real part
		for x in range(0, this.__GetLongestStringLength()):
			for y in range(0, this.GetNumberOfStrings()):
				if(x > len(this.__strings[y])-1):
					target.WriteByte(0);
				else:
					target.WriteByte(this.__strings[y][x]);
		
		#no imag part