# ==============================================================================
# DATA SOURCES & ARCHIVE
# ==============================================================================

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "main.py"
  output_path = "lambda_function.zip"
}

data "aws_iam_role" "existing_role" {
  name = "decemberborn-role-f317dr01"
}


# ==============================================================================
# LAMBDA FUNCTION
# ==============================================================================

import {
  to = aws_lambda_function.my_lambda
  id = "my_github_actions_lambda"
}

resource "aws_lambda_function" "my_lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  function_name    = "my_github_actions_lambda"
  role             = data.aws_iam_role.existing_role.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.12"
}


# ==============================================================================
# S3 BUCKET & EVENT TRIGGER
# ==============================================================================

import {
  to = aws_s3_bucket.csv_bucket
  id = "decemberborn"
}

resource "aws_s3_bucket" "csv_bucket" {
  bucket = "decemberborn"
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.csv_bucket.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.csv_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.my_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "input/"
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_permission.allow_s3]
}