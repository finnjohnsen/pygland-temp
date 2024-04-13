from machine import Pin, I2C, Timer
from micropython import const
import asyncio
import lib.sht31 as sht31
import lib.ssd1306 as ssd1306

print(f"Hei REPL")

i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=400000)
sensor = sht31.SHT31(i2c, addr=0x44)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

th = sensor.get_temp_humi()
temp = int("{0:.0f}".format(th[0]*100))
print(temp)

display.fill(0)
display.text(f"HEI REPL", 0, 24)
display.show()