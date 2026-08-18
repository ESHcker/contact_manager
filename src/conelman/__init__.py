import os

from flask import Flask
from flask_sqlalchemy_lite import SQLAlchemy
from . import contacts,db,auth


def create_app(test_config=None):
    #Create app and config environment variables
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_ENGINES={"default": "sqlite:///db.sqlite3"},
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    
    #Load the instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_prefixed_env()
    else:
        app.testing = True
        app.config |= test_config

    #Initialize db
    db.init_db(app)
    
    #Add contacts blueprint
    #Add url rule for root page
    app.register_blueprint(contacts.bp)
    app.add_url_rule('/', endpoint='index')

    #Add auth blueprint
    app.register_blueprint(auth.bp)
        
    return app