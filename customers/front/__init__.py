'''
This modules contains the front end customer blueprint.
'''

from flask import Blueprint
from customers.front import view as CustomerAPI

bp = Blueprint('front', __name__, url_prefix='/customer')

#Routes
bp.add_url_rule(
    '/register',
    view_func=CustomerAPI.Register.as_view('register')
)
bp.add_url_rule(
    '/profile',
    view_func=CustomerAPI.Profile.as_view('profile')
)
bp.add_url_rule(
    '/password',
    view_func=CustomerAPI.ChangePassword.as_view('password')
)
