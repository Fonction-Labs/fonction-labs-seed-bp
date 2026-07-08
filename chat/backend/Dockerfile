FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Install dependencies (no dev extras)
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY app/ ./app/

# Copy generated data (produced by the pipeline before docker build)
COPY data/processed/ ./data/processed/

# Copy assumptions (vc_case.yaml)
COPY data/assumptions/ ./data/assumptions/

# Copy project context files (for read_context tool)
COPY context/ ./context/

ENV DATA_PATH=/app/data/processed
ENV ASSUMPTIONS_PATH=/app/data/assumptions/vc_case.yaml
ENV PROJECT_ROOT=/app/context
ENV DOCS_PATH=/app/context/docs
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
