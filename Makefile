PROJECT_NAME := agents

marimo:
	uv run marimo edit

.PHONY: buildsrc
buildsrc: 
	buildsrc

.PHONY: tree
tree:
	buildsrc --tree

.PHONY: ensuregithub
ensuregithub:
	./tools/ensure-github-url

lint:
	ruff check .

format:
	black .

test: 
	uv run pytest -v -s -n auto

test-fast:
	uv run pytest -v -n auto -m "not slow"

test-slow:
	uv run pytest -v -s -m slow

test-single:
	uv run pytest -v -s

check: 
	make lint
	make format
	make buildsrc
	make tree

migrate:
	uv run yoyo apply --config yoyo.ini --batch

