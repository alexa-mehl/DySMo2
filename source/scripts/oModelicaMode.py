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
import os.path
import sys
import shutil
from subprocess import call
import xml.dom.minidom as dom
import numpy as np
import globalHeader as gl
import DyMatStruk as mat

#The name of the .mos script generated during the translation
SCRIPTNAME = "oMScript"
#set the oModelica /bin folder path
#do you like to extend your result directory? Then put in the string here:
EXTENSION = ""



## Provides all necessary methods for use with open Modelica
class oModelicaMode(mode):
    def __init__(self, model, transLst, arrToSave, solver, startTime, stopTime,
                 tolerance, IntervalNum, IntervalLen, fixed, modeID, modeName):
        mode.__init__(self, model, transLst, arrToSave, self.mapSolver(solver),
                      startTime, stopTime, tolerance, IntervalNum, IntervalLen,
                      fixed, modeID, modeName, model.moFile)
        self.myModel.addModeToList(self)  # add yourself to mode list
        self.initMatrix = []
        self.absModelPath = os.path.abspath(self.myModel.modelPath)
        self.absModePath = self.absModelPath + os.sep + self.myModel.resFolder\
                            + os.sep + self.modeName+'_m'+ str(modeID)
        self.xmlFileName = self. modeName + '_init.xml'
        # A copy of the original xml file, load if model was not translated
        self.xmlInitFile = self.modeName + "_initSave.xml"
        self.resultFileCSV = self.modeName + '_res.csv'
        self.init= [] # indizees von zu initialisierenden Variablen

    ## Map the available solver from utility.py to a string, so that open
    ## Modelica can use the solver settings
    #  @param solv: A valid solver entry of the solver enumeration in
    #               utility.py
    #  @return: A string with the corresponding OM Solver
    def mapSolver(self, solv):
        if solv == Solver.EULER:
            return "euler"
        elif solv == Solver.DASSL:
            return "dassl"
        elif solv == Solver.RKFIX2:
            return "rungekutta"
        elif solv == Solver.DOPRI5:
            return "dopri5"
        #default:
        else:
            sys.exit("Wrong solver settings")

    ## Translate the given .mo file. Generates the output directory. If this
    #  already exists, it will be deleted
    #  @requires: The corresponding model file containing the modelica code
    def translate(self):
        #remember the actual working dir
        simParameter = self.simulationInformation
        currentDir = os.getcwd()
        resPath = self.absModePath
        #check if the result path already exists
        if os.path.exists(self.absModePath) != 1:
            os.makedirs(self.absModePath)
        else:
            #delete all files in resultFolder and create an empty folder
            shutil.rmtree(self.absModePath)
            os.makedirs(self.absModePath)

        #change to result dir and generate the *.mos file for openModelica
        os.chdir(resPath)
        #write the corresponding mos file
        fileName = SCRIPTNAME
        mosfile = open(fileName + '.mos', 'w', 1)
        mosfile.write("loadModel(Modelica);\n")
        for item in self.myModel.moFile:
            mosfile.write("loadFile(\"..\\.." + os.sep + "\\" + item + "\");\n")

        # do a dummy simulation since it is not yet possible to do a
        # translation only
        mosfile.write("cd(\"" + self.absModePath + "\");\n")
        mosfile.write("simulate(" + self.modeName\
                       + ", stopTime="+str(simParameter.stopTime)+ ", startTime = 0, tolerance ="+str(simParameter.tolerance)+ ",stepSize ="+ str(simParameter.fixed) + ",method = \""+ str(simParameter.solver)+"\",numberOfIntervals = "+ str(simParameter.intervalNum)   +",outputFormat=\"mat\");\n")

        mosfile.close()

        #suppress output
        fnull = open(os.devnull, 'w')
        try:
            #call the open modelica compiler
            #TODO: Recognize a simulation error
            ret = call(gl.PP_OMPATH + ' ' + SCRIPTNAME + '.mos' + ' Modelica',
                       shell=True, stdout=fnull)
            print 'test' 
            print fnull
            gg =  [gl.PP_OMPATH + ' ' + SCRIPTNAME + '.mos' + ' Modelica']
            print gg
            if ret < 0:
                print >> sys.stderr, "Failure in simulation!", -ret
            else:
                print >> sys.stdout, "Mode " + self.modeName + \
                        " compiled successfully"
        except OSError, e:
            print >> sys.stderr, "Failure in execution of openModelica in\
             oModelica.py", e
        # generate a copy of xml file to load start-conditions on later runs!
        os.chdir(self.absModePath)
        shutil.copy(self.xmlFileName, self.xmlInitFile)
        #change directory back
        os.chdir(currentDir)

    ## Load the initial data from the generated xml file.
    #  @requires: The xml file generated by Modelica. (If not available, call
    #             translate first)
    def loadInitial(self):
        currentDir = os.getcwd()
        resPath = self.absModePath
        x0names_1 = []
        x0_1 = []      # array, see dsin.txt
        toAppend = []  # temporary list to append for initial matrix
        os.chdir(resPath)
        #load xml file:
        if (not os.path.isfile(self.xmlFileName) or\
            not os.path.isfile(self.xmlInitFile)):
            print  "Error in loadData (oModelica.py):\n"
            sys.exit("Initial xml file not found, check if an error occurred \
in your translation / simulation!\nIf this is the first time you see this \
message, try to translate your model again.")
        else:
            #restore the original xml file before simulation
            shutil.copy(self.xmlInitFile, self.xmlFileName)
            tree = dom.parse(self.xmlFileName)

        #read the data
        for entry in tree.childNodes[1].childNodes:
            if entry.nodeName == "DefaultExperiment":
                continue
            if entry.nodeName == "ModelVariables":
                for ReadInVars in entry.childNodes:
                    #check if it is a valid element
                    if ReadInVars.localName != None:
                        #create a initalValue matrix, similar to dymola
                        #(see dsin.txt)
                        saveVar = ReadInVars.getAttribute("classType")
                        if saveVar != ("rPar") and saveVar != ("iPar") and\
                           saveVar != ("bPar"):
                                x0names_1.append(ReadInVars.\
                                                 getAttribute("name"))
                        vartype = ReadInVars.childNodes[1]
                        fixed = vartype.getAttribute("fixed")
                        if fixed == "true":
                            r1 = -1
                        else:
                            r1 = 0
                        r3 = 0
                        r4 = 0
                        clType = ReadInVars.getAttribute("classType")
                        r5 = 1
                        dType = vartype.localName
                        if   dType == "Real":
                            r6 = 0
                            r2 = self.__filterCommentConvertToFloat(\
                                      vartype.getAttribute("start"))
                        elif dType == "Boolean":
                            r6 = 1
                            try:
                                r2 = self.__boolToFloat(\
                                          vartype.getAttribute("start"))
                            except Exception:
                                r2 = self.__filterCommentConvertToFloat(\
                                          vartype.getAttribute("start"))
                        elif dType == "Integer":
                            r6 = 2
                            r2 = self.__filterCommentConvertToFloat(\
                                      vartype.getAttribute("start"))
                        else:
                            sys.exit("An error occurred in oModelica.py\
                                     loadData(). Verify the assignment\
                                     of the variable data Types!")
                        if(clType != "rPar" and clType != "iPar"\
                           and clType != "bPar"):
                            #do not save the parameters in the data struct
                            toAppend = [r1, r2, r3, r4, r5, r6]
                            x0_1.append(toAppend)

        arrayToRet = np.array(x0_1)
        #print 'tttt'
        #print x0names_1
        #self.simulationInformation.initData = arrayToRet
        self.initValue = arrayToRet[:, 1]
        self.initNames = x0names_1
        
        self.initIndex = {}
        for i, name in enumerate(x0names_1):
                self.initIndex[name] = i        
        
        os.chdir(currentDir)


