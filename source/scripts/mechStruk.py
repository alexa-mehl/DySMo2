import mode
from utility import Environment, Solver
#Write down your model Parameter here

###############################################################################
##################################BEGIN expected user input####################
###############################################################################
#
#  The selected simulation parameters will be saved here
SOLVER = "dassl"        # solver
INT_LENGTH = 0  # interval lenght for saved data
INT_NUM = 500   # number of saved data
TOL = 3e-05     # tolerance of solver
FIXED = 0.01    # fixed step size
SIMTIME = 10    # simulation time


# Type in path and filename for the model here
FILEDIR = "..\..\sample\MechStruk"
MOFILE = ["mechanik.mo", "mechanikOM.mo"]
RESULTFOLDER = "resultDy"


MODE1 = "mechanik.wagen_struc"
MODE2 = "mechanikOM.ball_struc"
MODE3 = "mechanik.contact_struc"
#MODE4         = "mechanik.contact_wall"
MODELNAMELIST = [MODE1, MODE2, MODE3]
TOOLS = [Environment.DYMOLA, Environment.OMODELICA, Environment.DYMOLA]
SOLVERS = [Solver.DASSL, Solver.DASSL, Solver.DASSL]

# Which variables are you interested in?
# for saving use structures like: ['h', 'u']
outputVariablesToSave = []
#append for every mode the individual names to save
outputVariablesToSave.append(['x', 'y'])
# for plotting use: [['t','h'],['v','t'],['...','...']]
outputVariablesToPlot = [['t', 'y']]

#mapping list for the variables
# SWITCH MODE1 - > MODE2
outList = ['x', 'y', 'der(x)', 'der(y)']
inList = ['x', 'h', 'vx', 'vy']

#create modes for testing
translist1_2 = mode.transition(2, 'conditionToSimulate', outList, inList)
outputVariablesToSave.append([])


outList = ['x', 'h', 'vx', 'vy']
inList = ['x', 'damper.s_rel', 'vx', 'damper.v_rel']

translist2_3 = mode.transition(3, 'conditionToSimulate', outList, inList)

outputVariablesToSave.append(['x', 'h'])

# SWITCH MODE3 - > MODE2
outList = ['x', 'damper.s_rel', 'vx', 'damper.v_rel']
inList = ['x', 'h', 'vx', 'vy']

translist3_2 = mode.transition(2, 'conditionToSimulate', outList, inList)
outputVariablesToSave.append(['x', 'damper.s_rel'])

# SWITCH MODE2 -> MODE4   (against Wall, not used at the moment)
#outList =  ['x','damper.s_rel','vx', 'damper.v_rel' ]
#inList  =  ['damper.s_rel', 'x', 'vx', 'damper.v_rel' ]

#translist4_3 = model.transition(2, 'conditionToSimulate', outList, inList)
#outputVariablesToSave.append(['x', 'damper.s_rel'])

transitionsAll = []
transitionsAll.append([translist1_2])
transitionsAll.append([translist2_3])
transitionsAll.append([translist3_2])

###############################################################################
##################################END expected user input######################
###############################################################################
