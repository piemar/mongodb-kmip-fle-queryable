# Start Vault and unseal Vault providing config containing reference to HashiCorp license.txt

export VAULT_ADDR=http://127.0.0.1:8200
vault server -config=csfle_kmip/vault/config.hcl &
sleep 5
vault operator init -key-shares=1 -key-threshold=1 -format=json > init.json
unseal_keys=$(jq -r .unseal_keys_b64[0] < init.json)
root_token=$(jq -r .root_token < init.json)
vault operator unseal $unseal_keys
vault login token=$root_token
# Configure KMIP Secrets Engine
vault secrets enable -path=demo/kmip kmip
vault write demo/kmip/config listen_addrs=0.0.0.0:5697 default_tls_client_key_type=rsa default_tls_client_key_bits=2048 server_ips=127.0.0.1 tls_ca_key_type=rsa tls_ca_key_bits=2048
# Configure Role and Scope and Certs
vault read demo/kmip/ca
vault write -f demo/kmip/scope/mongodb
vault write demo/kmip/scope/mongodb/role/FLE tls_client_key_bits=2048 tls_client_key_type=rsa operation_all=true

vault write -format=json \
    demo/kmip/scope/mongodb/role/FLE/credential/generate \
    format=pem > credential.json
serial_number=$(jq -r .data.serial_number < credential.json)
jq -r .data.certificate < credential.json > csfle_kmip/certs/vv-ca.pem
jq -r .data.private_key < credential.json > csfle_kmip/certs/vv-key.pem    
cat csfle_kmip/certs/vv-ca.pem csfle_kmip/certs/vv-key.pem > csfle_kmip/certs/vv-client.pem
vault read demo/kmip/scope/mongodb/role/FLE/credential/lookup \serial_number=$serial_number -format=json > ca_chain.json
jq -r .data.certificate < ca_chain.json > csfle_kmip/certs/vv-ca.pem    
rm -rf *.json
echo "Access vault console http://localhost:8200/"
echo "Root Token: ${root_token}"