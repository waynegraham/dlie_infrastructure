provider "aws" {
  region = var.aws_region
}

# EKS Cluster
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.27"
  subnets         = var.private_subnets
  vpc_id          = var.vpc_id
  manage_aws_auth = true

  node_groups = {
    default = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
      instance_types   = ["t3.medium"]
    }
  }
}

# S3 Bucket for raw data
resource "aws_s3_bucket" "data_bucket" {
  bucket = var.bucket_name
  acl    = "private"
}

# RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier         = "${var.cluster_name}-db"
  engine             = "postgres"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20
  name               = "library"
  username           = var.db_user
  password           = var.db_password
  skip_final_snapshot = true
  vpc_security_group_ids = var.db_sg_ids
  db_subnet_group_name   = var.db_subnet_group
}