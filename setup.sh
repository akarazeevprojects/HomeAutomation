#!/usr/bin/env bash
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt-get -y install git vim screen tmux tor

# Python.
sudo apt-get -y install python-pip python3-pip python-dev python-rpi.gpio
sudo pip3 install virtualenv
virtualenv ~/.envs/home

# Nodejs.
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get -y install nodejs

# Homebridge.
sudo apt-get -y install libavahi-compat-libdnssd-dev
sudo npm install -g --unsafe-perm homebridge

# Initializing ~/.homebridge folder.
tmux new-session -d -s home
tmux send -t home.0 "homebridge" ENTER
sleep 2
tmux kill-session -t home

# Plugins.
sudo npm install -g homebridge-temperature-file
sudo npm install -g homebridge-cmdswitch2

# HomeAutomation project.
git clone https://github.com/akarazeevprojects/HomeAutomation
cd HomeAutomation

export PYTHONPATH=/home/pi/HomeAutomation:$PYTHONPATH
python3 home_automation/generate_config.py -r

# Launch the services.
source ~/.envs/home/bin/activate
pip3 install -r ~/HomeAutomation/requirements.txt
