#Model
model.default_solver = Solver("dassl");
model.translate = True;
model.init = {};
model.startTime = 0;
model.stopTime = 5;
model.observe = ['x', 'h'];

#First mode
mode1 = DymolaMode();
#mode1 = OpenModelicaMode();

mode1.modeRef = "bounceWall.Ball_struc";
mode1.files = ["bounceWall.mo"];
mode1.synonym = {'x' : 'x', 'h' : 'h'};

mode2 = DymolaMode();
mode2.modeRef = "bounceWall.Contact_struc";
mode2.files = ["bounceWall.mo"];
mode2.synonym = {'x':'x','h': 'damper.s_rel'};

mode3 = DymolaMode();
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


plot2 = ModePlot();
plot2.vars = ['h'];
plot2.drawGrid = 1;
plot2.labelXAxis = "time";
plot2.labelYAxis = "h";
plot2.fileName = 'modeplot.png';
plot2.show = True;

plot3 = VariablePlot();
plot3.vars = {'x' : Color.MAGENTA};
plot3.xAxisVar = 'time';
plot3.drawGrid = 1; #0 = no, 1 = yes
plot3.labelXAxis = "x";
plot3.labelYAxis = "y";

#Set the plots
model.plots = [plot2, plot3];