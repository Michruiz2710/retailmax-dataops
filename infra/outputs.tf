output "bucket_datos" {
  description = "Bucket S3 de datos del entorno"
  value       = aws_s3_bucket.datos.bucket
}

output "dev_workspace_id" {
  description = "ID de la instancia EC2 de DEV (vacio en QA y PROD)"
  value       = one(aws_instance.dev_workspace[*].id)
}

output "endpoint_base_datos" {
  description = "Endpoint de la base RDS (vacio en DEV)"
  value       = one(aws_db_instance.ventas[*].endpoint)
}