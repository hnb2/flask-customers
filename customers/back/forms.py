'''
Collection of forms for the back end customer API
'''

from flask.ext.wtf import Form
from wtforms import(
    StringField,
    BooleanField,
    IntegerField,
    ValidationError
)
from wtforms.validators import DataRequired, Email
from customers.common.services import CustomerService

class CustomerForm(Form):
    '''
    Basic form representing a Customer
    '''
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    cellphone = StringField('cellphone')
    newsletter = BooleanField('newsletter')

class CreateCustomerForm(CustomerForm):
    '''
    Form for the creation of a customer, has additionnal field.
    '''
    email = StringField('email', validators=[Email()])

    def validate_email(self, field):
        '''
        Custom validator for the email, make sure that it is not
        already used.

        :param field:
            Field object, the email string is in field.data
        '''
        customer = CustomerService.get_customer_by_email(field.data)

        if customer is not None:
            raise ValidationError(
                'Email address already taken.'
            )

class CustomerListForm(Form):
    '''
    Form for the view rendering a customer list.
    '''
    page = IntegerField('page')

    def validate_page(self, field):
        '''
        Make sure that the page number is a positive number

        :param field:
            Field object, the email string is in field.data
        '''
        if field.data < 0:
            raise ValidationError(
                'Page number has to be positive.'
            )
