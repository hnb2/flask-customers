'''
Contains the CustomerService class
'''

from customers.utils import db
from customers.common.models.customer import Customer

class CustomerService(object):
    '''
    Wrapper for accessing the customer tables. The point of this
    class is to separate the DB logic in order to have clean import
    statements and unit testable components. Plus it makes sure that
    the session is closed at the end (commit/rollback).
    '''

    RESULTS_PER_PAGE = 5

    @staticmethod
    def add_customer(customer):
        '''
        Add a new customer

        :param customer:
            A new Customer instance
        '''
        db.session.add(customer)
        db.session.commit()

    @staticmethod
    def update_customer(customer):
        '''
        Update an existing customer

        :param customer:
            An existing Customer instance
        '''
        db.session.merge(customer)
        db.session.commit()

    @staticmethod
    def get_customer_by_email(email):
        '''
        Return a customer by its email address

        :param email:
            A customer's email address
        '''
        return db.session.query(Customer).filter(
            Customer.email == email,
        ).first()

    @staticmethod
    def get_customer_by_id(customer_id):
        '''
        Return a customer by its id

        :param customer_id:
            A customer's id
        '''
        return db.session.query(Customer).filter(
            Customer.id == customer_id,
        ).first()

    @staticmethod
    def get_customers(start=0, stop=20):
        '''
        Return a list of customers

        :param start:
            Beginning index (0 based)

        :param stop:
            End index

        Example on how to retrieve the 5 first results ::

            CustomerService.get_customers(0, 5)

        Example on how to retrieve the second range of 5 results ::

            CustomerService.get_customers(5, 10)
        '''
        return db.session.query(Customer).slice(start, stop)

    @staticmethod
    def get_count_customers():
        '''
        Returns the total number of customers
        '''
        return db.session.query(Customer.id).count()

    @staticmethod
    def delete_customer_by_id(customer_id):
        customer = CustomerService.get_customer_by_id(customer_id)

        if customer is not None:
            db.session.delete(customer)
            db.session.commit()
            return True

        return False
