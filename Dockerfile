FROM python:3.14

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
COPY ./src src
RUN uv sync

CMD uv run uvicorn --host 0.0.0.0 --port 8000 src.${SERVICE}:app --reload

