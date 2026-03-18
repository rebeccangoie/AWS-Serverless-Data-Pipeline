# AWS Serverless Data Pipeline

### Project
I built a cloud-based pipeline that automatically cleans data files. Instead of manually opening Excel to fix empty rows, I set up a system where I just drop a CSV file into an S3 bucket and it cleans itself instantly.

### How it works
* **S3 Bucket:** I created a bucket with two folders: `uploads/` and `processed/`.
* **AWS Lambda:** I wrote a Python script using the Pandas library. I added a "Lambda Layer" so the function would have the tools it needs to handle data.
* **The Trigger:** I connected the bucket to the Lambda function. Now, the second a file hits the `uploads` folder, the code wakes up and runs.
* **Cleaning:** The code looks for empty rows (null values), removes them, and saves a brand new "cleaned" version of the file into the `processed` folder.

### Tools I used
* **Python 3.14** (for the cleaning logic)
* **AWS Lambda** (to run the code without a server)
* **Amazon S3** (to store the files)
* **IAM Roles** (to give the Lambda permission to read and write to the bucket)
