# agents

A Python project built with FastAPI and UV dependency management.

## Setup

```bash
# Install dependencies
uv sync

# Start the server
make start
```

## Development

```bash
# Run tests
make test

# Check code quality
make check

# Database migrations
make migrate
```

## API

- Health check: `GET /health`
- API documentation: `GET /docs` (when server is running)

