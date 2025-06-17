output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  value = module.eks.cluster_id
}

output "s3_bucket_name" {
  value = aws_s3_bucket.data_bucket.id
}

output "db_endpoint" {
  value = aws_db_instance.postgres.address
}