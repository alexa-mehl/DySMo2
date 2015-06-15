The framework ‘DySMo’ supports the user to create variable-structure models which can be simulated in different modeling environments. The framework is based on Python and uses some Python packages (see software.txt). 
DySMo already supports the simulation environments Dymola and OpenModelica (the old version of DySMo also supported Simulink). Dymola is tested the most for now. In this framework you can reuse your existing models and create a variable-structure models to either save simulation time, increase your model accuracy or you might just need the variable-structure approach to simulate your model at all.
DySMo has been tested with different examples, a few of them are given as examples (samples folder). The version is a beta Version. We are glad over every advice on how to improve the framework. If you need more functionality or have questions you can always contact us at a.mehlhase@tu-berlin.de, we will be happy to help and implement what is needed. 

WinPython 64bit 3.4.3.3 (portable Version) has all necessary Python libraries included. 

DySMo is only tested in Windows!

==============================
To install DySMo:

1. Use the installer "Install DySMo.exe" or copy the DySMo-folder (sample-folder is optional).
2. In the config.cfg set the path to Dymola and OpenModelica (at least one is needed)
3. Set the path to your Python installation in run.bat (or set the path to Python as environment variable)

There are different possibilities to simulate a model:

1: Use the run.bat. Use the explorer and drag&drop the config.py file, in which your model is described, into the run.bat
2: Start Python in the source folder (or any other folder) and use the command "DySMo.py config.py" (depending on your settings and the current path Python is started in, you need to use the absolute path to DySMo.py (in the src-folder) and the the config.py.