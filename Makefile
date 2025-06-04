install:
	pip install -r requirements.txt

format:
	black src/ tests/

lint:
	flake8 src/ tests/

test:
	pytest --cov=src tests/

run:
	python main.py
