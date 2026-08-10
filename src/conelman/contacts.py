from flask import (
    Blueprint, render_template, request, g, redirect, url_for, flash
)
from conelman.auth import login_required
from sqlalchemy import select,update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from . import db
from .models import Contact, User
from werkzeug.exceptions import abort

bp = Blueprint('contacts', __name__)

@bp.route("/")
def index():
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

def get_contact(contact_id):
    database = db.get_db()
    contact = database.session.scalars(select(Contact, User.username).join(User, Contact.user_id == User.id).where(Contact.id == contact_id)).first()

    if contact is None:
        abort(404, f"Contact id {contact_id} doesn't exist.")
    
    if contact.user_id != g.user.id:
        abort(403)

    return contact


@bp.route("/contact/<int:contact_id>/edit", methods = ('GET','POST'))
@login_required
def edit(contact_id):
    contact = get_contact(contact_id)

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        notes = request.form['notes']
        database = db.get_db()

        database.session.merge(Contact(id= contact_id, name = name, phone = phone, notes = notes,user_id = g.user.id))
        database.session.commit()
        return redirect(url_for("contacts.index"))
            
    return render_template('contacts/edit.html', contact = contact)


@bp.route("/contacts/<int:contact_id>/delete")
@login_required
def delete(contact_id):
    database = db.get_db()
    contact = get_contact(contact_id)

    database.session.delete(contact)
    database.session.commit()
    return redirect(url_for('index'))
