# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Expose port 8080 for Flask
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "api/check_date.py"]
