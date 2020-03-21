from flask import Flask


def create_app():
    """
    Application factory
    """
    app = Flask(__name__)

    with app.app_context():
        from .frontend.frontend import frontend_bp

        app.register_blueprint(frontend_bp)

    return app
