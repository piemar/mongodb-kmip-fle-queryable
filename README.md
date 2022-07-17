# MongoDB CSFLE with Hashicorp Vault and KMIP

Automate setup of CSFLE with HashiCorp Vault KMIP Secrets Engine.

The automation creates the following:
* Hashicorp Vault Enterprise
* Configures KMIP Secrets Engine
* Configure Scopes, Roles and other configuration
* Configures Certificate to be used to authenticate against Vault
* An test application that inserts a document with where some fields are CSFLE enabled.

# Update vault/license.txt with license key
Request license key from https://www.hashicorp.com/products/vault/trial and then update csfle_vault_kmip/vault/license.txt

# Update MongoDB Atlas connection string
String in file csfle_vault_kmip/configuration.py line 4, Replace USER, PASSWORD, CLUSTER NAME with your Atlas Connection String
```
connection_uri = "mongodb+srv://<USER>:<PASSWORD>@<CLUSTER-NAME>/?retryWrites=true&w=majority"
```
# Start Docker Container
A prebaked docker image that has HashiCorp Vault installed, start container in root of this repo
```
docker run -p 8200:8200 -it -v ${PWD}:/kmip piepet/mongodb-csfle:latest
```
# Start Vault and configure vault
Running below commands will start Vault Server and configure KMIP Secrets engine. Certificates will be generated, vv-client.pem, vv-ca.pem, vv-key.pem. The CSFLE configuration.py will refer to this certificates.
```
cd kmip
./start_and_configure_vault.sh
```

# Test CSFLE with KMIP as KMS provider
Python application that inserts a document with CSFLE configured. CSFLE is configured to use HashiCorp Vault KMIP Secrets Engine as KMS provider.
```
cd /kmip/csfle_vault_kmip/
python3 vault_encrypt_with_kmip.py
```

# Cleanup
If you want to rerun setup, delete vault/data folder. only the data folder.
```
cd /kmip/csfle_vault_kmip/vault/
rm -rf data
```