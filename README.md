# agents

Building a simple agent like a psycho from scratch in python.
No libs or sdks for the api's or agent.

Gunna hook it to an api w FastAPI, enable interrupts and such not. 

## Setup

```bash
# Install dependencies
uv sync

# Start the server (this won't work yet)
make start
```

## Development

```bash
# Run tests
make test

# Checks
make check

# Database migrations
make migrate
```

## API

- Health check: `GET /health`
- API documentation: `GET /docs` (when server is running)

