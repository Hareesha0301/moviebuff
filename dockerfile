# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application source code into the container
COPY . /app

# Set any environment variables if required
# ENV MY_ENV_VARIABLE value

# Expose any required ports (if your Python application listens on a specific port)
# EXPOSE 8080

# Define the command to run your Python application (replace "app.py" with your main Python script)
CMD ["python", "manage.py"]
