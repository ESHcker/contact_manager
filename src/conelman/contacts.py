from flask import (
    Blueprint, render_template, request
)
from sqlalchemy import select
from . import db
from .models import Contact

bp = Blueprint('contacts', __name__)

@bp.route("/")
def index():
    #ADD logic when user is logged
    database = db.get_db()
    contacts = database.session.scalars(select(Contact))
    return render_template('contacts/index.html', contacts = contacts)

@bp.route("/contacts/add", methods=('POST', 'GET'))
def add_contact():
    return render_template('contacts/add.html')