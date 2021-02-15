from flask_restx import marshal
from lambdas.helpers.utils.token import encode_auth_token

from lambdas.helpers.service import Service
from lambdas.helpers.response import build_response
from lambdas.models.models import auth_model


class AuthService(Service):

    def create(self):
        """Generate new jwt token"""

        token = encode_auth_token()
        return build_response(marshal(dict(token=token), auth_model))
