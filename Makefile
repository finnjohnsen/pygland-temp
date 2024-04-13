DEVICE=/dev/ttyACM0
D=a0
MPY_OUTPUT_DIR=mpy-out

dependencies:
	pipx install mpr
	pipx install mpy-cross

erase-flash:
	esptool.py --chip esp32c3 --port $(DEVICE) erase_flash

flash:
	esptool.py --chip esp32c3 --port $(DEVICE) --baud 921600 --before default_reset --after hard_reset --no-stub  write_flash --flash_mode dio --flash_freq 80m 0x0 firmware/ESP32_GENERIC_C3-20240222-v1.22.2.bin
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

deploy-mpy: rm
	mpr -d $(D) mkdir lib
	mpr -d $(D) mkdir lib/aioble
	mpr -d $(D) put $(MPY_OUTPUT_DIR)/lib/*.mpy /lib
	mpr -d $(D) put $(MPY_OUTPUT_DIR)/lib/aioble/*.mpy /lib/aioble
	mpr -d $(D) put $(MPY_OUTPUT_DIR)/*.mpy /
	mpr -d $(D) put -f config.json /config.json
	mpr -d $(D) put -f main.py /main.py
	mpr -d $(D) b

deploy-dev: rm
	mpr -d $(D) put -r lib /
	mpr -d $(D) put -f app.py /app.py
	mpr -d $(D) put -f tempble.py /tempble.py
	mpr -d $(D) put -f config.json /config.json
	mpr -d $(D) put -f main.py /main.py
	mpr -d $(D) b


APP_SRC 	= app.py boot.py tempble.py
LIBS_SRC 	= lib/sht31.py lib/ssd1306.py
LIB_AIOBLE_SRC  = lib/aioble/__init__.py lib/aioble/core.py lib/aioble/server.py lib/aioble/device.py
ALL_SRC 	= $(APP_SRC) $(LIBS_SRC) $(LIB_AIOBLE_SRC)
ALL_MPY 	= $(patsubst %.py, %.mpy, $(ALL_SRC))

mk-required-path:
	mkdir -p $(MPY_OUTPUT_DIR)/lib/aioble

%.mpy: %.py
	mpy-cross -march=xtensawin $< -o $(MPY_OUTPUT_DIR)/$@

mpy_: $(ALL_MPY)

mpy: mk-required-path mpy_

.PHONY: flash rm deploy mpy a $(ALL_MPY_) $(ALL_SRC_) $(APP_SRC_) $(LIBS_SRC_)
