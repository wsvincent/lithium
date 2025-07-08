# ---- Stage 1: Builder ----
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install system build tools needed for compiling CFFI and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
WORKDIR /app

# Install dependencies without dev packages
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy all source files
ADD . /app

# Sync again to install any local project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---- Stage 2: Runtime ----
FROM python:3.12-slim-bookworm

# Create app user (optional security)
RUN useradd -m app

# Copy from builder
COPY --from=builder --chown=app:app /app /app

# Set working dir
WORKDIR /app

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Set permissions
USER app

# Expose port
EXPOSE 8000

# Start server with Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "django_project.wsgi"]
