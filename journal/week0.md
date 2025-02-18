# Week 0 — Billing and Architectur 

### Technical Tasks Completed:

1. Discussed the bootcamp format and expectations.

2. Reviewed the business use-case for the project.

3. Analyzed an architectural diagram of the planned solution.

4. Learned how to use Lucid Charts to create architectural diagrams.

5. Explored C4 Models for visualizing software architecture.

6. Familiarized myself with the cloud services we will use during the bootcamp.


#### The C4 Model

The C4 Model is a framework for visualizing and documenting software architecture in a clear and structured way. It was created by Simon Brown and is widely used to communicate the architecture of a system to both technical and non-technical stakeholders. The model is based on the idea of abstraction and hierarchical decomposition, breaking down a system into four levels of detail:

+ Context
+ Containers
+ Components
+ Code

Each level provides a different perspective of the system, starting from a high-level overview and drilling down into more granular details. Here's an explanation of each level:

1. Context (Level 1)

This is the highest level of abstraction and provides a big-picture view of the system. It answers the question:
"What is the system, and how does it interact with users and other systems?"

+ Focus: The system as a whole and its relationships with external entities (e.g., users, other systems, or third-party services).
+ Key Elements:
- The system itself (the software you're building).
- Actors (users or external systems interacting with the system).
- Interactions between the system and external entities.

2. Containers (Level 2)

This level zooms into the system and breaks it down into containers. A container is a deployable unit that hosts code or data, such as a web application, mobile app, database, or file system. It answers the question:
"What are the high-level building blocks of the system, and how do they interact?"

+ Focus: The major structural elements of the system and how they communicate.
+ Key Elements:
- Containers (e.g., web servers, mobile apps, databases, microservices).
- Interactions between containers (e.g., APIs, messaging systems).

3. Components (Level 3)

This level dives deeper into each container and identifies its components. A component is a modular part of a container with a well-defined interface, such as a controller, service, or repository. It answers the question:
"What are the key components inside each container, and how do they work together?"

+ Focus: The internal structure of a container and the responsibilities of its components.
+ Key Elements:
- Components (e.g., user interface, business logic, data access layers).
- Interactions between components (e.g., method calls, events).

4. Code (Level 4)

This is the most detailed level and focuses on the implementation details of individual components. It answers the question:
"How is each component implemented in code?"

+ Focus: The actual code structure, classes, methods, and relationships.
+ Key Elements:
- Classes and their relationships (e.g., inheritance, composition).
- Methods and their interactions.

#### Why Use the C4 Model?

+ Clarity: It provides a clear and structured way to visualize software architecture at different levels of detail.
+ Communication: It helps bridge the gap between technical and non-technical stakeholders by starting with a high-level overview and gradually diving into details.
+ Scalability: It works well for both small and large systems, as it allows you to focus on the level of detail that matters most.
+ Tool Agnostic: The C4 Model can be created using any diagramming tool (e.g., Lucid Charts, Draw.io, or even pen and paper).


#### AWS Service used

1. Compute

+ Amazon ECS (Elastic Container Service): Runs the Flask backend application using Fargate (serverless compute for containers).
+ AWS Lambda: Serverless functions for:
- DynamoDB Stream Trigger
- Cognito Post-Configuration
- Presigned URL Generation
- Image Processing
- CORS Preflight Handling
- API Gateway Authorization

2. Storage

+ Amazon S3 (Simple Storage Service):
- Hosts the React frontend (static website).
- Stores raw assets (e.g., uploaded profile photos).
- Stores processed assets (e.g., thumbnails).
+ Amazon RDS (Relational Database Service): Hosts the PostgreSQL database for the backend application.
+ Amazon DynamoDB: NoSQL database for specific use cases, with a DynamoDB stream to trigger Lambda functions.

3. Networking

+ Amazon VPC (Virtual Private Cloud): Custom VPC with three public subnets for hosting resources.
+ Amazon Route 53: DNS service for managing the custom domain (example.com, www.example.com, api.example.com, assets.example.com).
+ Amazon CloudFront: Content Delivery Network (CDN) for:
- Serving the React frontend.
- Serving processed assets (e.g., profile photos).
+ Application Load Balancer (ALB): Distributes traffic to the ECS Fargate backend.

4. Security

+ Amazon Cognito: Manages user authentication (sign-up, login, sessions).
+ AWS Identity and Access Management (IAM): Manages permissions for AWS resources (e.g., Lambda functions, ECS tasks, S3 buckets).
+ AWS Certificate Manager (ACM): Provides HTTPS certificates for:
- CloudFront distributions.
- Application Load Balancer (ALB).
- API Gateway.

5. Developer Tools

+ AWS CodePipeline: CI/CD pipeline for automating the build and deployment process.
+ AWS CodeBuild: Builds the Docker image for the Flask backend and pushes it to ECR.
+ Amazon ECR (Elastic Container Registry): Stores the Docker image for the Flask backend.

6. Application Integration

+ Amazon API Gateway: HTTP API for:
- Exposing backend endpoints.
- Generating presigned URLs for file uploads.
- Handling CORS preflight requests.
+ Amazon S3 Event Notifications: Triggers Lambda functions when files are uploaded to the raw assets bucket.

7. Monitoring and Logging

+ Amazon CloudWatch (implied): Used for monitoring and logging:
- Lambda function execution.
- ECS tasks.
- API Gateway requests.
- ALB health checks.

8. Analytics

+ Amazon DynamoDB Streams: Captures changes to the DynamoDB table and triggers a Lambda function.

#### How These Services Work Together

+ Frontend:
- Hosted on S3, delivered via CloudFront, and managed by Route 53.

+ Backend:
- Runs on ECS Fargate, exposed via ALB and API Gateway, and interacts with RDS Postgres and DynamoDB.

+ Authentication:
- Managed by Cognito, with a Lambda function to insert users into RDS Postgres.

+ File Uploads:
- Handled by API Gateway, Lambda, and S3, with image processing triggered by S3 Event Notifications.

+ CI/CD:
- Automated using CodePipeline, CodeBuild, and ECR.

+ Security:
- HTTPS enabled via ACM, and permissions managed by IAM.

















