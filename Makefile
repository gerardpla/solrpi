# define the name of the virtual environment directory
VENV := .venv
PYTHON := $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements_base.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements_base.txt

$(VENV)/lib/python3.11/site-packages/rpi_ws281x: ./$(VENV)/bin/activate requirements_runtime.txt
	$(PIP) install -r requirements_runtime.txt

pkg: $(VENV)/lib/python3.11/site-packages/rpi_ws281x
	poetry build

test: runpytest

run: $(VENV)/lib/python3.11/site-packages/rpi_ws281x
	sudo $(PYTHON) solrpi_main.py

runpytest: $(VENV)/bin/activate
	$(PYTHON) -m pytest -rP

install:
	bash install.sh

uninstall:
	bash uninstall.sh

clean:
	rm -rf $(VENV)
	rm -rf dist

asciidemo: $(VENV)/bin/activate
	$(PYTHON) solrpi_demo_ascii.py

.PHONY: all test clean install
