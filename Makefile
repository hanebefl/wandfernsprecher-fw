


ifndef VIRTUAL_ENV
	# how to make this work?
	[ -d .venv ] || python -m venv .venv ;
	source .venv/bin/activate
endif




AMPY=.venv/bin/ampy
AMPY_PORT=/dev/ttyACM0

flash: out/*/*.py out/*.py
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
out/sim800l.py: source/sim800l.py
	$(AMPY) --port $(AMPY_PORT) put source/sim800l.py sim800l.py
	touch $@
out/phoneui.py: source/phoneui.py
	$(AMPY) --port $(AMPY_PORT) put source/phoneui.py phoneui.py
	touch $@
out/ui.py: source/ui.py
	$(AMPY) --port $(AMPY_PORT) put source/ui.py ui.py
	touch $@
out/pinout.py: source/pinout.py
	$(AMPY) --port $(AMPY_PORT) put source/pinout.py pinout.py
	touch $@
out/logging/__init__.py: source/logging/__init__.py
	$(AMPY) --port $(AMPY_PORT) put source/logging/__init__.py logging/__init__.py
	touch $@
