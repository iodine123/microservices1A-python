# Use an official Python runtime as a parent image
FROM python:3-alpine3.15

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Give permission to /app
RUN chmod -R 755 /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=app.py

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
