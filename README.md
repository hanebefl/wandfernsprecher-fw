# Wandfernsprecher Firmware
Based on Jeffrey N. Magee's [UpyPhone](https://github.com/jeffmer/micropython-upyphone), brutally mangeled to work without a touch screen, but with a rotary dial and switches on an esp32-c3.


## Hardware
This code is designed to run on custom hardware, the [GSM Wandfernsprecher](https://github.com/hanebefl/wandfernsprecher-hw) which is based on the ESP32-C3-WROOM-02 module.

## Uploading the code
### tl;dr
```bash
source .venv/bin/activate
make flash      # uploads changed files
make term       # opens a serial shell
make flash term # uploads all changes and opens a shell
```
### Prequisites
1. Make sure a compatible version of [Micropython](https://micropython.org/download/ESP32_GENERIC_C3/) is running on the ESP32.
2. Install ampy
    (a) run `python -m venv .venv` to create a virtual python environment
    (b) run `source .venv/bin/activate` to activate it
    (c) run `pip install adafruit-ampy` to install ampy
    (d) you may need to change the `AMPY_PORT` in the Makefile.
    
Make sure to activate the virtual environment once before use.

### Flashing
A Makefile is included for easy flashing. The command `make flash` will upload all changed files to the ESP32. This relies on "shadow files" in the out/ folder, to recognize changed files. If new files are necessary, add an entry to the Makefile, and add the shadow file (e.g. with `touch out/new_shadow_file,py`, an empty file is enough).


### Debug shell
You can get a debug shell with the command `make term`.