from flask import (
    Blueprint, render_template
)

bp = Blueprint('contacts', __name__)

@bp.route("/")
def index():
    return render_template('contacts/index.html')