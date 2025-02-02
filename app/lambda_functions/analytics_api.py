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


# app/lambda_functions/analytics_api.py
import json
import boto3
import os
from datetime import datetime, timedelta


def handler(event, context):
    """Lambda function to retrieve analytics data"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])

    try:
        # Get query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        category = query_params.get('category')
        days = int(query_params.get('days', '7'))

        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Query DynamoDB
        if category:
            response = table.query(
                IndexName='category-timestamp-index',
                KeyConditionExpression='category = :category AND #ts BETWEEN :start AND :end',
                ExpressionAttributeNames={'#ts': 'timestamp'},
                ExpressionAttributeValues={
                    ':category': category,
                    ':start': start_date.isoformat(),
                    ':end': end_date.isoformat()
                }
            )
        else:
            response = table.scan(
                FilterExpression='#ts BETWEEN :start AND :end',
                ExpressionAttributeNames={'#ts': 'timestamp'},
                ExpressionAttributeValues={
                    ':start': start_date.isoformat(),
                    ':end': end_date.isoformat()
                }
            )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'data': response['Items'],
                'count': response['Count']
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


