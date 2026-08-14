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

# import json
# import urllib.parse
# import boto3
# import pandas as pd
# import io

# s3 = boto3.client('s3')

# def lambda_handler(event, context):
#     # Extract bucket and file key from the S3 event object
#     bucket = event['Records'][0]['s3']['bucket']['name']
#     key = urllib.parse.unquote_plus(
#         event['Records'][0]['s3']['object']['key'], 
#         encoding='utf-8'
#     )
    
#     # Infinite loop guard: Skip if the triggering file is already in the output/ folder
#     if key.startswith('output/'):
#         return {
#             'statusCode': 200,
#             'body': json.dumps('Skipped output folder trigger to prevent recursion loop.')
#         }

#     try:
#         # Fetch the CSV file from S3 and load it into a pandas DataFrame
#         response = s3.get_object(Bucket=bucket, Key=key)
#         df = pd.read_csv(response['Body'])
        
#         # --- Do your DataFrame transformations here if needed ---
#         print(f"Dataframe preview:\n{df.head()}")
        
#         # Write the DataFrame to an in-memory CSV string buffer
#         csv_buffer = io.StringIO()
#         df.to_csv(csv_buffer, index=False)
        
#         # Define destination key in the output/ folder
#         output_key = "output/output.csv"
        
#         # Upload the converted DataFrame back to the same bucket
#         s3.put_object(
#             Bucket=bucket,
#             Key=output_key,
#             Body=csv_buffer.getvalue(),
#             ContentType='text/csv'
#         )
        
#         return {
#             'statusCode': 200,
#             'body': json.dumps(f'Successfully processed {key} and saved to {output_key}')
#         }
        
#     except Exception as e:
#         print(f"Error processing file {key} from bucket {bucket}: {str(e)}")        
#         raise e


######################################################################################

import json
import boto3
import csv
import io
from datetime import datetime
from datetime import datetime, timedelta

# Initialize the S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Define your bucket and file paths
    # Note: Modify these to match your actual bucket and file names
    bucket_name = 'decemberborn'
    input_key = 'input/sample.csv'

    utc_now = datetime.utcnow()
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    month_lowercase = ist_now.strftime('%B').lower()
    time_string = ist_now.strftime(f"%d{month_lowercase}_%I-%M-%S_%p")
    output_key = f'output/output_{time_string}.csv'


    # month_lowercase = now.strftime('%B').lower()
    # time_string = now.strftime(f"%d{month_lowercase}_%I-%M-%S_%p")
    # timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # output_key = f'output/output_{time_string}.csv'
    
    try:
        # 2. Read the CSV file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=input_key)
        
        # Read the file content and decode it from bytes to string
        csv_content = response['Body'].read().decode('utf-8')
        
        # 3. Process the CSV and add a new column
        input_data = csv.reader(io.StringIO(csv_content))
        output_buffer = io.StringIO()
        writer = csv.writer(output_buffer)
        
        # Read the header row and append the new column name
        header = next(input_data)
        header.append('processed_by') # Change this to your new column name
        writer.writerow(header)
        
        # Loop through rows and add the value for the new column
        for row in input_data:
            row.append('AWS-Lambda') # Value for the new column
            writer.writerow(row)
            
        # 4. Write the modified CSV back to the S3 output folder
        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=output_buffer.getvalue()
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed and saved to {output_key}')
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing file: {str(e)}')
        }

    