from machine import Pin, I2C, Timer
from micropython import const
import bluetooth
import asyncio
import lib.aioble as aioble
import lib.sht31 as sht31
import lib.ssd1306 as ssd1306

i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=400000)
sensor = sht31.SHT31(i2c, addr=0x44)

th = sensor.get_temp_humi()
temp = int("{0:.0f}".format(th[0]*100))
print(temp)