# ==========================================================================
# Infraestructura de RetailMax como codigo.
# El MISMO archivo crea DEV, QA o PROD; solo cambian las variables de
# infra/envs/<entorno>.tfvars. Por eso los entornos son identicos en
# estructura y QA es un espejo fiel de PROD.
# ==========================================================================

locals {
  es_dev  = var.environment == "dev"
  es_prod = var.environment == "prod"
}

# Bucket S3 de datos. En QA es el bucket de datos de staging que recibe
# el snapshot anonimizado de produccion
resource "aws_s3_bucket" "datos" {
  bucket = "retailmax-${var.environment}-data"
}

resource "aws_s3_bucket_versioning" "datos" {
  bucket = aws_s3_bucket.datos.id
  versioning_configuration {
    status = "Enabled" # cada objeto conserva sus versiones anteriores
  }
}

resource "aws_s3_bucket_public_access_block" "datos" {
  bucket                  = aws_s3_bucket.datos.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Instancia EC2 de trabajo: SOLO en DEV (bajo costo)
resource "aws_instance" "dev_workspace" {
  count         = local.es_dev ? 1 : 0
  ami           = var.dev_ami_id
  instance_type = var.dev_instance_type

  tags = {
    Name = "retailmax-dev-workspace"
  }
}

# Base de datos RDS PostgreSQL: en QA (espejo pequeno) y en PROD
# En PROD: alta disponibilidad, backups y proteccion contra borrado,
# que atacan directamente las caidas y el DROP TABLE accidental
resource "aws_db_instance" "ventas" {
  count                   = local.es_dev ? 0 : 1
  identifier              = "retailmax-${var.environment}-db"
  engine                  = "postgres"
  engine_version          = "16"
  instance_class          = var.db_instance_class
  allocated_storage       = var.db_allocated_storage
  username                = "retailmax_admin"
  password                = var.db_password
  multi_az                = local.es_prod
  backup_retention_period = local.es_prod ? 7 : 1
  deletion_protection     = local.es_prod
  skip_final_snapshot     = !local.es_prod
  storage_encrypted       = true
  publicly_accessible     = false
}

# Rol IAM con permisos restringidos (minimo privilegio):
# solo puede LEER el bucket de su propio entorno
resource "aws_iam_role" "lector_datos" {
  name = "retailmax-${var.environment}-lector-datos"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "solo_lectura" {
  name = "solo-lectura-bucket-${var.environment}"
  role = aws_iam_role.lector_datos.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:GetObject", "s3:ListBucket"]
      Resource = [
        aws_s3_bucket.datos.arn,
        "${aws_s3_bucket.datos.arn}/*"
      ]
    }]
  })
}