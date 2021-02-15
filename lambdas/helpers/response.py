import json
import pytz
from datetime import date, datetime
import decimal

from flask import make_response
from flask_restx._http import HTTPStatus


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return pytz.utc.localize(obj).isoformat()

    if isinstance(obj, decimal.Decimal):
        return float(obj)

    raise TypeError(f"Type { type(obj)} not serializable")


def build_response(body, status_code=HTTPStatus.OK):
    """Construct Response headers around body payload"""
    apig_response = {
        "statusCode": str(status_code),
        "body": json.dumps(body, default=json_serial),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        },
    }
    return apig_response


def make_error_response(errorstring, status_code=HTTPStatus.BAD_REQUEST):
    """ Construct error structure around an error string """
    resp = {"error": errorstring}
    return build_response(resp, status_code)


def flask_lambda_adapter(func, request):
    """
    To not couple our micro framework with Flask, we make it just
    accept the normal request send by serverless. Here we just transform
    it into an event concept normal to serverless endpoints.
    """
    service = func.__self__
    if not service:
        raise ValueError('No underlying service defined for this resource')

    event = {
        "httpMethod": request.method,
        "headers": request.headers,
        "queryStringParameters": request.args,
        "pathParameters": request.view_args,
        "body": request.data.decode() or "{}",
        "path": request.path,
    }
    # Set base request
    service.request = event

    lambda_response = func()
    response = make_response(
        lambda_response["body"], lambda_response["statusCode"]
    )

    return response
