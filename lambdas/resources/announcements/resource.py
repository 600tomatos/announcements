from flask import request
from flask_restx import Namespace
from flask_restx._http import HTTPStatus

from lambdas.helpers.resource import Resource
from lambdas.services.announcements import AnnouncementService
from lambdas.models.models import announcement_model, list_announcement_model
from lambdas.helpers.response import flask_lambda_adapter as lambda_adapter

ns = Namespace('announcements', description='CRUD operations over announcements')


@ns.route('')
@ns.doc(responses={
    HTTPStatus.CREATED: 'Created',
    HTTPStatus.BAD_REQUEST: 'Bad request',
    HTTPStatus.FORBIDDEN: 'Forbidden',
    HTTPStatus.INTERNAL_SERVER_ERROR: 'error: Unexpected response',
})
class ListOrCreateView(Resource):
    # Base service (Business logic layer)
    service = AnnouncementService()

    @ns.expect(announcement_model)
    @ns.response(code=HTTPStatus.CREATED, description='Announcement created successfully')
    def post(self):
        """Create new announcement"""

        return lambda_adapter(self.service.create, request)

    @ns.response(code=HTTPStatus.OK, model=[list_announcement_model], description='List of all announcements')
    def get(self):
        """List of all announcements"""

        return lambda_adapter(self.service.list, request)
