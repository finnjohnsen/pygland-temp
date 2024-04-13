.PHONY: flash rm deploy mpy $(ALL_MPY) $(ALL_SRC) $(APP_SRC) $(LIBS_SRC)

FIRMWARE=ESP32_GENERIC_C3-20240222-v1.22.2.bin

DEVICE=/dev/ttyACM0
D=a0
MPY_OUTPUT_DIR=mpy-out

dependencies:
	pipx install mpr
	pipx install mpy-cross

download-firmware:
	curl --create-dirs -O --output-dir firmware/ -J https://micropython.org/resources/firmware/$(FIRMWARE)

erase-flash:
	esptool.py --chip esp32c3 --port $(DEVICE) erase_flash

flash:
	esptool.py --chip esp32c3 --port $(DEVICE) --baud 921600 --before default_reset --after hard_reset --no-stub  write_flash --flash_mode dio --flash_freq 80m 0x0 firmware/$(FIRMWARE)
	sleep 2

ls:
	mpr -d $(D) ls

upload:
	mpr -d $(D) put *.py /

rm:
	mpr -d $(D) rm --rf /

rm-libs:
	mpr -d $(D) rm --Rf /lib

soft-reset:
	mpr -d $(D) x

sr: soft-reset

reset:
	mpr -d $(D) reboot

deploy-lib-mpy:
	mpr -d $(D) mkdir lib
	mpr -d $(D) mkdir lib/aioble
	mpr -d $(D) put $(MPY_OUTPUT_DIR)/lib/*.mpy /lib
	mpr -d $(D) put $(MPY_OUTPUT_DIR)/lib/aioble/*.mpy /lib/aioble

deploy-mpy: rm deploy-lib-mpy
	mpr -d $(D) put $(MPY_OUTPUT_DIR)/*.mpy /
	mpr -d $(D) put main.py /
	mpr -d $(D) put -f config.json /config.json
	mpr -d $(D) b

deploy-dev: rm
	mpr -d $(D) put -r lib /
	mpr -d $(D) put -f app.py /app.py
	mpr -d $(D) put -f tempble.py /tempble.py
	mpr -d $(D) put -f config.json /config.json
	mpr -d $(D) put -f main.py /main.py
	mpr -d $(D) b

APP_SRC 	= app.py tempble.py
LIBS_SRC 	= lib/sht31.py lib/ssd1306.py
LIB_AIOBLE_SRC  = lib/aioble/__init__.py lib/aioble/core.py lib/aioble/server.py lib/aioble/device.py lib/aioble/peripheral.py
ALL_SRC 	= $(APP_SRC) $(LIBS_SRC) $(LIB_AIOBLE_SRC)
ALL_MPY 	= $(patsubst %.py, %.mpy, $(ALL_SRC))

mk-required-path:
	mkdir -p $(MPY_OUTPUT_DIR)/lib/aioble

%.mpy: %.py
	mpy-cross -march=xtensawin $< -o $(MPY_OUTPUT_DIR)/$@

compile-mpy: $(ALL_MPY)

mpy: mk-required-path compile-mpy

developer-getting-started: dependencies download-firmware
clean-micropython-device: flash rm