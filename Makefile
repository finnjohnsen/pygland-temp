.PHONY: flash rm deploy
DEVICE=/dev/ttyACM0
D=a0

dependencies:
	pipx install mpr

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

deploy: flash rm
	mpr -d $(D) put -r lib /
	mpr -d $(D) put  -f app.py /app.py
	mpr -d $(D) put  -f tempble.py /tempble.py
	mpr -d $(D) put  -f config.json /config.json
	mpr -d $(D) put  -f main.py /main.py
	mpr -d $(D) b



