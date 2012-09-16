#!/usr/bin/python

## \mainpage Structural Dynamic Framework - API
##
## \section intro_sec Introduction
##Start here with your structural dynamics simulation experience.
## \section install_sec Installation
##
##To run the delivered examples:
##
##1. Install the delivered python version and all packages
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
##7. Run the simulation with "python testbench.py"
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
import checkTemplate as check
import expand

from utility import Environment, Solver

if gl.PP_USE_DYMOLA:
    import dymolaMode as dMode
if gl.PP_USE_OMODELICA:
    import oModelicaMode as oMode
if gl.PP_USE_SIMULINK:
    import SimulinkMode as simMode


################################BEGIN SW Switches############################

#  import your parameter file here
#
import pendulum as mParam
#import bouncing_ball as mParam
#import mechStruk as mParam
#import airCondition3 as mParam


#import bouncing_ballOM as mParam
#import pendelSimDym as mParam
#import pendelSim as mParam
#import rakete as mParam

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
if not gl.PP_USE_DYMOLA:
    if Environment.DYMOLA in mParam.TOOLS:
        sysExitWTool("Dymola")
if not gl.PP_USE_OMODELICA:
    if Environment.OMODELICA in mParam.TOOLS:
        sysExitWTool("Open Modelica")
if not gl.PP_USE_SIMULINK:
    if Environment.SIMULINK in mParam.TOOLS:
        sysExitWTool("Simulink")


## Function takes a predefined model and instantiates the corresponding modes
#    needs the mParam, if the globalSaveList length is not equal the
#    modeSaveList length, the function terminates the program with an error.
def instModes(model):
    #create the save list for every mode
    #TODO: check also if there is only one element in list!
    #      like -> or len(mParam.TOOLS) == 1:
    if not isinstance(mParam.TOOLS, list):
        mParam.TOOLS = expand.expandToList(mParam.TOOLS, mParam.MODELNAMELIST)
    if not isinstance(mParam.SOLVERS, list):
        mParam.TOOLS = expand.expandToList(mParam.SOLVERS, mParam.MODELNAMELIST)
    arrToSave = check.globalSaveList(mParam, model)
    check.allEntSameLenght(mParam)
    #instantiate the modes and add them to your given model
    for index, dummy in enumerate(mParam.MODELNAMELIST):
        if(mParam.TOOLS[index] == Environment.OMODELICA):
            oMode.oModelicaMode(model, mParam.transitionsAll[index],
                                arrToSave[index], Solver.DASSL, 0,
                                mParam.SIMTIME, mParam.TOL, mParam.INT_NUM,
                                mParam.INT_LENGTH, mParam.FIXED, (index + 1),
                                mParam.MODELNAMELIST[index])
        elif (mParam.TOOLS[index] == Environment.SIMULINK):
            simMode.SimulinkMode(model, mParam.transitionsAll[index],
                                 arrToSave[index], Solver.DASSL, 0,
                                 mParam.SIMTIME, mParam.TOL, mParam.INT_NUM,
                                 mParam.INT_LENGTH, mParam.FIXED, (index + 1),
                                 mParam.MODELNAMELIST[index])
        elif (mParam.TOOLS[index] == Environment.DYMOLA):
            dMode.dymolaMode(model, mParam.transitionsAll[index],
                             arrToSave[index], mParam.SOLVERS[index], 0,
                             mParam.SIMTIME, mParam.TOL, mParam.INT_NUM,
                             mParam.INT_LENGTH, mParam.FIXED, (index + 1),
                             mParam.MODELNAMELIST[index])
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
    model = m.model(mParam.FILEDIR, mParam.MODELNAMELIST, mParam.MOFILE,
                    mParam.RESULTFOLDER, mParam.SIMTIME,
                    mParam.outputVariablesToSave[GLOBALNAME_INDEX],
                    mParam.outputVariablesToPlot, mParam.TOOLS)

    instModes(model)

    #check if it is necessary to compile the model (only for Modelica models)
    if TRANSLATE or tempBuf == True:
        model.translateAllModes()

    model.startSwitch()

    print "success, program terminated ordinary"
    sys.exit(0)

if __name__ == "__main__":

    main()
