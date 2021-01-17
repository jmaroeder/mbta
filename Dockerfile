FROM python:3.8-slim

WORKDIR /usr/src/app

ENV \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.1.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONPATH="/usr/src/app" \
    PYTHONUNBUFFERED=1

RUN \
    apt-get update && apt-get install -y \
        tini \
    && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION"

COPY ./poetry.lock ./pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./mbta ./mbta
RUN poetry install --no-interaction

ENTRYPOINT ["/usr/bin/tini", "--", "mbta"]
CMD []
