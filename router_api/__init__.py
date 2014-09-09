from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import default_settings
from . import models

# Setup the app
app = Flask(__name__.split('.')[0], instance_relative_config=True)
app.config.from_object(default_settings)
app.config.from_pyfile('settings.py')

# Setup the db connection
db_engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'], 
    convert_unicode=True
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
)

# Set up the api
# TEMP: Don't really wanna use flask restless (just for quick and dirty testing)
from flask.ext.restless import APIManager
manager = APIManager(app, session=db_session)

# Create API endpoints, which will be available at /api/<tablename> by default.
manager.create_api(models.Account, methods=['GET', 'POST', 'DELETE'])
manager.create_api(models.User, methods=['GET', 'POST', 'DELETE'])
manager.create_api(models.Network, methods=['GET', 'POST', 'DELETE'])
manager.create_api(models.Screen, methods=['GET', 'POST', 'DELETE'])
manager.create_api(models.App, methods=['GET', 'POST', 'DELETE'])
manager.create_api(models.AppInstance, methods=['GET', 'POST', 'DELETE'])
