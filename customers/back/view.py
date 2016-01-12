'''
Contains the classes for manipulating customers on the backend side.
'''

import string
import random
from math import ceil
from flask import jsonify, request
from flask.views import MethodView
from customers.common.services import CustomerService
from customers.common.models.customer import Customer
from customers.back.forms import(
    CustomerForm,
    CreateCustomerForm,
    CustomerListForm
)

class AdminCustomer(MethodView):
    '''
    View for CRUD actions on the customers from the backend.
    '''

    @staticmethod
    def _generate_password(
        size=8,
        chars=string.ascii_uppercase + string.digits
    ):
        '''
        Generates a random string, can be used as a password.

        :param size:
            The length of the random string.

        :param chars:
            The set of strings to use, defaults are: the uppercase
            characters and the digits.

        Returns a random string.
        '''
        return ''.join(random.choice(chars) for _ in range(size))

    def get(self, customer_id):
        '''
        Returns one customer

        :param customer_id:
            The ID of the customer to retrieve.
        '''
        customer = CustomerService.get_customer_by_id(customer_id)

        if customer is None:
            return jsonify(
                msg="Could not find customer"
            )

        return jsonify(
            customer=customer.json
        )

    def post(self):
        '''
        Create a new customer

        Returns a json representation of a customer.
        '''
        form = CreateCustomerForm.from_json(request.get_json())

        if not form.validate_on_submit():
            return jsonify(errors=form.errors)

        customer = Customer(
            email=form.email.data,
            password=AdminCustomer._generate_password()
        )
        customer.data.cellphone = form.cellphone.data
        customer.data.first_name = form.first_name.data
        customer.data.last_name = form.last_name.data
        customer.data.newsletter = form.newsletter.data

        CustomerService.add_customer(customer)

        return jsonify(customer=customer.json)

    def put(self, customer_id):
        '''
        Update an existing customer.
        It is not possible to update the email address or the
        password using this service.

        TODO: Use patch when wtf-forms will be ready

        :param customer_id:
            The id of the customer to update

        Returns a json representation of a customer.
        '''
        form = CustomerForm.from_json(request.get_json())

        if not form.validate_on_submit():
            return jsonify(errors=form.errors)

        customer = CustomerService.get_customer_by_id(customer_id)

        if customer is None:
            return jsonify(msg="Could not find customer")

        customer.data.cellphone = form.cellphone.data
        customer.data.first_name = form.first_name.data
        customer.data.last_name = form.last_name.data
        customer.data.newsletter = form.newsletter.data

        CustomerService.update_customer(customer)

        return jsonify(customer=customer.json)

    def delete(self, customer_id):
        '''
        Delete a customer by its ID.

        :param customer_id:
            The id of the customer to delete

        Returns True if the customer has been found and deleted.
        '''
        result = CustomerService.delete_customer_by_id(customer_id)

        return jsonify(
            result=result
        )

class AdminCustomerList(MethodView):
    '''
    View for rendering a list of customers.
    '''

    def get(self):
        '''
        Support pagination style: 'page' json parameter.

        Returns a list of customers and pagination data.
        '''
        form = CustomerListForm.from_json(request.get_json())

        if not form.validate():
            return jsonify(errors=form.errors)

        page = form.page.data

        total = CustomerService.get_count_customers()
        total_pages = ceil(total / CustomerService.RESULTS_PER_PAGE)
        start = page * CustomerService.RESULTS_PER_PAGE
        stop = start + CustomerService.RESULTS_PER_PAGE

        raw_customers = CustomerService.get_customers(
            start=start,
            stop=stop
        )

        return jsonify(
            current_page=page,
            total_pages=int(total_pages),
            customers=[customer.json for customer in raw_customers]
        )
