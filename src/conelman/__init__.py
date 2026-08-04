from flask import Flask
from flask_sqlalchemy_lite import SQLAlchemy
from . import contacts
from .db import Base


def create_app(test_config=None):
    #Create app and put engine of sqlalchemy
    app = Flask(__name__)
    app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///db.sqlite3"}

    #Initialize db and create tables
    db =SQLAlchemy()
    db.init_app(app)
    with app.app_context():
        Base.metadata.create_all(db.engine)

    #Add contacts blueprint
    #Add url rule for root page
    app.register_blueprint(contacts.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app