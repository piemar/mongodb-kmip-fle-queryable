import configuration_queryable as configuration
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
    #1,2 Configure your KMIP Provider and Certificates
    #kmip_provider_config = configure_kmip_provider()    
    rotate()
if __name__ == "__main__":
    main()