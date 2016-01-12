'''
Initialize the application, please refer to the README.md file on how
to launch it.
'''

from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import wtforms_json
from customers.utils import db, bcrypt
from customers.errors import bp as errors_module
from customers.front import bp as front_module
from customers.back import bp as back_module

app = Flask(__name__)
app.config.from_pyfile('../conf/config.cfg')
app.config.from_envvar('CUSTOMERS_PROD_CONFIG', silent=True)

#Database
db.app = app
db.init_app(app)

#Migration
migrate = Migrate(app, db)

#Flask script manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#Bcrypt
bcrypt.init_app(app)

#WTForm json extension
wtforms_json.init()

#Register the blueprints
app.register_blueprint(errors_module)
app.register_blueprint(front_module)
app.register_blueprint(back_module)
