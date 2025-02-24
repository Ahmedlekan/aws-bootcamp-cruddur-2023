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

FROM python:3.10-slim-bookworm

WORKDIR /backend-flask

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]


## Build the Docker Image

docker build -t backend-flask .

## Run the Docker Container
- To run the container with default settings:

docker run --rm -p 4567:4567 backend-flask

- To run the container with environment variables:

docker run --rm -p 4567:4567 -e FRONTEND_URL="*" -e BACKEND_URL="*" backend-flask

## Endpoint Testing

To test the endpoint, use curl or open a browser:

1. Using curl

curl {https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}/api/activities/home}

2. Using a Browser

Open your browser and navigate to:

https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}/api/activities/home

Create a .gitignore file to exclude unnecessary files from the Docker build context:


## Containerized Frontend-react-js

FROM node:16-alpine

WORKDIR /frontend-react-js

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE ${PORT} 

CMD ["npm", "start"]

## Create docker compose yml file

A docker-compose.yml file allows you to define and run multi-container Docker applications.

 

### How to Use the Docker Compose File
1. Start the Services
Run the following command to start all services defined in the docker-compose.yml file:
docker-compose up

2. Stop the Services
To stop the services, run:
docker-compose down

3. Rebuild the Services
If you make changes to the Dockerfiles or the docker-compose.yml file, rebuild the services:
docker-compose up --build

4. View Logs
To view logs for a specific service, use:
docker-compose logs <service-name>

## Run a local development environment with PostgreSQL, DynamoDB alongside your Flask backend and React frontend
Update the compose file

version: "3.8"
services:
  backend-flask:
    environment:
      - FRONTEND_URL={"https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST"}
      - BACKEND_URL={"https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST"}
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
    command: python3 -m flask run --host=0.0.0.0 --port=4567
    depends_on:
      - postgres
      - dynamodb

  frontend:
    environment:
      - REACT_APP_BACKEND_URL={"https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST"}
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js
    command: sh -c "npm install && npm start"

  postgres:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal-network

  dynamodb:
    user: root 
    image: amazon/dynamodb-local:latest
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - ./docker/dynamodb:/home/dynamodblocal/data
    working_dir: /home/dynamodblocal
    command: -jar DynamoDBLocal.jar -sharedDb -dbPath ./data
    networks:
      - internal-network

volumes:
  postgres_data:
  dynamodb_data:

networks:
  internal-network:
    driver: bridge
    name: cruddur

### Start the Services
Run the following command to start all services defined in the docker-compose.yml file:
docker-compose up

## Create a DynamoDb table locally in your environment
aws dynamodb create-table \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Artist,AttributeType=S \
        AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --table-class STANDARD

### create an Item
aws dynamodb put-item \
    --endpoint-url http://localhost:8000 \
    --table-name Music  \
    --item \
        '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}, "Awards": {"N": "1"}}'

aws dynamodb put-item \
    --table-name Music  \
    --item \
        '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Howdy"}, "AlbumTitle": {"S": "Somewhat Famous"}, "Awards": {"N": "2"}}'
    --returned-consumed-capacity TOTAL

### Verify the Table and Items
aws dynamodb list-tables --endpoint-url http://localhost:8000

### Scan Table
aws dynamodb scan --endpoint-url http://localhost:8000 --table-name Music


# install PostgreSQL locally on your environment
curl -fssl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d pgdg.list

sudo apt update

sudo apt install -y postgresql-client-13 libpq-dev

To run
- psql -host localhost 


## Container Security Best Practices
What is container security?
Container security is the practice of protecting your applications hosted on compute services like containers. Common examples of application can be Single Page Application (SPA) or Microservices, API.

### Security Best Practices on AWS
1. Use AWS Secrets Manager
    What it does: Securely store and manage secrets like database credentials, API keys, and passwords.
    Best Practices:
   - Rotate secrets automatically using Secrets Manager.
   - Grant least privilege access to secrets using AWS Identity and Access Management (IAM).

2. Enable AWS Inspector
    What it does: Automatically assesses container images for vulnerabilities and compliance issues.
    Best Practices:
   - Integrate AWS Inspector with Amazon ECR (Elastic Container Registry) to scan images during the CI/CD pipeline.
   - Set up automated alerts for critical vulnerabilities.

3. Use Amazon ECR for Image Management
    What it does: Store, manage, and deploy Docker container images securely.
    Best Practices:
   - Enable image scanning in ECR to detect vulnerabilities.
   - Use lifecycle policies to clean up unused images.

4. Implement Network Security
    What it does: Control traffic to and from your containers.
    Best Practices:
   - Use AWS Security Groups and Network ACLs to restrict access.
   - Encrypt traffic using TLS/SSL.

5. Enable IAM Roles for Tasks (ECS/EKS)
    What it does: Assign IAM roles to ECS tasks or Kubernetes pods to grant permissions.
    Best Practices:
   - Use task roles instead of embedding credentials in containers.
   - Follow the principle of least privilege.

6. Use AWS Fargate for Serverless Containers
    What it does: Run containers without managing the underlying infrastructure.
    Best Practices:
   - Fargate automatically isolates tasks, reducing the risk of cross-container attacks.
   - Use Fargate to simplify compliance and security management.

7. Monitor with AWS CloudWatch and X-Ray
    What it does: Monitor container performance and trace requests across microservices.
    Best Practices:
   - Set up alarms for unusual activity (e.g., high CPU usage, failed requests).
   - Use X-Ray to identify performance bottlenecks and security issues.

8. Enable Encryption
    What it does: Protect data at rest and in transit.
    Best Practices:
   - Use AWS KMS to manage encryption keys.
   - Enable encryption for ECR repositories and EBS volumes.

9. Implement Least Privilege Access
    What it does: Restrict access to resources based on the principle of least privilege.
    Best Practices:
   - Use IAM policies to grant minimal permissions required for tasks.
   - Regularly review and update permissions.

10. Regularly Update and Patch
    What it does: Keep your containers and host systems up to date.
    Best Practices:
    - Use automated tools to apply patches and updates.
    - Monitor for new vulnerabilities using AWS Security Hub.



## Homework Challenges


