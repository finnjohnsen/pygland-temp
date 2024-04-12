from machine import Pin, I2C
import asyncio
import json
import lib.sht31 as sht31
import lib.ssd1306 as ssd1306
from tempble import TempBLE

class App:
    def __init__(self):
        with open("config.json") as f:
            self.config = json.load(f)

        self.i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=400000)
        self.sensor = sht31.SHT31(self.i2c, addr=0x44)
        try:
            self.display = ssd1306.SSD1306_I2C(128, 32, self.i2c)
        except OSError:
            print("No OLED")
            self.display = None
        self.bleConnectionEvent = asyncio.Event()
        self.bleConnected = False
        self.tempble = TempBLE(self.config["bleName"], self.bleConnectionEvent)

    def updateOLEDWithSensing(self, th):
        if self.display == None:
            return
        temp = "{0:.2f}".format(th[0])
        hum = "{0:.2f}".format(th[1])
        name = self.config['bleName']
        self.display.fill(0)
        self.display.text(f"{name}", 0, 24)
        self.display.text(f"{temp}", 0, 0)
        if self.bleConnected:
            self.display.text(f"B", 55, 10)
        else:
            self.display.text(f"-", 55, 10)
        self.display.text(f"{hum}%", 75, 0)
        self.display.show()

    async def updateOLED(self):
        if self.display == None:
            return
        while True:
            th = self.sensor.get_temp_humi()
            self.updateOLEDWithSensing(th)
            await asyncio.sleep_ms(self.config["updateIntervalMs"]["OLED"])

    async def updateBLECharacteristics(self):
        await asyncio.sleep_ms(500)
        while True:
            th = self.sensor.get_temp_humi()
            self.tempble.updateCharacteristics(th)
            await asyncio.sleep_ms(self.config["updateIntervalMs"]["BLE"])

    def startDisplayMessage(self):
        if self.display == None:
            return
        self.display.fill(0)
        self.display.text('Starter...', 0, 0, 1)
        self.display.show()

    async def bleConnectionWaiter(self, event):
        while True:
            self.bleConnected = False
            await event.wait()
            if event.is_set() and not self.bleConnected:
                self.bleConnected = True
            elif not event.is_set() and self.bleConnected:
                self.bleConnected = False
            await asyncio.sleep_ms(self.config["updateIntervalMs"]["OLED"])

    async def asyncMain(self):
        updaterOLED = asyncio.create_task(self.updateOLED())
        updaterBLECharacteristics = asyncio.create_task(self.updateBLECharacteristics())
        bleServer = asyncio.create_task(self.tempble.start())
        bleConnectionWaiter = asyncio.create_task(self.bleConnectionWaiter(self.bleConnectionEvent))
        await asyncio.gather(updaterOLED, updaterBLECharacteristics, bleConnectionWaiter, bleServer)

    def run(self):
        self.startDisplayMessage()
        asyncio.run(self.asyncMain())
        