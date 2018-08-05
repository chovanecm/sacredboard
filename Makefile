default:
	@echo make pydependencies		Install Python dependencies
	@echo make test		    run all tests
	@echo make pytest		run Python tests only. Python3.5 or higher must be installed.
	@echo make flake8		run Python code style checker
	@echo make pydocstyle		run Python documentation style checker
	@echo make qunit		run JavaScript unit tests. node.js required.
	@echo make eslint		run JavaScript code and documentation checker. node.js required

pydocstyle:
	pydocstyle sacredboard

flake8:
	flake8 sacredboard

pytest:
	python setup.py test -v

node_modules:	package.json
	npm install

qunit:	node_modules
	npm test

eslint:	node_modules
	npm run lint -s

pydependencies: pyrequirements pydevrequirements pytestrequirements

pytestrequirements: pytest-requirements.txt
	pip install -r pytest-requirements.txt

pyrequirements: requirements.txt
	pip install -r requirements.txt

pydevrequirements: dev-requirements.txt
	pip install -r dev-requirements.txt

test: pytest qunit flake8 pydocstyle eslint

clean:
	rm -r node_modules