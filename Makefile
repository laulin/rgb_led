install:
	@cp rgb_led.py /usr/local/bin/rgb_led
	@chmod a+x /usr/local/bin/rgb_led
	@echo "Installed !"

uninstall:
	@rm /usr/local/bin/rgb_led
	@echo "Uninstalled !"