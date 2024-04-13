# My temperature sensor project

The goal of this project is to have get my esp32+sensor working and have all the tooling in order for future projects to get started quickly.

The temperature and humidity are broadcasted on Bluetooth Low-Energy and shown on the OLED.

# Software
MicroPython

1. [optional]VSCode and PyMakr extension
1. make
1. **esptool.py** must be installed (for flashing)
1. pipx tools: *mpr* and *mpy-cross*: ```make dependencies```

# Hardware
- ESP32 C3 XIAO
- SHT31 - temperature sensor
- [Optional] SSD1306 - OLED 128x32

# Wiring
OLED is optional. There is try/catch in the code to tolerate missing connected OLED.

| ESP32 PIN    | DEVICE     | DEVICE PIN |
| ------------ | ---------- | ---------- |
| D4           | SHT31      | SDA        | 
| D5           | SSD1306    | SCL        | 


# Developer HOWTO
The */Makefile* is everything

## Download micropython tools and esp32c3 firmware
```make developer-getting-started```

## Flash esp32c3
Assumes USB is /dev/ttyACM0 (aka Linux). Modify **DEVICE** and **D** in *Makefile* if different ports are relevant on your computer.

Connect esp32c3 to USB and run ```make clean-micropython-device```

## Deploy

Deploy uncompiled .py -files (presumably slower startup)

```make mky && make deploy-dev```

... or deploy pre-compiled .mpy -files

```make mky && make deploy-mpy```

## Deploy many devices

To prevent every esp32 do announce as the same BLE name, change *bleName* in config.json between each device.

Then ```make clean-micropython-device && make deploy-mpy```

## Licensing

Libraries in lib/ *The MIT License (MIT)* licensed, so hopefully everthing is fine.

# Resources
https://docs.micropython.org/en/latest/esp32/quickref.html
https://wiki.seeedstudio.com/XIAO_ESP32C3_MicroPython/