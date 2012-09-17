Start here with your structural dynamics simulation experience.
This framework ‘DySMo’ supports the user to create variable-structure models which can be simulated in different modeling environments. The framework is based on Python and uses some Python packages (see the installation guide). 
DySMo already supports the simulation environments Dymola, OpenModelica and Simulink. Dymola is tested the most for now. In this framework you can reuse your existing models and create a variable-structure model out of it to either save simulation time, increase your model accuracy or you might just need the variable-structure approach to simulate your model at all.
DySMo has been tested with different examples, a few of them are given as examples, but it is not fully tested. It is still a Beta-Version which needs a lot of work. We are glad over every advice and help you can give. If you need more functionality or have questions you can always contact us at a.mehlhase@tu-berlin.de, we will be happy to help and implement what is needed. 




==============================
To run the delivered examples:

1. Install the delivered python version and all packages (see software.txt for the download links)

2. Set environment variables (refer to Install-Guide in Documentation)

3. Set all paths and desiered tools in "userSettings.py"

4. Build your solution with "python setup.py build" in your command window

5. Set the model you like to simulate in "scripts/main.py"

6. Set the model parameters and transitions in "scripts/<modelName>.py"

7. Run the simulation with "python main.py"