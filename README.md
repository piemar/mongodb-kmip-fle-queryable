# MongoDB CSFLE with Hashicorp Vault and KMIP

### Update vault/license.txt with license key
Request license key from https://www.hashicorp.com/products/vault/trial and then update license.txt

### Update MongoDB Atlas connection string in file configuration.py line 4
Replace USER, PASSWORD, CLUSTER NAME with your Atlas Connection String
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
./configure_kmip_vault.sh
```

# Test CSFLE with HashiCorp KeyVault
```
cd /kmip/csfle_kmip/
python3 vault_encrypt_with_kmip.py
```

# Cleanup
If you want to rerun setup, delete vault/data folder. only the data folder.
```
cd /kmip/csfle_kmip/vault/
rm -rf data
```