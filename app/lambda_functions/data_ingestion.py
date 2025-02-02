import json
import boto3
import os
from datetime import datetime


def handler(event, context):
    """Lambda function to ingest data into Kinesis stream"""
    kinesis = boto3.client('kinesis')

    try:
        # Extract data from the API Gateway event
        body = json.loads(event['body'])

        # Add timestamp
        body['timestamp'] = datetime.utcnow().isoformat()

        # Put record into Kinesis stream
        response = kinesis.put_record(
            StreamName=os.environ['KINESIS_STREAM_NAME'],
            Data=json.dumps(body),
            PartitionKey=str(body.get('user_id', 'default'))
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data ingested successfully',
                'sequenceNumber': response['SequenceNumber']
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }