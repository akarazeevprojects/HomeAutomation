## HomeAutomation with bot for Telegram and homebridge

[[video demonstration](https://youtu.be/CBYfVpwmrjc) of homebridge/HomeKit part]

![alt](https://img.youtube.com/vi/CBYfVpwmrjc/0.jpg)

Manual for installation of [Raspbian and homebridge on Raspberry Pi](https://akarazeev.github.io/home-automation-homekit/) and [a project of home automation via HomeKit using Raspberry Pi](https://akarazeev.github.io/proj_homeautomation/).

## Overview

First of all you need to install `homebridge` on your machine (Raspberry Pi) along with plugins (personally I use **cmdSwitch2** and **TemperatureFile** for now).

Then you need to configure your home automation system inside the `system.py` file.

After that just generate new `config.json` and replace `~/.homebridge/config.json` with newly generated `newconfig.json`:
```
python home_automation/generate_config.py -r
```

To start all services you can use `res/startup.sh` (with **screen** commands) or `res/tmux_startup.sh` (with **tmux** commands).

## Resources

| Name | Description     |
| :------------- | :------------- |
| [Etcher](https://etcher.io)       | Burn [Raspbian images](https://www.raspberrypi.org/downloads/raspbian/) to Raspberry Pi      |
| [homebridge](https://github.com/nfarina/homebridge)   | Server for [HomeKit](https://www.apple.com/ios/home/)  |
| [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)   | [Telegram](https://telegram.org) API wrapped into package for Python   |
