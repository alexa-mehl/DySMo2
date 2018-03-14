The framework `DySMo` supports the user to create variable-structure models which can be simulated in different modeling environments. The framework is based on Python and uses some Python packages (see software.txt). 
DySMo already supports the simulation environments Dymola and OpenModelica (the old version of DySMo also supported Simulink). Dymola is tested the most for now. In this framework you can reuse your existing models and create a variable-structure models to either save simulation time, increase your model accuracy or you might just need the variable-structure approach to simulate your model at all.
DySMo has been tested with different examples, a few of them are given as examples (samples folder). The version is a beta Version. We are glad over every advice on how to improve the framework. If you need more functionality or have questions you can always contact us at a.mehlhase@tu-berlin.de, we will be happy to help and implement what is needed. 

## Installation:
1. Install PySimulationLibrary. Use git to clone the repository "git@gitlab.tubit.tu-berlin.de:a.mehlhase/PySimulationLibrary.git" and follow the instructions there.
2. Use git to clone the repository from "git@gitlab.tubit.tu-berlin.de:amsun/dysmo.git".

## Simulate
To simulate a model run python with `DySMo/src/DySMo.py` as first argument and path to your variable-structure-model simulation description file as second.
Example:
````
python Path/To/DySMo/src/DySMo.py Path/To/Your/Model/somefile.py
````
For easier usage, we included a run.bat for Windows that you can use with easy drap&drop.
Simply drag your variable-structure-model simulation description on to the run.bat and it will simulate your model.
The Python-installer defaults to add the Python installation directory to the PATH enviroment variable. If you did not select this option, then you have to add the path to the Python-executeable to the `run.bat`, so that it can find the location of Python.
Be aware that problems may occur when the PySimulationLibrary does not have privileges to write files or so.
This may be only for several directories (usually some subfolder of your User folder should be fine).
If not then you have to run the command with Administator privileges, which usually does not work with drag & drop.
