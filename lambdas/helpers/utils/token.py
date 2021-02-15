import os
import uuid
import logging

from datetime import datetime, timedelta
import jwt

from lambdas.helpers.utils.utils import get_or_create_aws_parameter

# This value is used only for local server. For cloud random ssm param is used!
DEFAULT_SECRET_KEY = 'ff0a2987a037444296e6a341a330fbd7'

logger = logging.getLogger()


def get_sectet_key():
    """Get jwt sectet key"""

    jwt_secret_param_name = os.getenv('JWT_SECRET')
    if jwt_secret_param_name:
        # Get jwt secret of create random and save as ssm param
        secret_key = get_or_create_aws_parameter(jwt_secret_param_name, uuid.uuid4().hex)
        logger.info('secret key has been found in ssm store')
    else:
        # It means this is local server
        secret_key = DEFAULT_SECRET_KEY
        logger.info('Use default secret key')
    return secret_key


def encode_auth_token():
    """
    Generates the Auth Token

    """

    secret_key = get_sectet_key()
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow(),
            'sub': 1
        }
        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
    except Exception as e:
        return False


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    """

    secret_key = get_sectet_key()
    try:
        jwt.decode(auth_token, secret_key, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError as e:
        logger.warning(str(e))
        return False
    except jwt.InvalidTokenError as e:
        logger.warning(str(e))
        return False
