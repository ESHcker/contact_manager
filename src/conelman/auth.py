from flask import (
    Blueprint, render_template, request
)

from . import db

bp = Blueprint('auth', __name__ , url_prefix='/auth')

@bp.route("/auth/register", methods=("GET", "POST"))
def register():
    return render_template('auth/register.html')
