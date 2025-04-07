Architecture and AWS Service used. 

## Architecture

## AWS Service used

1. Compute

- Amazon ECS (Elastic Container Service): Runs the Flask backend application using Fargate (serverless compute for containers).

- AWS Lambda: Serverless functions for:
   - DynamoDB Stream Trigger 
   - Cognito Post-Configuration
   - Presigned URL Generation
   - Image Processing
   - CORS Preflight Handling
   - API Gateway Authorization

2. Storage

- Amazon S3 (Simple Storage Service):
    - Hosts the React frontend (static website).
    - Stores raw assets (e.g., uploaded profile photos).
    - Stores processed assets (e.g., thumbnails).
    - Amazon RDS (Relational Database Service): Hosts the PostgreSQL database for the backend application.
    - Amazon DynamoDB: NoSQL database for specific use cases, with a DynamoDB stream to trigger Lambda functions.

3. Networking

- Amazon VPC (Virtual Private Cloud): Custom VPC with three public subnets for hosting resources.

- Amazon Route 53: DNS service for managing the custom domain (example.com, www.example.com, api.example.com, assets.example.com).

- Amazon CloudFront: Content Delivery Network (CDN) for:
    - Serving the React frontend.
    - Serving processed assets (e.g., profile photos).
    - Application Load Balancer (ALB): Distributes traffic to the ECS Fargate backend.

4. Security

- Amazon Cognito: Manages user authentication (sign-up, login, sessions).
- AWS Identity and Access Management (IAM): Manages permissions for AWS resources (e.g., Lambda functions, ECS tasks, S3 buckets).
- AWS Certificate Manager (ACM): Provides HTTPS certificates for:
   - CloudFront distributions.
   - Application Load Balancer (ALB).
   - API Gateway.

5. Developer Tools

- AWS CodePipeline: CI/CD pipeline for automating the build and deployment process.
- AWS CodeBuild: Builds the Docker image for the Flask backend and pushes it to ECR.
- Amazon ECR (Elastic Container Registry): Stores the Docker image for the Flask backend.

6. Application Integration

- Amazon API Gateway: HTTP API for:
    - Exposing backend endpoints.
    - Generating presigned URLs for file uploads.
    - Handling CORS preflight requests.
    - Amazon S3 Event Notifications: Triggers Lambda functions when files are uploaded to the raw assets bucket.

7. Monitoring and Logging

- Amazon CloudWatch (implied): Used for monitoring and logging:
    - Lambda function execution.
    - ECS tasks.
    - API Gateway requests.
    - ALB health checks.

8. Analytics

- Amazon DynamoDB Streams: Captures changes to the DynamoDB table and triggers a Lambda function.

#### How These Services Work Together

Frontend:

- Hosted on S3, delivered via CloudFront, and managed by Route 53.

Backend:

- Runs on ECS Fargate, exposed via ALB and API Gateway, and interacts with RDS Postgres and DynamoDB.

Authentication:

- Managed by Cognito, with a Lambda function to insert users into RDS Postgres.

File Uploads:

- Handled by API Gateway, Lambda, and S3, with image processing triggered by S3 Event Notifications.

CI/CD:

- Automated using CodePipeline, CodeBuild, and ECR.

Security:

- HTTPS enabled via ACM, and permissions managed by IAM.
