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

from exceptions.ModeException import ModeException


class IllegalMappingException(ModeException):
    # Constructor
    def __init__(this, fromMode, fromVar, transition, toVar):
        ModeException.__init__(this)

        this.__fromMode = fromMode
        this.__fromVar = fromVar
        this.__transition = transition
        this.__toVar = toVar

    # Magic methods
    def __str__(this):
        return "Illegal mapping (" + this.__fromVar + " : " + this.__toVar + ") in transition " + str(this.__transition.get_id()) + " from Mode " + str(this.__fromMode.get_id())
