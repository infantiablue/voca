import os
from flask import Flask
from flask.templating import render_template
from flask_assets import Environment, Bundle
from flask_login import login_required
from app import auth, profile
from .models import db


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ.get('APP_SETTINGS'))

    # Initialize database instance
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)

    # Setup login manager
    auth.login_manager.init_app(app)
    auth.login_manager.login_view = 'auth.bp.login'

    # Set up PostCSS for Tailwind
    assets = Environment()
    assets.init_app(app)

    css = Bundle('src/css/*.css', filters='postcss',
                 output='dist/css/bundle.css')
    assets.register('css', css)

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    return app
