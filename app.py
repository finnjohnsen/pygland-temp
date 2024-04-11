from machine import Pin, I2C
import asyncio
import lib.sht31 as sht31
import lib.ssd1306 as ssd1306
#from tempble import TempBLE

class App:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=400000)
        self.sensor = sht31.SHT31(self.i2c, addr=0x44)
        self.display = ssd1306.SSD1306_I2C(128, 32, self.i2c)
#        self.tempble = TempBLE()

    async def updateOLED(self, th):
        temp = "{0:.2f}".format(th[0])
        hum = "{0:.2f}".format(th[1])
        self.display.fill(0)
        self.display.text(f"{temp}", 0, 0)
        self.display.text(f"{hum}%", 80, 25, 1)
        self.display.show()

    async def update(self):
        print("Running updater")
        while True:
            print("Updating")
            th = self.sensor.get_temp_humi()
            self.updateOLED(th)
            await asyncio.sleep_ms(5000)

    def startDisplayMessage(self):
        self.display.fill(0)
        self.display.text('Starter...', 0, 0, 1)
        self.display.show()

    def run(self):
        self.startDisplayMessage()
        asyncio.run(self.update())
        
