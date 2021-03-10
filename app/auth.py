from flask import Blueprint, request, render_template, redirect, flash, abort
from flask_login import login_manager, login_required, logout_user, LoginManager, login_user, current_user
from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import ValidationError
from .models import db, User
# from .utils import is_safe_url
from werkzeug.security import check_password_hash, generate_password_hash

# initialize login manager
login_manager = LoginManager()

# initialize Blueprint
bp = Blueprint('auth', __name__)


# Custom validator to check unique username
def unique_username(form, field):
    if User.query.filter_by(username=form.username.data).first():
        raise ValidationError('This username has been reistered.')


# Custom validator to check unique email
def unique_email(form, field):
    if User.query.filter_by(email=form.email.data).first():
        raise ValidationError('This email address has been registered.')


class RegistrationForm(Form):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4, max=25),
        unique_username
    ])
    email = StringField('Email Address', [
        validators.Length(min=6, max=35),
        unique_email
    ])
    password = PasswordField('Password', [
        validators.Length(min=4, max=25),
        validators.DataRequired(),
        validators.EqualTo('confirmation', message='Passwords must match.')
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
        return redirect('/dashboard')

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
        return redirect('/dashboard')
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if a logged user try to accesss
    if current_user.is_authenticated:
        return redirect('/dashboard')

    """Login user"""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Query database for username
        logged_user = User.query.filter_by(
            username=form.username.data).first()

        if not logged_user:
            flash("Username is not existed.")
            return render_template('login.html', form=form)
        # print(logged_user.username)
        # Ensure username exists and password is correct
        if not check_password_hash(logged_user.hash, form.password.data):
            flash("Incorrect Password.")
            return render_template('login.html', form=form)

        # Remember which user has logged in
        login_user(logged_user)
        # flash("Logged in successfully.")

        # next = request.args.get('next')
        # # is_safe_url should check if the url is safe for redirects.
        # # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return abort(400)

        # Redirect user to home page
        return redirect('/dashboard')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
