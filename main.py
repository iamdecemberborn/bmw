# import json

# def lambda_handler(event, context):
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from GitHub Actions and Terraform! test ')
#     }



import json
import urllib.parse
import boto3
import csv

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket and file key from the S3 event object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], 
        encoding='utf-8'
    )
    
    try:
        # Fetch the CSV file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        lines = response['Body'].read().decode('utf-8').splitlines()
        
        # Parse the CSV contents
        reader = csv.DictReader(lines)
        for row in reader:
            print(row)  # Process each row here
            
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {key}')
        }
        
    except Exception as e:
        print(f"Error processing file {key} from bucket {bucket}: {str(e)}")
        raise e