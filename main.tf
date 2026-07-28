terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# 1. Zip your main.py file
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "main.py"
  output_path = "lambda_function.zip"
}

# 2. Fetch your EXISTING IAM Role from AWS
data "aws_iam_role" "existing_role" {
  name = "decemberborn-role-f317dr01"
}

# 3. Deploy the AWS Lambda using the existing role
resource "aws_lambda_function" "my_lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  function_name    = "my_github_actions_lambda_v2"
  role             = data.aws_iam_role.existing_role.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.12"
}
