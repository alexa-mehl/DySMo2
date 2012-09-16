# -*- coding: utf-8 -*-
"""
  Copyright (C) 2012  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
  This file is part of modelica3d 
  (https://mlcontrol.uebb.tu-berlin.de/redmine/projects/modelica3d-public).

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
   
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import definitions as d
from utility import Env, Solver

#Write down your model Parameter here

##############################################################################
##################################BEGIN expected user input###################
##############################################################################

#### default simulation information, if it isn't overwirtten in the specific modes this setting is used #####

simInfo = d.simInfo() ### DO NOT CHANGE###


# change here #
simInfo.startTime = 0     # SET: start time of simulation
simInfo.stopTime = 10     # SET: simulation time
simInfo.solver = Solver.DASSL # SET: default solver for the model
simInfo.tolerance = 3e-05      # tolerance of solver
simInfo.intervalNum = 500    # number of saved data
simInfo.intervalLen = 0   # interval lenght for saved data
simInfo.fixed = 0   # fixed step size

# end change simulation information #

####### DEFINE A MODEL #########

model = d.model() ### DO NOT CHANGE###

model.simInfo = simInfo ### DO NOT CHANGE###

model.moFile = ["mechanik.mo", "mechanikOM.mo"] # SET: name of Modelfiles, separated by comma
model.modelPath = "..\..\sample\MechStruk" # SET: set directory in which the model files are
model.resFolder = "result" # SET: the result folder where the simulation results are saved
model.arrToSave = ['x', 'y'] # SET: the names of the variables you want to save, these names will apprear in the observer date file, but the variables might be called differently in each mode
model.plotList = [['t', 'y']] # SET: data to be plotted at the end of the simulation. (t represents time), names correspond to the arrToSave names


########################################### DEFINE A MODE ###########################################
mode1 = d.mode() 

mode1.modeName = "mechanik.wagen_struc" # SET: name of the model for this mode
mode1.tool = Env.DYMOLA # SET: tool which is used for the simulation of this mode
mode1.arrToSave = ['x', 'y'] # SET: variables to be observed, these will be saved under the specified names in the model
mode1.simInfo = d.simInfo() # SET: empty solver settings, means the global settings are used
#### Example on how to change specific solver information just for this mode
#mode1.simInfo.solver = Solver.RADAU
#mode1.simInfo.tolerance = 1e-03

####### DEFINE TRANSITIONS FOR THE DEFINED MODE #############

trans1_2 = d.trans() # creates ne instance of a transistion

trans1_2.modeIDToSw = 2 # SET: mode ID of the next mode
trans1_2.outName = ['x', 'y', 'der(x)', 'der(y)']  # SET: variable names to read from mode1
trans1_2.inName = ['x', 'h', 'vx', 'vy'] # SET: corresponding variable names to be initialized in the new mode

########  Add transitions to mode ############

mode1.transitions = [trans1_2] # add transistions to the mode, if more than one transition was created add them comma separated


########################################### END OF MODE ###########################################



########################################### DEFINE A MODE ###########################################
mode2 = d.mode() 

mode2.modeName = "mechanikOM.ball_struc"
mode2.tool = Env.OMODELICA
mode2.arrToSave = ['x', 'h']
mode2.simInfo = d.simInfo() #### here a simInfo object can be addded


####### DEFINE TRANSITIONS FOR THE DEFINED MODE #############

trans2_3 = d.trans()

trans2_3.modeIDToSw = 3
trans2_3.outName = ['x', 'h', 'vx', 'vy']
trans2_3.inName =  ['x', 'damper.s_rel', 'vx', 'damper.v_rel']


########  Add transitions to mode ############

mode2.transitions = [trans2_3]


########################################### END OF MODE ###########################################

########################################### DEFINE A MODE ###########################################
mode3 = d.mode() 

mode3.modeName = "mechanik.contact_struc"
mode3.tool = Env.DYMOLA
mode3.arrToSave = ['x', 'damper.s_rel']
mode3.simInfo = d.simInfo() #### here a simInfo object can be addded


####### DEFINE TRANSITIONS FOR THE DEFINED MODE #############

trans3_2 = d.trans()

trans3_2.modeIDToSw = 2
trans3_2.outName = ['x', 'damper.s_rel', 'vx', 'damper.v_rel']
trans3_2.inName =  ['x', 'h', 'vx', 'vy']


########  Add transitions to mode ############

mode3.transitions = [trans3_2]


########################################### END OF MODE ###########################################





#### ADD MODES TO MODEL ####

model.modes = [mode1, mode2, mode3]



##############################################################################
##################################END expected user input#####################
##############################################################################
