import json
from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from sqlalchemy import desc
from sqlalchemy.sql.expression import func
from .models import db, User
from wtforms import Form, PasswordField, validators
from werkzeug.security import check_password_hash, generate_password_hash
from .word import AddWordForm, SearchForm
bp = Blueprint('profile', __name__)


class AccountForm(Form):
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', [
        validators.Length(min=4, max=25),
        validators.DataRequired(),
        validators.EqualTo('confirmation', message='Passwords must match.')
    ])
    confirmation = PasswordField('Repeat Password')


@bp.route('/dashboard')
@login_required
def dashboard():
    addword_form = AddWordForm()
    search_form = SearchForm()
    words = current_user.words.order_by(
        desc('timestamp')).limit(10)
    total_words = current_user.words.count()
    random_word = {}
    temp = current_user.words.filter_by().order_by(
        func.random()).first()
    if temp:
        random_word['text'] = temp.text
        try:
            with open(f'cache/{random_word["text"]}.json') as json_file:
                data = json.load(json_file)
                random_word['definition'] = data[0]['sense'][0]['entry'][0]['definition']
                random_word['lexical'] = data[0]['sense'][0]['lexical']
        except FileNotFoundError:
            random_word = None
    return render_template('dashboard.html', words=words, random_word=random_word, addword_form=addword_form, search_form=search_form, total_words=total_words)


@ bp.route('/account', methods=['GET', 'POST'])
@ login_required
def account():
    form = AccountForm(request.form)
    if request.method == "POST" and form.validate():
        # Ensure username exists and password is correct
        if not check_password_hash(current_user.hash, form.current_password.data):
            flash('Incorrect current password.', category="error")
            return redirect('/account')
        else:
            current_user.hash = generate_password_hash(
                form.new_password.data)
            db.session.commit()
            flash('Changed password successfully.', category="success")
            return redirect('/dashboard')
    return render_template('account.html', form=form)
