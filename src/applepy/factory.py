"""Flask application factory for creating configured app instances."""

from flask import Flask

from applepy.db import db
from applepy.env import DATABASE_URL


def create_app(config: str | None = None) -> Flask:
    """Create and configure a Flask application instance.

    This factory function creates a new Flask app with the specified configuration.
    It enables multiple app configurations (development, testing, production) and
    allows for dependency injection and better testing support.

    Args:
        config: Configuration mode ('development', 'testing', 'production').
               Defaults to 'development' if not specified.

    Returns:
        Configured Flask application instance with database initialized.
    """
    app = Flask("applepy")

    # Set default configuration
    if config is None:
        config = "development"

    # Configure application based on mode
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

    # Enable SQL echo in development mode for debugging
    app.config["SQLALCHEMY_ECHO"] = config == "development"

    # Initialize database with app
    db.init_app(app)

    return app
