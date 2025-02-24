# Stage 1: Build stage
FROM python:3.10-slim-bookworm AS build

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

# Stage 2: Final stage
FROM python:3.10-slim-bookworm

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=4567

# Set the working directory inside the container
WORKDIR /backend-flask

# Copy only the necessary files from the build stage
COPY --from=build /backend-flask/requirements.txt .
COPY --from=build /backend-flask/app.py .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE ${PORT}

# Command to run the Flask application
CMD ["./start.sh"]

