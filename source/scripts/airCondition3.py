import mode
from utility import Environment, Solver
#Write down your model Parameter here

###############################################################################
##################################BEGIN expected user input####################
###############################################################################
#
#  The selected simulation parameters will be saved here

INT_LENGTH = 0  # interval lenght for saved data
INT_NUM = 500  # number of saved data
TOL = 0.0000001     # tolerance of solver
FIXED = 0    # fixed step size
SIMTIME = 700    # simulation time

# Type in path and filename for the model here
FILEDIR = "..\..\sample\TestStruc"
MOFILE = ["package.mo"]
RESULTFOLDER = "resultDy"


MODE1 = "TestStruc.DiskretisierungGrobFixedInitNoPipe.ZweiVerdampferkreis"
MODE2 = "TestStruc.DiskretisierungGrobFixedInitNoPipe.EinVerdampferkreis"

MODELNAMELIST = [MODE1, MODE2]
TOOLS = [Environment.DYMOLA, Environment.DYMOLA]
SOLVERS = [Solver.RADAU, Solver.RADAU]


    #Which variables are you interested in?
# for saving use structures like: ['h', 'u']
outputVariablesToSave = []
#append for every mode the individual names to save
outputVariablesToSave.append(['pipe1.p[1]','pipe2.p[1]','pipe1.h[1]','pipe2.h[1]','evaporator.summary.p_in', 'evaporator.summary.T_in','CPUtime', 'trapezoid.y','summary.SpecificCharge','summary.M_ref'])
outputVariablesToPlot = [['t', 'pipe1.p[1]'],['t', 'pipe2.p[1]'],['t', 'pipe2.h[1]'],['t', 'evaporator.summary.p_in'],['t', 'evaporator.summary.T_in'],['t', 'CPUtime'],['t', 'trapezoid.y'],['t','summary.SpecificCharge'],['t','summary.M_ref']]


#All vars for mode1
#mapping list for the variables
outList = ['.*','specificCharge_single']
inList = ['.*', 'init.charge_init']


#create modes for testing
translist1_2 = mode.transition(2, 'conditionToSimulate', outList, inList)
outputVariablesToSave.append(['pipe1.p[1]','pipe2.p[1]','pipe1.h[1]','pipe2.h[1]','evaporator.summary.p_in', 'evaporator.summary.T_in','CPUtime', 'trapezoid.y','summary.SpecificCharge','summary.M_ref'])
outputVariablesToSave.append(['pipe1.p[1]','pipe2.p[1]','pipe1.h[1]','pipe2.h[1]','evaporator.summary.p_in', 'evaporator.summary.T_in','CPUtime', 'trapezoid.y','summary.SpecificCharge','summary.M_ref'])


outList = []
inList = []


translist2_3 = mode.transition(1, 'conditionToSimulate', outList, inList)


outputVariablesToSave.append(['pipe1.p[1]','pipe2.p[1]','pipe1.h[1]','pipe2.h[1]','evaporator.summary.p_in', 'evaporator.summary.T_in','CPUtime', 'trapezoid.y','summary.specificcharge'])
#translist2_3 = mode.transition(2, 'conditionToSimulate', outList, inList)

transitionsAll = []
transitionsAll.append([translist1_2])
transitionsAll.append([translist2_3])
transitionsAll.append([translist2_3])

###############################################################################
##################################END expected user input######################
###############################################################################
