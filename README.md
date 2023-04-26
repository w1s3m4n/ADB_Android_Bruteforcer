# Simple Android ADBBruteforcer

## Description

This tool is made for testing purposes and uses ADB (Android Debug Shell). It allows you to use two bruteforcing methods: tap and locksettings.
The __tap__ option is only tested on a OnePlus device with Oxygen OS. If you want to use it in other devices, you should map the device screen enabling UI debug on Developer Options. The __lockscreen__ method can be used on all Android devices.

### Disclaimer

This tool is not a valid, fast and exploiter tool for Android. You need to have the following scenario:
* **Developer Options unlocked** (you can do it by tapping from 5 to 10 times on the Build number in Settings -> System)
* **Debug Mode activaded** (Located in Developer Options)
* **PC trusted by your phone** (allow it on the dialog spawned when connecting your device to your PC)

## Usage
```
usage: python3 ADBBruteforcer.py [-h] [-n NDIGITS] [-m METHOD] [-c COOLDOWN]

optional arguments:
  -h, --help                        Show this help message and exit
  -n NDIGITS, --ndigits NDIGITS     The number of PIN digits
  -m METHOD, --method METHOD        The method to use ('touch' or 'locksettings')
  -c COOLDOWN, --cooldown COOLDOWN  Seconds to wait if a cooldown is detected
```

## Installation
You have to have python3.x installed
```
pip install -U -r requirements.txt
```

### Legal note
*This tool is only developed for testing and demo purposes. The creator will not accept any responsabilities regarding an ilegal or bad usage of the tool*

Made by @Hackermate_ (w1s3m4n)