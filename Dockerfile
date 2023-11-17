FROM python:3.8.16-slim

ARG ENVIRONMENT="prod"

RUN apt update \
    && apt upgrade -y \
    && apt install -y curl \
        locales \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip poetry

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

COPY pyproject.toml .
COPY poetry.lock .

RUN [ "$ENVIRONMENT" = "prod" ] && poetry install --no-dev || poetry install

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/code/docker-entrypoint.sh" ]

CMD ["api", "8000"]
