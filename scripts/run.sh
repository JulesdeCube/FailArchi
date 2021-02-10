#! /bin/bash

source ~/.local/lib/failachi/.venv/bin/activate
python3 ~/.local/lib/failachi/main.py $@
deactivate