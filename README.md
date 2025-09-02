# agents

Building a simple agent like a psycho from scratch in python.
Gunna hook it to an api w FastAPI, enable interrupts and such not. 

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

