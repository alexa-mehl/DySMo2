import mode
from utility import Environment, Solver
#Write down your model Parameter here

##############################################################################
##################################BEGIN expected user input###################
##############################################################################
#
#  The selected simulation parameters will be saved here
INT_LENGTH = 0   # interval lenght for saved data
INT_NUM = 500    # number of saved data
TOL = 3e-03      # tolerance of solver
FIXED = 0        # fixed step size
SIMTIME = 10     # simulation time

# Type in path and filename for the model here
FILEDIR = "..\..\sample\BouncingBallBeispiel"
MOFILE = ['BouncingBall.mo']
RESULTFOLDER = "result"
MODEL1 = "BouncingBall.ball_struc"
MODEL2 = "BouncingBall.contact_struc"
MODELNAMELIST = [MODEL1, MODEL2]
# give the tool to simulate for every mode:
TOOLS = [Environment.DYMOLA, Environment.DYMOLA]
SOLVERS = [Solver.DASSL, Solver.DASSL]

# Which variables are you interested in?
outputVariablesToSave = []
# append for every mode the individual names to save
# REMEMBER COMMA :['h', 'u']
outputVariablesToSave.append(['h', 'v', 'switch_to'])
# Try for example: ['h','v'],,['v','t']
outputVariablesToPlot = [['h', 'v'], ['t', 'h']]


#mapping list for the variables
outList = ['v', 'h']
inList = ['damper.v_rel', 'damper.s_rel']


#create modes for testing
translist0_1 = mode.transition(2, 'conditionToSimulate', outList, inList)
# if there is a name difference between the vars to save and theglobal
# outputVariablesToSave, append it here otherwise leave the array empty
# Note: If not empty then same length as 'outputVariablesToSave'
outputVariablesToSave.append([])

translist1_0 = mode.transition(1, 'conditionToSimulate', inList, outList)
#if there is a name difference between the vars to save and the
#global outputVariablesToSave, append it here otherwise leave the array empty
#Note: If not empty then same length as 'outputVariablesToSave'
outputVariablesToSave.append(['damper.s_rel', 'damper.v_rel', 'switch_to'])

transitionsAll = []
transitionsAll.append([translist0_1])
transitionsAll.append([translist1_0])
##############################################################################
##################################END expected user input#####################
##############################################################################
