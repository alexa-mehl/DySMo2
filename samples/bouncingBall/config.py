#Model
model.default_solver = Solver("dassl");
model.translate = True;
model.init = {};
model.startTime = 0;
model.stopTime = 10;
model.observe = ['v', 'h'];

#First mode
mode1 = DymolaMode();
#mode1 = OpenModelicaMode();

mode1.modeRef = "BouncingBall.Ball_struc";
mode1.files = ["BouncingBall.mo"];
mode1.synonym = {'v' : 'v', 'h' : 'h'};

#Second mode
mode2 = DymolaMode();
#mode2 = OpenModelicaMode();
#mode2.solver.tolerance = 1e-10;
mode2.modeRef = "BouncingBall.Contact_struc";
mode2.files = ["BouncingBall.mo"];
mode2.synonym = {'v' : 'v', 'h' : 'h'};

#Transition from mode 1 to mode 2
trans1_2 = Transition();
trans1_2.post = mode2;
trans1_2.mapping = { 'damper.v_rel':'v', 'damper.s_rel':'h'};

trans2_1 = Transition();
trans2_1.post = mode1;
trans2_1.mapping = {'v':'damper.v_rel' ,  'h':'damper.s_rel'};

mode1.transitions = [trans1_2];
mode2.transitions = [trans2_1];

#Set the modes
model.modes = [mode1, mode2];


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