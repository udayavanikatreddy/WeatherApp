#!/bin/bash

# Install pip and setuptools
python3 -m pip install --upgrade pip setuptools

# Create virtual environment
python3 -m virtualenv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requirements
pip3 install -r requirements.txt

# Start the application
python3 run.py
