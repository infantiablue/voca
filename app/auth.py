from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_manager, login_required, logout_user, LoginManager, login_user, current_user
from wtforms import Form, StringField, PasswordField, validators
from .models import db, User
from werkzeug.security import check_password_hash, generate_password_hash

# initialize login manager
login_manager = LoginManager()

# initialize Blueprint
bp = Blueprint('auth', __name__)


class RegistrationForm(Form):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4, max=25),
    ])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmation', message='Passwords must match')
    ])
    confirmation = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4, max=25),
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@bp.route('/join', methods=['GET', 'POST'])
def register():
    # Redirect if a logged user try to accesss
    if current_user.is_authenticated:
        return redirect('/')

    """Register user"""
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(username=form.username.data, email=form.email.data,
                        hash=generate_password_hash(form.password.data))

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Thanks for your registration.')
        return redirect('/')
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if a logged user try to accesss
    if current_user.is_authenticated:
        return redirect('/')

    """Login user"""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Query database for username
        logged_user = User.query.filter_by(
            username=form.username.data).first()
        print(logged_user.username)
        # Ensure username exists and password is correct
        if not check_password_hash(logged_user.hash, form.password.data):
            return redirect('/login')

        # Remember which user has logged in
        login_user(logged_user)
        flash("Logged in successfully.")

        # Redirect user to home page
        return redirect('/')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
