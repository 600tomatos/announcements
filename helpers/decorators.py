from flask_restx._http import HTTPStatus

from helpers.response import make_error_response
from helpers.utils.token import decode_auth_token

def inject_decorators(decorators):
    """
    This decorator can be applied only to service class definition
    Applying this decorator means applying this decorator to all methods of the given class.
    Method execution begins inside the func_exec_context function
    """

    def decorator(func_or_class):
        if isinstance(func_or_class, type):
            # Wrap all method of provided service to this decorator
            func_or_class._apply_decorator_to_methods(decorator)
            return func_or_class

        def func_exec_context(service):

            request = service.request
            for decorator in decorators:
                error_response = decorator(request)
                if error_response:
                    return error_response

            func = func_or_class
            return func(service)

        return func_exec_context

    return decorator


def token_required(request):
    """Check Authorization key in header"""

    authorization = request.headers.get('Authorization', '')
    token = authorization.replace('Bearer', '').strip()

    # Try to decode jwt token
    if not decode_auth_token(token):
        return make_error_response('Invalid token', HTTPStatus.FORBIDDEN)
