#!/bin/sh
unset LD_LIBRARY_PATH
. ~/.profile
pipenv run python ngcm700_status.py
