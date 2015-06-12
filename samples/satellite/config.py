#Model
model.default_solver = Solver("dassl");
model.default_solver.intervalLength = 0.001;
model.translate = True;
model.init = {};
model.startTime = 0;
model.stopTime = 190000;
model.observe = ['x', 'h', 'vx', 'vy', 'v'];

#First mode
mode1 = DymolaMode();
mode1.modeRef = "Satellite.PlanetRocket";
mode1.files = ["Satellite.mo"];
mode1.synonym = {'x' : 'rocket.x', 'h' : 'rocket.height', 'vx':'rocket.vx', 'vy':'rocket.vy', 'v':'rocket.v'};

#Second mode
mode2 = DymolaMode();
mode2.modeRef = "Satellite.PlanetSatellite";
mode2.files = ["Satellite.mo"];
mode2.synonym = {'x' : 'satellite.x', 'h' : 'satellite.y', 'vx':'satellite.vx', 'vy':'satellite.vy', 'v':'satellite.v'};


#Third mode
mode3 = OpenModelicaMode();
mode3.modeRef = "Satellite.PlanetSatelliteChange";
mode3.files = ["Satellite1.mo"];
mode3.synonym = {'x' : 'satellite.x', 'h' : 'satellite.y', 'vx':'satellite.vx', 'vy':'satellite.vy', 'v':'satellite.v'};


#Transition from mode 1 to mode 2
trans1_2 = Transition();
trans1_2.post = mode2;
trans1_2.mapping = {'satellite.y' : 'rocket.height' , 'satellite.x' : 'rocket.x', 'satellite.vx' : 'rocket.vx', 'satellite.vy' : 'rocket.vy'}; #stern wäre gut

mode1.transitions = [trans1_2];

#Transition from mode 2 to mode 3
trans2_3 = Transition();
trans2_3.post = mode3;
trans2_3.mapping = {'satellite.y':'satellite.y', 'satellite.x': 'satellite.x', 'satellite.vx': 'satellite.vx', 'satellite.vy': 'satellite.vy' }; #stern wäre gut

mode2.transitions = [trans2_3];


#Transition from mode 3 to mode 2
trans3_2 = Transition();
trans3_2.post = mode2;
trans3_2.mapping = {'satellite.y':'satellite.y', 'satellite.x': 'satellite.x', 'satellite.vx': 'satellite.vx', 'satellite.vy': 'satellite.vy' }; #stern wäre gut

mode3.transitions = [trans3_2];


#Set the modes
model.modes = [mode1, mode2, mode3];

plot1 = ModePlot();
plot1.vars = ['h'];
plot1.drawGrid = 1;
plot1.labelXAxis = "time";
plot1.labelYAxis = "h";
plot1.fileName = 'modeplot.png';
plot1.show = True;

plot2 = VariablePlot();
plot2.vars = {'v' : Color.MAGENTA};
plot2.xAxisVar = 'time';
plot2.drawGrid = 1; #0 = no, 1 = yes
plot2.labelXAxis = "time";
plot2.labelYAxis = "v";

plot3 = VariablePlot();
plot3.vars = {'vx' : Color.MAGENTA};
plot3.xAxisVar = 'time';
plot3.drawGrid = 1; #0 = no, 1 = yes
plot3.labelXAxis = "time";
plot3.labelYAxis = "vx";

plot4 = VariablePlot();
plot4.vars = {'vy' : Color.MAGENTA};
plot4.xAxisVar = 'time';
plot4.drawGrid = 1; #0 = no, 1 = yes
plot4.labelXAxis = "time";
plot4.labelYAxis = "vy";

plot5 = VariablePlot();
plot5.vars = {'h' : Color.MAGENTA};
plot5.xAxisVar = 'x';
plot5.drawGrid = 1; #0 = no, 1 = yes
plot5.labelXAxis = "x";
plot5.labelYAxis = "h";

#Set the plots
model.plots = [plot1, plot2, plot3, plot4, plot5];