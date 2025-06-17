variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  type        = string
  description = "EKS cluster name"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID for EKS"
}

variable "private_subnets" {
  type        = list(string)
  description = "List of private subnet IDs"
}

variable "bucket_name" {
  type        = string
  description = "S3 bucket name for raw data"
}

variable "db_user" {
  type        = string
}

variable "db_password" {
  type        = string
  sensitive   = true
}

variable "db_sg_ids" {
  type        = list(string)
  description = "Security group IDs allow traffic to RDS"
}

variable "db_subnet_group" {
  type        = string
  description = "RDS subnet group name"
}