
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
# This file implements the switching method. The switching method uses the other classes and 
# methods from these classes to simulate the variable-structure model. 
# Also methods to plot and save simulation data are implemented here.
#==============================================================================
import scipy.io
import os
import pylab as plt
import numpy as np
import sys
from copy import deepcopy
# high level file operations (e.g. delete an non empty directory)
import shutil
import multiprocessing
import time

SAVE_ADDITIONAL_FOLDER = False
PLOT_RESULT = True
folderPartialData = r"partialData"


## assumes the mode changes, save the global simulation data and starts the
## plot method
class switch:
    def __init__(self, myModel):
        self.myModel = myModel
        self.finalDataPath = myModel.resultPath
        self.resFileHandler = ""
        # in this list the data which will be saved into a mat-file is stored
        self.saved_data = []
        # represents a nested list with the names in the self.saved_data file
        self.saved_names = []

    ## Run the simulation and switch between the modes
    def runSimulation(self):
        
        
        # read initial values for simulation start
        for mode in self.myModel.modeList:
            mode.loadInitial()
            

        # Start Simulation: Run through all modes, jump in at mode 0
        act_mode = self.myModel.modeList[0]
        # start time for now always 0
        t = 0
        # Flag to indicate  whether the while loop is active
        loopIsActive = True
        # create new data file in our result path with the results of the first
        # mode
        self.resFileHandler = self.finalDataPath + '\\FinalOutfile.mat'
        # count all conditions
        transitionCounter = 0
        simTime = 0
        mapTime = 0
        endTime = 0
        cpuTime = 0
        initTime = 0
        iterate = -1
        startTime  = time.time()
        while (t < self.myModel.getGlStopTime()
               and loopIsActive):
            print iterate
            print t
            iterate = iterate +1
            #lets simulate ...
            act_mode.simulationInformation.startTime = t
            act_mode.simulationInformation.stopTime = self.myModel.getGlStopTime()
            ss = time.time()
            
            #print 'init start'
            act_mode.saveInit_all()
            initTime = initTime +time.time()-ss
            
            #print 'sim start'
            ss = time.time()
            act_mode.simulate()
            simTime = simTime + time.time()-ss
            #Get the end values, these are the start values for the next mode
            
            #print 'sim end'
            ss = time.time()
            t, end_val = act_mode.getEndVal()
            print 'endTime'
            print t
            cpuTime = cpuTime + end_val[-1]
            endTime = endTime + (time.time()-ss)
            #print 'end read'


            #add the mode id to the result file
            if act_mode.arrToSave[0] != []:
                self.saved_data = act_mode.addData(act_mode.modeID,
                                               self.saved_data,
                                               act_mode.arrToSave[0])
                                               
                                             

            # Save all simulation results in a separate folder, if necessary
            if(SAVE_ADDITIONAL_FOLDER):
                # Generate resultFolder
                if(transitionCounter == 0):
                    folderToSave = self.__generateParitalFolder()

                act_mode.saveAllData(folderToSave, transitionCounter)

            #get the end values from the simulated mode
            #-> start values form the following mode
            #switch to next mode
            #remember the actual indices
            if t < self.myModel.getGlStopTime():
                #print act_mode.simulationInformation.endNames
                
                SwitchTo, SwitchID = act_mode.getSwitchTo()
                if SwitchID == -1:
                    loopIsActive = False  # break the while loop

                old_mode = act_mode

                if SwitchTo > 0:
                    act_mode, transition = self.__assignModeAndTransIndex(old_mode, SwitchTo, SwitchID)
                    # do the allocation only, if the variable myOutNameInd is 0
                    if len(transition.myOutNameInd) == 0:
                        mapStart = time.time()
                        transition.followInNameInd, transition.myOutNameInd = self.__assignNameInd(transition, act_mode, old_mode)
                        mapTime = mapTime + (time.time() - mapStart)

                    act_mode.initValue[transition.followInNameInd] = old_mode.endValue[transition.myOutNameInd] 
                    transition.fct(act_mode, old_mode)
                   
                    #init = transition.fct(act_mode.initNames, deepcopy(act_mode.initValue), old_mode.endNames, old_mode.endValue) 
                    #act_mode.setInit(range(len(act_mode.initValue)), act_mode.initValue)



                transitionCounter += 1  # increment internal transition counter
                #print 'mapping'
            
        #End while

        ## Save Results in final mat file
        # detect the variable names that should be saved
        varNamesToSave = deepcopy(self.myModel.getGlSaveList())
        self.saved_names = deepcopy(self.myModel.getGlSaveList())
        #append time and mode id to saved_names
        self.saved_names.insert(0, 't')
        self.saved_names.insert((len(self.saved_data) - 1), 'modeID')
        indToSave = []
        for count, dummy in enumerate(varNamesToSave):
            indToSave.append(self.saved_names.index(varNamesToSave[count]))
            
        #append modeID
        indToSave.append(self.saved_names.index('modeID'))
        #save results to mat file
        
        print '\n\n\n'
        print 'SIMULATION_TIME'
        print time.time()-startTime
        
        print 'CPU calc time'
        print  cpuTime
        
        print 'simulation time'
        print simTime
        
        print 'init time'
        print initTime
        
        print 'MAP Time'
        print mapTime
        
        print 'End Time'
        print endTime
        
        print 'iterate'
        print iterate
        
        if act_mode.arrToSave[0] != []:
            self.__saveFinalDataToMat(indToSave)
            if(PLOT_RESULT):
                self.__plotResults()
            else:
                print"No plot requested, simulation done"
        ## Plot the results if requested
        print 'blub'

