'''
This module contains the error blueprint to handle all the
common HTTP errors.
'''

from flask import Blueprint, jsonify

bp = Blueprint('errors', __name__)

def _generic_error(error, message, code):
    '''
    Generic error handler

    :param error:
        A python error, is None for a normal HTTP error

    :param message:
        A custom error message to return

    :param code:
        The HTTP error code to use
    '''
    response = jsonify(error=message)
    response.status_code = code
    return response

@bp.app_errorhandler(400)
def bad_request(error):
    '''
    Error handler for 400

    :param error:
        A python error, is None for a normal HTTP error
    '''
    return _generic_error(error, 'Bad request', 400)

@bp.app_errorhandler(401)
def unauthorized(error):
    '''
    Error handler for 401

    :param error:
        A python error, is None for a normal HTTP error
    '''
    return _generic_error(
        error,
        'Please login with proper credentials',
        401
    )

@bp.app_errorhandler(404)
def page_not_found(error):
    '''
    Error handler for 404

    :param error:
        A python error, is None for a normal HTTP error
    '''
    return _generic_error(error, 'Page not found', 404)

