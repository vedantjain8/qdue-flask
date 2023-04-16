# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt and gunicorn
RUN apt-get update
RUN apt-get install -y sqlite3
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Environment variable
ENV GUNICORN_WORKERS=4
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Expose the port for the app to run on
EXPOSE 80

# Start the app with gunicorn
ENTRYPOINT ["sh", "run.sh"]