## The method assign the indices to the names in the nameList in the data
    #  field
        # @param varNamesLst  The strings of the variable names
        # @param dataToSearch The corresponding data field where the indices
        #        should be found
        # @return retIndexLst The list of indices you searched
    def __assignNameInd(self, transition, act_mode, old_mode):


        varNamesLsIn = transition.inName
        varNamesLsOut = transition.outName
        dataToSearchIn = act_mode.initIndex
        dataToSearchOut= old_mode.endIndex
        
        retIndexIn = []
        retIndexOut = []
        
        findExtra = []
        
        for i, name in enumerate(varNamesLsOut):
             try:
                retIndexOut.append(dataToSearchOut[name])
             except KeyError:
                 if name == '*':
                    findExtra = dataToSearchIn.keys()

                
        for i, name in enumerate(varNamesLsIn):
            try:
                retIndexIn.append(dataToSearchIn[name])
            except KeyError:
                print 'will net'
                
                
    
        for i, name in enumerate(findExtra):
            try:             
                a = dataToSearchIn[name]
                b = dataToSearchOut[name]
                retIndexIn.append(a)
                retIndexOut.append(b)
            except KeyError:
                print 'nicht identisch'
        

        return retIndexIn, retIndexOut

    ## Help function, print an error message to the console
    def __printErrorAssign(self, names):
        print "Error in __assignNameInd:"
        print "Your variable: " + names + " was not located in the searched\
data array!"
        print "Possible reasons are:"
        print "1. Check weather the variable names are spelled correct\
in the corresponding in and out lists."
        print "2. Do you try to switch in a wrong mode?"
        print "3. Did an error occurred during the translation? Try to\
translate your model again."

    ## compare the two lists and raise a waring if the elements are not the
    #  same
    #  @param list1: first list, compare each element with each in
    #  @param list2: second list.
    def __compareNamesAWarn(self, list1, list2):
        splittedList2 = []  # All elements list 2 without prefix
        temp = []  # Help list
        for lists in list2:
            for element in lists:
                temp.append(element.split('.')[1])
            splittedList2.append(temp)
            temp = []
        # Compare each element in list1 with the cut in list2:
        for listnum, lists in enumerate(list1):
            for element in lists:
                if element.split('.')[1] in splittedList2[listnum]:
                    continue
                else:
                    print "Warning, during list mapping:" + element\
                    + " is not present in both lists!"
        return

    ## Save the simulated array to final mat file, where save[0] = t,
    #  save[1] = varToSave1 ...
        #@param indexData The indices from the data that will be stored in file
    def __saveFinalDataToMat(self, indexData):
        toSave = [[]]
        toSave[0] = self.saved_data[0]  # append time in row 0
        for count, dummy in enumerate(indexData):
            toSave.append(self.saved_data[indexData[count]])
        #append mode id
        toSave.append(self.saved_data[len(self.saved_data) - 1])
        #save data to *.mat
        scipy.io.savemat(self.resFileHandler, {'names':
               (self.saved_names), 'data': (toSave)}, format='4')

    ## Plot the mat file, only for debugging
    def __loadAndPrintMatFile(self, fileToLoad):
        fileToPrint = scipy.io.loadmat(fileToLoad)
        print fileToPrint
        os.system('pause')

    ## This function try to resolve the Mode and Transition index for next mode
        #@param switchTo   The next mode to simulate
        #@return modeIndex The corresponding index in the mode list
        #@return transIndMOne The actual (!) index of the transition (for name
        #        mapping!)
    def __assignModeAndTransIndex(self, actMode, switchTo, switchID):
        modeIndex = -1
        transIndMOne = -1
        #try to get the indices
        
        for transition in actMode.transList:
            if switchID:
                if transition.label == int(switchID):
                    transIndMOne = actMode.transList.index(transition)
                    new_transition = transition
                    switchTo = transition.modeIDToSw
            else:              
                if transition.modeIDToSw == int(switchTo):
                    transIndMOne = actMode.transList.index(transition)
                    new_transition = transition        
        
        for mode in self.myModel.modeList:
            if mode.modeID == int(switchTo):
                modeIndex = self.myModel.modeList.index(mode)
                new_mode = mode


        #catch the errors
        print 'switch_to'
        print switchTo
        print transIndMOne
        print actMode.modeID
        #print new_transition.modeIDToSw
        if modeIndex == -1:
            print "Error in __assignModeAndTransIndex:"
            print "Mode not found in list, possible reasons are:"
            print "1. Is the mode registered in the modeID list? (You tried to\
switch to mode: ", int(switchTo), ")"
            print "2. Does the simulation terminate with the correct mode ID?"
            sys.exit("An error occurred during the assignment of the switch\
index")
        elif transIndMOne == -1:
            print "Error in __assignModeAndTransIndex:"
            print "Transition not found in the actual transition list"
            print "Have you registered all necessary transitions?"
            sys.exit("An error occurred during the assignment of the\
transition index")
        else:
            return new_mode, new_transition

    ## Save the output data from every mode in a mat file, in additional folder
    #  varNames
    # @param appended: number of appended data
    def __generateParitalFolder(self):
        resPath = self.finalDataPath + "\\" + folderPartialData
        #create folder
        if os.path.exists(resPath) != 1:
            # directory doesn t exist, create new
            os.makedirs(resPath)
        else:  # delete whole directory
            shutil.rmtree(resPath)
            os.makedirs(resPath)
        return resPath

    ##Plot all saved variable in a multi color plot (up to 4 colors, one for
    # each mode)
    def __plotResults(self):
        print 'start plotResults'
        #plot result, if necessary
        xInd = []
        yInd = []
        xNames = []
        yNames = []
        modeIDInd = []  # vector with mode IDs
        if self.myModel.plotList != []:
            for pairs in self.myModel.plotList:
                #collect indices from saved_data
                xInd.append(self.saved_names.index(pairs[0]))
                yInd.append(self.saved_names.index(pairs[1]))
                xNames.append(pairs[0])
                yNames.append(pairs[1])
        modeIDInd.append(self.saved_names.index('modeID'))

        print "close all plots to terminate..."
        self.plotDiffColours(xInd, yInd, xNames, yNames, modeIDInd)
