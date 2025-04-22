# Week 2 — Distributed Tracing

AWS X-RAY Traces

Instrument X-Ray for Flask

Install the SDK using the following command

```bash
pip install aws-xray-sdk
```

Instrument Your Application

```bash
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)

# Configure X-Ray
xray_recorder.configure(service='MyBackendService')
XRayMiddleware(app, xray_recorder)
```


Create a json file

aws xray create-sampling-rule --cli-input-json file://json/xray.json

```bash
{
  "SamplingRule": {
    "RuleName": "MySamplingRule",
    "ResourceARN": "*",
    "Priority": 1,
    "FixedRate": 0.1,  # 10% of requests
    "ReservoirSize": 100,
    "ServiceName": "*",
    "ServiceType": "*",
    "Host": "*",
    "HTTPMethod": "*",
    "URLPath": "*",
    "Version": 1
  }
}
```


To create a group to group traces together

```bash
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"backend-flask\")"
```


Run the X-Ray Daemon on Docker compose 

```bash
xray-daemon:
    image: amazon/aws-xray-daemon
    command: ["-o", "-b", "0.0.0.0:2000"]
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_REGION=us-east-1
      - AWS_EC2_METADATA_DISABLED=true
    ports:
      - "2000:2000/udp"
    healthcheck:
      test: ["CMD", "netstat -an | grep :2000"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
```


Modify your backend-flask. compose.yml backend env


```bash
backend-flask:
    environment:
      - FRONTEND_URL=https://3000-ahmedlekan-awsbootcampc-kl3gd35korz.ws-us118.gitpod.io
      - BACKEND_URL=https://4567-ahmedlekan-awsbootcampc-kl3gd35korz.ws-us118.gitpod.io
      - AWS_XRAY_URL="*4567-ahmedlekan-awsbootcampc-kl3gd35korz.ws-us118.gitpod.io"
      - AWS_XRAY_DAEMON_ADDRESS=xray-daemon:2000
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_REGION=us-east-1
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
    command: python3 -m flask run --host=0.0.0.0 --port=4567
    depends_on:
      - postgres
      - dynamodb
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4567/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```











