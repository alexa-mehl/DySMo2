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

#Local
from Mat.MatrixTypeEvaluator import *;

class Matrix:
	#Constructor
	def __init__(this, columns, rows):
		this.__rows = [];
		for y in range(0, rows):
			row = [];
			for x in range(0, columns):
				row.append(0);
			this.__rows.append(row);
		
		this.__desiredOutputEncoding = None;
		
	#Magic methods
	def __str__(this):
		return str(len(this.__rows[0])) + "x" + str(len(this.__rows)) + "Matrix";
	
	#Private methods
	def __WriteValue(this, value, target, encoding):
		if(encoding == 0): #TYPE_FLOAT64
			target.WriteFloat64(value);
		elif(encoding == 1): #TYPE_FLOAT32
			target.WriteFloat32(value);
		elif(encoding == 2): #TYPE_INT32
			target.WriteInt32(value);
		elif(encoding == 3): #TYPE_INT16
			target.WriteInt16(value);
		elif(encoding == 5): #TYPE_UINT8
			target.WriteByte(value);
		else:
			raise Exception("Not implemented for case " + str(encoding));
	
	#Public methods
	def GetNumberOfColumns(this):
		return len(this.__rows[0]);
		
	def GetNumberOfRows(this):
		return len(this.__rows);
		
	def GetValue(this, x, y):
		#print("y", y);
		#print("row[y]", this.__rows[y]);
		#print("x", x);
		#print("rows[y][x]", this.__rows[y][x]);
		return this.__rows[y][x];
		
	def SetDesiredOutputPrecision(this, encoding):
		this.__desiredOutputEncoding = encoding;
		
	def SetValue(this, x, y, value):
		this.__rows[y][x] = value;
		
	def Transpose(this):
		nCols = this.GetNumberOfColumns();
		nRows = this.GetNumberOfRows();
		rows = this.__rows;
		
		this.__init__(nRows, nCols);
		
		for x in range(0, nCols):
			for y in range(0, nRows):
				this.SetValue(y, x, rows[y][x]);
		
	def Write(this, matrixName, target):
		if(this.__desiredOutputEncoding is None):
			evaluator = MatrixTypeEvaluator(this.__rows);
			encoding = evaluator.GetType();
		else:
			encoding = this.__desiredOutputEncoding;
			
		target.WriteUInt32(encoding * 10); #type
		target.WriteUInt32(this.GetNumberOfRows()); #rows
		target.WriteUInt32(this.GetNumberOfColumns()); #cols
		target.WriteUInt32(0); #imagf
		target.WriteUInt32(len(matrixName)+1); #namelen
		target.WriteASCII(matrixName); #name
		target.WriteByte(0); #\0
		
		#real part
		for x in range(0, this.GetNumberOfColumns()):
			for y in range(0, this.GetNumberOfRows()):
				this.__WriteValue(this.__rows[y][x], target, encoding);
		
		#no imag part