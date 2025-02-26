FROM python:3.10-slim-bookworm

# Set the working directory
WORKDIR /backend-flask

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 4567

# Command to run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]