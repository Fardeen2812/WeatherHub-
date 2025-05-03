terraform {
  backend "azurerm" {
    resource_group_name  = "weatherhub-rg"
    storage_account_name = "weatherhubstorage"
    container_name       = "weatherhubcontainer"
    key                  = "terraform.tfstate"
  }
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = var.aks_name

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  depends_on = [azurerm_container_registry.acr]
}

resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id         = azurerm_kubernetes_cluster.aks.identity[0].principal_id
  role_definition_name = "AcrPull"
  scope                = azurerm_container_registry.acr.id
}

resource "azurerm_redis_cache" "redis" {
  name                = var.redis_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  capacity            = 1
  family              = "C"
  sku_name            = "Basic"
}

resource "azurerm_postgresql_flexible_server" "PostgreSQL" {
  name                   = "weatherhub-db-server-westus"
  location               = "westus"
  resource_group_name    = azurerm_resource_group.rg.name
  administrator_login    = "weatherhubadmin"
  administrator_password = "TemporaryPassword123!"
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
  version                = "13"
}

resource "azurerm_postgresql_flexible_server_database" "PostgreSQL_db" {
  name      = var.postgres_db_name
  server_id = azurerm_postgresql_flexible_server.PostgreSQL.id
  charset   = "UTF8"
}

resource "azurerm_key_vault" "kv" {
  name                       = var.key_vault_name
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  sku_name                   = "standard"
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
}

resource "azurerm_key_vault_access_policy" "example" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  secret_permissions = [
    "Get",
  ]
}

resource "azurerm_container_registry" "acr" {
  name                = "${var.redis_name}acr"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_storage_account" "rgstr" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "azstrcontainer" {
  name               = var.container_name
  storage_account_id = azurerm_storage_account.rgstr.id
}

data "azurerm_client_config" "current" {}

data "azurerm_key_vault_secret" "postgres_admin_password" {
  name         = "postgres-admin-password"
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_container_group" "jenkins" {
  name                = "jenkins-container"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  ip_address_type     = "Public"

  container {
    name   = "jenkins"
    image  = "jenkins/jenkins:lts"
    cpu    = "1"
    memory = "2"

    ports {
      port     = 8080
      protocol = "TCP"
    }

    ports {
      port     = 50000
      protocol = "TCP"
    }
  }
}

output "jenkins_url" {
  value = azurerm_container_group.jenkins.ip_address
}

