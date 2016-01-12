'''
This module contains the login utilities, which is not a blueprint.
Part of it from: http://flask.pocoo.org/snippets/8/
'''

from functools import wraps
from flask import request, g, abort
from customers.common.services import CustomerService

def check_auth(username, password):
    '''
    This function is called to check if a username /
    password combination is valid.

    :param username:
        The email address used in the basic auth field

    :param password:
        The password used in the basic auth field
    '''
    customer = CustomerService.get_customer_by_email(username)

    if customer is not None:
        if customer.check_password(password):
            g.customer = customer
            return True

    return False

def requires_auth(func):
    '''
    Decorator to use for any view which requires an authenticated
    customer.
    Example::

        @requires_auth
        def view_my_profile(self):
            return g.customer.data

    :param func:
        The function to call
    '''

    @wraps(func)
    def decorated(*args, **kwargs):
        '''
        The inner decorator
        '''
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            abort(401)
        return func(*args, **kwargs)

    return decorated
