encrypted_namespace = "DEMO-KMIP-FLE.users"
key_vault_namespace = "DEMO-KMIP-FLE.datakeys"
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
        "tlsCAFile": "vault/certs/FLE/vv-ca.pem",
        "tlsCertificateKeyFile": "vault/certs/FLE/vv-client.pem"
    }
}
