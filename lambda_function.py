import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FeedbackTable')

def lambda_handler(event, context):
    try:
        # Check if body exists in the event
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Request body is missing'})
            }
            
        body = json.loads(event['body'])
        
        name = body.get('name', 'Anonymous')
        session = body.get('session', 'General')
        rating = int(body.get('rating', 0))
        comments = body.get('comments', '')
        
        if rating < 1 or rating > 5:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Rating must be between 1 and 5'})
            }

        feedback_item = {
            'id': str(uuid.uuid4()),
            'name': name,
            'session': session,
            'rating': rating,
            'comments': comments,
            'timestamp': datetime.utcnow().isoformat()
        }

        table.put_item(Item=feedback_item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Feedback saved. Thank you!',
                'status': 'success'
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }