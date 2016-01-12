# Customers API

## Install the project

Manage and load the virtualenv ;

 * `virtualenv env --no-site-package`
 * `source env/bin/activate`

Install the dependencies : `python setup.py develop`

## Deploy the project

### Database

Create/Update the database (Default on Postgresql):

 * `CREATE USER dev WITH PASSWORD 'dev';`
 * `CREATE DATABASE customers_dev owner dev;`
 * `python manage.py db upgrade`

If you make changes to the models, you have to generate a migration
script using: `python manage.py db migrate`.
Review the script manually, in case some elements are missing.
Don't forget to upgrade the database after the migration.

If you need to go back to a different database version:
`python manage.py db downgrade`

Display your current version: `python manage.py db current`

### Application

Launch the application: `python manage.py runserver`

#### Production mode using gunicorn + nginx + supervisord:

 * Make sure you changed the default `SECRET_KEY` in conf/config.cfg
 * `CUSTOMERS_PROD_CONFIG=/<ABSOLUTE_PATH>/conf/config_prod.cfg`
 * `export CUSTOMERS_PROD_CONFIG`
 * Copy the conf/nginx.conf file in sites-available (update the path)
 * Then make a ln in sites-enabled
 * Restart nginx: `sudo /etc/init.d/nginx restart`
 * Copy the supervisord file (update the path in the file)
 * `sudo supervisorctl -c /supervisord/supervisord.conf`
 * `reread`
 * `update`
 * `restart flask_customers`
 * `quit`

Go back to the development mode: `unset CUSTOMERS_PROD_CONFIG`

### Testing

Create/Update the test database (Default on Postgresql):

 * `CREATE DATABASE customers_test owner dev;`

Run: `python setup.py test -a "tests"`

Or if you installed pytest-cov, you can generate a coverage report by
running: `python setup.py test -a "--cov customers tests/"`

Want to make it look fancier ? I don't see why not:
`python setup.py test -a "--cov-report html --cov customers tests/"`

### Distribute the project

 * Create a source distribution: `python setup.py sdist`
 * Create a binary distribution: `python setup.py bdist`
 * Install in development mode: `pyton setup.py develop`
 * Install in production mode: `python setup.py install`


### Generate documentation

Sphinx is installed as a requirement. You can run the following
at the root of the project to generate the source doc:

`sphinx-apidoc -o docs/source customers`

Then build the documentation in the HTML format:

`cd docs && make html`

For more option, checkout the help option of the Makefile.

For a quicker use, run `generate_doc.sh`

## API Usage

Please go through the docs/source/api.rst (or its generated format)
for more details about the API and some CURL examples.

## Notes

CSRF protection is not necessary in a stateless API not
relying on sessions or cookies. Source :
http://stackoverflow.com/questions/21357182/csrf-token-necessary-when-using-stateless-sessionless-authentication

Install Pylint with pip from your virtualenv in order to have it know
the libraries installed through pip (and get rid of VIM errors) :
`pip install -i http://pypi.python.org/simple pylint`

## TODO

 * Refactor tests position ? And unit test the http errors supported
 * Checkout how to use requirements-dev.txt or requirements-test.txt (http://docs.openstack.org/developer/keystone/setup.html)
 * Investigate design for admin side of API (authorization, blueprint)
 * Implement 'active' logic in login.py (?)
 * Checkout CI (tox, gogs+buildbot => github+travis)
 * Checkout openshift free plan
 * Checkout fabric
 * Checkout celery+rabbitmq and design for email service
 * Implement import customer from other CMS/CRM...
 * Use a new table `extra` and `customer_extra` to store id|key|type and customer_id|key_id|value
