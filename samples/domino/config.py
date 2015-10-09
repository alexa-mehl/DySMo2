# Dominostein trifft anderen Stein
def crash(act, old):
	import math
	active =  int(old.get_endValue('active') +1)
	fallen= int(old.get_endValue('fallen'))
				
	D_val = old.get_endValue('D')
	Z_val = old.get_endValue('stones[1].Z')

	phipush = math.asin(D_val/Z_val);
	KO = (1+math.cos(2*phipush))/2;
	KR = 1 -math.cos(phipush);

	o = []
	p = []
	for i in range(1,active):
		omega = old.get_endValue('stones['+str(i)+'].omega')
		phi = old.get_endValue('stones['+str(i)+'].phi')
		p.append(phi)
		if i == active-1:
			o.append(omega*KR)
		else:
			o.append(omega)
			
	act.set_parameters({'active':active,'fallen':fallen});
	act.compile()
	act.read_init()
		
	for i in range(1,active):
		act.set_initialValue('stones['+str(i)+'].omega', o[i-1]);
		act.set_initialValue('stones['+str(i)+'].phi', p[i-1]);
	act.set_initialValue('stones['+str(active)+'].omega', o[-1]*KO/KR);
	act.set_initialValue('stones['+str(active)+'].phi', 0);
	
# Dominostein gefallen
def fall(act, old):
	active =  int(old.get_endValue('active'))-1
	fallen =  int(old.get_endValue('fallen')+1)

	o = []
	p = []
	for i in range(2,active+2):
		omega = old.get_endValue('stones['+str(i)+'].omega')
		phi = old.get_endValue('stones['+str(i)+'].phi')
		o.append(omega)
		p.append(phi)
		
	act.set_parameters({'active':active,'fallen':fallen});
	act.compile()
	act.read_init()
	
	for i in range(1,active+1):
		act.set_initialValue('stones['+str(i)+'].omega', o[i-1]);
		act.set_initialValue('stones['+str(i)+'].phi', p[i-1]);
	
	
# Ende der Simulation     
def end(act, old):
	t = old.get_endValue('time')
	act.get_model().stopTime = t

model.translate = True;
model.default_solver = Solver("dassl") # Solver 
model.init = {'stones[1].omega': 0.1} # Init
model.stopTime = 5 # Stopzeit 
model.startTime = 0 # Startzeit
model.observe = ['stones[1].phi','stones[2].phi','stones[1].omega']  

mode = DymolaMode()
mode.files = ['domino.mo'] # Modelica Dateien 
mode.modeRef = "domino.stones" # Modelica-Model
mode.synonym={'stones[1].phi':'stones[1].phi', 'stones[1].omega':'stones[1].omega'}

# Stein getroffen
trans1 = Transition() 
trans1.post = mode #Wechsel zu sich selbst
trans1.init_function = crash # Funktionsaufruf
trans1.mapping = {}; # Kein Mapping

# Stein gefallen
trans2 = Transition()
trans2.post = mode #Wechsel zu sich selbst
trans2.init_function = fall # Funktionsaufruf
trans2.mapping = {}; # Kein Mapping

# Simulationsende
trans3 = Transition()
trans3.post = mode #Wechsel zu sich selbst
trans3.init_function = end # Funktionsaufruf
trans3.mapping = {}; # Kein Mapping

mode.transitions = [trans1, trans2, trans3] 

model.modes = [mode]

#Create plots
plot1 = VariablePlot();
plot1.vars = {'stones[1].phi' : Color.MAGENTA};
plot1.drawGrid = 1; #0 = no, 1 = yes
plot1.labelXAxis = "x-axis";
plot1.labelYAxis = "y-axis";
plot1.fileName = 'variableplot.png';
plot1.show = True;

plot2 = ModePlot();
plot2.vars = ['stones[1].phi'];
plot2.drawGrid = 1;
plot2.labelXAxis = "time";
plot2.labelYAxis = "phi";
plot2.fileName = 'modeplot.png';
plot2.show = True;




#Set the plots
model.plots = [plot1, plot2];
