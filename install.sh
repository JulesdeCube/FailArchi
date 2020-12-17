#! /bin/bash

sudo apt install python3 python3-venv python3-virtualenv

mkdir -p ~/.local/lib/failachi
git clone  git@github.com:JulesdeCube/failachi.git ~/.local/lib/failachi

python3 -m venv ~/.local/lib/failachi/.venv
source ~/.local/lib/failachi/.venv/bin/activate
python3 -m pip install -r ~/.local/lib/failachi/requirements.txt


mkdir -p ~/.local/bin
ln -s ~/.local/lib/failachi/main.py ~/.local/bin/failachi
