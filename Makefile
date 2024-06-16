


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
	python -m serial $(AMPY_PORT) --exit-char 24

out/main.py: source/main.py
	cp $< $@
	$(AMPY) --port $(AMPY_PORT) put out/main.py main.py
out/dial/dial.py: source/dial/dial.py
	cp $< $@
	$(AMPY) --port $(AMPY_PORT) put out/dial/dial.py dial/dial.py
out/dial/__init__.py: source/dial/__init__.py
	cp $< $@
	$(AMPY) --port $(AMPY_PORT) put out/dial/__init__.py dial/__init__.py
out/sim800/sim800.py: source/sim800/sim800.py
	cp $< $@
	$(AMPY) --port $(AMPY_PORT) put out/sim800/sim800.py sim800/sim800.py
out/sim800/__init__.py: source/sim800/__init__.py
	cp $< $@
	$(AMPY) --port $(AMPY_PORT) put out/sim800/__init__.py sim800/__init__.py
out/aioble/%.py: source/aioble/%.py
	cp $< $@
	echo "foo"
# $(AMPY) --port $(AMPY_PORT) put "$@"

