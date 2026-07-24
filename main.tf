terraform {
  required_version = ">= 1.0.0"

  # Optional: If you are using Terraform Cloud, uncomment and set your details:
  # backend "remote" {
  #   organization = "YOUR-ORGANIZATION-NAME"
  #   workspaces {
  #     name = "YOUR-WORKSPACE-NAME"
  #   }
  # }
}

# Single test resource
resource "null_resource" "example" {
  triggers = {
    value = "Testing GitHub Actions workflow"
  }
}