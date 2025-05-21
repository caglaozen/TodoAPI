VENV_PATH = venv
PYTHON = python3
PIP = pip

.PHONY: clean setup uninstall install update-requirements test style-check format

clean:
	rm -rf $(VENV_PATH)
	rm -rf __pycache__

setup:
	python3.13 -m venv $(VENV_PATH)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

uninstall:
	$(PIP) freeze | xargs pip uninstall -y

install:
	$(PIP) install -r requirements.txt

update-requirements:
	$(PIP) freeze > requirements.txt

test:
	$(PYTHON) -m unittest discover -s test/unit/

style-check:
	black src/ test/ --line-length=120 --target-version=py312 --check
	isort . --profile black --line-length 120 --python-version 312 --check

format:
	black src/ test/ --line-length=120 --target-version=py312
	isort . --profile black --line-length 120 --python-version 312
