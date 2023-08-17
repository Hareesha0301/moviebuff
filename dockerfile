# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the requirements file into the container
COPY requirements.txt /app/
RUN pip install --upgrade pip 
# Install dependencies
RUN pip install Django
RUN pip install -r requirements.txt


# Make port 8000 available to the world outside this container
EXPOSE 8000


COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Define the command to run your application
CMD ["/app/docker-entrypoint.sh"]
