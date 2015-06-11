#Model
model.default_solver = Solver("dassl");
model.translate = True;
model.init = {};
model.startTime = 0;
model.stopTime = 8;
model.observe = ['x', 'y'];

#First mode
mode1 = DymolaMode();
mode1.solver.tolerance = 3e-05;
mode1.modeRef = "NailPendulum.pendulum_struc";
mode1.files = ["NailPendulum.mo"];
mode1.synonym = {'x' : 'x', 'y' : 'y'};

#Second mode
mode2 = DymolaMode();
mode2.solver.tolerance = 3e-05;
mode2.modeRef = "NailPendulum.ball_struc";
mode2.files = ["NailPendulum.mo"];
mode2.synonym = {'x' : 'x', 'y' : 'y'};

#Transition from first mode to first mode
trans1_1 = Transition();
trans1_1.post = mode1;
trans1_1.mapping = {'phi' : 'phi', 'dphi' : 'dphi', 'long' : 'long'};

#Transition from first mode to second mode
trans1_2 = Transition();
trans1_2.post = mode2;
trans1_2.mapping = {'x' : 'x', 'y' : 'y', 'vx' : 'der(x)', 'vy' : 'der(y)', 'L' : 'L', 'n.x' : 'n.x', 'n.y' : 'n.y', 'long' : 'long'};

#Set transitions for first mode
mode1.transitions = [trans1_1, trans1_2];

#Transition from second mode to first mode
trans2_1 = Transition();
trans2_1.post = mode1;
trans2_1.mapping = {'phi' : 'phi1', 'dphi' : 'der(phi)', 'long' : 'long'};

#Set transitions for second mode
mode2.transitions = [trans2_1];

#Set modes
model.modes = [mode1, mode2];

#Create Plots
plot1 = ModePlot();
plot1.vars = {'y'};
plot1.xAxisVar = 'x';
plot1.drawGrid = 1;
plot1.labelXAxis = "x";
plot1.labelYAxis = "y";
plot1.fileName = 'pendulum.png';
plot1.show = True;

#Set Plots
model.plots = [plot1];