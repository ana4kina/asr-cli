#!/usr/bin/env bash
set -e
python3 -m pip install Cython
python3 -m pip install -e .
python3 interface.py