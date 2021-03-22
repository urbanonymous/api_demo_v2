.DEFAULT_GOAL := all
	
.PHONY: all
all: build start

.PHONY: build
build:
	bash ./scripts/build.sh

.PHONY: start
start:
	bash ./scripts/start.sh

.PHONY: stop
stop:
	bash ./scripts/stop.sh

.PHONY: clean
clean:
	docker rmi mongo
	docker rmi api_demo_v2-backend
	docker rmi rasa-engine
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -type d -name '*.egg-info' `
	rm -rf `find . -type d -name 'pip-wheel-metadata' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
