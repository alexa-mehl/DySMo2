# Model
model.default_solver = Solver("dassl")
#model.default_tool = "Dymola";
model.translate = True  # compile models
model.init = {}
model.startTime = 0
model.stopTime = 30
model.observe = ['v', 'h']

# First mode
mode1 = Mode()

#mode1.tool = "OpenModelica";
mode1.modeRef = "Ball.FlyingBall"
mode1.files = ["Ball.mo"]
mode1.synonym = {'v': 'v', 'h': 'h'}

# Transition from mode 1 to mode 1


def bounce(actMode, oldMode):
    v = oldMode.get_endValue('v')
    actMode.set_initialValue('v', v * (-1))


# Transition from mode 1 to mode 2
trans1_2 = Transition()
trans1_2.post = mode1
trans1_2.mapping = {'h': 'h'}
trans1_2.init_function = bounce


mode1.transitions = [trans1_2]

# Set the modes
model.modes = [mode1]

plot1 = ModePlot()
plot1.vars = ['h']
plot1.drawGrid = 1
plot1.labelXAxis = "time"
plot1.labelYAxis = "v"
plot1.fileName = 'v.png'
plot1.show = True

plot2 = VariablePlot()
plot2.vars = {'v': Color.MAGENTA}
plot2.xAxisVar = 'time'
plot2.drawGrid = 1  # 0 = no, 1 = yes
plot2.labelXAxis = "x"
plot2.labelYAxis = "y"
plot2.fileName = "xy.png"
plot2.show = True

# Set the plots
model.plots = [plot1, plot2]
