# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables with default values
ENV HOST=${HOST:-localhost}
ENV PORT=${PORT:-8001}
ENV POSTGRES_USER=${POSTGRES_USER:-admin}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-password}
ENV POSTGRES_DB=${POSTGRES_DB:-devOps}
ENV POSTGRES_SERVER=${POSTGRES_SERVER:-localhost}
ENV POSTGRES_PORT=${POSTGRES_PORT:-5432}
ENV REDIS_HOST=${REDIS_HOST:-localhost}
ENV REDIS_PORT=${REDIS_PORT:-6379}
ENV SECRET_KEY=${SECRET_KEY:-Hard_Too_Guest_2024}
ENV JWT_ALGORITHM=${JWT_ALGORITHM:-HS256}
ENV ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES:-30}
ENV PRODUCTION=${PRODUCTION:-False}

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
