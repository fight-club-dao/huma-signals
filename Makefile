.PHONY: lint, lint-check, test, run-local

lint:
	poetry run autoflake --in-place --remove-all-unused-imports --verbose -r huma_signals tests
	poetry run black huma_signals tests --target-version py310
	poetry run flake8 huma_signals tests --max-line-length 120 --ignore "E203, W503"
	poetry run isort huma_signals tests
	poetry run mypy --show-error-codes .
	poetry run pylint huma_signals

lint-check:
	poetry run black huma_signals tests --target-version py310 --check
	poetry run flake8 huma_signals tests --max-line-length 120 --ignore "E203, W503"
	poetry run isort --check huma_signals tests
	poetry run mypy --show-error-codes .
	poetry run pylint huma_signals

test:
	ENV=test poetry run python3 -m pytest -v --cov=huma_signals --color=yes --cov-report term-missing --ignore=tests/adapters/request_network

run-local:
	ENV=development poetry run python3 -m uvicorn main:app --reload --port 8001

build-image:
	docker build -t huma-signals -f Dockerfile.lambda .

push-image: build-image
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 778966706143.dkr.ecr.us-east-2.amazonaws.com
	docker tag huma-signals:latest 778966706143.dkr.ecr.us-east-2.amazonaws.com/huma-signals:latest
	docker push 778966706143.dkr.ecr.us-east-2.amazonaws.com/huma-signals:latest
