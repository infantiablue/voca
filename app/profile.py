from flask import Blueprint

bp = Blueprint('profile', __name__)


@bp.route('/dashboard')
def dashboard():
    return 'Dashboard'


@bp.route('/add')
def add():
    return 'Add word'


@bp.route('/edit')
def edit():
    return 'Edit'


@bp.route('/account')
def account():
    return 'Account '
