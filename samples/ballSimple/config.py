#Model
model.default_solver = Solver("dassl");
model.translate = False;
model.init = {};
model.startTime = 0;
model.stopTime = 30;
model.observe = ['v', 'h'];

#First mode
mode1 = DymolaMode();
#mode1 = OpenModelicaMode();

mode1.modeRef = "Ball.FlyingBall";
mode1.files = ["Ball.mo"];
mode1.synonym = {'v' : 'v', 'h' : 'h'};

#Transition from mode 1 to mode 1
def bounce(actMode, oldMode):
	v = oldMode.get_endValue('v');
	actMode.set_initialValue('v', v * (-1));

#Transition from mode 1 to mode 2
trans1_2 = Transition();
trans1_2.post = mode1;
trans1_2.mapping = {'h' : 'h'};
trans1_2.init_function = bounce;


mode1.transitions = [trans1_2];

#Set the modes
model.modes = [mode1];

plot2 = ModePlot();
plot2.vars = ['h'];
plot2.drawGrid = 1;
plot2.labelXAxis = "time";
plot2.labelYAxis = "v";
plot2.fileName = 'modeplot.png';
plot2.show = True;

plot3 = VariablePlot();
plot3.vars = {'v' : Color.MAGENTA};
plot3.xAxisVar = 'time';
plot3.drawGrid = 1; #0 = no, 1 = yes
plot3.labelXAxis = "x";
plot3.labelYAxis = "y";

#Set the plots
model.plots = [plot2, plot3];