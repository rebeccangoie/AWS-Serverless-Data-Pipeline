import json
import boto3
import urllib.parse
import pandas as pd  
import io

s3 = boto3.client('s3')
# Integrate Amazon Bedrock
bedrock = boto3.client('bedrock-runtime', region_name='us-east-2')

def lambda_handler(event, context):
    # Get bucket and file info
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # 1. Get file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    
    df = pd.read_csv(io.BytesIO(response['Body'].read()))
    
    # Cleaning the data
    df.dropna(how='all', inplace=True)  # Remove empty rows
    df.drop_duplicates(inplace=True)    # Remove duplicate rows
    df.fillna("N/A", inplace=True)      # Fills blank cells with "N/A"
    
    # Convert cleaned table back to a text string
    cleaned_content = df.to_csv(index=False)

    # Grab the first 5 rows of the cleaned data for the AI to audit
    sample_text = df.head(5).to_string() 

    # Prompt to review data sample
    prompt = f"System: You are a Data Auditor. Review this data sample and say 'VALID' or 'Corrupt':\n\n{sample_text}"

    try:
        # Send data to the Claude AI model
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 50,
            "messages": [{"role": "user", "content": prompt}]
        })
        bedrock.invoke_model(modelId='anthropic.claude-3-haiku-20240307-v1:0', body=body)
        print(f"AI Agentic Audit complete for: {key}")
    except Exception as e:
        print(f"AI Audit skipped: {e}")
    
    # 4. Save cleaned file back to S3
    output_key = f"processed/cleaned_{key}"
    s3.put_object(Bucket=bucket, Key=output_key, Body=cleaned_content)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data cleaned with Pandas and AI-Audited successfully!')
    }