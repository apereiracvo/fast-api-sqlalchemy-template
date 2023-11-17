# FastAPI Backend

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
task pyenv-create # Create virtualenv with pyenv
pyenv activate sample_api # Activate virtualenv
task pyenv-setup # Install dependencies in virtualenv
```
#### Or Using venv (Windows)
```bash
task venv-create
task venv-activate
```
### 2. Run DB and API
#### a) Spin up and build DB
```bash
task docker-db-up
task upgrade
```
#### b) Run API with Python
Note: virtualenv must be active
```bash
cd app/
python main.py
```