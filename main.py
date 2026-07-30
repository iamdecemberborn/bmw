# import json

# def lambda_handler(event, context):
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from GitHub Actions and Terraform! test ')
#     }



# import json
# import urllib.parse
# import boto3
# import csv

# s3 = boto3.client('s3')

# def lambda_handler(event, context):
#     # Extract bucket and file key from the S3 event object
#     bucket = event['Records'][0]['s3']['bucket']['name']
#     key = urllib.parse.unquote_plus(
#         event['Records'][0]['s3']['object']['key'], 
#         encoding='utf-8'
#     )
    
#     try:
#         # Fetch the CSV file from S3
#         response = s3.get_object(Bucket=bucket, Key=key)
#         lines = response['Body'].read().decode('utf-8').splitlines()
        
#         # Parse the CSV contents
#         reader = csv.DictReader(lines)
#         for row in reader:
#             print(row)  # Process each row here
            
#         return {
#             'statusCode': 200,
#             'body': json.dumps(f'Successfully processed {key}')
#         }
        
#     except Exception as e:
#         print(f"Error processing file {key} from bucket {bucket}: {str(e)}")
#         raise e
    

###################################################################################################################

import json
import urllib.parse
import boto3
import pandas as pd
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket and file key from the S3 event object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], 
        encoding='utf-8'
    )
    
    # Infinite loop guard: Skip if the triggering file is already in the output/ folder
    if key.startswith('output/'):
        return {
            'statusCode': 200,
            'body': json.dumps('Skipped output folder trigger to prevent recursion loop.')
        }

    try:
        # Fetch the CSV file from S3 and load it into a pandas DataFrame
        response = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(response['Body'])
        
        # --- Do your DataFrame transformations here if needed ---
        print(f"Dataframe preview:\n{df.head()}")
        
        # Write the DataFrame to an in-memory CSV string buffer
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        
        # Define destination key in the output/ folder
        output_key = "output/output.csv"
        
        # Upload the converted DataFrame back to the same bucket
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {key} and saved to {output_key}')
        }
        
    except Exception as e:
        print(f"Error processing file {key} from bucket {bucket}: {str(e)}")
        
        raise e



