encrypted_namespace = "DEMO-CSFLE-KMIP.users"
key_vault_namespace = "DEMO-CSFLE-KMIP.datakeys"
connection_uri = "mongodb+srv://<USER>:<PASSWORD>@<CLUSTER-NAME>?retryWrites=true&w=majority"
shared_library_path ="/csfle_shared_lib/mongo_crypt_v1.so"
# Configure the "kmip" provider.
kms_providers = {
    "kmip": {
        "endpoint": "localhost:5697"
    }
}
kms_tls_options = {
    "kmip": {
        "tlsCAFile": "/kmip/csfle_kmip/certs/vv-ca.pem",
        "tlsCertificateKeyFile": "/kmip/csfle_kmip/certs/vv-client.pem"
    }
}