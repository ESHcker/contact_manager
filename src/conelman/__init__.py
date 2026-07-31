import os

from flask import Flask
from . import contacts


def create_app(test_config=None):
    app = Flask(__name__)
    #Add contacts blueprint
    #Add url rule for root page
    app.register_blueprint(contacts.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app