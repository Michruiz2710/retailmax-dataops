variable "region" {
  description = "Region de AWS"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Entorno a crear: dev, qa o prod"
  type        = string

  validation {
    condition     = contains(["dev", "qa", "prod"], var.environment)
    error_message = "environment debe ser dev, qa o prod."
  }
}

variable "dev_instance_type" {
  description = "Tamano de la instancia EC2 de DEV (bajo costo)"
  type        = string
  default     = "t3.medium"
}

variable "dev_ami_id" {
  description = "Imagen (AMI) de la estacion de trabajo de DEV"
  type        = string
  default     = "ami-0abcdef1234567890" # valor simulado
}

variable "db_instance_class" {
  description = "Tamano de la base RDS (QA es un espejo mas pequeno de PROD)"
  type        = string
  default     = "db.t3.medium"
}

variable "db_allocated_storage" {
  description = "Almacenamiento de la base RDS en GB"
  type        = number
  default     = 50
}

variable "db_password" {
  description = "Contraseña de la base: se pasa con TF_VAR_db_password desde un gestor de secretos"
  type        = string
  sensitive   = true
  default     = null # DEV no crea base RDS, asi que no la necesita
}