from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from . import db
from .models import User
from sqlalchemy.exc import IntegrityError

bp = Blueprint('auth', __name__ , url_prefix='/auth')

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        database = db.get_db()
        error = None
        try:   
            #ADD hash for password later
            database.session.add(User(username = username, password = password))
            database.session.commit()
        except IntegrityError:
            error = f"Username {username} is already registered"
        else:
            return redirect(url_for("contacts.index"))
        
        flash(error)

    return render_template('auth/register.html')
