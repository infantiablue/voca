import json
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func, null
# from .models import User, Word

bp = Blueprint('profile', __name__)


@bp.route('/dashboard')
@login_required
def dashboard():
    words = current_user.words
    random_word = {}
    temp = words.filter_by().order_by(
        func.random()).first()
    random_word['text'] = temp.text
    random_word['definition'] = None
    try:
        with open(f'cache/{random_word["text"]}.json') as json_file:
            data = json.load(json_file)
            random_word['definition'] = data[0]['sense'][0]['entry'][0]['definition']
            random_word['lexical'] = data[0]['sense'][0]['lexical']
    except FileNotFoundError:
        random_word = None
    return render_template('dashboard.html', words=words, random_word=random_word)


@bp.route('/account')
def account():
    return 'Account '
