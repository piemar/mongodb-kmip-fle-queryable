"""
Automatically encrypt and decrypt a field with a KMIP KMS provider.
Example modified from https://pymongo.readthedocs.io/en/stable/examples/encryption.html#providing-local-automatic-encryption-rules
"""
import configuration_fle as configuration
from pprint import pprint
from bson.codec_options import CodecOptions
from pymongo import MongoClient
from pymongo.encryption import ClientEncryption


def rotate():
    client = MongoClient(configuration.connection_uri)
    client_encryption = ClientEncryption(
        configuration.kms_providers,  # pass in the kms_providers variable from the previous step
        configuration.key_vault_namespace,
        client,
        CodecOptions(),
        kms_tls_options=configuration.kms_tls_options,
    )    
    client_encryption.rewrap_many_data_key({})    
    pprint("Keys rotated")


def main():
    rotate()
if __name__ == "__main__":
    main()