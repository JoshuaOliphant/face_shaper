# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
ADD . /app

# Create necessary directories
RUN mkdir -p app/static/css \
    && mkdir -p app/static/js \
    && mkdir -p app/templates/partials

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Run as non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Reset the entrypoint
ENTRYPOINT []

# Expose port
EXPOSE 8000

# Create a script to check for environment variables and start the application
RUN echo '#!/bin/sh\n\
    if [ -z "$ANTHROPIC_API_KEY" ]; then\n\
    echo "Error: ANTHROPIC_API_KEY environment variable is required"\n\
    exit 1\n\
    fi\n\
    \n\
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000\n'\
    > /app/start.sh && chmod +x /app/start.sh

# Use the start script as the command
CMD ["/app/start.sh"]
