:: check if virtual environment exists
IF NOT EXIST .\venv\NUL call setup_dev.bat

call venv\scripts\activate.bat
python -m osziplotter.main