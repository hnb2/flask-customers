'''
Customer API
'''

from flask import jsonify, request, g
from flask.views import MethodView
from customers.common.models.customer import Customer
from customers.common.services import CustomerService
from customers.login import requires_auth
from customers.front.forms import (
    RegistrationForm,
    ProfileForm,
    PasswordForm
)

class Register(MethodView):
    '''
    Register a new customer
    '''

    def post(self):
        '''
        Create a new customer.

        Returns its ID.
        '''
        form = RegistrationForm.from_json(request.get_json())

        if not form.validate_on_submit():
            return jsonify(errors=form.errors)

        customer = Customer(
            email=form.email.data,
            password=form.password.data
        )

        CustomerService.add_customer(customer)

        return jsonify(id=customer.id)

class Profile(MethodView):
    '''
    Manage the customer's profile
    '''

    @requires_auth
    def get(self):
        '''
        Returns the Customer profile
        '''
        return jsonify(customer=g.customer.json)

    @requires_auth
    def put(self):
        '''
        Update the Customer profile

        TODO: when this get merged and available on pypi :
        https://github.com/wtforms/wtforms/pull/147/files

        Sample::

            form.populate_obj(g.customer.data, partial=False)

        Also, consider::

            form.patch_data

        Returns the Customer profile
        '''
        form = ProfileForm.from_json(request.get_json())

        if not form.validate_on_submit():
            return jsonify(errors=form.errors)

        form.populate_obj(g.customer.data)

        CustomerService.update_customer(g.customer)

        return jsonify(customer=g.customer.json)


class ChangePassword(MethodView):
    '''
    Change the customer's password
    '''

    @requires_auth
    def patch(self):
        '''
        Change the password of a customer, requires the old password.

        Returns a success message.
        '''
        form = PasswordForm.from_json(request.get_json())

        #Here we are not using form.validate_on_submit because it
        # will only work for PUT and POST request methods.
        if not form.validate() or not request.method == "PATCH":
            return jsonify(errors=form.errors)

        g.customer.set_password(form.password.data)

        CustomerService.update_customer(g.customer)

        return jsonify(msg="OK")
