#! /bin/bash

sudo apt install git python3 python3-pip python3-venv python3-virtualenv -y

mkdir -p ~/.local/lib/failachi
git clone https://github.com/JulesdeCube/FailArchi.git ~/.local/lib/failachi

python3 -m venv ~/.local/lib/failachi/.venv
source ~/.local/lib/failachi/.venv/bin/activate
python3 -m pip install wheel
python3 -m pip install -r ~/.local/lib/failachi/requirements.txt
deactivate

mkdir -p ~/.local/bin
ln -s ~/.local/lib/failachi/scripts/run.sh ~/.local/bin/failachi
chmod +x ~/.local/lib/failachi/scripts/run.sh

echo 'PATH="$HOME/.local/bin:$PATH"' > ~/.profile