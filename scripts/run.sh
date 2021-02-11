#! /bin/bash

ABSDIR=$(dirname "$(readlink -f $0)")/..

source $ABSDIR/.venv/bin/activate
python3 $ABSDIR/main.py $@
deactivate