# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the script into the container
COPY receiver.py .
COPY utilities ./utilities
COPY __init__.py .

# Install any dependencies required by the script
RUN pip install pika requests

# Run the script when the container starts
CMD ["python", "receiver.py"]