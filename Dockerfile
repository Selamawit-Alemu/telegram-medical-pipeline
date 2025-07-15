# S:\AI MAstery\week-7\telegram-medical-pipeline\Dockerfile
# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Default command (e.g., just keep the container running if no specific command is provided)
# CMD ["python", "-c", "import time; time.sleep(infinity)"] # Or a more realistic default
# For a Dagster code server, this CMD is often overridden by docker-compose,
# so 'bash' can still be useful if you plan to manually shell into the container.
# However, if it's meant to be a running service, it needs a continuous process.
# For this specific setup where `command` is explicitly set in docker-compose, `CMD ["bash"]` is OK.
# But just be aware that if you tried to run `docker run your_image`, it would just give you a bash shell.
