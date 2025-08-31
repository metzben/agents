# AI Agents Python Project

This repository is devoted to building an AI agent in pure Python using Anthropic APIs directly. It's a template project for building AI-powered services and agents with FastAPI as the web framework.

## Project Overview

- **Purpose**: A template project for building AI-powered services and agents
- **Core Technologies**: Python, FastAPI, SQLite
- **Key Features**:
  - RESTful API for agent interaction
  - Integration with Google Cloud Secret Manager for secure key handling
  - Custom client for interacting with the Anthropic (Claude) API
  - Database migration support using `yoyo-migrations`
  - Containerization with Docker
  - Structured development environment with linting, formatting, and testing commands

## Technology Stack

- **Language**: Python (>=3.13)
- **Web Framework**: FastAPI
- **Dependency Management**: `uv`
- **Database**: SQLite
- **Database Migrations**: `yoyo-migrations`
- **Testing**: `pytest`, `pytest-xdist`
- **Linting & Formatting**: `ruff`, `black`
- **Containerization**: Docker
- **Configuration**: `python-dotenv`
- **API Interaction**: 
  - `requests`: General purpose HTTP client
  - `AnthropicClient`: Custom client for the Anthropic API
- **AI/LLM Libraries**: `dspy`, `openai`, `tiktoken`, `litellm`

## Directory Structure

For the complete project directory structure, see [dir_structure.md](dir_structure.md).

### Key Directories

- **`baseservice/`**: Contains sample service with API routes, business logic, and models
- **`clients/`**: Houses clients for external APIs (Anthropic API client)
- **`repository/`**: Handles database interactions with SQLite optimizations
- **`migrations/`**: Database migration scripts managed by `yoyo-migrations`

## Architecture & Key Files

- **`main.py`**: Main entry point for the FastAPI application
- **`config.py`**: Manages application configuration from `.env` files and Secret Manager
- **`secret_manager.py`**: Client for securely fetching secrets from Google Cloud Secret Manager
- **`pyproject.toml`**: Project dependencies and metadata for `uv`
- **`Makefile`**: Shortcut commands for common development tasks
- **`Dockerfile`**: Container environment definition

## Development Workflow

### Setup

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Configuration**:
   - Copy `.env` to `.env.local`
   - Update `GCP_PROJECT_ID` and other variables in `.env.local` as needed

### Running the Application

- Start the web server:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8081 --reload
  ```
  
- Or run the main script (uses port from `.env` file):
  ```bash
  uv run python main.py
  ```

## Development Commands

**IMPORTANT:** Always use `uv run` when running Python scripts or tests.

### Common Commands (from Makefile)

- **Run all tests (parallel)**:
  ```bash
  make test
  ```

- **Run fast tests**:
  ```bash
  make test-fast
  ```

- **Run specific test**:
  ```bash
  uv run pytest test_collect.py::test_function_name -v -s
  ```

- **Lint the code**:
  ```bash
  make lint
  ```

- **Format the code**:
  ```bash
  make format
  ```

- **Run all checks (lint, format, etc.)**:
  ```bash
  make check
  ```

### Database Operations

- **Apply database migrations**:
  ```bash
  make migrate
  # Or directly: uv run yoyo apply --config yoyo.ini --batch
  ```

## API Endpoints

The FastAPI application provides:

- **`/`**: Root endpoint
- **`/health`**: Health check endpoint  
- **`/user/{username}`**: User-specific endpoints

## Testing

The project uses `pytest` with parallel execution support via `pytest-xdist`. All tests should be run with `uv run` prefix for proper dependency management.

## External Integrations

- **Anthropic API**: Custom client in `clients/anthropic_client.py` for Claude API interactions
- **Google Cloud Secret Manager**: Secure secret storage and retrieval
- **Database**: SQLite with optimized connection handling and migration support
