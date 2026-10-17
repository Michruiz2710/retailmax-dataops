terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # El estado (terraform.tfstate) NO va en Git ya que informacion no apta para todos
  # Se guarda en un bucket S3 con bloqueo para que dos personas no lo pisen
  backend "s3" {
    bucket         = "retailmax-terraform-state"
    key            = "dataops/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "retailmax-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project     = "retailmax-dataops"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}