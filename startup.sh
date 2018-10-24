#!/usr/bin/env bash
su -c "screen -dmS home bash -c 'cd /home/pi/WD/home_automation; homebridge;'" -s /bin/sh pi
su -c "screen -dmS temp bash -c 'cd /home/pi/WD/home_automation; python3 temp.py;'" -s /bin/sh pi
su -c "screen -dmS tg bash -c 'cd ~/WD/home_automation/ && source ~/.envs/home/bin/activate && python3 bot.py'" -s /bin/sh pi