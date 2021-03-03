from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User, Word

bp = Blueprint('profile', __name__)


@bp.route('/')
@login_required
def dashboard():
    words = current_user.words
    return render_template('index.html', words=words)


@bp.route('/account')
def account():
    return 'Account '
