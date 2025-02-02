import json
import boto3
import os
from decimal import Decimal


def handler(event, context):
    """Lambda function to process records from Kinesis and store in DynamoDB"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])

    try:
        for record in event['Records']:
            # Decode and parse the data
            payload = json.loads(record['kinesis']['data'])

            # Process the data (example: calculate metrics)
            processed_data = {
                'id': payload.get('id'),
                'timestamp': payload.get('timestamp'),
                'metric_value': Decimal(str(payload.get('value', 0))),
                'category': payload.get('category'),
                # Add any additional processed fields
            }

            # Store in DynamoDB
            table.put_item(Item=processed_data)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully processed {len(event["Records"])} records'
            })
        }
    except Exception as e:
        print(f'Error processing records: {str(e)}')
        raise e