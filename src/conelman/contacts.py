from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('contacts', __name__)

@bp.route("/")
def index():
    return render_template('contacts/index.html')

@bp.route("/contacts/add", methods=('POST', 'GET'))
def add_contact():
    return render_template('contacts/add.html')