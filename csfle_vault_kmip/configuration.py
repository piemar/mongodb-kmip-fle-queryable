
encrypted_namespace = "DEMO-CSFLE-KMIP.users"
key_vault_namespace = "DEMO-CSFLE-KMIP.datakeys"
connection_uri = "mongodb+srv://<USER>:<PASSWORD>@<CLUSTER-NAME>?retryWrites=true&w=majority"
# Configure the "kmip" provider.
kms_providers = {
    "kmip": {
        "endpoint": "localhost:5697"
    }
}
kms_tls_options = {
    "kmip": {
        "tlsCAFile": "certs/vv-ca.pem",
        "tlsCertificateKeyFile": "certs/vv-client.pem"
    }
}