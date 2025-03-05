# -----------------------------------------------------------------------------
# Use an official lightweight Python image as the base image.
# This image includes Python 3.9 on a slim Debian base, which minimizes size.
# -----------------------------------------------------------------------------
FROM python:3.9-slim

# -----------------------------------------------------------------------------
# Set environment variables to optimize Python behavior:
# PYTHONDONTWRITEBYTECODE prevents Python from writing .pyc files to disk.
# PYTHONUNBUFFERED ensures that the output from the Python application
# is sent straight to the terminal (useful for logging).
# -----------------------------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------------------------------------------------------
# Set the working directory within the container to /app.
# All subsequent commands (COPY, RUN, etc.) will be executed in this directory.
# -----------------------------------------------------------------------------
WORKDIR /app

# -----------------------------------------------------------------------------
# Copy the requirements.txt file from your local machine into the container.
# This file contains the list of dependencies needed for your Flask application.
# -----------------------------------------------------------------------------
COPY requirements.txt /app/requirements.txt

# -----------------------------------------------------------------------------
# Upgrade pip and install the Python dependencies specified in requirements.txt.
# This command will ensure that all necessary packages are installed.
# -----------------------------------------------------------------------------
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# -----------------------------------------------------------------------------
# Copy the entire project directory into the container's /app directory.
# This includes the Flask application (app.py), static files, templates, and README.
# -----------------------------------------------------------------------------
COPY . /app

# -----------------------------------------------------------------------------
# Expose port 5000 so that the container can accept requests on that port.
# This is the port that the Flask application will run on.
# -----------------------------------------------------------------------------
EXPOSE 5000

# -----------------------------------------------------------------------------
# Define the default command to run the Flask application.
# The CMD instruction specifies the command to run when the container starts.
# -----------------------------------------------------------------------------
CMD ["python", "app.py"]
