#!/usr/bin/env bash
tmux new-session -d -s home
tmux send -t home.0 "homebridge" ENTER

tmux new-session -d -s temp
tmux send -t temp.0 "cd /home/pi/WD/home_automation/home_automation && python3 temp.py" ENTER

tmux new-session -d -s tg
tmux send -t tg.0 "cd /home/pi/WD/home_automation/home_automation && source ~/.envs/home/bin/activate && python3 bot.py" ENTER