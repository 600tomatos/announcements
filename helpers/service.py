import json

from types import SimpleNamespace
from six import string_types

from helpers.dynamo_db import DynamoClient


class Service:
    """Base service class for business logic tasks"""

    def __init__(self):
        self._request = None

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, event):
        self._request = self._build_request(event)

    def _build_request(self, event):
        request = SimpleNamespace()
        request.event = event
        try:
            stage = "local" if "localhost" in event["headers"]["Host"] else None
        except KeyError:
            stage = None

        request.stage = stage

        request.db_client = DynamoClient(is_local=bool(stage))
        request.data = self._get_event_body(request.event)
        request.args = request.event.get("queryStringParameters", {})
        request.view_args = request.event.get("pathParameters", {})
        request.path = request.event.get("path", None)
        request.method = request.event.get("httpMethod", None)
        request.headers = request.event.get("headers", {})

        return request

    def _get_event_body(self, event):
        """Extract body from section from event payload

        During testing it was found that different invocation of the lambdas
        caused the body to be sent in differnt formats.  This method handles
        the checking of the format and returns a python dict
        """
        if isinstance(event.get("body", None), string_types):
            try:
                return json.loads(event["body"])
            except json.decoder.JSONDecodeError:
                raise ValueError("Invalid JSON request.data")

        return event.get("body", {})

    @classmethod
    def _apply_decorator_to_methods(cls, decorator):
        """
        This helper can apply a given decorator to all methods on the current
        Resource.
        """

        for method in cls._methods():
            method_name = method.lower()
            decorated_method_func = decorator(getattr(cls, method_name))
            setattr(cls, method_name, decorated_method_func)

    @classmethod
    def _methods(cls):
        """All service methods"""

        return [func for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith('_')]
