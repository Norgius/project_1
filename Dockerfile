FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG BASE_DIR=/opt/app
WORKDIR ${BASE_DIR}

ENV \
    # python
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # uv
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen

COPY ./src ./src
COPY ./libs ./libs

ENV \
    PATH="${BASE_DIR}/.venv/bin:$PATH" \
    PYTHONPATH="${BASE_DIR}/src/:${BASE_DIR}/libs/"

WORKDIR ${BASE_DIR}/src

EXPOSE 80/tcp

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []
CMD ["fastapi", "run", "main.py", "--port", "80"]
