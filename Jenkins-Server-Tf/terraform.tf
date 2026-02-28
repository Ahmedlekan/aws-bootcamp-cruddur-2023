terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket = "jenkin-server001"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }

  required_version = "~> 1.13.2"
}

