install:
	pip install -r requirements.txt

test:
	PYTHONPATH=src pytest -v

run:
	PYTHONPATH=src python -m defai.cli $(ADDRESS)

docker-build:
	docker build -t defai-systems .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
