from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder='../frontend', # Path to the frontend static files
        static_folder='../frontend', # Path to the frontend templates
    )

    from .routes import register_routes
    register_routes(app)

    return app
