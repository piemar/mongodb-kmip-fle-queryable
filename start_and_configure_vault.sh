# Start Vault and unseal Vault providing config containing reference to HashiCorp license.txt

export VAULT_ADDR=http://127.0.0.1:8200
vault server -config=kmip-with-hashicorp-key-vault/vault/config.hcl &
sleep 5
vault operator init -key-shares=1 -key-threshold=1 -format=json > init.json
unseal_keys=$(jq -r .unseal_keys_b64[0] < init.json)
root_token=$(jq -r .root_token < init.json)
vault operator unseal $unseal_keys
vault login token=$root_token
# Configure KMIP Secrets Engine for FLE
vault secrets enable -path=demo/kmip kmip
vault write demo/kmip/config listen_addrs=0.0.0.0:5697 default_tls_client_key_type=rsa default_tls_client_key_bits=2048 server_ips=127.0.0.1 tls_ca_key_type=rsa tls_ca_key_bits=2048
# Configure Role and Scope and Certs
vault read demo/kmip/ca
vault write -f demo/kmip/scope/mongodb
vault write demo/kmip/scope/mongodb/role/FLE tls_client_key_bits=2048 tls_client_key_type=rsa operation_all=true

vault write -format=json \
    demo/kmip/scope/mongodb/role/FLE/credential/generate \
    format=pem > fle_credential.json
serial_number=$(jq -r .data.serial_number < fle_credential.json)
jq -r .data.certificate < fle_credential.json > kmip-with-hashicorp-key-vault/vault/certs/fle/vv-ca.pem
jq -r .data.private_key < fle_credential.json > kmip-with-hashicorp-key-vault/vault/certs/fle/vv-key.pem    
cat kmip-with-hashicorp-key-vault/vault/certs/fle/vv-ca.pem kmip-with-hashicorp-key-vault/vault/certs/fle/vv-key.pem > kmip-with-hashicorp-key-vault/vault/certs/fle/vv-client.pem
vault read demo/kmip/scope/mongodb/role/FLE/credential/lookup \serial_number=$serial_number -format=json > fle_ca_chain.json
jq -r .data.certificate < fle_ca_chain.json > kmip-with-hashicorp-key-vault/vault/certs/fle/vv-ca.pem    
rm -rf *.json

vault write demo/kmip/scope/mongodb/role/QUERYABLE tls_client_key_bits=2048 tls_client_key_type=rsa operation_all=true
vault write -format=json \
    demo/kmip/scope/mongodb/role/QUERYABLE/credential/generate \
    format=pem > queryable_credential.json
serial_number=$(jq -r .data.serial_number < queryable_credential.json)
jq -r .data.certificate < queryable_credential.json > kmip-with-hashicorp-key-vault/vault/certs/queryable/vv-ca.pem
jq -r .data.private_key < queryable_credential.json > kmip-with-hashicorp-key-vault/vault/certs/queryable/vv-key.pem    
cat kmip-with-hashicorp-key-vault/vault/certs/queryable/vv-ca.pem kmip-with-hashicorp-key-vault/vault/certs/queryable/vv-key.pem > kmip-with-hashicorp-key-vault/vault/certs/queryable/vv-client.pem
vault read demo/kmip/scope/mongodb/role/QUERYABLE/credential/lookup \serial_number=$serial_number -format=json > queryable_ca_chain.json
jq -r .data.certificate < queryable_ca_chain.json > kmip-with-hashicorp-key-vault/vault/certs/queryable/vv-ca.pem    
rm -rf *.json
echo "==========================================="
echo "Access vault console http://localhost:8200/"
echo "Root Token: ${root_token}"
echo "==========================================="