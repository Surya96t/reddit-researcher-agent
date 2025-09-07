# Use a single stage for development
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY pyproject.toml requirements.txt ./

# Create virtual environment and install dependencies
RUN uv venv .venv && \
    .venv/bin/pip install -r requirements.txt

# Set PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY . .

# Install the app in development mode
RUN .venv/bin/pip install -e .

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]