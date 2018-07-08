#!/bin/sh
unset LD_LIBRARY_PATH
source ~/.profile
pipenv run python ngcm700_status.py
