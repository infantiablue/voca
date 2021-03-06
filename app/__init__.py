import os
from flask import Flask, redirect, render_template
from flask_assets import Environment, Bundle
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import auth, profile, word
from .models import db


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ.get('APP_SETTINGS'))

    # Initialize database instance
    db.init_app(app)

    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    # Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(word.bp)

    # Custom Error Page
    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    # Setup login manager
    auth.login_manager.init_app(app)
    auth.login_manager.login_view = 'auth.login'

    # Set up PostCSS for Tailwind
    assets = Environment()
    assets.init_app(app)

    css = Bundle('src/css/*.css', filters='postcss',
                 output='dist/css/bundle.css')
    assets.register('css', css)

    @app.route('/')
    # @login_required
    def index():
        return redirect('/dashboard')

    return app
