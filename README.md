# Cloud-Based AI Data Pipeline

I built a cloud-based pipeline that automatically cleans data files. Instead of manually opening Excel to fix empty rows, I set up a system where I just drop a CSV file into an S3 bucket and it cleans itself instantly.

### How it works
* **S3 Bucket:** I created a bucket with two folders: `uploads/` and `processed/`.
* **AWS Lambda:** I wrote a Python script using the Pandas library. I added a "Lambda Layer" so the function would have the tools it needs to handle data.
* **The Trigger:** I connected the bucket to the Lambda function. Now, the second a file hits the `uploads` folder, the code wakes up and runs.
* **The Agentic AI Layer:** Before saving, the system sends a sample of the data to **Amazon Bedrock**. I programmed an AI "Auditor" to review the first few rows and verify that the data is valid and hasn't been corrupted during processing.
* **Cleaning & Verification:** The code removes empty rows (null values), confirms integrity via the AI agent, and saves a brand new "cleaned" version of the file into the `processed` folder.

### Tools I used
* **Python 3.14** (for the cleaning logic)
* **AWS Lambda** (to run the code without a server)
* **Amazon S3** (to store the files)
* **Amazon Bedrock** (to integrate the AI Agentic Auditor)
* **IAM Roles** (to give the Lambda permission to read/write to the bucket and invoke the AI model)
* **Infrastructure as Code (YAML)** (to architect the multiple components into a single system)
