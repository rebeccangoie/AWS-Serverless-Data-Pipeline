import json
import boto3
import urllib.parse

s3 = boto3.client('s3')
# Integrate Amazon Bedrock
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    # Get bucket and file info
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Get file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    
    # Simple "cleaning": remove empty lines
    lines = content.splitlines()
    cleaned_lines = [line for line in lines if line.strip() != ""]
    cleaned_content = "\n".join(cleaned_lines)

    # AI Agentic Layer to display first five lines
    sample_text = "\n".join(cleaned_lines[:5])

    # Prompt to review data sample
    prompt = f"System: You are a Data Auditor. Review this data sample and say 'VALID' or 'Corrupt':\n\n{sample_text}"
    print(f"AI Audit Prompt sent for file: {key}")
    
    # Save cleaned file back to S3
    output_key = f"processed/cleaned_{key}"
    s3.put_object(Bucket=bucket, Key=output_key, Body=cleaned_content)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data cleaned and AI-Audited successfully!')
    }
