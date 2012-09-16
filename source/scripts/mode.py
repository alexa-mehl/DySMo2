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


import sys


## record class to avoid confusing, nested dataarrays
class transition:
## Constructor
    #  @param modeName The mode name corresponding with the modelName in
    #                  class model
    #  @param modeID   A unique Mode number to identify the mode to switch
    #  @param condition set any switching conditions (string, optional)
    #  @param outList  Means a switch to mode "switch to"
    #  @param inList   was mapped to the corresponding outList (both lists have
    #                  to have the same length)
    def __init__(self, switchTo, condition, outList, inList):
        self.modeIDToSw = switchTo
        self.modeIndexToSW = (switchTo - 1)
        self.condition = condition
        # these two have to be mapped once, not by the user
        self.outName = outList
        self.inName = inList
        self.myOutNameInd = []
        self.followInNameInd = []
        #the 4 following lists are only used, if wildcards are used
        self.nestedOutIndex = []
        self.nestedOutNames = []
        self.nestedFolIndex = []
        self.nestedFolNames = []
        # represents the indices from the vars the user is interested in
        self.indVarsToSimulOut = []


## Simulation information, unique for all modes
class simInformation:
    ## Constructor
    # @param
    # @param
    def __init__(self, startTime, stopTime, solver, tolerance, IntervalNum,
                 IntervalLen, fixed):
        self.startTime = startTime
        self.stopTime = stopTime
        self.solver = solver
        self.tolerance = tolerance
        self.intervalNum = IntervalNum
        self.intervalLen = IntervalLen
        self.fixed = fixed
        self.initData = []
        self.initValue = []
        self.initNames = []
        self.endValue = []
        self.endNames = []
        #self.resPath = resultPath

    def setInitData(self, data):
        self.initData = data


## This class should map all special tool settings like solver settings to one
#    unique format that can used in the following program
class mode(object):
    ## Constructor
    # @param transLst Contains all information about the simulation. For
    #        further information about the attributes refer to class transition
    def __init__(self, model, transLst, arrToSave, solver, startTime, stopTime,
                 tolerance, IntervalNum, IntervalLen, fixed, modeID, modeName,
                 moFile):
            self.transList = []
            for transitions in transLst:
                self.transList.append(transitions)
            self.arrToSave = []
            self.arrToSave.append(arrToSave)
            self.simulationInformation = simInformation(startTime, stopTime,
                                                        solver, tolerance,
                                                        IntervalNum,
                                                        IntervalLen, fixed)
            self.modeID = modeID
            self.moFile = moFile      # corresponding mo File
            self.modeName = modeName  # name
            self.myModel = model      # corresponding model
            self.absModelPath = ""

    # mode is abstract, its not allowed to instantiate a basis object
    def mapSolver(self, solv):
        raise Exception('Method not implemented for basis class!')

    def getModeID(self):
        raise Exception('Method not implemented for basis class!')

    def translate(self, modeName, resultPath, moFile):
        raise Exception('Method not implemented for basis class!')

    def loadData(self):
        raise Exception('Method not implemented for basis class!')

    def simulate(self):
        raise Exception('Method not implemented for basis class!')

    def getEndVal(self, data):
        raise Exception('Method not implemented for basis class!')

    def addData(self, path, modeID, data, varNames):
        raise Exception('Method not implemented for basis class!')

    def setModeName(self, name):
        raise Exception('Method not implemented for basis class!')

        ## This function collects switch_to form the given end_values and names
        # @param endValues The database from a mode that terminates
        # @param endNames  The corresponding names in the database
        # @param index     The index where the switch_to variable can be found
        # @return swTo     Integer with the switch_to from the simulation,
        #                  -1 if switch to is not vaild
    def getSwitchTo(self, endValues, endNames):
        #get the index from the name
        helpInd = -1
        try:
            helpInd = endNames.index("switch_to")
        except ValueError:
            print "switch_to not found, expected last mode -> break while"
            return -1
        try:
            return endValues[helpInd]
        except IndexError:
            print "Error in __getSwitchTo:"
            sys.exit("Corresponding value not found")
