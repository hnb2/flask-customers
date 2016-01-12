'''
To run these tests you need to create a test database, instructions
are inside the README.md
'''

import customers
from customers.utils import db
import unittest
import json
import base64

class CustomersTestCase(unittest.TestCase):
    '''
    Test the customers application
    '''

    EMAIL = 'test@test.org'
    PASSWORD = 'test'

    def setUp(self):
        '''
        Create a test app and init the database
        '''
        customers.app.config.from_pyfile('../conf/config_test.cfg')
        self.app = customers.app.test_client()
        db.create_all()

        #Create a customer
        self._create_dummy_customer()

    def tearDown(self):
        '''
        Drop the database
        '''
        db.session.close()
        db.drop_all()

    def _open(self, url, method, headers=None, data=None):
        '''
        Wrapper to make a request using the dummy values for
        basic auth
        '''
        #This will raise a 40x if the content type is set and yet
        # there is no data to send
        content_type = "application/json"
        if data is None:
            content_type = None

        return self.app.open(
            path='/customer/%s' % url,
            method=method,
            data=data,
            headers=headers,
            content_type=content_type
        )

    def _open_with_auth(
        self,
        url,
        method,
        username,
        password,
        data=None
    ):
        '''
        Wrapper to make a request using Basic auth
        '''
        return self._open(
            url,
            method,
            data=data,
            headers={
                'Authorization': 'Basic ' +\
                base64.b64encode(
                    username + ":" + password
                )
            }
        )

    def _open_with_dummy_auth(self, url, method, data=None):
        '''
        Wrapper to make a request using the dummy values for
        basic auth
        '''
        return self._open_with_auth(
            url,
            method,
            self.EMAIL,
            self.PASSWORD,
            data=data
        )

    def _create_dummy_customer(self):
        '''
        Create a dummy customer
        '''
        data = dict(email=self.EMAIL, password=self.PASSWORD)
        resp = self._open(
            'register',
            'POST',
            data=json.dumps(data),
        )
        json_data = json.loads(resp.get_data())
        self.assertEqual(json_data.get('id'), 1)

    def test_register(self):
        '''
        Test the register command
        '''
        #Without parameters => failure
        resp = self._open('register', 'POST')
        json_data = json.loads(resp.get_data())

        self.assertIsNotNone(json_data.get('errors'))
        self.assertIsNotNone(json_data['errors'].get('email'))
        self.assertIsNotNone(json_data['errors'].get('password'))

        #Missing parameters => failure
        data = dict(password="test")
        resp = self._open(
            'register',
            'POST',
            data=json.dumps(data),
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNotNone(json_data.get('errors'))
        self.assertIsNotNone(json_data['errors'].get('email'))

        #Email format invalid => failure
        data = dict(email="test@", password="test")
        resp = self._open(
            'register',
            'POST',
            data=json.dumps(data),
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNotNone(json_data.get('errors'))
        self.assertIsNotNone(json_data['errors'].get('email'))

        #Correct parameters => success
        data = dict(email='test2@test.org', password='test2')
        resp = self._open(
            'register',
            'POST',
            data=json.dumps(data),
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNone(json_data.get('errors'))
        self.assertIsNotNone(json_data.get('id'))

        #Same request (same email address) => failure
        resp = self._open(
            'register',
            'POST',
            data=json.dumps(data),
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNotNone(json_data.get('errors'))
        self.assertIsNotNone(json_data['errors'].get('email'))

    def test_get_profile(self):
        '''
        Test that we can retrieve the profile of the current customer
        '''
        #Without credentials => failure
        resp = self._open_with_auth(
            'profile',
            'GET',
            '',
            ''
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNotNone(json_data.get('error'))

        #With credentials => success
        resp = self._open_with_dummy_auth(
            'profile',
            'GET'
        )
        json_data = json.loads(resp.get_data())
        customer = json_data.get('customer')
        customer_data = customer.get('data')

        self.assertIsNone(json_data.get('error'))
        self.assertIsNotNone(customer)
        self.assertIsNotNone(customer.get('email'))
        self.assertIsNotNone(customer.get('id'))
        self.assertIsNotNone(customer.get('data'))
        self.assertIsNotNone(customer_data.get('cellphone'))
        self.assertIsNotNone(customer_data.get('first_name'))
        self.assertIsNotNone(customer_data.get('last_name'))
        self.assertIsNotNone(customer_data.get('newsletter'))
        self.assertIsNotNone(customer_data.get('created'))

    def test_put_profile(self):
        '''
        Test if we can update the profile of the current customer
        '''
        #With credentials => success
        data = dict(cellphone=123456789)
        resp = self._open_with_dummy_auth(
            'profile',
            'PUT',
            data=json.dumps(data)
        )
        json_data = json.loads(resp.get_data())
        customer = json_data.get('customer')
        customer_data = customer.get('data')

        self.assertIsNone(json_data.get('error'))
        self.assertIsNotNone(customer)
        self.assertIsNotNone(customer.get('email'))
        self.assertIsNotNone(customer.get('id'))
        self.assertIsNotNone(customer.get('data'))
        self.assertEqual(customer_data.get('cellphone'), '123456789')
        self.assertIsNotNone(customer_data.get('first_name'))
        self.assertIsNotNone(customer_data.get('last_name'))
        self.assertIsNotNone(customer_data.get('newsletter'))
        self.assertIsNotNone(customer_data.get('created'))

    def test_password(self):
        '''
        Test if we can change the password of the current customer
        '''
        #No data => failure
        resp = self._open_with_dummy_auth(
            'password',
            'PATCH'
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNotNone(json_data.get('errors'))

        #Old password is not correct => failure
        data = dict(old_password='test2', password='test', confirm='test')
        resp = self._open_with_dummy_auth(
            'password',
            'PATCH',
            data=json.dumps(data)
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNotNone(json_data.get('errors'))

        #new password and confirm do not match => failure
        data = dict(old_password='test', password='test2', confirm='test')
        resp = self._open_with_dummy_auth(
            'password',
            'PATCH',
            data=json.dumps(data)
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNotNone(json_data.get('errors'))

        #old_password password match and new+confirm match => success
        data = dict(old_password='test', password='test2', confirm='test2')
        resp = self._open_with_dummy_auth(
            'password',
            'PATCH',
            data=json.dumps(data)
        )
        json_data = json.loads(resp.get_data())

        self.assertIsNone(json_data.get('errors'))

if __name__ == '__main__':
    unittest.main()
