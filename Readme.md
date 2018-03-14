The framework `DySMo` supports the user to create variable-structure models which can be simulated in different modeling environments. The framework is based on Python and uses some Python packages (see `DySMo\software.txt`). 
DySMo already supports the simulation environments Dymola and OpenModelica (the old version of DySMo also supported Simulink). Dymola is tested the most for now. In this framework you can reuse your existing models and create a variable-structure models to either save simulation time, increase your model accuracy or you might just need the variable-structure approach to simulate your model at all.
DySMo has been tested with different examples, a few of them are given as examples (samples folder). The version is a beta Version. I am glad for every advice on how to improve the framework. If you need more functionality or have questions - do not hesitate to open an issue.

## Dependency
DySMo depends on PySimulationLibrary as kind of technical backend. Use git to clone the repository [https://github.com/jmoeckel/PySimulationLibrary](https://github.com/jmoeckel/PySimulationLibrary) and follow the instructions there.

## Simulate
To simulate a model run python with `DySMo/src/DySMo.py` as first argument and path to your variable-structure-model simulation description file as second.
Example:
````
python Path/To/DySMo/src/DySMo.py Path/To/Your/Model/somefile.py
````
For easier usage, we included a run.bat for Windows that you can use with easy drap&drop.
Simply drag your variable-structure-model simulation description on to the `run.bat` and it will simulate your model.
The Python-installer defaults to add the Python installation directory to the PATH environment variable. If you did not select this option, then you have to add the path to the Python-executable to the `run.bat`, so that it can find the location of Python.
Be aware that problems may occur when the PySimulationLibrary does not have privileges to write files or so.
This may be only for several directories (usually some subfolder of your User folder should be fine).
If not then you have to run the command with Administrator privileges, which usually does not work with drag & drop.

## Remark
Just in case it skipped your attention: This is a forked repository! The original DySMo framework has been developed by Alexandra Mehlhase and Amir Czwink. This repository contains some adjustments and some improvements especially for the usecase: Dymola as a simulation tool. 
