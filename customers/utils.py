'''
This is a little trick to avoid circular imports by initializing
some flask extensions which usually take the app object in their
constructor. But this time, the app object will be passed once they
have been initialized here.
'''

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

#Database
db = SQLAlchemy()

#Bcrypt encryption
bcrypt = Bcrypt()
