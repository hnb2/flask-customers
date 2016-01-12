'''
Contains the Customer class
'''

from sqlalchemy.orm import relationship
from customers.utils import db, bcrypt
from customers.common.models.customer_data import CustomerData

class Customer(db.Model):
    '''
    A customer represents a set of email/bcrypt hashed password,
    required to access authorized parts of the application.
    It has a 1-1 relationship with CustomerData which holds more
    information.
    '''

    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    active = db.Column(db.Boolean)
    data = relationship('CustomerData', uselist=False, backref='customer')

    def __init__(self, email='', password=''):
        '''
        Constructor for the Customer class, it will initialize a
        customer with an email and a CLEAR password, which will be
        encrypted. This customer will be disabled by default, and
        its data will be initialized empty.

        :param email:
            The email address of the customer

        :param password:
            Clear password of the customer
        '''
        self.email = email
        self.set_password(password)
        self.active = False
        self.data = CustomerData()

    def set_password(self, password):
        '''
        Hash a password using bcrypt

        :param password:
            Clear password to set
        '''
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        '''
        Generate a hash for the given password

        :param password:
            Clear password

        Returns a hashed password
        '''
        return bcrypt.generate_password_hash(password)

    def check_password(self, other_password):
        '''
        Check the current customer's password against another one

        :param other_password:
            Clear password

        Returns true if the password matches, false otherwise
        '''
        return bcrypt.check_password_hash(
            self.password,
            other_password
        )

    @property
    def json(self):
        '''
        Return a json representation of a customer
        '''
        return dict(
            id=self.id,
            email=self.email,
            data=self.data.json
        )