#==============================================================================

    ## Simulate the mode with the given conditions in the parameter file
    #  @requires: A successfully translated model, the xml file with the
    #             initial conditions
    def simulate(self):
        #save all init-data (edit xml-file)
        #self.__saveInit_all()
        #start the simulation
        currentDir = os.getcwd()
        resPath = self.absModePath
        os.chdir(resPath)
        #start simulation
        os.system("." + os.sep + self.modeName+ ' -overrideFile init.txt')#+', startTime ='+str(self.simulationInformation.startTime))
        os.chdir(currentDir)
        

    ## Write the initial condition bevore simulation
    #  @param ind: List with the current indices of the array arr
    #  @param arr: corresponding initial data
    #  @param endState: TODO
    def setInit(self, ind, arr):
        #TODO: Warum zusaetzlich initData['initialValue']????
        self.init = ind
        print 'len'
        print len(ind)
        print len(arr)        
        
        self.initValue[ind] = arr
        return self.initValue[:]

    ## Get the last value of a simulation (the start value for next mode)
    #  @return: Array with the end Value from each simulation variable.
    #           First value is time
    def getEndVal(self):
        s = mat.DyMatStruk(self.absModePath + os.sep + self.modeName + '_res.mat')
        #print s.names
        #print type(s.names(2))        
        
        self.endNames = s.names(2)+s.names(1)
        
        self.endIndex = {}
        for i, name in enumerate(self.endNames):
                self.endIndex[name] = i
        

        simData = s.getVarArray(s.names(2),False)        
        paraData = s.getVarArray(s.names(1), False)  
        
        self.simData = s        
        
        end_val = np.append(simData[:,-1],paraData[:,-1])
        

        times = s.getVarArray(self.endNames[0:1]) 
        t = times[0,-1]
        print t
        
        
        self.endValue = end_val
        return t, end_val
        

    ## Add additional data to the existing simulation results. If a mode have
    #  generated new simulation data, call this method to concatenate the data.
    #  @param modeID: ID (1 - n) of the mode which generated the data
    #  @param data: Matrix with simulation results
    #  @param varNames: Array with the corresponding names to data
    #  @return: A concatenated data matrix, first entry time -> last modeID
    def addData(self, modeID, data, varNames):
        #return self.toInterface.addData(path, modeID, data, varNames)
                
        s = self.simData
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
        
        
    ## Remove a comment, if necessary
    # @param inUnicode: unicode-set from openModelica .xml file
    #                   (<ScalarVariable> "start" = inString)
    # @return value: number -- float convertible
    def __filterCommentConvertToFloat(self, inUnicode):
        if not '/*' in inUnicode:
            return float(inUnicode)
        else:
            #filter the comment out of unicode string
            s = unicode(inUnicode)
            pos = s.find('/*')
            return float(s[:pos])

    ## Convert boolean to float for initial array
    # @param inUnicode: A unicode, containing "true" or "false"
    # @return value: float if input==true -> 1.0 else if input==false ->0.0
    def __boolToFloat(self, inUnicode):
        if "true" in inUnicode:
            return float(1.0)
        elif "false" in inUnicode:
            return float(0.0)
        else:
            raise Exception("Unexpected error in oModelica __boolToFloat,\
                            expected boolean Unicode, get '%s'" % inUnicode)

    ## Save all simulation parameter to corresponding xml-file
    def saveInit_all(self):
        simParameter = self.simulationInformation
        currentDir = os.getcwd()
        resPath = self.absModePath 
        os.chdir(resPath)
        if os.path.exists("init.txt"):
             os.remove("init.txt")
        f = open("init.txt", "w")
        inits = ''
        #print self.init
        if self.init == []:  
            for index, name in enumerate(self.initNames):
                if name[0] == '$':
                    print 'leer'
                else:
                    inits = inits+','+ str(name) + '=' + str(self.initValue[index])
            
        else:
            for i  in self.init:
                inits = inits+','+ str(self.initNames[i]) + '=' + str(self.initValue[i])
        
        
        f.write('stopTime='+str(simParameter.stopTime)+',startTime='+str(simParameter.startTime)+',tolerance ='+str(simParameter.tolerance)+ ',stepSize ='+ str(simParameter.fixed) + ',method = '+ str(simParameter.solver)+',numberOfIntervals = '+ str(simParameter.intervalNum)+inits)#+str(simParameter.stopTime))
        f.close()
        os.chdir(currentDir)
        
        
    ## Additional function: save ALL simulation results in an additional
    #  folder.
    # @param folder: the absolute path, where the files are saved
    # @param transNo: a transition counter, to find the data it will be
    #                 saved as part of the filename
    def saveAllData(self, folder, transNo):
        shutil.copy(self.absModePath + '\\' + self.resultFileCSV, folder)
        # rename the dres.mat file
        shutil.move(folder + '\\' + self.resultFileCSV, \
                    folder + '\\allData_TransNo_' + str(transNo) + '.csv')
