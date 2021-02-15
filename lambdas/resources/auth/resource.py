from flask import request
from flask_restx import Namespace
from flask_restx._http import HTTPStatus

from lambdas.helpers.resource import Resource
from lambdas.services.auth import AuthService
from lambdas.models.models import auth_model
from lambdas.helpers.response import flask_lambda_adapter as lambda_adapter

ns = Namespace('auth', description='Token management')


@ns.route('')
@ns.doc(responses={
    HTTPStatus.OK: 'Success',
    HTTPStatus.BAD_REQUEST: 'Bad request',
    HTTPStatus.INTERNAL_SERVER_ERROR: 'error: Unexpected response',
})
class AuthView(Resource):
    # Base service (Business logic layer)
    service = AuthService()

    @ns.response(code=200, model=auth_model, description='Get auth token')
    def post(self):
        """Generate new jwt token"""

        return lambda_adapter(self.service.create, request)
