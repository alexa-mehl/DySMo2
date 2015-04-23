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

import struct;

class OutputStream:
	#Constructor
	def __init__(this, target):
		this.__target = target;
		
	#Public methods
	def WriteASCII(this, str):
		for x in str:
			this.WriteByte(x);
			
	def WriteByte(this, value):			
		if(type(value) == float):
			value = int(value);
		if(type(value) == str):
			value = ord(value);
			
		this.__target.write(bytes([value]));
		
	def WriteFloat32(this, value):
		s = struct.pack('f', value);
		this.__target.write(s);
		
	def WriteFloat64(this, value):
		s = struct.pack('d', value);
		this.__target.write(s);
		
	def WriteInt16(this, value):
		if(type(value) == float):
			value = int(value);
		
		this.WriteByte(value & 0xFF);
		this.WriteByte((value >> 8) & 0xFF);
		
	def WriteInt32(this, value):
		this.WriteByte(value & 0xFF);
		this.WriteByte((value >> 8) & 0xFF);
		this.WriteByte((value >> 16) & 0xFF);
		this.WriteByte((value >> 24) & 0xFF);
		
	def WriteUInt32(this, value):
		this.WriteByte(value & 0xFF);
		this.WriteByte((value >> 8) & 0xFF);
		this.WriteByte((value >> 16) & 0xFF);
		this.WriteByte((value >> 24) & 0xFF);