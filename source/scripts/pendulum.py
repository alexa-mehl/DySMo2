import mode
from utility import Environment, Solver
#Write down your model Parameter here

###############################################################################
##################################BEGIN expected user input####################
###############################################################################
#
#  The selected simulation parameters will be saved here
ALGO = Solver.DASSL        # solver
SOLVER = "dassl"        # solver
INT_LENGTH = 0          # interval lenght for saved data
INT_NUM = 500        # number of saved data
TOL = 3e-05      # tolerance of solver
FIXED = 0          # fixed step size
SIMTIME = 10         # simulation time

# Type in path and filename for the model here
FILEDIR = "..\..\sample\pendulum"
MOFILE = ["PendelScript.mo"]
RESULTFOLDER = "resultDY"
MODEL1 = "PendelScript.pendel_struc"
MODEL2 = "PendelScript.ball_struc"
MODELNAMELIST = [MODEL1, MODEL2]
TOOLS = [Environment.DYMOLA, Environment.DYMOLA]
SOLVERS = [Solver.DASSL, Solver.DASSL]

#Which variables are you interested in?
# for saving use structures like: ['h', 'u']
# these are global variable names.
# Please note: the names doesnot have to fit with real output names in the
#              single modes. if the names dosnot fit, change the
#              'outputVAriablToSaveMx' and append it to the corresponding mode.
outputVariablesToSave = []
#append for every mode the individual names to save
outputVariablesToSave.append(['x', 'y'])
# for plotting use: [['t','h'],['v','t'],['...','...']]
# note :do not plot variables which are not in the globalSaveList!
outputVariablesToPlot = [['t', 'y'], ['x', 'y']]


#mapping list for the variables
outList = ['x', 'y', 'der(x)', 'der(y)']
inList = ['x', 'y', 'vx', 'vy']
#if there is a name difference between the vars to save and the
#global outputVariablesToSave, append it here otherwise leave the array empty
#Note: If not empty then same length as 'outputVariablesToSave'
outputVariablesToSave.append([])

#create modes for testing

translist1_2 = mode.transition(2, 'conditionToSimulate', outList, inList)

outList = ['x', 'der(phi)','phi']
inList = ['x', 'dphi','phi']
#if there is a name difference between the vars to save and the
#global outputVariablesToSave, append it here otherwise leave the array empty
#Note: If not empty then same length as 'outputVariablesToSave'
outputVariablesToSave.append([])

translist2_1 = mode.transition(1, 'conditionToSimulate', outList, inList)
transitionsAll = []
transitionsAll.append([translist1_2])
transitionsAll.append([translist2_1])
###############################################################################
##################################END expected user input######################
###############################################################################
