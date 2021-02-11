#! /bin/bash

sudo apt install git python3 python3-pip python3-venv python3-virtualenv -y

mkdir -p ~/.local/lib/failarchi
git clone https://github.com/JulesdeCube/FailArchi.git ~/.local/lib/failarchi

python3 -m venv ~/.local/lib/failarchi/.venv
source ~/.local/lib/failarchi/.venv/bin/activate
python3 -m pip install wheel
python3 -m pip install -r ~/.local/lib/failarchi/requirements.txt
deactivate

mkdir -p ~/.local/bin
ln -s ~/.local/lib/failarchi/scripts/run.sh ~/.local/bin/failarchi
chmod +x ~/.local/lib/failarchi/scripts/run.sh

echo 'PATH="$HOME/.local/bin:$PATH"' > ~/.profile