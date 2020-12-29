:: check if virtual environment exists
IF NOT EXIST .\venv\NUL python -m venv venv

call venv\scripts\activate.bat
pip install -r requirements.txt