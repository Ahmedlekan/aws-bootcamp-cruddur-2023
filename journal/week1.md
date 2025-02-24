# Week 1 — Docker and App Containerization

## Technical Tasks
In this class, we are going to:
- [x] Create a new GitHub repo
- [x] Launch the repo within a Gitpod workspace
- [x] Configure Gitpod.yml configuration, eg. VSCode Extensions
- [x] Clone the frontend and backend repo
- [x] Explore the codebases
- [x] Ensure we can get the apps running locally
- [x] Write a Dockerfile for each app
- [x] Ensure we get the apps running via individual container
- [x] Create a docker-compose file
- [x] Ensure we can orchestrate multiple containers to run side by side
- [x] Mount directories so we can make changes while we code

## Business Scenario
Your company has received the code repositories for the demo application from the contracted web-development firm. The company wants you to investigate the codebases, and ensure you can get them running.

The fractional CTO has suggested we first begin containerizing the applications for both developer and production use, and their reasons stayed why:
- To avoid lack of documentation of application and OS configuration
- To ensure the effort of application and OS configuration is factored in before investing lots of feature development
- If we decide to hire our technical team members we can quickly replicate these environments in any preferred choice.

The fractional CTO has asked that everything be developed in Gitpod, (a Cloud Developer Environment). This will allow the CTO at a press of a button launch the developer environment in a clean state to help with any tricky or emergency implementations, and ensure developer accountability.

Gitpod was since it supports multiple Version Control Services (VCS).. The company has invested considerable effort already in Atlassian JIRA working with the web-dev firm, and repo’s highly likely might be moved to Atlassian BitBucket to take advantage of better integrations within the Atlassian’s ecosystem.

## Weekly Outcome
- Gain practical knowledge working with common docker command and running container images for the purpose of local development
- Gain practical knowledge of working within a Cloud Development environment
- Be able to navigate a backend and front web-application and generally understand how they work

## Containerized Backend
# Use the official Python 3.10 slim image
FROM python:3.10-slim-bookworm

# Set the working directory inside the container
WORKDIR /backend-flask

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_ENV=development
ENV FLASK_APP=app.py  # Replace with your Flask app entry point if different

# Expose the port the app will run on
EXPOSE 4567

# Command to run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]






















## Homework Challenges

