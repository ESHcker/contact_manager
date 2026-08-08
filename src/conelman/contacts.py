from flask import (
    Blueprint, render_template, request, g, redirect, url_for, flash
)
from conelman.auth import login_required
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from . import db
from .models import Contact

bp = Blueprint('contacts', __name__)

@bp.route("/")
def index():
    #ADD logic when user is logged
    database = db.get_db()
    contacts = None

    if g.user: 
        contacts = database.session.scalars(select(Contact).where(Contact.user_id == g.user.id))
    return render_template('contacts/index.html', contacts = contacts)

@bp.route("/contacts/add", methods=('POST', 'GET'))
@login_required
def add():
    if request.method == "POST":
        name =  request.form["name"]
        phone = request.form["phone"]
        notes = request.form["notes"]
        database = db.get_db()

        try:
            database.session.add(Contact(name = name, phone = phone, notes = notes, user_id = g.user.id))
            database.session.commit()
        except IntegrityError:
            flash(f"The number is already registered.")
        else:
            return redirect(url_for('contacts.index'))

    return render_template('contacts/add.html')