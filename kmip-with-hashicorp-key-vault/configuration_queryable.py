
encrypted_namespace = "DEMO-KMIP-QUERYABLE.users"
key_vault_namespace = "DEMO-KMIP-QUERYABLE.datakeys"
connection_uri = "mongodb+srv://myadmin:X1231Xc121e@mongodb-day-demo.jf9tm8r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
shared_library_path ="/shared_lib/mongo_crypt_v1.so"
# Configure the "kmip" provider.
kms_providers = {
    "kmip": {
        "endpoint": "localhost:5697"
    }
}
kms_tls_options = {
    "kmip": {
        "tlsCAFile": "vault/certs/QUERYABLE/vv-ca.pem",
        "tlsCertificateKeyFile": "vault/certs/QUERYABLE/vv-client.pem"
    }
}