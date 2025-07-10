PYTHON_VERSION := 3.13
.PHONY: setup lint install-hooks

setup:
	@echo "Setting up the development environment with uv..."
	@uv venv --python $(PYTHON_VERSION)
	@uv pip install -e .[dev]
	@echo "Setup complete. Activate the virtual environment with 'source .venv/bin/activate'"

install-hooks:
	@echo "Installing pre-commit hooks..."
	@.venv/bin/pre-commit install

lint:
	@echo "Running linters..."
	@.venv/bin/pre-commit run --all-files
