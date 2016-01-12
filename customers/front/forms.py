'''
Collection of forms for the customer API
'''

from flask import g
from flask_wtf import Form
from wtforms import StringField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from customers.common.services import CustomerService

class RegistrationForm(Form):
    '''
    Validators for the registration form
    '''
    email = StringField('email', validators=[Email()])
    password = StringField('password', validators=[DataRequired()])

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

class ProfileForm(Form):
    '''
    Validators for the profile form
    '''
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    cellphone = StringField('cellphone')
    newsletter = BooleanField('newsletter')

class PasswordForm(Form):
    '''
    Validators for the change password form
    '''
    old_password = StringField('old_password', [DataRequired()])
    password = StringField(
        'new_password',
        [DataRequired(), EqualTo('confirm')]
    )
    confirm = StringField('confirm', [DataRequired()])

    def validate_old_password(self, field):
        '''
        Custom validator to check that the old password matches
        the current one as a security feature.

        :param field:
            Field object, the password string is in field.data
        '''
        if not g.customer.check_password(field.data):
            raise ValidationError(
                "The old password is not matching."
            )
