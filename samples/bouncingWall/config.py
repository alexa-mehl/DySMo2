#Model
model.default_solver = Solver("dassl");
model.translate = True;
model.init = {};
model.startTime = 0;
model.stopTime = 5;
model.observe = ['x', 'h'];

#First mode
mode1 = Mode();

mode1.modeRef = "bounceWall.Ball_struc";
mode1.files = ["bounceWall.mo"];
mode1.synonym = {'x' : 'x', 'h' : 'h'};

mode2 = Mode();

mode2.modeRef = "bounceWall.Contact_struc";
mode2.files = ["bounceWall.mo"];
mode2.synonym = {'x':'x','h': 'damper.s_rel'};

mode3 = Mode();
mode3.modeRef = "bounceWall.Contact_wall";
mode3.files = ["bounceWall.mo"];
mode3.synonym = {'x':'x', 'h':'h'};

#Transition from mode 1 to mode 2
trans1_2 = Transition();
trans1_2.post = mode2;
trans1_2.mapping = {'x': 'x', 'damper.s_rel':'h', 'vx':'vx', 'damper.v_rel':'vy'};

#Transition from mode 1 to mode 3
trans1_3 = Transition();
trans1_3.post = mode3;
trans1_3.mapping = {'damper.s_rel':'x', 'h':'h', 'damper.v_rel':'vx', 'v':'vy'};

#Transition from mode 2 to mode 1
trans2_1 = Transition();
trans2_1.post = mode1;
trans2_1.mapping = {'h':'damper.s_rel', 'x':'x', 'vx':'vx', 'vy':'damper.v_rel'};

#Transition from mode 3 to mode 1
trans3_1 = Transition();
trans3_1.post = mode1;
trans3_1.mapping = {'x':'damper.s_rel', 'vx':'damper.v_rel', 'h':'h', 'vy':'v'};


mode1.transitions = [trans1_2, trans1_3];
mode2.transitions = [trans2_1];
mode3.transitions = [trans3_1];
#Set the modes
model.modes = [mode1, mode2, mode3];


plot1 = ModePlot();
plot1.vars = ['h'];
plot1.drawGrid = 1;
plot1.labelXAxis = "time";
plot1.labelYAxis = "h";
plot1.fileName = 'h.png';
plot1.show = True;

plot2 = VariablePlot();
plot2.vars = {'x' : Color.MAGENTA};
plot2.xAxisVar = 'time';
plot2.drawGrid = 1; #0 = no, 1 = yes
plot2.labelXAxis = "x";
plot2.labelYAxis = "y";
plot2.fileName = 'xy.png';
plot2.show = True;

#Set the plots
model.plots = [plot1, plot2];
