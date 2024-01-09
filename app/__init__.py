from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import routes
    from .routes.home import home
    from .routes.embedding import embedding
    from .routes.query import query

    # Register routes
    app.register_blueprint(home)
    app.register_blueprint(embedding)
    app.register_blueprint(query)

    return app