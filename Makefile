# define the name of the virtual environment directory
VENV := .venv

# default target, when make executed without arguments
all: venv

venv_base: requirements_base.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements_base.txt

venv_runtime: requirements_base.txt requirements_runtime.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements_base.txt -r requirements_runtime.txt

pkg: venv_runtime
	poetry build

test: runpytest

run: venv_runtime
	sudo ./$(VENV)/bin/python solrpi_main.py

runpytest: venv_base
	./$(VENV)/bin/python3 -m pytest -rP

install:
	bash install.sh

uninstall:
	bash uninstall.sh

clean:
	rm -rf $(VENV)
	rm -rf dist

asciidemo: venv_base
	./$(VENV)/bin/python3 solrpi_demo_ascii.py

.PHONY: all venv test clean install
