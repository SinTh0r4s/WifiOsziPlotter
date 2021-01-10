WifiOszi

This repository provides the code for the PC Frontend of the WifiOszo PRoject. This project is intended to provide
basic oscilloscope access to unknown GND potentials without the risk of destroying a 20k gadget.

![Application screenshot](https://https://gitlab.lrz.de/wifioszi/pyplotter/-/blob/screenshot/screenshot.jpg?raw=true)

Any board will announce itself automatically to the application and will appear as possibility in the board selector
on the top left. The rest of the application will always referrence to the selected board. Any board will also announce
its capabilities which are listed in the board information right below the board selector.
In the bottom left you can set a trigger for a specific channel and voltage. As soon as the trigger is hit the board
will fill its available RAM with measurements and, as soon as that is done, transmit those measurements to the
application. Incoming measurements will always be rendered as soon as they arrive. Technically it is possible for
transmissions to be corrupted (UDP) which will lead to the application not receiving any measurements. If a trigger
was hit and you don't get any measurements please try again. Should be a very rare case though.
On the right hand side you can select all the measurement sets you received from the selected board. The data is
only deleted once the application is closed. So you can try multiple measurements and only export the one of interest.
I hope this gadget will save someone some time.

SETUP

To run the code in this repository you need to provide a Python 3.7 installation. You are free to try other versions,
but at the time of development Python 3.10 did not work so don't expect it to.
For Windows users there are 4 scripts in this repository to fulfill certain setup duties. If those scripts won't work
the most likely cause is a wrong Python version or a missing PATH entry. If the scripts won't work on windows, open
a Command Promp (cmd.exe) and enter 'python --version'. It should reply with 'Python 3.7.X'.

Due to a bug in matplotlib it is required to use an older, specific version: 'matplotlib 2.2.2'. Further, there
is also a bug in numpy which requires you to not use version 1.19.4. Please use numpy 1.19.3 instead or try
more recent releases as soon as they become available. Please note, that all requirements are specified in
'requirements.txt' and this file is used to install dependencies. Dependencies are handled in the provided scripts.

With 'setup_dev.bat' you will create the virtual environment for python and install required dependencies. 

'run_gui.bat' will invoke 'setup-dev.bat' if no virtual environment is found and afterwards runs the code supplied.

'run_test.bat' will invoke 'setup-dev.bat' if no virtual environment is found and afterwards runs the tests.

Further, you can package the code into a single .exe file or a folder of an .exe file and its dependencies. While
the first is best for handling, the latter has significant fast load time.

As development environment i can reccomend PyCharm by JetBrains. Simply open the repositories folder and run main.py.
