API Definition
==============

Register
--------

Create a new customer. He will be disabled by default, and will not be
able to login and therfore do actions which requires to be
authenticated until he activates its account.

Route : /customer/register

Method : POST

CURL example ::

    curl --data '{"email": "test@test.org", "password": "test"}' http://127.0.0.1:5000/customer/register -H "Content-type: application/json"

Input
~~~~~

::

    {
        email : [string: customer's email],
        password : [string: customer's password]
    }

Output
~~~~~~

Success ::

    {
        customer_id: [int: id of the newly created customer]
    }

Failure ::

    {
        errors: {
            <field_name>: [
                "<error_message>,
                ..."
            ],
            ...
        }
    }

Get profile
-----------

Return the profile of the currently logged in customer.

**REQUIRES AUTHENTICATED CUSTOMER**

Route : /customer/profile

Method : GET

CURL example ::

    curl --user test@test.org:test http://127.0.0.1:5000/customer/profile

Input
~~~~~

no input

Output
~~~~~~

Success ::

    {
        id: [int: customer's id],
        email: [string: customer's email],
        data: {
            first_name: [string: customer's first name],
            last_name: [string: customer's last name],
            cellphone: [string: customer's cellphone number]
        }
    }

Failure ::

    {
        errors: {
            <field_name>: [
                "<error_message>,
                ..."
            ],
            ...
        }
    }

Update profile
--------------

Update the profile of the currently logged in customer.

**REQUIRES AUTHENTICATED CUSTOMER**

Route : /customers/profile

Method : PUT

CURL example ::

    curl -X PUT --user test@test.org:test --data '{"cellphone": 123456789}' http://127.0.0.1:5000/customer/profile -H "Content-type: application/json"

Input
~~~~~

::

    {
        first_name: [string: customer's first name],
        last_name: [string: customer's last name],
        cellphone: [string: customer's cellphone number],
        newsletter: [string: is the customer suscribing to the newsletter]
    }

Output
~~~~~~

Success ::

    {
        id: [int: customer's id],
        email: [string: customer's email],
        data: {
            first_name: [string: customer's first name],
            last_name: [string: customer's last name],
            cellphone: [string: customer's cellphone number]
        }
    }

Failure ::

    {
        errors: [string: error message]
            <field_name>: [
                "<error_message>,
                ..."
            ],
            ...
        }
    }

Change password
---------------

Update the password of the currently logged in customer.

**REQUIRES AUTHENTICATED CUSTOMER**

Route : /customers/password

Method : PATCH

CURL example ::

    curl -X PATCH --user test@test.org:test --data '{"old_password": "test", "password": "test2", "confirm": "test2"}' http://127.0.0.1:5000/customer/password -H "Content-type: application/json"

Input
~~~~~

::

    {
        old_password: [string: customer's current password],
        password: [string: customer's new password],
        confirm: [string: same as 'password' to make sure there were no mistakes]
    }

Output
~~~~~~

Success ::

    {
        msg: "OK"
    }

Failure ::

    {
        errors: {
            <field_name>: [
                "<error_message>,
                ..."
            ],
            ...
        }
    }
