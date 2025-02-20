# Use the official Python 3.10 slim image
FROM python:3.10-slim-bookworm

# Set environment variables
ENV FLASK_ENV=development
ENV PORT=4567

# Set the working directory inside the container
WORKDIR /backend-flask

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE ${PORT}

# Command to run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]