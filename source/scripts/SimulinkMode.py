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

## This file represents the interface that have to be provided for each
## single modeling tool. If you want to add a tool to the framework, start here
from mode import mode
import os
import os.path
import scipy.io
import numpy as np
import pymat


#The name of the .mos script gernerated during the translation
SCRIPTNAME = "oMScript"
#set the oModelica /bin folder path
#do you like to extend your result directory? Then put in the string here:
EXTENSION = ""
STP_SIZE = "0.01"  # set your desired StepSize, constant for now
OMPath = r"C:/OpenModelica1.8.1/bin/omc "


class SimulinkMode(mode):
    def __init__(self, model, transLst, arrToSave, solver, startTime, stopTime, tolerance, IntervalNum, IntervalLen, fixed, modeID, modeName):
        self.modeName = modeName
        self.session = []
        mode.__init__(self, model, transLst, arrToSave, '', startTime, stopTime, tolerance, IntervalNum, IntervalLen, fixed, modeID, modeName, model.moFile)
        self.myModel.addModeToList(self)  #add yourself to mode list
        self.absModelPath = os.path.abspath(self.myModel.modelPath)
        self.dirUnderPath = modeName  #Contains the directoryName in ..\result\<underpath
        self.simData = []
    
    def translate(self):
        print 'not needed only session opened'
        
    def loadInitial(self):
        self.matlab = pymat.MatlabCom()
        self.matlab.open()
        self.simulationInformation.initNames, self.simulationInformation.initValue = self.__loadMat('init')
        self.simulationInformation.initData = []
        
    def __loadMat(self, file):
        self.matlab.eval ("run('" + self.absModelPath + "\\" + self.modeName + "_" + file + ".m')")        
        self.matlab.eval ("cd " + self.absModelPath)
        self.matlab.eval ("save " + self.modeName + "_" + file)
        test = scipy.io.loadmat(self.absModelPath + '\\' + self.modeName + "_" + file + '.mat')
        self.matlab.eval ("clear")    
        labels = test.keys()
        initValue = []
        initNames = []
        for item in labels:
            if len(item) < 3 or item[0:2] != '__':
                initNames.append(item)
                initValue.append(test[item][0][0])        
        return initNames, initValue
        
            
    def setInit(self, ind, arr):
        counter = 0
        for i in ind:            
            self.simulationInformation.initValue[i] = arr[counter]   
            counter = counter + 1
    
    def setInitSim(self):
        counter = 0;
        for name in self.simulationInformation.initNames:            
            self.matlab.put({name : self.simulationInformation.initValue[counter].astype('float')})   
            counter = counter + 1            
            
    def simulate(self):
        self.matlab.eval ("cd " + self.absModelPath)
        self.setInitSim()
        self.matlab.eval ("clear logsout") 
        self.matlab.eval ("sim('" + self.modeName + ".mdl', 'startTime', '" + str(self.simulationInformation.startTime) + "' , 'stopTime', '" + str(self.simulationInformation.stopTime) + "')")        
        self.matlab.eval ("logsout = ans")  
        
    def getEndVal(self):
        self.matlab.eval ("clear yout") 
        self.matlab.eval ("yout = logsout.get('logsout')")  
        self.matlab.eval ("[dataNames, simData] = extract2(yout)")
        self.simData = self.matlab.get('simData')
        dummy = self.matlab.get('dataNames').tolist()
        for item in dummy:
            self.simulationInformation.endNames.append(item[0])
        return self.simData[-1, -1], self.simData[-1, :]
            
        
    def addData(self, modeID, data, varNames):
        self.matlab.eval ("dataMatrix =  []")
        self.matlab.eval ("dataMatrix(:,1) = simData(:,end)")
        for var in varNames:
            self.matlab.eval ("ind = find(strncmp('" + var + "',dataNames,length('" + var + "')))")
            self.matlab.eval ("dataMatrix(:,end+1) = simData(:,ind)")
        
        self.matlab.put({'modeID' : modeID})
        self.matlab.eval ("m = ones(size(dataMatrix,1),1)")
        self.matlab.eval ("dataMatrix(:,end+1) =double(modeID) * m")
        
        dataMatrix = self.matlab.eval("dataMatrix= dataMatrix'")
        dataMatrix = self.matlab.get("dataMatrix")
        self.matlab.eval('clear dataMatrix m modeID ind')
            
        if len(data) == 0:
            data = dataMatrix
        else:
            data = np.concatenate((data, dataMatrix), 1)
            
        return data
            
    def getSwitchTo(self, end_val, end_names):
        self.matlab.eval ("ind = find(strncmp('switch_to',dataNames,length('switch_to')))")
        self.matlab.eval ("switch_to = simData(end,ind)")
        switch_to = self.matlab.get('switch_to')
        self.matlab.eval('clear ind switch_to')
        return switch_to