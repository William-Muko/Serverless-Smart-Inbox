# Smart Inbox Manual Testing Guide

Test your Serverless Smart Inbox system using the AWS Console with this step-by-step guide.

## Method 1: AWS S3 Console (Recommended)

### Step 1: Access S3 Console
1. Go to [AWS Console](https://console.aws.amazon.com)
2. Search for "S3" in the services
3. Click on **S3**

### Step 2: Find Your Bucket
1. Look for bucket named: `smart-inbox-emails-021009501201`
2. Click on the bucket name

### Step 3: Upload Test Email
1. Click **Upload** button
2. Click **Add files**
3. Create a new JSON file on your computer with test content (see examples below)
4. Upload to the `incoming/` folder
5. Click **Upload**

### Step 4: Check Results
1. Wait 10-15 seconds for processing
2. Navigate to `processed/` folder
3. Look for new folders: `positive/`, `neutral/`, or `escalate/`
4. Click on the processed file to view sentiment analysis results

---

## Method 2: AWS Lambda Console (Direct Testing)

### Step 1: Access Lambda Console
1. Go to AWS Console → Search "Lambda"
2. Click on **Lambda**

### Step 2: Find Your Function
1. Look for function: `EmailSortingProcessor`
2. Click on the function name

### Step 3: Create Test Event
1. Click **Test** button
2. Select **Create new test event**
3. Choose **S3 Put** template
4. Replace the test event with:
```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "smart-inbox-emails-021009501201"
        },
        "object": {
          "key": "incoming/test_positive.json"
        }
      }
    }
  ]
}
```
5. Name it "TestPositiveEmail"
6. Click **Save**

### Step 4: Upload Test File First
1. Go to S3 console
2. Upload your test JSON to `incoming/test_positive.json`

### Step 5: Run Test
1. Back in Lambda console
2. Click **Test**
3. View execution results and logs

---

## Method 3: CloudWatch Logs (Monitor Processing)

### Step 1: Access CloudWatch
1. AWS Console → Search "CloudWatch"
2. Click **CloudWatch**

### Step 2: View Logs
1. Click **Log groups** in left menu
2. Find `/aws/lambda/EmailSortingProcessor`
3. Click on the log group
4. Click on latest log stream

### Step 3: Monitor Real-time
1. Upload email via S3 console
2. Refresh CloudWatch logs to see processing
3. View sentiment analysis results in logs

---

## Test Email Examples

### Positive Email (Should go to positive/)
```json
{
  "from": "happy.customer@example.com",
  "to": "support@company.com",
  "subject": "Thank you for excellent service!",
  "body": "I'm absolutely thrilled with your product. The customer service was amazing and everything works perfectly. Keep up the great work!",
  "timestamp": "2024-01-15T14:30:00Z"
}
```

### Negative Email (Should go to escalate/)
```json
{
  "from": "angry@customer.com",
  "to": "support@company.com",
  "subject": "TERRIBLE SERVICE - REFUND NOW!",
  "body": "This is the worst experience ever. Your product is broken and support is useless. I demand a full refund immediately!",
  "timestamp": "2024-01-15T15:00:00Z"
}
```

### Urgent Email (Should go to escalate/)
```json
{
  "from": "client@business.com",
  "to": "support@company.com",
  "subject": "URGENT: Critical system failure",
  "body": "We have a critical system failure that needs immediate attention. This is blocking our entire operation. Please respond ASAP!",
  "timestamp": "2024-01-15T16:00:00Z"
}
```

### Neutral Email (Should go to neutral/)
```json
{
  "from": "info@company.com",
  "to": "support@company.com",
  "subject": "Account Information Update",
  "body": "Please update your account information by logging into your dashboard. This is a routine maintenance notification.",
  "timestamp": "2024-01-15T17:00:00Z"
}
```

---

## Expected Results

After uploading each test email, you should see:

1. **Processing Time**: 5-15 seconds
2. **File Location**: `processed/{category}/{timestamp}_{filename}.json`
3. **Added Analysis**: Sentiment scores, urgency detection, auto-response
4. **Categories**:
   - `positive/` - Happy, satisfied customers
   - `neutral/` - Informational, routine messages
   - `escalate/` - Negative sentiment or urgent keywords

---

## Troubleshooting

### Email Not Processing
- Check CloudWatch logs for errors
- Verify file is in `incoming/` folder
- Ensure JSON format is valid

### Wrong Category
- Review sentiment scores in processed file
- Check for urgent keywords: "urgent", "critical", "asap", "immediate"
- Negative sentiment (>50%) automatically escalates

### No Auto-Response
- Check Lambda function logs
- Verify Comprehend permissions
- Ensure all required fields are in email JSON

---

## Quick Test Workflow

1. **Create test file** → Save as `test_email.json`
2. **Upload to S3** → `incoming/` folder
3. **Wait 15 seconds** → Processing time
4. **Check results** → `processed/` folder
5. **View analysis** → Download and open processed file

The easiest method is **S3 Console** - just drag and drop JSON files into the `incoming/` folder and watch them get processed automatically!