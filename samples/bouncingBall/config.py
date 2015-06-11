#Model
model.default_solver = Solver("dassl");
model.translate = True;
model.init = {};
model.startTime = 0;
model.stopTime = 10;
model.observe = ['v', 'h'];

#First mode
mode1 = DymolaMode();

mode1.modeRef = "BouncingBall.Ball_struc";
mode1.files = ["BouncingBall.mo"];
mode1.synonym = {'v' : 'v', 'h' : 'h'};

#Second mode
mode2 = DymolaMode();
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


plot1 = ModePlot();
plot1.vars = ['h'];
plot1.drawGrid = 1;
plot1.labelXAxis = "time";
plot1.labelYAxis = "v";
plot1.fileName = 'modeplot.png';
plot1.show = True;

plot2 = VariablePlot();
plot2.vars = {'v' : Color.MAGENTA};
plot2.xAxisVar = 'time';
plot2.drawGrid = 1; #0 = no, 1 = yes
plot2.labelXAxis = "x";
plot2.labelYAxis = "y";
plot2.show = True;

#Set the plots
model.plots = [plot1, plot2];