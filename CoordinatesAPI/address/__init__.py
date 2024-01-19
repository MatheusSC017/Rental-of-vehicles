import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from . import routers

# Load variables from the .env file into the environment
load_dotenv()


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app, test_config)
    api = Api(app)
    routers.initialize_routes(api)
    return app


def configure_app(app, test_config):
    secret_key = os.getenv('SECRET_KEY_COORDINATES')
    database_uri = os.getenv('COORDINATES_DATABASE_URI')

    if not secret_key:
        raise ValueError("Missing required configuration values")

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        DATABASE_URI=database_uri
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
