:: check if virtual environment exists
IF NOT EXIST .\venv\NUL call setup_dev.bat

call venv\scripts\activate.bat
pyinstaller osziplotter\main.py --name "OsziPlotter" --noconsole
pyinstaller osziplotter\main.py --name "OsziPlotter" --noconsole --onefile