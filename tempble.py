import bluetooth
from micropython import const
import lib.aioble as aioble

class TempBLE:
    ENV_SENSE_UUID = bluetooth.UUID(0x181A)
    ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
    ENV_SENSE_HUM_UUID = bluetooth.UUID(0x2A6F)
    GENERIC_THERMOMETER = const(768)
    ADV_INTERVAL_US = const(250000)

    temp_service = aioble.Service(ENV_SENSE_UUID)
    temp_char = aioble.Characteristic(temp_service, ENV_SENSE_TEMP_UUID, read=True, notify=True)
    hum_char = aioble.Characteristic(temp_service, ENV_SENSE_HUM_UUID, read=True, notify=True)

    def __init__(self):
        ""

    def updateCharacteristics(self, th):
        temp = int("{0:.0f}".format(th[0]*100))
        self.temp_char.write(temp.to_bytes(4, "little"), send_update=True)
        hum = int("{0:.0f}".format(th[1]*100))
        self.hum_char.write(hum.to_bytes(4, "little"), send_update=True)

    async def start(self):
        print("Starting BLE")
        aioble.register_services(self.temp_service)
        self.connection = await aioble.advertise(
            self.ADV_INTERVAL_US,
            name="pytemp-1",
            services=[self.ENV_SENSE_UUID],
            appearance=self.GENERIC_THERMOMETER,
            manufacturer=(0xabcd, b"1234"),
    )