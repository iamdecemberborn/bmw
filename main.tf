terraform {
  required_version = ">= 1.0.0"
  
  # If you are using Terraform Cloud, uncomment and configure this section:
  # backend "remote" {
  #   organization = "YOUR-ORGANIZATION-NAME"
  #   workspaces {
  #     name = "YOUR-WORKSPACE-NAME"
  #   }
  # }
}

# Example test resource that doesn't cost anything or deploy real hardware
resource "null_resource" "example" {
  triggers = {
    value = "Testing GitHub Actions workflow"
  }
}



terraform {
  required_version = ">= 1.0.0"
}

# Example test resource
resource "null_resource" "example" {
  triggers = {
    value = "Testing GitHub Actions workflow"
  }
}