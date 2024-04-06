#!/bin/env bash

python -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt

python -m pip install .
python -m y
