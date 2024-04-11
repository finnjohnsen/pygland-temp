from machine import Pin, I2C, Timer
from micropython import const
import bluetooth
import asyncio
import lib.aioble as aioble
import lib.sht31 as sht31
import lib.ssd1306 as ssd1306

#import app

_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
_ENV_SENSE_HUM_UUID = bluetooth.UUID(0x2A6F)
_GENERIC_THERMOMETER = const(768)

_ADV_INTERVAL_US = const(250000)

temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_char = aioble.Characteristic(temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True)
hum_char = aioble.Characteristic(temp_service, _ENV_SENSE_HUM_UUID, read=True, notify=True)

aioble.register_services(temp_service)


async def updateBLE():
    connection = await aioble.advertise(
        _ADV_INTERVAL_US,
        name="pytemp-1",
        services=[_ENV_SENSE_UUID],
        appearance=_GENERIC_THERMOMETER,
        manufacturer=(0xabcd, b"1234"),
    )

temp:int = 2400
temp_char.write(temp.to_bytes(4, "little"), send_update=True)


asyncio.run(updateBLE())
