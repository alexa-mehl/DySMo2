## A utility file provides common used functions


## simple implementation of an enum typt to improve readability
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
    #
    # use it like this:
    # Color = enum('RED','BLUE','YELLOW',...)
    # Color.RED  => 0

# Save all in the program used enums here:
# choose the Environment used for the simulation
Env = enum('DYMOLA', 'OMODELICA', 'SIMULINK')
Translationmode = enum('RUN', 'COMPILE', 'RUNANDCOMPILE')
Solver = enum('EULER', 'DASSL', 'LSODAR', 'RKFIX2', 'RKFIX3', 'RKFIX4',
              'LSODE1', 'LSODE2', 'DOPRI5', 'DOPRI8', 'GRK4T', 'ODASSL',
              'MEXX', 'DEABM', 'RADAU')
