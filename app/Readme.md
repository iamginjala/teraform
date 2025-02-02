# Serverless Event-Driven Analytics Pipeline

A real-time analytics pipeline built using AWS serverless services. This project demonstrates the implementation of a scalable, event-driven architecture for processing and analyzing streaming data.

## Architecture Overview

![Architecture Diagram]

The pipeline consists of the following components:
- API Gateway: Provides REST API endpoints for data ingestion and analytics
- Lambda Functions: Serverless compute for data processing
- Kinesis: Handles real-time data streaming
- DynamoDB: NoSQL database for processed data storage
- CloudWatch: Monitoring and logging

## Features

- Real-time data ingestion through REST API
- Scalable stream processing with AWS Kinesis
- Serverless compute with AWS Lambda
- Automated Infrastructure as Code using AWS CDK
- Monitoring and alerting with CloudWatch
- Query API for analytics retrieval

## Prerequisites

- AWS Account
- AWS CLI configured with appropriate credentials
- Node.js (v14 or later)
- Python 3.9 or later
- AWS CDK CLI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/serverless-analytics-pipeline.git
cd serverless-analytics-pipeline
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
npm install -g aws-cdk
```

4. Deploy the infrastructure:
```bash
cdk deploy
```

## Usage

### Data Ingestion
Send data to the pipeline using the ingestion API endpoint:

```bash
curl -X POST https://your-api-endpoint/prod/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "id": "event123",
    "category": "sales",
    "value": 100.50,
    "user_id": "user456"
  }'
```

### Retrieving Analytics
Query the analytics API endpoint:

```bash
# Get all data from the last 7 days
curl https://your-api-endpoint/prod/analytics

# Filter by category and time range
curl https://your-api-endpoint/prod/analytics?category=sales&days=30
```

## Project Structure

```
├── app/
│   └── lambda_functions/
│       ├── data_ingestion.py
│       ├── data_processor.py
│       └── analytics_api.py
├── infrastructure/
│   └── app_stack.py
├── tests/
├── requirements.txt
└── README.md
```

## Testing

```bash
python -m pytest tests/
```

## Monitoring

The application uses CloudWatch for monitoring and logging. Key metrics include:
- API Gateway request counts and latencies
- Lambda function execution metrics
- Kinesis stream metrics
- DynamoDB read/write capacity

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- AWS Documentation
- AWS CDK Examples
- Serverless Framework Documentation