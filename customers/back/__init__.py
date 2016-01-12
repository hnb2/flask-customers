'''
TODO
'''

from flask import Blueprint
from customers.back import view as AdminCustomerAPI

bp = Blueprint('back', __name__, url_prefix='/admin/customer')

#Routes
bp.add_url_rule(
    '/',
    view_func=AdminCustomerAPI.AdminCustomerList.as_view('get_all')
)

bp.add_url_rule(
    '/<int:customer_id>',
    view_func=AdminCustomerAPI.AdminCustomer.as_view('get')
)

bp.add_url_rule(
    '/',
    view_func=AdminCustomerAPI.AdminCustomer.as_view('all')
)
