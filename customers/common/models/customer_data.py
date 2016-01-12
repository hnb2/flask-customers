'''
Contains the CustomerData class
'''

from datetime import datetime
from customers.utils import db

class CustomerData(db.Model):
    '''
    Holds information about a customer. It could have been possible
    to keep all those columns in the customer table, but it was
    decided to split the table in two in order to
    increase the SQL performances during queries.
    '''

    __tablename__ = 'customer_data'

    #I dont like the idea of a separate PK for this
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    cellphone = db.Column(db.String)
    newsletter = db.Column(db.Boolean)
    created = db.Column(db.DateTime)

    def __init__(
        self,
        first_name='',
        last_name='',
        cellphone='',
        newsletter=False
    ):
        '''
        Constructor for the CustomerData class. It will use the
        current time for the created field, which cannot be passed
        as a parameter.

        :param first_name:
            The first name of the customer

        :param last_name:
            The last name of the customer

        :param cellphone:
            The cellphone number of the customer

        :newsletter:
            Boolean identifying whereas the customer subscribed to
            the newsletter or not.
        '''
        self.first_name = first_name
        self.last_name = last_name
        self.cellphone = cellphone
        self.newsletter = newsletter
        self.created = datetime.now()

    @property
    def json(self):
        '''
        Return a json representation of customer data
        '''
        return dict(
            first_name=self.first_name,
            last_name=self.last_name,
            cellphone=self.cellphone,
            newsletter=self.newsletter,
            created=self.created.strftime('%Y/%m/%d')
        )
