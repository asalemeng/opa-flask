# Use the official Python base image
FROM python:3.12.2-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the Flask app code into the container
COPY . /app

# Install Flask app dependencies
RUN pip install -r requirements.txt

# Expose the port number on which the Flask app will run
EXPOSE 8000

# Command to run the Flask app
CMD ["python", "app.py"]
