


ifndef VIRTUAL_ENV
	# how to make this work?
	[ -d .venv ] || python -m venv .venv ;
	source .venv/bin/activate
endif




AMPY=.venv/bin/ampy
AMPY_PORT=/dev/ttyACM0

flash: out2/*/*.py out2/*.py
.PHONY: flash

term:
	python -m serial $(AMPY_PORT) --exit-char 24 --raw

# out/main.py: source/main.py
# 	$(AMPY) --port $(AMPY_PORT) put source/main.py main.py
# 	touch $@
# out/dial/dial.py: source/dial/dial.py
# 	$(AMPY) --port $(AMPY_PORT) put source/dial/dial.py dial/dial.py
# 	touch $@
# out/dial/__init__.py: source/dial/__init__.py
# 	$(AMPY) --port $(AMPY_PORT) put source/dial/__init__.py dial/__init__.py
# 	touch $@
# out/sim800/sim800.py: source/sim800/sim800.py
# 	$(AMPY) --port $(AMPY_PORT) put source/sim800/sim800.py sim800/sim800.py
# 	touch $@
# out/sim800/sim800_serial.py: source/sim800/sim800_serial.py
# 	$(AMPY) --port $(AMPY_PORT) put source/sim800/sim800_serial.py sim800/sim800_serial.py
# 	touch $@
# out/sim800/__init__.py: source/dial/__init__.py
# 	$(AMPY) --port $(AMPY_PORT) put source/sim800/__init__.py sim800/__init__.py
# 	touch $@
# out/logging/__init__.py: source/logging/__init__.py
# 	$(AMPY) --port $(AMPY_PORT) put source/logging/__init__.py logging/__init__.py
# 	touch $@
# out/logging/handlers.py: source/logging/handlers.py
# 	$(AMPY) --port $(AMPY_PORT) put source/logging/handlers.py logging/handlers.py
# 	touch $@
# out/aioble/%.py: source/aioble/%.py
# 	cp $< $@
#	$(AMPY) --port $(AMPY_PORT) put out/aioble/$@ aioble/$@
# $(AMPY) --port $(AMPY_PORT) put "$@"



out2/main.py: source2/main.py
	$(AMPY) --port $(AMPY_PORT) put source2/main.py main.py
	touch $@
out2/dial/dial.py: source2/dial/dial.py
	$(AMPY) --port $(AMPY_PORT) put source2/dial/dial.py dial/dial.py
	touch $@
out2/dial/__init__.py: source2/dial/__init__.py
	$(AMPY) --port $(AMPY_PORT) put source2/dial/__init__.py dial/__init__.py
	touch $@
out2/sim800l.py: source2/sim800l.py
	$(AMPY) --port $(AMPY_PORT) put source2/sim800l.py sim800l.py
	touch $@
out2/phoneui.py: source2/phoneui.py
	$(AMPY) --port $(AMPY_PORT) put source2/phoneui.py phoneui.py
	touch $@
out2/ui.py: source2/ui.py
	$(AMPY) --port $(AMPY_PORT) put source2/ui.py ui.py
	touch $@
out2/pinout.py: source2/pinout.py
	$(AMPY) --port $(AMPY_PORT) put source2/pinout.py pinout.py
	touch $@
out2/logging/__init__.py: source2/logging/__init__.py
	$(AMPY) --port $(AMPY_PORT) put source2/logging/__init__.py logging/__init__.py
	touch $@
