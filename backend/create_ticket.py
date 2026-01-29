import json
import boto3
import uuid
from datetime import datetime

# Initialize clients
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
table = dynamodb.Table('ServerlessTickets')

# ⚠️ REPLACE THIS WITH YOUR ACTUAL SNS TOPIC ARN
SNS_TOPIC_ARN = "arn:aws:sns:eu-central-1:123456789:AdminAlerts"

def lambda_handler(event, context):
    try:
        # Parse incoming JSON from API Gateway
        body = json.loads(event['body'])
        user_email = body['email']
        issue_text = body['issue']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing email or issue in request')
        }

    # Generate unique ID
    ticket_id = str(uuid.uuid4())

    # 1. Save Ticket to DynamoDB
    table.put_item(Item={
        'ticket_id': ticket_id,
        'email': user_email,
        'issue': issue_text,
        'status': 'OPEN',
        'created_at': str(datetime.now())
    })

    # 2. Send Email Alert via SNS
    message = f"New Ticket Alert!\n\nUser: {user_email}\nIssue: {issue_text}\nID: {ticket_id}"
    
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="🔥 New Help Desk Ticket Created"
        )
    except Exception as e:
        print(f"SNS Error: {e}") # Log error but don't fail the ticket creation

    # 3. Return Success
    return {
        'statusCode': 200,
        'body': json.dumps(f"Ticket {ticket_id} created and Admin notified!")
    }
