import os

from flask_restx import Api

from resources.auth.resource import ns as auth_ns
from resources.announcements.resource import ns as announcement_ns
from models.models import announcement_model, list_announcement_model, auth_model

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


def upgrade_app(app):
    api = Api(app,
              title='Announcemts API',
              version='1.0',
              description=f'API specification for {os.environ.get("STAGE", "local")} environment',
              authorizations=authorizations,
              security='apikey',
              doc='/'
              )

    # Declare serialization/deserialization models
    api.models[announcement_model.name] = announcement_model
    api.models[list_announcement_model.name] = list_announcement_model
    api.models[auth_model.name] = auth_model

    # Add namespaces
    api.add_namespace(auth_ns)
    api.add_namespace(announcement_ns)
