.PHONY: all clean

SOURCES := $(shell echo src/*.py)
TARGETS := $(patsubst src/%.py,%.json,$(SOURCES))

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

%.json: src/%.py venv
	venv/bin/python $< $@

venv: requirements.txt
	type virtualenv >/dev/null
	rm -rf $@
	(virtualenv $@ && $@/bin/pip install -r $<) || rm -rf $@
