#!/bin/env bash

# Make venv
python -m venv .venv
source .venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt

# Install and run this project
python -m pip install .
python -m y
