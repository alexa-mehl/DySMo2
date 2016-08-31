#Model
model.default_solver = Solver("dassl");
model.default_solver.tolerance = 3e-05;
model.translate = True;
model.init = {};
model.startTime = 0;
model.stopTime = 10;
model.observe = ['y'];

#First mode
mode1 = Mode();
mode1.modeRef = "mechanics.vehicle_struc";
mode1.files = ["mechanics.mo"];
mode1.synonym = {'y' : 'y'};

#Second Mode
mode2 = Mode();
mode2.modeRef = "mechanics.ball_struc";
mode2.files = ["mechanics.mo"];
mode2.synonym = {'y' : 'h'};

#Third Mode
mode3 = Mode();
mode3.modeRef = "mechanics.contact_struc";
mode3.files = ["mechanics.mo"];
mode3.synonym = {'y' : 'h'};

#Transition from first mode to second mode
trans1_2 = Transition();
trans1_2.post = mode2;
trans1_2.mapping = {'x' : 'x', 'h' : 'y', 'vx' : 'der(x)', 'vy' : 'der(y)'};
mode1.transitions = [trans1_2];

#Transition from second mode to third mode
trans2_3 = Transition();
trans2_3.post = mode3;
trans2_3.mapping = {'x' : 'x', 'damper.s_rel' : 'h', 'vx' : 'vx', 'damper.v_rel' : 'vy'};
mode2.transitions = [trans2_3];

#Transition from third mode to second mode
trans3_2 = Transition();
trans3_2.post = mode2;
trans3_2.mapping = {'x' : 'x', 'h' : 'damper.s_rel', 'vx' : 'vx', 'vy' : 'damper.v_rel'};
mode3.transitions = [trans3_2];

#Set modes
model.modes = [mode1, mode2, mode3];

#Plot
plot1 = ModePlot();
plot1.vars = {'y'};
plot1.drawGrid = 1;
plot1.labelXAxis = "time";
plot1.labelYAxis = "y";
plot1.fileName = 'yplot.png';
plot1.show = True;

model.plots = [plot1];
