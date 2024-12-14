


ifndef VIRTUAL_ENV
	# how to make this work?
	[ -d .venv ] || python -m venv .venv ;
	source .venv/bin/activate
endif




AMPY=.venv/bin/ampy
AMPY_PORT=/dev/ttyACM0

flash: out/*/*.py out/main.py
.PHONY: flash

term:
	python -m serial $(AMPY_PORT) --exit-char 24 --raw

out/main.py: source/main.py
	$(AMPY) --port $(AMPY_PORT) put source/main.py main.py
	touch $@
out/dial/dial.py: source/dial/dial.py
	$(AMPY) --port $(AMPY_PORT) put source/dial/dial.py dial/dial.py
	touch $@
out/dial/__init__.py: source/dial/__init__.py
	$(AMPY) --port $(AMPY_PORT) put source/dial/__init__.py dial/__init__.py
	touch $@
out/sim800/sim800.py: source/sim800/sim800.py
	$(AMPY) --port $(AMPY_PORT) put source/sim800/sim800.py sim800/sim800.py
	touch $@
out/sim800/sim800_serial.py: source/sim800/sim800_serial.py
	$(AMPY) --port $(AMPY_PORT) put source/sim800/sim800_serial.py sim800/sim800_serial.py
	touch $@
out/sim800/__init__.py: source/dial/__init__.py
	$(AMPY) --port $(AMPY_PORT) put source/sim800/__init__.py sim800/__init__.py
	touch $@
out/logging/__init__.py: source/logging/__init__.py
	$(AMPY) --port $(AMPY_PORT) put source/logging/__init__.py logging/__init__.py
	touch $@
out/logging/handlers.py: source/logging/handlers.py
	$(AMPY) --port $(AMPY_PORT) put source/logging/handlers.py logging/handlers.py
	touch $@
out/aioble/%.py: source/aioble/%.py
	cp $< $@
#	$(AMPY) --port $(AMPY_PORT) put out/aioble/$@ aioble/$@
# $(AMPY) --port $(AMPY_PORT) put "$@"

