## Set up

#### Create a virtual conda environment with all the packages
1. Run conda create -n venv_name and source activate venv_name, where venv_name is the name of your virtual environment.
2. Install all conda packages
2. Run conda install pip. This will install pip to your venv directory.
3. Find your anaconda directory, and find the actual venv folder. It should be somewhere like /anaconda/envs/venv_name/.
4. Install all pip packages by doing /anaconda/envs/venv_name/bin/pip install package_name.

#### Set up Interpreter in Pycharm
1. Add virtual environment by clicking on the interpreter in the bottom right
2. Click add interpreter and then virtual environment
3. Let the interpreter path point to "/home/sevi/anaconda3/envs/vreveal/bin/python" (the python file inside your conda virtual environment's bin folder)

#### Set up debug/run configuration
1. in the drop down menu on the top right next to the run and debug symbol click edit configurations
2. click on the plus in the top left and hit python
3. script path: "/home/sevi/PycharmProjects/revealapp/50_deployment/REAL/testfile.py"
4. Python Interpreter: pointing to your venv
5. WOrking Directory: "/home/sevi/PycharmProjects/revealapp/50_deployment/REAL"
6. OK

#### Good to know
The script is creating a directory on your Desktop called "TEST_revealStorage" to save the model and embeddings.


