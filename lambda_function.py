import json
import boto3
from botocore.exceptions import ClientError

ses_client = boto3.client('ses', region_name='ap-northeast-1') 

def lambda_handler(event, context):
    try:
        print(f"Received event: {json.dumps(event)}")
        body = json.loads(event['body'])
        recipient = body.get('recipient')
        subject = body.get('subject')
        body_content = body.get('body')
        if not recipient or not subject or not body_content:
            raise ValueError("Missing required fields in the event payload.")
        try:
            response = ses_client.send_email(
                Source='rskavinraj12345@gmail.com',  
                Destination={
                    'ToAddresses': [
                        recipient
                    ],
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': body_content
                        }
                    }
                }
            )
            print(f"Email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
            print(f"Failed to send email: {e.response['Error']['Message']}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Failed to send email: {e.response['Error']['Message']}"})
            }
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Email triggered successfully",
                "recipient": recipient,
                "subject": subject
            })
        }
        return response

    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Bad request: {str(e)}"})
        }

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
