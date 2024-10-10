push:
	git add . && codegpt commit . && git push

clean:
	rm -Rf ./dist

setup:
	virtualenv .venv -p python3.10
	./.venv/bin/pip install pip-tools

install:
	./.venv/bin/pip-compile ./requirements/requirements.txt ./requirements/dev-requirements.txt -v --output-file ./requirements.txt
	./.venv/bin/pip-sync -v

install-hook:
	pre-commit install

lint:
	pre-commit run --all-files
