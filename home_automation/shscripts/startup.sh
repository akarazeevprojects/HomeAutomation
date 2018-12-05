#!/usr/bin/env bash
su -c "screen -dmS app bash -c 'cd /home/pi/HomeAutomation/home_automation && source ~/.envs/home/bin/activate && python3 app.py'" -s /bin/sh pi
su -c "screen -dmS home bash -c 'homebridge;'" -s /bin/sh pi
su -c "screen -dmS temp bash -c 'cd /home/pi/HomeAutomation/home_automation/home_automation && source ~/.envs/home/bin/activate && python3 temp.py;'" -s /bin/sh pi
su -c "screen -dmS tg bash -c 'cd /home/pi/HomeAutomation/bot && source ~/.envs/home/bin/activate && python3 bot.py'" -s /bin/sh pi
