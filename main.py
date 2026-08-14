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

    