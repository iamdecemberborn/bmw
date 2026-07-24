print("Hello, World!")
##checking thhis line afterremoving Fine-grained personal access tokens


import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from GitHub Actions and Terraform!')
    }

