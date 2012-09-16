
# -*- coding: utf-8 -*-
"""
  Copyright (C) 2012  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
  This file is part of modelica3d 
  (https://mlcontrol.uebb.tu-berlin.de/redmine/projects/modelica3d-public).

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

#==============================================================================
# This file defines some basic classes for the template to specify variable-structure models.
# These classes are not necessary in the rest of the framework.
#==============================================================================



## Simulation information, unique for all modes
class simInfo:
    ## Constructor
    # @param
    # @param
    def __init__(self):
        self.startTime = []
        self.stopTime = []
        self.solver = []
        self.tolerance = []
        self.intervalNum = []
        self.intervalLen = []
        self.fixed = []


## model
class model:
    ## Constructor
    # @param
    # @param
    def __init__(self):
        self.moFile = []
        self.modelPath = []
        self.resFolder = []
        self.plotList = []
        self.modes = []
        self.arrToSave = []
        self.simInfo = []
        
        
## model
class mode:
    ## Constructor
    # @param
    # @param
    def __init__(self):
        self.arrToSave = []
        self.simInfo = []
        self.modeName = []
        self.tool = []
        self.transitions = []
        
        
        
class trans:
## Constructor
    #  @param modeName The mode name corresponding with the modelName in
    #                  class model
    #  @param modeID   A unique Mode number to identify the mode to switch
    #  @param condition set any switching conditions (string, optional)
    #  @param outList  Means a switch to mode "switch to"
    #  @param inList   was mapped to the corresponding outList (both lists have
    #                  to have the same length)
    def __init__(self):
        self.modeIDToSw = []
        #self.condition = []
        self.outName = []
        self.inName = []