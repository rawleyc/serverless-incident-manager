import json
import boto3

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ServerlessTickets')

def lambda_handler(event, context):
    try:
        # Scan the table to get all items (Efficient for small labs, use Query for prod)
        response = table.scan()
        items = response['Items']
        
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving tickets: {str(e)}")
        }
