variable "region" {
  description = "Aws Regios"
  type        = string
  default     = "us-east-1"
}

variable "key_name" {
  description = "Key name"
  type        = string
  default     = "Jenkins-key"
}

variable "instance_name" {
  description = "Jenkins server"
  type        = string
  default     = "Jenkins-server"
}

variable "iam_role" {
  description = "iam role"
  type        = string
  default     = "Jenkins-role"
}