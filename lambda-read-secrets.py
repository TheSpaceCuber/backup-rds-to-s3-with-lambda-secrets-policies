import json
import boto3
import base64

# Your secret's name and region
secret_name = "database-1-secret"
region_name = "ap-southeast-1"

#Set up our Session and Client
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)


def lambda_handler(event, context):
    # TODO implement
    # Calling SecretsManager
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    #Raw Response
    print(get_secret_value_response)
