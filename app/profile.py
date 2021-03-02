from flask import Blueprint

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/dashboard')
def dashboard():
    return 'Dashboard'


@profile_bp.route('/add')
def add():
    return 'Add word'


@profile_bp.route('/edit')
def edit():
    return 'Edit'


@profile_bp.route('/account')
def account():
    return 'Account '
