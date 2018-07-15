#!/bin/sh
unset LD_LIBRARY_PATH
. ~/.profile
~/.local/bin/pipenv run python ngcm700_reboot.py
