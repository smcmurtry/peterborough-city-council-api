.PHONY: run install clean

venv:
	python3 -m venv venv

install: venv
	. venv/bin/activate && pip install -r requirements.txt

run: install
	. venv/bin/activate && python app.py

clean:
	rm -rf venv
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
