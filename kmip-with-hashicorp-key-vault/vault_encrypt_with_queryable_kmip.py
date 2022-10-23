"""
Automatically encrypt and decrypt a field with a KMIP KMS provider.
"""
import json
from multiprocessing import connection
import os
import configuration_queryable as configuration
from pprint import pprint
from bson.codec_options import CodecOptions
from bson import json_util
from pymongo import MongoClient
from pymongo.encryption import (Algorithm,
                                ClientEncryption)
from pymongo.encryption_options import AutoEncryptionOpts

def configure_data_keys(kmip_configuration):
    db_name, coll_name = configuration.key_vault_namespace.split(".", 1)
    key_vault_client = MongoClient(configuration.connection_uri)
    key_vault_client[db_name][coll_name].create_index(
    [("keyAltNames", 1)],
    unique=True,
    partialFilterExpression={"keyAltNames": {"$exists": True}},
)
    client_encryption = ClientEncryption(
    kmip_configuration["kms_providers"],
    configuration.key_vault_namespace,
    MongoClient(configuration.connection_uri),
    # The CodecOptions class used for encrypting and decrypting.
    # This should be the same CodecOptions instance you have configured
    # on MongoClient, Database, or Collection. We will not be calling
    # encrypt() or decrypt() in this example so we can use any
    # CodecOptions.
    CodecOptions(),
    kms_tls_options=kmip_configuration["kms_tls_options"])

    # Create a new data key and json schema for the encryptedField.
    # https://dochub.mongodb.org/core/client-side-field-level-encryption-automatic-encryption-rules
    data_key_id_1 = client_encryption.create_data_key(
        'kmip', key_alt_names=['pymongo_encryption_example_1'])

    data_key_id_2 = client_encryption.create_data_key(
        'kmip', key_alt_names=['pymongo_encryption_example_2'])

    data_key_id_3 = client_encryption.create_data_key(
        'kmip', key_alt_names=['pymongo_encryption_example_3'])

    encryption_data_keys = {"key1": data_key_id_1,"key2":data_key_id_2, "key3":data_key_id_3}

    return encryption_data_keys

def configure_queryable_session(encrypted_fields_schema):
    auto_encryption = AutoEncryptionOpts(
        configuration.kms_providers,
        configuration.key_vault_namespace,
        encrypted_fields_map=encrypted_fields_schema,
        kms_tls_options=configuration.kms_tls_options,
        schema_map=None,
        crypt_shared_lib_path=configuration.shared_library_path
    )
    return auto_encryption

def create_schema(data_keys):
    # We are creating a collection that has an validation schema attached, 
    # that uses the encrypt attribute to define which fields should be encrypted.
    encrypted_db_name = configuration.database_namespace
    encrypted_coll_name = "users"
    encrypted_fields_map = {
        f"{encrypted_db_name}.{encrypted_coll_name}": {
            "fields": [
                {
                    "keyId": data_keys["key1"],
                    "path": "contact.email",
                    "bsonType": "string",
                    "queries": {"queryType": "equality"},
                },
                {
                    "keyId": data_keys["key2"],
                    "path": "contact.mobile",
                    "bsonType": "string",
                    "queries": {"queryType": "equality"},
                },
                {
                    "keyId": data_keys["key3"],
                    "path": "ssn",
                    "bsonType": "string",
                    "queries": {"queryType": "equality"},
                }
            ],
        },
    }
    return encrypted_fields_map

def reset():    
    db_name, coll_name = configuration.encrypted_namespace.split(".", 1)
    coll = MongoClient(configuration.connection_uri)[db_name][coll_name]
    # Clear old data
    coll.drop()

def create_user(csfle_options):
    mongo_client_csfle = MongoClient(configuration.connection_uri,auto_encryption_opts=csfle_options)    
    db_name, coll_name = configuration.encrypted_namespace.split(".", 1)
    coll = mongo_client_csfle[db_name][coll_name]
    # Clear old data
    coll.insert_one({
        "firstName": 'Alan',
        "lastName":  'Turing',
        "ssn":       '901-01-0001',
        "address": {
            "street": '123 Main',
            "city": 'Omaha',
            "zip": '90210'
        },
        "contact": {
            "mobile": '202-555-1212',
            "email":  'alan@example.com'
        }
    })
    print("Queryable Encryption: Decrypted document:")
    print("===================")    
    pprint((coll.find_one({"ssn":"901-01-0001"})))
    unencrypted_coll = MongoClient(configuration.connection_uri)[db_name][coll_name]
    print("Queryable Encryption: Encrypted document:")
    print("===================")    

    pprint((unencrypted_coll.find_one()))

def configure_kmip_provider():
    return {"kms_providers":configuration.kms_providers,"kms_tls_options":configuration.kms_tls_options}

def main():
    reset()
    #1,2 Configure your KMIP Provider and Certificates
    kmip_provider_config = configure_kmip_provider()
    #3 Configure Encryption Data Keys
    data_keys_config = configure_data_keys(kmip_provider_config)
    #4 Create Schema for Queryable Encryption, will be stored in database
    encrypted_fields_map = create_schema(data_keys_config)
    #5 Run Query
    create_user(configure_queryable_session(encrypted_fields_map))
if __name__ == "__main__":
    main()