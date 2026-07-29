output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.csv_bucket.id
}

output "s3_input_folder" {
  description = "Folder where CSV files trigger Lambda"
  value       = "s3://${aws_s3_bucket.csv_bucket.id}/input/"
}

output "lambda_function_arn" {
  description = "ARN of the deployed Lambda function"
  value       = aws_lambda_function.my_lambda.arn
}