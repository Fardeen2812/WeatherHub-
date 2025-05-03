output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name

}

output "redis_hostname" {
  value = azurerm_redis_cache.redis.hostname

}

output "postgresql_fqdn" {
  value = azurerm_postgresql_flexible_server.PostgreSQL.fqdn

}