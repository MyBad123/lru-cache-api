FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get remove --purge -y curl \
    && apt-get autoremove -y

ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root
COPY app /app/app
COPY api /app/api
EXPOSE 8000