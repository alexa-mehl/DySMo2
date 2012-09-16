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

#!/usr/bin/python

## \mainpage Structural Dynamic Framework - API
##
## \section intro_sec Introduction
##Start here with your structural dynamics simulation experience.
## \section install_sec Installation
##
##To run the delivered examples:
##
##1. Install the delivered python version and all packages (folder addOns)
##
##2. Set environment variables (refer to Install-Guide in Documentation)
##
##3. Set all paths and desiered tools in "userSettings.py"
##
##4. Build your solution with "python setup.py build" in your command window
##
##5. Set the model you like to simulate in "scripts/testbench.py"
##
##6. Set the model parameters and transitions in "scripts/<modelName>.py"
##
##7. Run the simulation with "python main.py"
##
##
##

## Global (system) python imports

import os.path
import sys
#check if header exists (setup.py was successfully)
if not os.path.isfile('globalHeader.py'):
    sys.exit("Global header file not found, run setup.py first!")

# Local (package) python imports
import globalHeader as gl
import model as m
import mode as transition

from utility import Env

if gl.PP_USE_DYMOLA:
    import dymolaMode as dMode
if gl.PP_USE_OMODELICA:
    import oModelicaMode as oMode
if gl.PP_USE_SIMULINK:
    import SimulinkMode as simMode


################################BEGIN SW Switches############################

#  import your parameter file here
#
import advancedBallDO as mParam
#import bouncingballD as mParam
#import pendulumDS as mParam
#import bounceWall as mParam
#import airCondition3 as mParam


TRANSLATE = True

###################################END SW Switches###########################
#index of the global names, refer to honigman.py
GLOBALNAME_INDEX = 0


## Exit the program with an error message, user tried to simulate with a tool
#  that he have not specified during setup process
def sysExitWTool(tool):
    sys.exit("You try to simulate with " + tool + "!\nYour " + tool
    + ''' option is not installed at the moment.
Run Setup again or change your tool to simulate!''')

## First check if user have not installed an environment and try to simulate
#  with it
toolList = []

for mode in mParam.model.modes:
    toolList.append(mode.tool)


if not gl.PP_USE_DYMOLA:
    if Env.DYMOLA in toolList:
        sysExitWTool("Dymola")
if not gl.PP_USE_OMODELICA:
    if Env.OMODELICA in toolList:
        sysExitWTool("Open Modelica")
if not gl.PP_USE_SIMULINK:
    if Env.SIMULINK in toolList:
        sysExitWTool("Simulink")


## Function takes a predefined model and instantiates the corresponding modes
#    needs the mParam, if the globalSaveList length is not equal the
#    modeSaveList length, the function terminates the program with an error.
def instModes(model):
    #create the save list for every mode
    #TODO: check also if there is only one element in list!
    #      like -> or len(mParam.TOOLS) == 1:
#==============================================================================
#     if not isinstance(mParam.TOOLS, list):
#         mParam.TOOLS = expand.expandToList(mParam.TOOLS, mParam.MODELNAMELIST)
#     if not isinstance(mParam.SOLVERS, list):
#         mParam.TOOLS = expand.expandToList(mParam.SOLVERS, mParam.MODELNAMELIST)
#     arrToSave = check.globalSaveList(mParam, model)
#     check.allEntSameLenght(mParam)
#==============================================================================
    #instantiate the modes and add them to your given model
    for index, mode in enumerate(mParam.model.modes):
        
        if mode.simInfo.solver == []:
            mode.simInfo.solver = mParam.model.simInfo.solver
        if (mode.simInfo.tolerance) == []:
            mode.simInfo.tolerance = mParam.model.simInfo.tolerance
        if (mode.simInfo.intervalNum) == []:
            mode.simInfo.intervalNum = mParam.model.simInfo.intervalNum
        if (mode.simInfo.intervalLen) == []:
            mode.simInfo.intervalLen = mParam.model.simInfo.intervalLen
        if (mode.simInfo.fixed) == []:
            mode.simInfo.fixed = mParam.model.simInfo.fixed
        
        trans = []
        for tran in mode.transitions:
            trans.append(transition.transition(tran.modeIDToSw, 'conditionToSimulate', tran.outName, tran.inName))
        
        if(mode.tool == Env.OMODELICA):
            oMode.oModelicaMode(model, trans,
                                mode.arrToSave, mode.simInfo.solver, mParam.model.simInfo.startTime,
                                mParam.model.simInfo.stopTime, mode.simInfo.tolerance, mode.simInfo.intervalNum,
                                mode.simInfo.intervalLen, mode.simInfo.fixed, (index + 1),
                                mode.modeName)
        elif (mode.tool  == Env.SIMULINK):
            simMode.SimulinkMode(model, trans,
                                mode.arrToSave, mode.simInfo.solver, mParam.model.simInfo.startTime,
                                mParam.model.simInfo.stopTime, mode.simInfo.tolerance, mode.simInfo.intervalNum,
                                mode.simInfo.intervalLen, mode.simInfo.fixed, (index + 1),
                                mode.modeName)
        elif (mode.tool  == Env.DYMOLA):
            dMode.dymolaMode(model, trans,
                                mode.arrToSave, mode.simInfo.solver, mParam.model.simInfo.startTime,
                                mParam.model.simInfo.stopTime, mode.simInfo.tolerance, mode.simInfo.intervalNum,
                                mode.simInfo.intervalLen, mode.simInfo.fixed, (index + 1),
                                mode.modeName)
        else:
            sys.exit("""User specified mode not found in corresponding
                        Environment-enumeration""")

    #before we start the translation / simulation check some errors that may
    #have occurred: check weather the user tried to instantiate a mode with
    #id = 0?
    for mode in model.modeList:
        if mode.modeID == 0:
            sys.exit("Error: The mode named: " + mode.modeName
                     + """ has the ID 0!\nA mode ID must not be zero!
                     Please change the ID and try again ...""")


#main function to test the single functionality
def main():
    #catch the first parameter from the user, if available:
    tempBuf = False
    try:
        sys.argv[1]
    except IndexError:
        tempBuf = False
    else:
        # argv[1] exists
        if sys.argv[1] == "1":
            tempBuf = True

    #instantiate an test object
    model = m.model(mParam.model.modelPath, mParam.model.moFile,
                    mParam.model.resFolder, mParam.simInfo.stopTime,
                    mParam.model.arrToSave,
                    mParam.model.plotList)


    instModes(model)

    #check if it is necessary to compile the model (only for Modelica models)
    if TRANSLATE or tempBuf == True:
        model.translateAllModes()

    model.startSwitch()

    print "success, program terminated ordinary"
    sys.exit(0)

if __name__ == "__main__":

    main()
