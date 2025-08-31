FROM python:3.11-slim-bookworm
WORKDIR /app

# Install wget and uv
RUN apt-get update && apt-get install -y wget &&     wget -qO- https://astral.sh/uv/install.sh | sh

# Copy pyproject.toml for dependency resolution
COPY pyproject.toml* /app/

# Try to copy requirements.txt if it exists
COPY requirements.txt* /app/ || true

# Create requirements.txt if it doesn't exist and install dependencies
RUN if [ ! -f requirements.txt ] && [ -f pyproject.toml ]; then         uv pip compile pyproject.toml > requirements.txt;     fi &&     if [ -f requirements.txt ]; then         uv pip install -r requirements.txt;     fi

# Copy application code
COPY . .

EXPOSE 8080
CMD ["python", "main.py"]
