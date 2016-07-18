VENV_NAME := venv
PYTHON := $(CURDIR)/$(VENV_NAME)/bin/python
PIP := $(CURDIR)/$(VENV_NAME)/bin/pip

.PHONY: install-hooks
install-hooks: dependencies
	$(PIP) install pre_commit
	$(PYTHON) -m pre_commit.main install -f --install-hooks


.PHONY: venv
venv:
	virtualenv $(VENV_NAME)

.PHONY: dependencies
dependencies: venv

.PHONY: clean
clean:
	# Delete compiled files
	find . -name '*.pyc' -delete
	# Delete python cache directory
	find . -name '__pycache__' | xargs rm -rf
	# Remove local virtual environment and tox environments
	rm -rf venv .tox
