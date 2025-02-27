# Stage 1: Build stage
FROM python:3.10-slim-bookworm AS build

# Set environment variables
ENV FLASK_ENV=development
ENV PORT=4567
# Fix for module import
ENV PYTHONPATH=/backend-flask 

# Set the working directory inside the container
WORKDIR /backend-flask

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Stage 2: Final stage
FROM python:3.10-slim-bookworm

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=4567
# Fix for module import
ENV PYTHONPATH=/backend-flask

# Set the working directory inside the container
WORKDIR /backend-flask

# Copy everything (fix missing files issue)
COPY --from=build /backend-flask .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 4567

# Command to run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]

