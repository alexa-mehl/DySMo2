#Model
model.default_solver = Solver("dassl");
model.translate = True;
model.init = {};
model.startTime = 0;
model.stopTime = 10;
model.observe = ['x', 'y'];

#First mode
mode1 = DymolaMode();
#mode1 = OpenModelicaMode();
mode1.solver.tolerance = 1e-4;
mode1.modeRef = "pendulum.Pendulum_struc";
mode1.files = ["pendulum.mo"];
mode1.synonym = {'x' : 'x', 'y' : 'y'};

#Second mode
mode2 = DymolaMode();
#mode2 = OpenModelicaMode();
mode2.solver.tolerance = 1e-4;
mode2.modeRef = "pendulum.Ball_struc";
mode2.files = ["pendulum.mo"];
mode2.synonym = {'x' : 'x', 'y' : 'y'};

#Transition from mode 1 to mode 2
trans1_2 = Transition();
trans1_2.post = mode2;
trans1_2.mapping = {'x' : 'x', 'y' : 'y',  'vx': 'der(x)' ,  'vy':'der(y)'};

#Transition from mode 2 to mode 1
def speed(actMode, oldMode):
	actMode.set_initialValue('dphi', 0.0);

trans2_1 = Transition();
trans2_1.post = mode1;
trans2_1.mapping = {'x' : 'x', 'phi' : 'phi'};
trans2_1.init_function = speed;

mode1.transitions = [trans1_2];
mode2.transitions = [trans2_1];

#Set the modes
model.modes = [mode1, mode2];

#Create plots
plot1 = VariablePlot();
plot1.vars = {'x' : Color.MAGENTA, 'y' : Color.BLACK};
plot1.drawGrid = 1; #0 = no, 1 = yes
plot1.labelXAxis = "x-axis";
plot1.labelYAxis = "y-axis";
plot1.fileName = 'variableplot.png';

plot2 = ModePlot();
plot2.vars = ['x', 'y'];
plot2.drawGrid = 1;
plot2.labelXAxis = "asd";
plot2.labelYAxis = "2314";
plot2.fileName = 'modeplot.png';
plot2.show = True;

plot3 = VariablePlot();
plot3.vars = {'y' : Color.MAGENTA};
plot3.xAxisVar = 'x';
plot3.drawGrid = 1; #0 = no, 1 = yes
plot3.labelXAxis = "x";
plot3.labelYAxis = "y";

#Set the plots
model.plots = [plot1, plot2, plot3];