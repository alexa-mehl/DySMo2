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
from utility import Solver
import scipy.io
import os
import numpy as np
import win32ui
import dde
import subprocess
import time
import shutil    # high level file operations (e.g. delete non empty directory)
import DyMatStruk as mat
import sys
import string
import globalHeader as gl


## A concept to make the server connection to dymola static,
## so that not every mode must open a dymola instance
class dymolaConnector():
    dyIsOpen = False        # allow only one open instance of dymola
    DDEserver = ""
    conversation = ""
    actOpenedMoFiles = []   # a list with all opened mo files,
                            # prevent to open a mo file twice


## The different modes with their individual settings, inherit from mode
class dymolaMode(mode):
    def __init__(self, model, transLst, arrToSave, solver, startTime, stopTime,
                 tolerance, IntervalNum, IntervalLen, fixed, modeID, modeName):
        self.solver = "euler"
        #call the parent constructor
        mode.__init__(self, model, transLst, arrToSave, self.mapSolver(solver),
                      startTime, stopTime, tolerance, IntervalNum, IntervalLen,
                      fixed, modeID, modeName, model.moFile)
        #add yourself to mode list
        self.myModel.addModeToList(self)
        self.absModelPath = os.path.abspath(self.myModel.modelPath)
        self.absModePath = self.absModelPath + '\\' + self.myModel.resFolder \
        + '\\' + getDirName(self.modeName)

    ## mapSover takes on of the given Solver in utility.py and maps it to tool
    #  specified settings. for dymola specific settings, refer to "dsin.txt"
        # @param solv One of the solvers, given in Solver (refer to utility.py)
    def mapSolver(self, solv):
        if solv == Solver.EULER:
            self.solver = "euler"
            return 11
        elif solv == Solver.DASSL:
            self.solver = "dassl"
            return 8
        elif solv == Solver.LSODAR:
            self.solver = "lsodar"
            return 4
        elif solv == Solver.RKFIX2:
            self.solver = "rkfix2"
            return 12
        elif solv == Solver.RKFIX3:
            self.solver = "rkfix3"
            return 13
        elif solv == Solver.RKFIX4:
            self.solver = "rkfix4"
            return 14
        elif solv == Solver.RADAU:
            self.solver = "radau"
            return 15
        elif solv == Solver.LSODE1:
            self.solver = "lsode1"
            return 2
        elif solv == Solver.LSODE2:
            self.solver = "lsode2"
            return 3
        elif solv == Solver.DOPRI5:
            self.solver = "dopri5"
            return 5
        elif solv == Solver.DOPRI8:
            self.solver = "dopri8"
            return 6
        elif solv == Solver.GRK4T:
            self.solver = "grk4t"
            return 7
        elif solv == Solver.ODASSL:
            self.solver = "odassl"
            return 9
        elif solv == Solver.MEXX:
            self.solver = "mexx"
            return 10
        elif solv == Solver.DEABM:
            self.solver = "deabm"
            return 1
        #default:
        else:
            sys.exit("Wrong solver settings")

    def openModel(self, moFile):
        #is the mo file already open?
        if (moFile in dymolaConnector.actOpenedMoFiles):
            return
        else:
            #remember the actual working dir
            currentDir = os.path.abspath(os.curdir)
            os.chdir(self.myModel.modelPath)
            dymolaConnector.conversation.Exec("openModel(\"" + moFile + "\")")
            #switch back to actual directory
            os.chdir(currentDir)
            #now the mo File is opened
            dymolaConnector.actOpenedMoFiles.append(moFile)
            return

    # open interface for switch.py, for same behavior from all classes
    def translate(self):
        self.__openDymola()
        #open all needed mo files
        for uFile in self.myModel.moFile:
            self.openModel(uFile)
        fullName = self.modeName
        underpath = self.myModel.resultPath + "\\" + getDirName(fullName)
        #check weather the sub directory already exists
        if os.path.exists(underpath) != 1:
            os.makedirs(underpath)
        else:
            #delete all files in resultFolder and create an empty folder
            shutil.rmtree(underpath)
            os.makedirs(underpath)
        #dymola: switch to result folder to save the results at the right place
        dymolaConnector.conversation.Exec("cd(\"" + self.myModel.resFolder
                                         + "/" + getDirName(fullName) + "\")")
        dymolaConnector.conversation.Exec("simulateModel(\"" + fullName + "\",\
                                stopTime=0, method= \"" + self.solver + "\" )")
        #dymolaConnector.conversation.Exec("translateModel(\"" + fullName + "\")")
        #dymola: change back to actual model directory
        dirNameValidForDym = string.replace(self.absModelPath, '\\', '/')
        dymolaConnector.conversation.Exec("cd(\"" + dirNameValidForDym + "\")")

    def loadInitial(self):
        # return self.toInterface.loadData(self.modeName)
        currentDir = os.path.abspath(os.curdir)
        os.chdir(gl.PP_ALISTDIR)
        path = self.absModePath

        if os.path.isfile(path + '\dsin.mat'):
            os.remove(path + '\dsin.mat')

        if self.modeID == 1:
            if os.path.isfile(path + '\dsin.mat') == False:
                os.system('alist.exe -b ' + path + '\dsin.txt ' + path\
                           + '\dsin.mat')
        else:               
            if os.path.isfile(path + '\dsin.mat') == False:
                os.system('alist.exe -b ' + path + '\dsfinal.txt ' + path\
                           + '\dsin.mat')
        loadMathPath = path + '\dsin.mat'
        loadMathPath.replace("/", "\\")
        data = scipy.io.loadmat(loadMathPath)
        x0names_1, x0_1 = self.__getVar(data)
        os.chdir(currentDir)
        #data['initialValue'][:,0] = data2['initialValue'][:,0] 
        self.simulationInformation.initData = data
        self.simulationInformation.initValue = x0_1[:, 1]
        self.simulationInformation.initNames = x0names_1
        self.simulationInformation.endData = data
        self.simulationInformation.endValue = x0_1[:, 1]
        self.simulationInformation.endNames = x0names_1
        self.simulationInformation.endNames = x0names_1

    def simulate(self):
        #self.toInterface.simulate(self.modeName, self.simulationInformation)
        self.saveInit_all()
        currentDir = os.path.abspath(os.curdir)
        path = self.absModePath
        # start dymosim.exe
        os.chdir(path)
        os.system(path + '\dymosim.exe ' + path + '\dsin.mat ' + path
                  + '\dres.mat>null')
        # rename from dsfinal to dsfinal.mat
        # don t work with the -b option ...
        os.chdir(gl.PP_ALISTDIR)
        os.system('alist.exe -b ' + path + '\dsfinal.txt ' + path
                  + '\dsfinal.mat ')
        os.chdir(currentDir)

    def setInit(self, ind, arr):
        #TODO: Warum zusaetzlich initData['initialValue']????
        self.simulationInformation.initData['initialValue'][ind, 1] = arr
       
    def getEndVal(self):
        data = scipy.io.loadmat(self.absModePath + '/dsfinal.mat')
        exp = data['experiment']
        dummy, x = self.__getVar(data)
        t = exp[0][0]
        self.simulationInformation.endValue = x[:, 1]
        self.simulationInformation.initData = data	
        self.simulationInformation.initValue = x[:, 1]
        return t, x[:, 1]

    def addData(self, modeID, data, varNames):
        #return self.toInterface.addData(path, modeID, data, varNames)
        s = mat.DyMatStruk(self.absModePath + '\dres.mat')
        a = s.getVarArray(varNames)
        temp = [None] * len(a[0])
        ind = 0
        for dummy in temp:
            temp[ind] = modeID
            ind = ind + 1
        #new data file?
        if len(data) == 0:
            data = np.concatenate((a, [temp]), axis=0)
        else:
            myarr = np.concatenate((a, [temp]), axis=0)
            data = np.concatenate((data, myarr), 1)
        return data

    def __getVar(self, data):
        # gives  all names and values from dsin file
        initialname = [s.strip() for s in data['initialName']]
        initialname = [s.replace("\x00", "") for s in initialname]
        initialValue = data['initialValue']
        return initialname, initialValue

    ## Save all initial data to the dsin.mat, call this before the simulation
    ## start
    def saveInit_all(self):
        modelName = self.modeName
        simParameter = self.simulationInformation
        #only use the last part for directory
        mNameOnly = getDirName(modelName)
        # saves the initial data in dsin.mat to start the simulation.
        # The default can be changes through the input parameters here all
        # initial values are given in one matrix
        Aclass = simParameter.initData['Aclass']
        experiment = simParameter.initData['experiment']
        experiment[0] = simParameter.startTime
        experiment[1] = simParameter.stopTime
        experiment[2] = simParameter.intervalLen
        experiment[3] = simParameter.intervalNum
        experiment[4] = simParameter.tolerance
        experiment[5] = simParameter.fixed
        experiment[6] = simParameter.solver
        initialname = simParameter.initData['initialName']
        method = simParameter.initData['method']
        settings = simParameter.initData['settings']
        scipy.io.savemat(self.absModelPath + '\\' + self.myModel.resFolder
                         + '\\' + mNameOnly + '/dsin.mat', mdict=\
                         {'Aclass': (Aclass), 'experiment': (experiment), \
                          'initialName': (initialname), \
                          'initialValue': (self.simulationInformation.\
                                           initData['initialValue']), \
                          'method': (method), 'settings': (settings)}, \
                          format='4')

    def __openDymola(self):
        if(dymolaConnector.dyIsOpen == True):
            return
        else:
            dymolaConnector.dyIsOpen = True
            dymolaConnector.DDEserver = dde.CreateServer()
            dymolaConnector.DDEserver.Create("TestClient")
            currentDir = os.path.abspath(os.curdir)
            os.chdir(self.myModel.modelPath)
            dymolaConnector.conversation = dde.CreateConversation(\
                                           dymolaConnector.DDEserver)
            subprocess.Popen([gl.PP_DYMOLAPATH], stdin=subprocess.PIPE)
            time.sleep(5)
            dymolaConnector.conversation.ConnectTo("dymola", " ")
            os.chdir(currentDir)
            dymolaConnector.conversation.Exec("OutputCPUtime:=true;")

    ## Close Dymola
    def __closeDymola(self):
        if(self.dyIsOpen):
            dymolaConnector.conversation.Exec("exit()")
            dymolaConnector.dyIsOpen = False
        else:
            return

    ## Additional function: save ALL simulation results in an additional
    #  folder.
    # @param folder: the absolute path, where the files are saved
    # @param transNo: a transition counter, to find the data it will be
    #                 saved as part of the filename
    def saveAllData(self, folder, transNo):
        shutil.copy(self.absModePath + '\dres.mat', folder)
        # rename the dres.mat file
        shutil.move(folder + '\dres.mat', folder + '\\allData_TransNo_'
                    + str(transNo) + '.mat')

#TODO: consider if this functions should be global lib (utility.py) functions?
    ## The following functions helps to cut a given string with a given
    #  separator '.' or '_' and get the first or last part


    ## Get the directory name in the correct format
    # @param modleName A string separated by '.'like: "iam.aString.sep"
    # @return last part of the string separated by "_": "aString_sep"
def getDirName(modelName):
        return __cutStringsWSeperator(modelName, "_")


    # help functions
def __cutStringsWSeperator(strToCut, seperator):
        spltList = strToCut.split(".")  # after operation spltList[0]: mo file
                                                        # spltList[1]: modeName
        retString = ""
        for count, comp in enumerate(spltList):
            if count == 0:
                continue  # drop first
            if count == 1:
                retString += comp
            else:
                retString += seperator + comp
        return retString
