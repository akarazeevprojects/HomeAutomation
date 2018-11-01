## HomeAutomation with bot for Telegram and [homebridge](https://github.com/nfarina/homebridge)

First of all you need to install `homebridge` on your machine (Raspberry Pi) along with plugins (personally I use **cmdSwitch2** and **TemperatureFile** for now).

Then you need to configure your home automation system inside the `system.py` file.

After that just generate new `config.json` and replace `~/.homebridge/config.json` with newly generated `newconfig.json`:
```
<<<<<<< HEAD
python3 home_automation/generate_config.py -r
=======
python home_automation/generate_config.py -r
>>>>>>> 62d8a3ca74d5ae84bdfdabb1dad1e8954bede276
```

To start all services you can use `res/startup.sh` (with **screen** commands) or `res/tmux_startup.sh` (with **tmux** commands).
