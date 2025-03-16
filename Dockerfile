FROM python:3.13.2-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app

RUN uv sync --frozen

CMD ["uv", "run", "start"]
