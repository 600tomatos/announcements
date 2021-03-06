from flask_restx import marshal
from flask_restx._http import HTTPStatus

from lambdas.helpers.service import Service
from lambdas.validators.announcement_validator import AnnouncementValidator

from lambdas.helpers.response import (
    build_response,
    make_error_response
)
from lambdas.helpers.decorators import inject_decorators, token_required
from lambdas.models.models import list_announcement_model


@inject_decorators(decorators=[token_required])
class AnnouncementService(Service):

    def create(self):
        """Create new announcement"""

        db_client = self.request.db_client
        title = self.request.data.get('title')
        description = self.request.data.get('description')

        # Validate request values
        error = AnnouncementValidator.check(dict(title=title, description=description))
        if error:
            return make_error_response(error)

        response = db_client.save_announcement(title, description)
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if status_code != HTTPStatus.OK:
            return make_error_response('Unable to save announcement')

        return build_response('ok', HTTPStatus.CREATED)

    def list(self):
        """Get list of all announcements"""

        db_client = self.request.db_client
        response = db_client.get_all_announcements()
        return build_response(marshal(response['Items'], list_announcement_model))
