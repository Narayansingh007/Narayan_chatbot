# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK data
RUN python -m nltk.downloader punkt

# Copy the application code
COPY . .

# Load environment variables from .env file
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Expose the port the application will run on
EXPOSE 8080

# Run the command to start the application when the container launches
CMD ["gunicorn", "app:app", "--workers", "3", "--bind", "0.0.0.0:8080"]