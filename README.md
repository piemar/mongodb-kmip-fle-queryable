# MongoDB CSFLE with Hashicorp Vault and KMIP

Automate setup of CSFLE and Queryable Encrption with HashiCorp Vault KMIP Secrets Engine.

The automation creates the following:
* Hashicorp Vault Enterprise
* Configures KMIP Secrets Engine
* Configure Scopes, Roles and other configuration
* Configures Certificate to be used to authenticate against Vault
* An test application that inserts a document with where some fields are CSFLE and Queryable Encryption enabled.

# Update vault/license.txt with license key
Request license key from https://www.hashicorp.com/products/vault/trial and then update kmip-with-hashicorp-key-vault/vault/license.txt

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

# Test KMIP as KMS provider
Python application that inserts a document with CSFLE configured. CSFLE is configured to use HashiCorp Vault KMIP Secrets Engine as KMS provider.

## CSFLE Schema Stored in Database
```
cd /kmip/kmip-with-hashicorp-key-vault/
python3.8 vault_encrypt_with_csfle_kmip.py
```

## CSFLE Schema Stored in Client
```
cd /kmip/kmip-with-hashicorp-key-vault/
python3.8 vault_encrypt_with_csfle_kmip_client_schema.py
```

## Queryable Encryption
```
cd /kmip/kmip-with-hashicorp-key-vault/
python3.8 vault_encrypt_with_queryable_kmip.py
```

The application will automatically encrypt/decrypt the fields defined in the validation schema thats attached to the users collection. Fields that should be shown encrypted are ssn, contact.mobile, contact.email

You should now be able to see in compass that fields that are encrypted have ****** shown as value. 

# Cleanup
If you want to rerun setup, delete vault/data folder. only the data folder.
```
cd /kmip/kmip-with-hashicorp-key-vault/vault/
rm -rf data
```