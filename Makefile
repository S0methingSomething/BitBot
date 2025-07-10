.PHONY: setup

setup:
	@echo "Setting up the development environment with uv..."
	@uv venv --python python3
	@uv pip compile pyproject.toml -o requirements.txt
	@uv pip install -r requirements.txt
	@uv pip install -r requirements-dev.txt
	@echo "Setup complete. Activate the virtual environment with 'source .venv/bin/activate'"
