# Use a single stage for development, starting from a slim Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install uv, our fast package manager
RUN pip install --no-cache-dir uv

# Copy the source code
COPY . .

# Install dependencies using uv directly into the system Python
RUN uv pip install -e . --system

# Set the default command for the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]