# Pronotez Backend

## Description
Production-ready dockerized async REST API on FastAPI with SQLAlchemy and PostgreSQL

## Pre-requirements
1. [Taskfile](https://taskfile.dev/): Improved version of Makefile
2. [Docker](https://www.docker.com/): Containers
3. [Pyenv](https://github.com/pyenv/pyenv-installer) or [Python 3.8+](https://www.python.org/)

### Available tasks with Taskfile
```bash
task -l  # list of tasks with descriptions
task -a  # list of all tasks
```

## Setup - Docker
1. Build docker containers (API and DB)
   * `task docker-build` or `docker compose build`
2. Run docker containers
   * `task docker-up` or `docker compose up -d`
3. Stop docker containers
   * `task docker-stop` or `docker compose stop`
4. Stop and delete containers
   * `task docker-down` or `docker compose down`

## Setup - Development

### 1. Prepare virtual environment
#### Using Pyenv (MacOS)
```bash
task pyenv-create
pyenv activate <venv-name>
```
#### Or Using venv (Windows)
```bash
task venv-create
task venv-activate
```

### 2. Run API
```bash
task run # Run API locally
task upgrade # Apply migrations to DB
```

### Features
- `pytest` with automatic rollback after each test case
- db session stored in Python's `context variable`
- configs for `mypy`, `pylint`, `isort` and `black`
- `Alembic` for DB migrations
- `Poetry` python package manager
- CI with Github
