from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker

from . import default_settings

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
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

