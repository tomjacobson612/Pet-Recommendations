# Use an official Python image as a base
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8080

# Run app
CMD ["python", "app.py"]

