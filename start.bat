@echo off

REM Install pip and setuptools
python3 -m pip install --upgrade pip setuptools

REM Create a virtual environment
python3 -m virtualenv .venv

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Install the requirements
pip3 install -r requirements.txt

REM Start the application
python3 run.py
