
APP = SHEA
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

# To allow prompts in setup-venv.sh, set to 'false'.
INSTALL_DEFAULT = true

run: $(VENV)/bin/activate
	$(PYTHON) shea.py

setup: scripts/setup-venv.sh requirements.txt
	./scripts/setup-venv.sh $(APP) $(VENV) $(INSTALL_DEFAULT)

upgrade: $(VENV) requirements.txt
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
