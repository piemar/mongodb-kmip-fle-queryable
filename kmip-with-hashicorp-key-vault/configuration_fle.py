database_namespace = "DEMO-KMIP-FLE"
encrypted_namespace = "DEMO-KMIP-FLE.users"
key_vault_namespace = "DEMO-KMIP-FLE.datakeys"
connection_uri = "mongodb+srv://<USER>:<PASSWORD>@<CLUSTER-NAME>?retryWrites=true&w=majority"
shared_library_path ="/shared_lib/mongo_crypt_v1.so"
# Configure the "kmip" provider.
kms_providers = {
    "kmip": {
        "endpoint": "localhost:5697"
    }
}
kms_tls_options = {
    "kmip": {
        "tlsCAFile": "vault/certs/fle/vv-ca.pem",
        "tlsCertificateKeyFile": "vault/certs/fle/vv-client.pem"
    }
}