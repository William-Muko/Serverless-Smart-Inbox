import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
comprehend = boto3.client('comprehend')

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'smart-inbox-emails')
URGENT_KEYWORDS = ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'important', 'deadline']

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        email_obj = s3.get_object(Bucket=bucket, Key=key)
        email_data = json.loads(email_obj['Body'].read())
        
        result = process_email(email_data)
        route_email(bucket, key, email_data, result)
        
    return {'statusCode': 200, 'body': json.dumps('Processing complete')}

def process_email(email_data):
    text = f"{email_data.get('subject', '')} {email_data.get('body', '')}"
    
    sentiment_response = comprehend.detect_sentiment(Text=text[:5000], LanguageCode='en')
    sentiment = sentiment_response['Sentiment']
    scores = sentiment_response['SentimentScore']
    
    urgency = detect_urgency(text.lower())
    
    return {
        'sentiment': sentiment,
        'scores': scores,
        'urgency': urgency,
        'category': categorize(sentiment, urgency),
        'auto_response': generate_response(sentiment, urgency)
    }

def detect_urgency(text):
    return any(keyword in text for keyword in URGENT_KEYWORDS)

def categorize(sentiment, urgency):
    if sentiment == 'NEGATIVE' or urgency:
        return 'escalate'
    elif sentiment == 'POSITIVE':
        return 'positive'
    else:
        return 'neutral'

def generate_response(sentiment, urgency):
    if urgency:
        return "Your urgent message has been escalated to our priority team."
    elif sentiment == 'NEGATIVE':
        return "We apologize for any inconvenience. A specialist will contact you shortly."
    elif sentiment == 'POSITIVE':
        return "Thank you for your message! We appreciate your feedback."
    else:
        return "Thank you for contacting us. We'll respond within 24 hours."

def route_email(bucket, key, email_data, result):
    category = result['category']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    output_data = {**email_data, 'analysis': result, 'processed_at': timestamp}
    output_key = f"processed/{category}/{timestamp}_{key.split('/')[-1]}"
    
    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=json.dumps(output_data, indent=2),
        ContentType='application/json'
    )
