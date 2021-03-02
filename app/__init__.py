import os
from flask import Flask
from .auth import auth_bp
from .profile import profile_bp


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ.get('APP_SETTINGS'))

    # register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)

    # setup login manager
    # TODO
    # login_manager.init_app(app)
    # login_manager.login_view = 'profile_bp.login'

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
