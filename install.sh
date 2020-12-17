#! /bin/sh
mkdir -p ~/.local/lib/failachi
git clone  git@github.com:JulesdeCube/failachi.git ~/.local/lib/failachi

mkdir -p ~/.local/bin
ln -s ~/.local/lib/failachi/main.py ~/.local/bin/failachi