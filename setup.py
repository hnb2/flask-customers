'''
Flask-customers is a set of APIs to handle customers in a neutral way.
It should be used in a micro services design or part of a larger app
and therefore share the database to leverage the use of foreign keys.
It uses basic auth for accessing some parts of the API and bcrypt for
hashing passwords.
'''

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    '''
    Wrapper for pytest launcher
    '''

    user_options = [(
        'pytest-args=',
        'a',
        "Arguments to pass to py.test"
    )]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

#Reading the Pip install requirements
with open('requirements.txt') as file:
    install_requires = file.read()

setup(
    name='flask-customers',
    version='0.1.0',
    #TODO: url='http://',
    license='MIT',
    author='Pierre Guillemot',
    author_email='pierreguillemot@yahoo.fr',
    description='Self contained neutral customer API',
    long_description=__doc__,
    packages=['customers'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    classifiers=[
        ''
    ]
)
