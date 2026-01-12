# Intelligent Email Sorting System

Serverless email routing system using AWS Lambda, S3, and Amazon Comprehend for sentiment analysis and automatic categorization.

## Architecture

- **AWS SAM**: Infrastructure as Code deployment framework
- **S3 Bucket**: Stores incoming and processed emails
- **Lambda Function**: Analyzes emails using Amazon Comprehend
- **Amazon Comprehend**: Detects sentiment and urgency
- **IAM Roles**: Manages permissions

## Features

✅ **Sentiment Detection**: Positive, Neutral, Negative
✅ **Urgency Detection**: Keywords like "urgent", "critical", "asap"
✅ **Auto-Routing**: Emails sorted into categories
✅ **Response Templates**: Auto-generated based on sentiment
✅ **Escalation**: Negative/urgent emails flagged

## Email Categories

- `escalate/` - Negative sentiment or urgent keywords
- `positive/` - Positive sentiment
- `neutral/` - Neutral sentiment

## Deployment

### Prerequisites
- AWS CLI configured
- SAM CLI installed
- Python 3.11+

### Steps

```bash
# Deploy infrastructure
sam build
sam deploy --guided

# Upload test email
aws s3 cp test_email.json s3://smart-inbox-emails-{ACCOUNT_ID}/incoming/test_email.json
```

## Email Format

```json
{
  "from": "sender@example.com",
  "to": "recipient@example.com",
  "subject": "Email subject",
  "body": "Email content",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Output Format

Processed emails include analysis:

```json
{
  "from": "sender@example.com",
  "subject": "...",
  "body": "...",
  "analysis": {
    "sentiment": "NEGATIVE",
    "scores": {
      "Positive": 0.01,
      "Negative": 0.95,
      "Neutral": 0.03,
      "Mixed": 0.01
    },
    "urgency": true,
    "category": "escalate",
    "auto_response": "Your urgent message has been escalated..."
  }
}
```

## Testing

```bash
# Upload test email
aws s3 cp test_email.json s3://YOUR-BUCKET/incoming/

# Check processed results
aws s3 ls s3://YOUR-BUCKET/processed/ --recursive
```

## Cost Optimization

- Lambda: Pay per invocation
- S3: Pay for storage
- Comprehend: $0.0001 per unit (100 chars)

## Monitoring

Check CloudWatch Logs:
```bash
aws logs tail /aws/lambda/EmailSortingProcessor --follow
```
