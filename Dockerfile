# Start from a base image that includes Python and pip
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies including pkg-config, libsystemd-dev, and dbus-1 development packages
RUN apt-get update \
    && apt-get install -y pkg-config libsystemd-dev libdbus-1-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on
EXPOSE 80

# Command to run your application
CMD [ "python", "app.py" ]
