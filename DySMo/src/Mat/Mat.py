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

#Global
import struct;
#Local
from Mat.Matrix import *;
from Mat.TextMatrix import *;

class Mat:
	#Constructor
	def __init__(this):
		this.__matrices = {};
		
	#Magic methods
	def __str__(this):
		result = "";
		for key in this.__matrices:
			m = this.__matrices[key];
			if(type(m) == Matrix):
				result = result + key + " " + str(m.GetNumberOfRows()) + "x" + str(m.GetNumberOfColumns()) + ", ";
			elif(type(m) == TextMatrix):
				result = result + key + " " + str(m.GetNumberOfStrings()) + ", ";
		return result;
	
	#Private methods
	def __ReadMatrix(this, input):
		type = this.__ReadUInt32(input);
		numberFormat = int(type / 1000);
		if(not(numberFormat == 0)):
			raise Exception("NOT IMPLEMENTED");
		if(not(int((type % 1000) / 100) == 0)):
			raise Exception("Not a Matlab v4 file");
		dataFormat = int((type % 100) / 10);
		matrixType = type % 10;
		rows = this.__ReadUInt32(input);
		cols = this.__ReadUInt32(input);
		imaginaryFlag = this.__ReadUInt32(input);
		if(imaginaryFlag == 1):
			raise Exception("NOT IMPLEMENTED");
		nameLength = this.__ReadUInt32(input);
		name = this.__ReadMatrixName(input, nameLength);
		
		if(matrixType == 0): #full numeric matrix
			m = this.AddMatrix(name, cols, rows);
		elif(matrixType == 1): #text matrix
			m = this.AddTextMatrix(name, rows);
			
		this.__ReadMatrixData(input, dataFormat, rows, cols, m);
		
	def __ReadMatrixData(this, input, dataFormat, rows, cols, matrix):
		for x in range(0, cols):
			for y in range(0, rows):
				matrix.SetValue(x, y, this.__ReadMatrixDataEntry(input, dataFormat));
			
	def __ReadMatrixDataEntry(this, input, dataFormat):
		if(dataFormat == 0): #float64
			return struct.unpack('d', input.read(8))[0];
		elif(dataFormat == 1): #float32
			return struct.unpack('f', input.read(4))[0];
		elif(dataFormat == 2): #int32
			return this.__ReadInt32(input);
		elif(dataFormat == 5): #uint8
			b = input.read(1);
			return b[0];
		else:
			raise Exception("NOT IMPLEMENTED" + str(dataFormat));
	
	def __ReadMatrixName(this, input, length):
		result = "";
		while(length > 1):
			b = input.read(1);
			result = result + chr(b[0]);
			length = length - 1;
		input.read(1); #null byte
		return result;
		
	def __ReadInt32(this, input):
		raw = input.read(4);
		value = (raw[3] << 24) | (raw[2] << 16) | (raw[1] << 8) | raw[0];
		
		if(raw[3] & 0x80):
			return -0x100000000 + value;
		
		return value;
		
	def __ReadUInt32(this, input):
		raw = input.read(4);
		
		return (raw[3] << 24) | (raw[2] << 16) | (raw[1] << 8) | raw[0];
		#return (raw[0] << 24) | (raw[1] << 16) | (raw[2] << 8) | raw[3];
	
	#Public methods
	def AddMatrix(this, name, columns, rows):
		m = Matrix(columns, rows);
		this.__matrices[name] = m;
		return m;
	
	def AddTextMatrix(this, name, nStrings):
		m = TextMatrix(nStrings);
		this.__matrices[name] = m;
		return m;
		
	def GetMatrix(this, name):
		return this.__matrices[name];
		
	def Load(this, fileName):
		file = open(fileName, "rb");
		file.seek(0, 2); #2 = SEEK_END
		fileSize = file.tell();
		file.seek(0, 0); #0 = SEEK_SET
		
		while(file.tell() < fileSize): #Read matrices
			this.__ReadMatrix(file);
			
		file.close();
		
	def Write(this, target):
		for key in this.__matrices:
			this.__matrices[key].Write(key, target);