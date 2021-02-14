import logging

from boto3 import client

client = client('ssm')


def get_or_create_aws_parameter(name, default):
    """ return raw aws parameter or create new of does not exists"""

    try:
        # get aws parameter
        value = client.get_parameter(Name=name, WithDecryption=True)
        return value["Parameter"]["Value"]
    except client.exceptions.ParameterNotFound:
        logging.warning(f'Paramenter {name} will be created')
        client.put_parameter(
            Name=name,
            Value=str(default),
            Type='SecureString')

    return default
