variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
  default     = "weatherhub-rg"

}
variable "location" {
  description = "The Azure region to deploy the resources."
  type        = string
  default     = "East US"

}

variable "aks_name" {
  description = "The name of the AKS cluster."
  type        = string
  default     = "weatherhub-aks"

}

variable "redis_name" {
  description = "The name of the Redis cache."
  type        = string
  default     = "weatherhubredis"

}

variable "postgres_server_name" {
  description = "The name of the PostgreSQL server."
  type        = string
  default     = "weatherhub-db-server"

}
variable "postgres_db_name" {
  description = "The name of the PostgreSQL database."
  type        = string
  default     = "weatherhubdb"

}
variable "key_vault_name" {
  description = "The name of the Key Vault."
  type        = string
  default     = "weatherhub-kv"

}

variable "storage_account_name" {
  description = "The name of the storage account."
  type        = string
  default     = "weatherhubstorage"

}
variable "container_name" {
  description = "The name of the container in the storage account."
  type        = string
  default     = "weatherhubcontainer"

}

variable "subscription_id" {
  description = "The Azure subscription ID."
  type        = string
  default     = "630ae77a-ba26-4d59-84db-ecd63996c7a6"
  
}