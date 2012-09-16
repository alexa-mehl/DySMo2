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

import os.path
import os
import sys
import shutil
import switch as sw

DATARESULT = 'outputData'


## This class provides information about the model and the switching states.
#  Furthermore it supplies the interface between user and program.
class model:
    ## Constructor
    #  @param mPath Path where the model.mo is located
    #  @param modelNam List with the names from the different models (must
    #                  exist in fName.mo!)
    #  @param mFile file name of the *.mo
    #  @param rFolder Name of the result folder
    #  @param glStopTime Represents the global simulation time
    def __init__(self, mPath, mFile, rFolder, glStopTime, glSaveList, plotList):
            self.mName_list = []   # Mode name list
            self.moFile = mFile
            #self.tools = tools
            self.modelPath = mPath
            self.resultPath = mPath + os.sep + rFolder
            self.resFolder = rFolder
            # generated automatically only for internal use
            self.moFilePath = []
            # List with modes about the change between two modes
            self.modeList = []
            self.plotList = plotList
            self.startNames = ""
            self.startValues = []
            self.switch = sw.switch(self)   # generate switch instance
            self.__glStopTime = glStopTime              # set global stop tim
            self.__globalSaveList = glSaveList
            ind = 0
            for dummy in mFile:
                self.moFilePath.append(self.modelPath + os.sep + mFile[ind])
                ind = ind + 1
            if os.path.exists(self.moFilePath[0]) != 1:
                # error mo file not found
                sys.exit(".mo file '%s' not found! Program halt..." % self.moFilePath[0])

    def getGlStopTime(self):
            return self.__glStopTime

    def getGlSaveList(self):
            return self.__globalSaveList

    ## Add a mode to the list, necessary for switching information
    def addModeToList(self, modeToAdd):
            self.modeList.append(modeToAdd)

    ## Replace method for the modelName-list (=^modes), the actual name list
    # will be replaced with the new list
    #  @param newList New list with the models to simulate
    def replaceModelNameList(self, newList):
            #Delete the old list
            # split the strings to indicate the mo file
            spltList = []
            # a list containing all .mo file names to check in this function
            tempmoFileNames = []

            #Setup new items
            for item in newList:
                spltList = item.split(".")  # after: spltList[0]: mo file
                temp = ""                          # spltList[1]: modeName
                for count, dummy in enumerate(spltList):
                    if count == 0:
                        continue
                    elif count == 1:
                        temp += spltList[count]
                    else:
                        temp += "_" + spltList[count]

                tempmoFileNames.append(spltList[0])
            #check whether the moFile is correct
            for item in tempmoFileNames:
                item += '.mo'
                if not item in self.moFile:
                    print "Error in replaceModelNameList (form model.py):"
                    print "mode and corresponding mo file from model\
                        parameters does not fit, possible reasons are:"
                    print "The name of your .mo file and your package have to\
                           be equal!"
                    sys.exit("error (model.py)--- Program exit")

    ## Select the path of the result directory.
    #  @param rPath The Path where the directory should be generated
    #  @param overwrite If this flag is true, the existing directory will be
    #         deleted and replaced by the new data
    def creatResultDir(self, rFolder, overwrite):
        self.resultPath = self.modelPath + os.sep + rFolder
        if os.path.exists(self.resultPath) != 1:
            # directory does not exist, creat new
            os.makedirs(self.resultPath)
        else:
            if overwrite == True:
                print "Dir already exists, overwrite flag set directory\
                       recreated"
                # delete all files in resultOM and create an empty folder
                shutil.rmtree(self.resultPath)
                os.makedirs(self.resultPath)
            else:
                sys.exit("Directory already exists, overwrite bit not\
                         selected, Program halt...")

        # @param varToSee Which variables should
    def startSwitch(self):
        self.switch.runSimulation()

        ## Compile the given model, the modeHandler have to set in previous
    def translateAllModes(self):
        for modeToTrans in self.modeList:
            modeToTrans.translate()
