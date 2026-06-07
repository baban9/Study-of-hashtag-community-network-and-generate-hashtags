.PHONY: setup run test clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

run:
	cd hashtagApp && ../.venv/bin/python app.py

test:
	.venv/bin/python -c "import sys; sys.path.insert(0,'hashtagApp'); import config; print('config ok')"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
