#Model
model.default_solver = Solver("dassl");
model.default_solver.numberOfIntervals = 500;
model.translate = False;
model.init = {};
model.startTime = 0;
model.stopTime = 100000;
model.observe = ['T1'];

def more(actMode, oldMode):
	result = oldMode.get_last_result();
	time = result.get_value('time', 5);
	num = 1
	
	for i in [1,2]:
		T = result.get_value('m1.T', 5);
		for j in range(1,5):
			actMode.set_initialValue('m'+ str(num)+'.T', T)  
			num = num+1  
	
	actMode.get_model().setCurrentTime(time)

def less(actMode, oldMode):
	num = 1
	for i in [1,2]:
		Temp = 0
		for j in range(1,5):
			Temp = Temp + oldMode.get_endValue('m' + str(num)+'.T');
			num = num + 1
		actMode.set_initialValue('m' + str(i)+'.T', Temp/4);
			

#First mode
mode1 = DymolaMode();
mode1.modeRef = "pipe.elements2";
mode1.files = ["pipe.mo"];
mode1.synonym = {'T1' : 'm1.T', 'CPUtime' : 'CPUtime'};


#Second mode
mode2 = DymolaMode();
mode2.modeRef = "pipe.elements10";
mode2.files = ["pipe.mo"];
mode2.synonym = {'T1' : 'm1.T', 'CPUtime' : 'CPUtime'};



#Transition from mode 1 to mode 2
trans1_2 = Transition();
trans1_2.post = mode2;
trans1_2.mapping = {}; #stern wäre gut
trans1_2.init_function = more

mode1.transitions = [trans1_2];

#Transition from mode 2 to mode 3
trans2_1 = Transition();
trans2_1.post = mode1;
trans2_1.mapping = {}; #stern wäre gut
trans2_1.init_function = less

mode2.transitions = [trans2_1];

#Set the modes
model.modes = [mode1, mode2];

plot1 = ModePlot();
plot1.vars = ['T1'];
plot1.drawGrid = 1;
plot1.labelXAxis = "Time[s]";
plot1.labelYAxis = "Temperature[K]";
plot1.fileName = 'modeplot.png';
plot1.show = True;

#Set the plots
model.plots = [plot1];