#
    def plotDiffColours(self, xNameInd, yNameInd, xNames, yNames, modeVekt):
        print 'start plotDiffColours'
        index = 1
        changeInd = []
        toIndNum = []  # vector with all corresponding indices for colour
        for i, dummy in enumerate(self.saved_data[modeVekt]):
            
            for j, items in enumerate(dummy):
                
                if items != index:
                    toIndNum.append(index)
                    index = items
                    changeInd.append(j)

        toIndNum.append(index)
        changeInd.append(j)
        #plotData = []   # array for mapping in multiprocessing
                        # [0] xData [1] yData [3] xName [4] yName [5] index for
                        # color change
        for i, dummy in enumerate(xNameInd):
            myPlotColour([self.saved_data[xNameInd[i]],
                             self.saved_data[yNameInd[i]],
                             xNames[i], yNames[i], (i + 1),
                             changeInd, toIndNum])
        plt.show()
 #           plotData.append([self.saved_data[xNameInd[i]],
 #                            self.saved_data[yNameInd[i]],
 #                            xNames[i], yNames[i], (i + 1),
 #                            changeInd, toIndNum])
        #pool = multiprocessing.Pool()
        #pool.map(myPlotColour, plotData)


## Postprocessing for plot appearance. Select your line colors and axes-labels
#  @param data: Matrix includes necessary plot information
#                data[0]: x-Data  (Type:double)
#                data[1]: y-Data  (Type:double)
#                data[2]: x-label (Type: string)
#                data[3]: y-label (Type: string)
#                data[4] & [5]: Reserved, do not USE!
#                data[6]: ModeID, responsible for line-color!
def myPlotColour(data):
    print 'in myPlotColour'
    f1 = plt.figure()
    tempstart = 0
    for i, changes in enumerate(data[5]):
        #print 'i'
        col = ''
        if data[6][i] == 1:
            col = 'b'
        elif data[6][i] == 2:
            col = 'r'
        elif data[6][i] == 3:
            col = 'g'
        elif data[6][i] == 4:
            col = 'y'
        plt.plot(data[0][tempstart:changes], data[1][tempstart:changes],
                col)
        tempstart = changes
        del col
    
    plt.xlabel(data[2])
    plt.ylabel(data[3])
    plt.grid(1)
    
