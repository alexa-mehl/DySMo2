model.stopTime = 10
model.observe = ['x', 'y']

# simulink mode
mode1 = Mode()
mode1.modeRef = "pendel"
mode1.files = ['pendel.mdl']

# modelica mode
mode2 = Mode()
mode2.modeRef = "PendelScript.ball_struc"
mode2.files = ['PendelScript.mo']

# Transition from mode 1 to mode 2
trans1_2 = Transition()
trans1_2.post = mode2
trans1_2.mapping = {'x': 'x', 'y': 'y', 'vx': 'dx', 'vy': 'dy'}

# Transition from mode 2 to mode 1
trans2_1 = Transition()
trans2_1.post = mode1
trans2_1.mapping = {'start_phi': 'phi', 'start_dphi': 'der(phi)'}

# Set transitions
mode1.transitions = [trans1_2]
mode2.transitions = [trans2_1]

# Set the modes
model.modes = [mode1, mode2]


# Create plots
plot1 = ModePlot()
plot1.vars = ['y']
plot1.xAxisVar = 'x'
plot1.fileName = 'position.png'
plot1.show = True

plot2 = ModePlot()
plot2.vars = ['y']
plot2.fileName = 'y.png'
plot2.show = True

# Set the plots
model.plots = [plot1, plot2]
