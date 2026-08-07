from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g 
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from . import db
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__ , url_prefix='/auth')

@bp.route("/register", methods=("GET", "POST"))
def register():
    #When send form, add new user and redirect to login is sucessful
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        database = db.get_db()
        error = None
        
        try:   
            #ADD hash for password later
            database.session.add(User(username = username, password = generate_password_hash(password)))
            database.session.commit()
        except IntegrityError:
            error = f"Username {username} is already registered"
        else:
            return redirect(url_for("auth.login"))
        
        flash(error)
    #When arent sending form, visualize form
    return render_template('auth/register.html')

@bp.route("/login", methods = ("GET","POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        database = db.get_db()
        user_registered = database.session.scalar(select(User).where(User.username == username))

        if user_registered == None or not check_password_hash(user_registered.password, password):
            flash(f"This user or password are incorrect. Try again")
        elif check_password_hash(user_registered.password, password):
            session.clear()
            session['user_id'] = user_registered.id
            return redirect(url_for("contacts.index"))
        
    return render_template('auth/login.html')

@bp.before_app_request
def load_login_user():
    user_id = session.get('user_id')

    if user_id == None:
        g.user = None
    else:
        database = db.get_db()
        g.user = database.session.scalar(select(User).where(User.id == user_id))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('contacts.index'))