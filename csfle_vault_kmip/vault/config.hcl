
storage "file" {
  path    = "csfle_vault_kmip/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"
}

disable_mlock = true
license_path = "csfle_vault_kmip/vault/license.txt"

api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = true
