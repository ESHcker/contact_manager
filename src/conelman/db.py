from flask import current_app
from flask_sqlalchemy_lite import SQLAlchemy
from .models import Base,Contact

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        Base.metadata.create_all(db.engine)

def get_db():
    return db
    

    

