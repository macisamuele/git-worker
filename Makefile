VENV_NAME := venv
PYTHON := $(CURDIR)/$(VENV_NAME)/bin/python
PIP := $(CURDIR)/$(VENV_NAME)/bin/pip
export GIT_SHA ?= $(USER)-$(shell git rev-parse --short HEAD)

.PHONY: install-hooks
install-hooks: dependencies
	$(PIP) install pre_commit
	$(PYTHON) -m pre_commit.main install -f --install-hooks


.PHONY: test
test:
	docker build -t git-worker:${GIT_SHA} tests
	$(eval CID := $(shell docker run -d -it -P git-worker:$(GIT_SHA)))
	$(eval CPORT := $(shell docker inspect --format='{{(index (index .NetworkSettings.Ports "8181/tcp") 0).HostPort}}' $(CID)))
	$(eval export GIT_SERVER := "http://localhost:$(CPORT)")
	$(eval export CONTAINER_ID := "$(CID)")
	tox -e pytest

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
