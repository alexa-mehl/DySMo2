
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
        for modes in self.myModel.modeList:
            modes.loadInitial()

        # Start Simulation: Run through all modes, jump in at mode 0
        act_mode = self.myModel.modeList[0]
        # start time for now always 0
        t = 0
        # Flag to indicate  whether the while loop is active
        loopIsActive = True
        # create new data file in our result path with the results of the first
        # mode
        self.resFileHandler = self.finalDataPath + '/FinalOutfile.mat'
        # count all conditions
        transitionCounter = 0
        while (t < self.myModel.getGlStopTime()
               and loopIsActive):
            print 'time:', t
            #lets simulate ...
            act_mode.simulationInformation.startTime = t
            act_mode.simulationInformation.stopTime \
 = self.myModel.getGlStopTime()
            act_mode.simulate()

            #Get the end values, these are the start values for the next mode
            t, end_val = act_mode.getEndVal()

            #add the mode id to the result file
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
                SwitchTo = int(act_mode.getSwitchTo(end_val,
                               act_mode.simulationInformation.endNames))
                if SwitchTo == -1:
                    loopIsActive = False  # break the while loop

                old_mode = act_mode

                if SwitchTo > 0:
                    act_mode, transition = self.__assignModeAndTransIndex(
                                                        old_mode, SwitchTo)
                    # do the allocation only, if the variable myOutNameInd is 0
                    if len(transition.myOutNameInd) == 0:
                        transition.followInNameInd, transition.myOutNameInd = self.__assignNameInd(transition.inName, transition.outName, act_mode.simulationInformation.initNames, old_mode.simulationInformation.endNames)
                        

                    print "Switch to modeID:", int(SwitchTo)
                    endValArr = np.array(end_val)
                    #endState = old_mode.simulationInformation.initData['initValue'][transition.myOutNameInd, 0]
                    #endState = old_mode.simulationInformation.initValue[transition.myOutNameInd]
                    arr = endValArr[transition.myOutNameInd]
                    act_mode.setInit(transition.followInNameInd, arr)

                transitionCounter += 1  # increment internal transition counter
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
        self.__saveFinalDataToMat(indToSave)

        ## Plot the results if requested
        if(PLOT_RESULT):
            self.__plotResults()
        else:
            print"No plot requested, simulation done"

## The method assign the indices to the names in the nameList in the data
    #  field
        # @param varNamesLst  The strings of the variable names
        # @param dataToSearch The corresponding data field where the indices
        #        should be found
        # @return retIndexLst The list of indices you searched
    def __assignNameInd(self, varNamesLsIn, varNamesLsOut, dataToSearchIn, dataToSearchOut):

        retIndexIn = []
        retIndexOut = []
        
        if len(varNamesLsIn)==0:
            
            ind_try = []
            names_try = []
            for i, name in enumerate(dataToSearchIn):
                ind_try.append(i)
                names_try.append(name)
            for i, name in enumerate(dataToSearchOut):
                if name  in names_try:
                    idx = names_try.index(name)
                    retIndexOut.append(i)
                    retIndexIn.append(ind_try[idx])
        
        else:
        
            for ind, names in enumerate(varNamesLsIn):
                
                if '.*' not in names:
                    #no wildcard used, simple mapping: exit if variables not match:
                    try:
                        retIndexIn.append(dataToSearchIn.index(names))
                        retIndexOut.append(dataToSearchOut.index(varNamesLsOut[ind]))
                    except ValueError:
                        self.__printErrorAssign(names)
                        sys.exit("An error occurred during the assignment of the\
    name index")
                else:
                    print names
                    # wildcard used, search nestedInd and nestedNames:
                    # take the prefix and compare for speed
                    preName = names.split('.')[0]
                    ind_try = []
                    #ind_try2 = []
                    names_try = []
                    for i, name in enumerate(dataToSearchIn):
                        if preName in name[0:len(preName)]:
                                ind_try.append(i)
                                names_try.append(name)
                    for i, name in enumerate(dataToSearchOut):
                        if name  in names_try:
                            idx = names_try.index(name)
                            retIndexOut.append(i)
                            retIndexIn.append(ind_try[idx])

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
    def __assignModeAndTransIndex(self, actMode, switchTo):
        modeIndex = -1
        transIndMOne = -1
        #try to get the indices
        for mode in self.myModel.modeList:
            if mode.modeID == int(switchTo):
                modeIndex = self.myModel.modeList.index(mode)
                new_mode = mode

        for transition in actMode.transList:
            if transition.modeIDToSw == int(switchTo):
                transIndMOne = actMode.transList.index(transition)
                new_transition = transition

        #catch the errors
        if modeIndex == -1:
            print "Error in __assignModeAndTransIndex:"
            print "Mode not found in list, possible reasons are:"
            print "1. Is the mode registered in the modeID list? (You try to\
switch to mode: ", int(switchTo), ")"
            print "2. Do the simulation terminate with the correct mode ID?"
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

    def plotDiffColours(self, xNameInd, yNameInd, xNames, yNames, modeVekt):
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
        plotData = []   # array for mapping in multiprocessing
                        # [0] xData [1] yData [3] xName [4] yName [5] index for
                        # color change
        for i, dummy in enumerate(xNameInd):
            plotData.append([self.saved_data[xNameInd[i]],
                             self.saved_data[yNameInd[i]],
                             xNames[i], yNames[i], (i + 1),
                             changeInd, toIndNum])

        pool = multiprocessing.Pool()
        pool.map(myPlotColour, plotData)


## Postprocessing for plot appearance. Select your line colors and axes-labels
#  @param data: Matrix includes necessary plot information
#                data[0]: x-Data  (Type:double)
#                data[1]: y-Data  (Type:double)
#                data[2]: x-label (Type: string)
#                data[3]: y-label (Type: string)
#                data[4] & [5]: Reserved, do not USE!
#                data[6]: ModeID, responsible for line-color!
def myPlotColour(data):
    tempstart = 0
    for i, changes in enumerate(data[5]):
        col = ''
        if data[6][i] == 1:
            col = 'b'
        elif data[6][i] == 2:
            col = 'g'
        elif data[6][i] == 3:
            col = 'r'
        elif data[6][i] == 4:
            col = 'y'
        plt.plot(data[0][tempstart:changes], data[1][tempstart:changes],
                col)
        tempstart = changes
        del col

    plt.xlabel(data[2])
    plt.ylabel(data[3])
    plt.grid(1)
    plt.show()
