from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import routes
    from .routes.home import home

    # Register routes
    app.register_blueprint(home)

    return app